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
data class LessonTopic(
    val id: String,
    val title: Bilingual,
    val sections: List<LessonSection>,
    val diagramIds: List<String>,
    val quiz: List<QuizQuestion>,
    /** One-based original figure-register section numbers; no source images remapped. */
    val figurePages: Set<Int> = emptySet()
)
data class LessonUnit(val id: String, val title: Bilingual, val topics: List<LessonTopic>)
data class ContentPack(val schemaVersion: Int, val credit: String, val units: List<LessonUnit>) {
    val topics: List<LessonTopic> get() = units.flatMap { it.topics }
    fun findTopic(id: String): LessonTopic? = topics.firstOrNull { it.id == id }
}

enum class ReadingLanguage { EN, TA }

object LearningLogic {
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
    /** Reading pages are 0..lastPage-1; lastPage itself contains the quiz. */
    fun lastPage(topic: LessonTopic): Int = sectionPages(topic).size
    fun isQuizPage(topic: LessonTopic, page: Int): Boolean = page == lastPage(topic)
    fun pageAfter(topic: LessonTopic, current: Int): Int = (current + 1).coerceAtMost(lastPage(topic))
    fun pageBefore(current: Int): Int = (current - 1).coerceAtLeast(0)
    fun title(topic: LessonTopic, page: Int): Bilingual = when {
        page <= 0 -> topic.title
        page >= lastPage(topic) -> Bilingual("Practice", "பயிற்சி")
        else -> topic.sections[sectionPages(topic)[page].first()].heading
    }
    fun search(pack: ContentPack, query: String): List<LessonTopic> {
        val needle = query.trim().lowercase()
        if (needle.isEmpty()) return pack.topics
        return pack.topics.filter { topic ->
            sequenceOf(topic.title.en, topic.title.ta, topic.id)
                .plus(topic.sections.asSequence().flatMap {
                    sequenceOf(it.heading.en, it.heading.ta, it.body.en, it.body.ta)
                }).any { it.lowercase().contains(needle) }
        }
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
