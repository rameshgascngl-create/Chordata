package `in`.gasc.zoology.chordata.data

import android.content.Context
import `in`.gasc.zoology.chordata.domain.*
import org.json.JSONArray
import org.json.JSONObject

object ContentRepository {
    fun load(context: Context): ContentPack {
        val raw = context.assets.open("chordata_content.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
        val root = JSONObject(raw)
        require(root.getInt("schemaVersion") == 1) { "Unsupported content schema" }
        val units = root.getJSONArray("units").toList { item ->
            LessonUnit(
                item.getString("id"), item.getJSONObject("title").bilingual(),
                item.getJSONArray("topics").toList { topic ->
                    LessonTopic(
                        topic.getString("id"), topic.getJSONObject("title").bilingual(),
                        topic.getJSONArray("sections").toList { section ->
                            LessonSection(section.getString("key"), section.getJSONObject("heading").bilingual(),
                                section.getJSONObject("body").bilingual())
                        },
                        topic.optJSONArray("diagramIds")?.stringList() ?: emptyList(),
                        topic.getJSONArray("quiz").toList { q ->
                            QuizQuestion(q.getJSONObject("question").bilingual(),
                                q.getJSONArray("options").toList { it.bilingual() },
                                q.getInt("correctIndex"), q.getJSONObject("explanation").bilingual())
                        }
                    )
                }
            )
        }
        val pack = ContentPack(root.getInt("schemaVersion"), root.getString("credit"), units)
        require(pack.units.size == 5 && pack.topics.size == 39) { "Incomplete course pack" }
        require(pack.topics.sumOf { it.sections.size } == 127) { "Missing lessons" }
        require(pack.topics.sumOf { it.quiz.size } == 117) { "Missing quiz items" }
        require(pack.topics.sumOf { it.diagramIds.size } == 64) { "Diagram register mismatch" }
        require(pack.topics.all { it.quiz.all { q -> q.options.size == 4 && q.correctIndex in 0..3 } })
        return pack
    }

    private fun JSONObject.bilingual() = Bilingual(getString("en"), getString("ta"))
    private inline fun <T> JSONArray.toList(transform: (JSONObject) -> T): List<T> =
        (0 until length()).map { transform(getJSONObject(it)) }
    private fun JSONArray.stringList(): List<String> = (0 until length()).map { getString(it) }
}
