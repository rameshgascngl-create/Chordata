import `in`.gasc.zoology.chordata.domain.*

private fun b(value: String) = Bilingual(value, "தமிழ்")
private fun q(answer: Int) = QuizQuestion(b("Question"), listOf(b("A"), b("B"), b("C"), b("D")), answer, b("Explanation"))
private fun topic(id: String, n: Int = 3) = LessonTopic(id, b("Topic $id"),
    (1..n).map { LessonSection("key-$it", b("Heading"), b("Content")) },
    listOf("diagram-$id"), listOf(q(0), q(3), q(1)))

fun main() {
    var checks = 0
    fun checkThat(condition: Boolean, label: String) {
        check(condition) { "FAILED: $label" }
        checks++
    }
    val first = topic("u1-origin")
    val second = topic("u1-general-characters", 5)
    val pack = ContentPack(1, "credit", listOf(LessonUnit("u1", b("Unit I"), listOf(first, second))))
    checkThat(LearningLogic.lastPage(first) == 4, "overview + sections + quiz")
    checkThat(LearningLogic.pageBefore(0) == 0, "lower page bound")
    checkThat(LearningLogic.pageAfter(first, 4) == 4, "upper page bound")
    checkThat(LearningLogic.pageAfter(first, 0) == 1, "sequential forward")
    checkThat(LearningLogic.pageBefore(3) == 2, "sequential backward")
    checkThat(LearningLogic.isQuizPage(first, 4), "quiz is last page")
    checkThat(!LearningLogic.isQuizPage(first, 3), "lesson is not quiz")
    checkThat(LearningLogic.title(first, 0).en == "Topic u1-origin", "overview title")
    checkThat(LearningLogic.title(first, 1).en == "Heading", "section title")
    checkThat(LearningLogic.title(first, 4).ta == "பயிற்சி", "Tamil quiz title")
    checkThat(LearningLogic.search(pack, "general").map { it.id } == listOf(second.id), "search English")
    checkThat(LearningLogic.search(pack, "தமிழ்").size == 2, "search Tamil")
    checkThat(LearningLogic.search(pack, "missing").isEmpty(), "search absent")
    checkThat(LearningLogic.search(pack, " ").size == 2, "empty search returns all")
    checkThat(LearningLogic.score(listOf(0, 3, 1), first.quiz) == 3, "perfect quiz")
    checkThat(LearningLogic.score(listOf(1, -1, 1), first.quiz) == 1, "partial quiz")
    checkThat(LearningLogic.score(emptyList(), first.quiz) == 0, "unanswered quiz")
    checkThat(LearningLogic.percent(0, 39) == 0, "zero progress")
    checkThat(LearningLogic.percent(39, 39) == 100, "complete progress")
    checkThat(LearningLogic.percent(50, 39) == 100, "progress bounded")
    checkThat(LearningLogic.percent(0, 0) == 0, "empty pack safe")
    checkThat(LearningLogic.nextTopic(pack, first.id)?.id == second.id, "chapter forward")
    checkThat(LearningLogic.nextTopic(pack, second.id) == null, "last chapter boundary")
    checkThat(LearningLogic.nextTopic(pack, "bogus") == null, "unknown chapter safe")
    println("PASS: $checks Kotlin core assertions")
}
