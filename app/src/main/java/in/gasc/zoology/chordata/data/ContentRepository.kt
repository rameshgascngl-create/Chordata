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
        // Supplement only: the checksum-protected syllabus text and figure pages
        // are not rewritten. All pointwise material is fully offline and bilingual.
        val pointsRaw = context.assets.open("chordata_learning_points.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val pointsRoot = JSONObject(pointsRaw)
        require(pointsRoot.getInt("schemaVersion") == 1) { "Unsupported learning-points schema" }
        val supplements = pointsRoot.getJSONArray("sections").toList { entry ->
            val topicId = entry.getString("topicId")
            val sectionKey = entry.getString("sectionKey")
            val points = entry.getJSONArray("points").toList { p -> p.bilingual() }
            require(points.size == 3 && points.all {
                it.en.isNotBlank() && it.ta.isNotBlank()
            }) { "Incomplete bilingual learning points for $topicId / $sectionKey" }
            Triple(topicId, sectionKey, points)
        }
        require(supplements.size == 39) { "Expected 39 targeted topic enrichments" }
        val pointsBySection = supplements.associate { (topicId, sectionKey, points) ->
            (topicId to sectionKey) to points
        }
        require(pointsBySection.size == supplements.size) { "Duplicate learning-point section" }
        // One-based figure placements come from the existing immutable slot
        // register; page packing never edits or reassigns a figure.
        val figureRegistry = JSONObject(context.assets.open("figure_slots.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() })
        val figurePagesByTopic = figureRegistry.getJSONArray("slots").toList { slot ->
            slot.getString("topicId") to slot.getInt("page")
        }.groupBy({ it.first }, { it.second }).mapValues { (_, pages) -> pages.toSet() }

        val units = root.getJSONArray("units").toList { item ->
            LessonUnit(
                item.getString("id"), item.getJSONObject("title").bilingual(),
                item.getJSONArray("topics").toList { topic ->
                    LessonTopic(
                        topic.getString("id"), topic.getJSONObject("title").bilingual(),
                        topic.getJSONArray("sections").toList { section ->
                            LessonSection(section.getString("key"), section.getJSONObject("heading").bilingual(),
                                section.getJSONObject("body").bilingual(),
                                pointsBySection[topic.getString("id") to section.getString("key")]
                                    ?: emptyList())
                        },
                        topic.optJSONArray("diagramIds")?.stringList() ?: emptyList(),
                        topic.getJSONArray("quiz").toList { q ->
                            QuizQuestion(q.getJSONObject("question").bilingual(),
                                q.getJSONArray("options").toList { it.bilingual() },
                                q.getInt("correctIndex"), q.getJSONObject("explanation").bilingual())
                        },
                        figurePagesByTopic[topic.getString("id")] ?: emptySet()
                    )
                }
            )
        }
        val pack = ContentPack(root.getInt("schemaVersion"), root.getString("credit"), units)
        require(pack.units.size == 5 && pack.topics.size == 39) { "Incomplete course pack" }
        require(pack.topics.sumOf { it.sections.size } == 127) { "Missing lessons" }
        require(pack.topics.sumOf { it.quiz.size } == 117) { "Missing quiz items" }
        require(pack.topics.sumOf { it.diagramIds.size } == 64) { "Diagram register mismatch" }
        require(figureRegistry.getJSONArray("slots").length() == 64) {
            "Incomplete registered figure placement"
        }
        require(pack.topics.all { topic ->
            topic.figurePages.all { it in 1..topic.sections.size }
        }) { "Registered figure page outside the chapter" }
        val registered = pack.topics.flatMap { topic ->
            topic.sections.map { topic.id to it.key }
        }.toSet()
        require(pointsBySection.keys.all { it in registered }) {
            "Supplement references a missing lesson section"
        }
        require(pack.topics.all { topic -> topic.sections.count { it.keyPoints.isNotEmpty() } == 1 }) {
            "Each syllabus topic needs one targeted pointwise explanation"
        }
        require(pack.topics.sumOf { topic -> topic.sections.sumOf { it.keyPoints.size } } == 117) {
            "Incomplete pointwise enrichment"
        }
        require(pack.topics.all { it.quiz.all { q -> q.options.size == 4 && q.correctIndex in 0..3 } })
        return pack
    }

    private fun JSONObject.bilingual() = Bilingual(getString("en"), getString("ta"))
    private inline fun <T> JSONArray.toList(transform: (JSONObject) -> T): List<T> =
        (0 until length()).map { transform(getJSONObject(it)) }
    private fun JSONArray.stringList(): List<String> = (0 until length()).map { getString(it) }
}
