package `in`.gasc.zoology.chordata.domain

data class Bilingual(val en: String, val ta: String)
data class QuizQuestion(
    val question: Bilingual,
    val options: List<Bilingual>,
    val correctIndex: Int,
    val explanation: Bilingual
)
data class LessonSection(
    val key: String, val heading: Bilingual, val body: Bilingual,
    val keyPoints: List<Bilingual> = emptyList()
)
data class TextbookChapter(val id: String, val title: Bilingual, val sections: List<LessonSection>)

data class LessonTopic(
    val id: String,
    val title: Bilingual,
    val sections: List<LessonSection>,
    val diagramIds: List<String>,
    val quiz: List<QuizQuestion>,
    /** One-based original figure-register section numbers; no source images remapped. */
    val figurePages: Set<Int> = emptySet(),
    val textbookChapters: List<TextbookChapter> = emptyList()
)
data class LessonUnit(val id: String, val title: Bilingual, val topics: List<LessonTopic>)
data class ContentPack(val schemaVersion: Int, val credit: String, val units: List<LessonUnit>) {
    val topics: List<LessonTopic> get() = units.flatMap { it.topics }
    fun findTopic(id: String): LessonTopic? = topics.firstOrNull { it.id == id }
}

enum class ReadingLanguage { EN, TA }

object LearningLogic {
    private val sentenceAbbreviation = Regex(
        """(?:\b[A-Z]\.|\b(?:e\.g|i\.e|cf|vs|fig|figs|no|vol|et al|sp|spp)\.)$""",
        RegexOption.IGNORE_CASE
    )
    private val sentenceStart = Regex("""\s+(?=[“"‘'’(]*[A-Z\u0B80-\u0BFF])""")
    private val sentenceEnd = Regex("""[.!?][”"’')]*$""")

    /** Divide the complete source text into points without dropping any words. */
    fun answerPoints(text: String): List<String> {
        val points = mutableListOf<String>()
        var start = 0
        for (space in sentenceStart.findAll(text)) {
            val candidate = text.substring(start, space.range.first).trim()
            if (sentenceEnd.containsMatchIn(candidate) && !sentenceAbbreviation.containsMatchIn(candidate)) {
                points.add(candidate)
                start = space.range.last + 1
            }
        }
        text.substring(start).trim().takeIf { it.isNotEmpty() }?.let { points.add(it) }
        return points
    }

    /**
     * Textbook pages are groups of contiguous section indices, not fixed
     * one-section screens. The chapter guide remains alongside section one.
     *
     * For short three-section lessons, section two and the unillustrated
     * final section share a scrollable page, reclaiming the blank half-screen
     * shown on tall phones. A figure in section three remains on its own page
     * to preserve the specimen's teaching context.
     *
     * Figure slots retain their original one-based page mapping.
     */
    fun sectionPages(topic: LessonTopic): List<List<Int>> {
        val n = topic.sections.size
        if (n == 0) return emptyList()
        if (n == 3 && 3 !in topic.figurePages) {
            return listOf(listOf(0), listOf(1, 2))
        }
        return (0 until n).map { listOf(it) }
    }
    /** Pack consecutive original textbook paragraphs without blank pages.
     *  Registered legacy figures remain tied to the original sectionPages. */
    fun textbookPages(topic: LessonTopic): List<List<LessonSection>> {
        val sections = topic.textbookChapters.flatMap { it.sections }
        if (sections.isEmpty()) return emptyList()
        val pages = mutableListOf<List<LessonSection>>()
        var current = mutableListOf<LessonSection>()
        var wordCount = 0
        for (section in sections) {
            val words = section.body.en.trim().split(Regex("\\s+")).size
            if (current.isNotEmpty() && wordCount + words > 230) {
                pages.add(current.toList())
                current = mutableListOf()
                wordCount = 0
            }
            current.add(section)
            wordCount += words
        }
        if (current.isNotEmpty()) pages.add(current.toList())
        return pages
    }
    /** Reading pages include all core and textbook sections; last page is quiz. */
    fun lastPage(topic: LessonTopic): Int = sectionPages(topic).size + textbookPages(topic).size
    fun isQuizPage(topic: LessonTopic, page: Int): Boolean = page == lastPage(topic)
    fun pageAfter(topic: LessonTopic, current: Int): Int = (current + 1).coerceAtMost(lastPage(topic))
    fun pageBefore(current: Int): Int = (current - 1).coerceAtLeast(0)
    fun title(topic: LessonTopic, page: Int): Bilingual = when {
        page <= 0 -> topic.title
        page >= lastPage(topic) -> Bilingual("Practice", "பயிற்சி")
        page < sectionPages(topic).size -> topic.sections[sectionPages(topic)[page].first()].heading
        else -> textbookPages(topic)[page - sectionPages(topic).size].first().heading
    }
    /**
     * Search titles before body mentions: a query for a type-study species must
     * open that chapter, not an earlier classification lesson that names it.
     * Preserve syllabus order within each relevance tier and search both languages.
     */
    fun search(pack: ContentPack, query: String): List<LessonTopic> {
        val needle = query.trim().lowercase()
        if (needle.isEmpty()) return pack.topics
        return pack.topics.mapIndexedNotNull { index, topic ->
            val titles = sequenceOf(topic.title.en, topic.title.ta, topic.id)
                .plus(topic.textbookChapters.asSequence().flatMap { chapter ->
                    sequenceOf(chapter.title.en, chapter.title.ta)
                }).map { it.lowercase() }.toList()
            val headings = topic.sections.asSequence().flatMap {
                sequenceOf(it.heading.en, it.heading.ta)
            }.plus(topic.textbookChapters.asSequence().flatMap { chapter ->
                chapter.sections.asSequence().flatMap {
                    sequenceOf(it.heading.en, it.heading.ta)
                }
            })
            val bodies = topic.sections.asSequence().flatMap {
                sequenceOf(it.body.en, it.body.ta)
            }.plus(topic.textbookChapters.asSequence().flatMap { chapter ->
                chapter.sections.asSequence().flatMap {
                    sequenceOf(it.body.en, it.body.ta)
                }
            })
            val rank = when {
                titles.any { it == needle } -> 0
                titles.any { it.startsWith(needle) } -> 1
                titles.any { needle in it } -> 2
                headings.any { needle in it.lowercase() } -> 3
                bodies.any { needle in it.lowercase() } -> 4
                else -> -1
            }
            if (rank < 0) null else Triple(rank, index, topic)
        }.sortedWith(compareBy<Triple<Int, Int, LessonTopic>> { it.first }
            .thenBy { it.second }).map { it.third }
    }
    fun score(selections: List<Int>, questions: List<QuizQuestion>): Int =
        questions.indices.count { i -> selections.getOrNull(i) == questions[i].correctIndex }
    fun percent(completed: Int, total: Int): Int = if (total == 0) 0 else
        (completed.coerceIn(0, total) * 100) / total
    fun nextTopic(pack: ContentPack, id: String): LessonTopic? =
        pack.topics.indexOfFirst { it.id == id }.let { i ->
            if (i in 0 until pack.topics.lastIndex) pack.topics[i + 1] else null
        }
}
