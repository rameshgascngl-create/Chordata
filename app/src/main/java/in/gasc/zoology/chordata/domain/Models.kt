package `in`.gasc.zoology.chordata.domain

data class Bilingual(val en: String, val ta: String)
data class QuizQuestion(
    val question: Bilingual,
    val options: List<Bilingual>,
    val correctIndex: Int,
    val explanation: Bilingual
)
data class LessonSection(val key: String, val heading: Bilingual, val body: Bilingual)
data class LessonTopic(
    val id: String,
    val title: Bilingual,
    val sections: List<LessonSection>,
    val diagramIds: List<String>,
    val quiz: List<QuizQuestion>
)
data class LessonUnit(val id: String, val title: Bilingual, val topics: List<LessonTopic>)
data class ContentPack(val schemaVersion: Int, val credit: String, val units: List<LessonUnit>) {
    val topics: List<LessonTopic> get() = units.flatMap { it.topics }
    fun findTopic(id: String): LessonTopic? = topics.firstOrNull { it.id == id }
}

enum class ReadingLanguage { EN, TA }

object LearningLogic {
    /** 0 = chapter overview; 1..sections.size = individual section; last = quiz. */
    fun lastPage(topic: LessonTopic): Int = topic.sections.size + 1
    fun isQuizPage(topic: LessonTopic, page: Int): Boolean = page == lastPage(topic)
    fun pageAfter(topic: LessonTopic, current: Int): Int = (current + 1).coerceAtMost(lastPage(topic))
    fun pageBefore(current: Int): Int = (current - 1).coerceAtLeast(0)
    fun title(topic: LessonTopic, page: Int): Bilingual = when {
        page <= 0 -> topic.title
        page > topic.sections.size -> Bilingual("Practice", "பயிற்சி")
        else -> topic.sections[page - 1].heading
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
