package `in`.gasc.zoology.chordata.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import `in`.gasc.zoology.chordata.domain.ReadingLanguage

/** Locally stored only; no internet permission and Android backup disabled. */
class ProgressStore(context: Context) {
    private val prefs = context.getSharedPreferences("chordata_progress_v1", Context.MODE_PRIVATE)
    fun completed(): Set<String> = prefs.getStringSet("done", emptySet())?.toSet() ?: emptySet()
    fun bookmarks(): Set<String> = prefs.getStringSet("saved", emptySet())?.toSet() ?: emptySet()
    fun saveCompleted(value: Set<String>) { prefs.edit().putStringSet("done", value.toSet()).apply() }
    fun saveBookmarks(value: Set<String>) { prefs.edit().putStringSet("saved", value.toSet()).apply() }
    fun language(): ReadingLanguage = runCatching {
        ReadingLanguage.valueOf(prefs.getString("lang", "EN") ?: "EN")
    }.getOrDefault(ReadingLanguage.EN)
    fun saveLanguage(value: ReadingLanguage) { prefs.edit().putString("lang", value.name).apply() }
    fun textScale(): Float = prefs.getFloat("scale", 1f).coerceIn(1f, 2f)
    fun saveTextScale(value: Float) { prefs.edit().putFloat("scale", value.coerceIn(1f, 2f)).apply() }
    fun saveQuizScore(topicId: String, score: Int) {
        prefs.edit().putInt("quiz:$topicId", score).apply()
    }
    fun quizScore(topicId: String): Int? = if (prefs.contains("quiz:$topicId"))
        prefs.getInt("quiz:$topicId", 0) else null

    /**
     * Human-readable, offline, user-controlled JSON export. The caller writes it
     * through Android Storage Access Framework; no storage/network permission.
     */
    fun exportLearningData(): String {
        val scores = JSONObject()
        for ((key, value) in prefs.all) {
            if (key.startsWith("quiz:") && value is Int) {
                scores.put(key.removePrefix("quiz:"), value)
            }
        }
        return JSONObject()
            .put("format", "chordata-learning-progress")
            .put("version", 1)
            .put("completed", JSONArray(completed().sorted()))
            .put("bookmarks", JSONArray(bookmarks().sorted()))
            .put("quizScores", scores)
            .put("language", language().name)
            .put("textScale", textScale().toDouble())
            .toString(2)
    }

    /**
     * Validate EVERY field before changing any saved progress. A malformed,
     * oversized or unrelated JSON file must never erase existing records.
     * Import replaces the local dataset only when the entire payload is valid.
     */
    fun importLearningData(payload: String): Boolean = runCatching {
        require(payload.length in 1..65536)
        val json = JSONObject(payload)
        require(json.getString("format") == "chordata-learning-progress")
        require(json.getInt("version") == 1)
        val idFormat = Regex("[A-Za-z0-9_-]{1,128}")
        fun readIds(field: String): Set<String> {
            val array = json.getJSONArray(field)
            require(array.length() <= 256)
            val result = mutableSetOf<String>()
            for (i in 0 until array.length()) {
                val id = array.getString(i)
                require(idFormat.matches(id))
                require(result.add(id))
            }
            return result
        }
        val completedIds = readIds("completed")
        val savedIds = readIds("bookmarks")
        val quiz = json.getJSONObject("quizScores")
        require(quiz.length() <= 256)
        val scores = mutableMapOf<String, Int>()
        val names = quiz.keys()
        while (names.hasNext()) {
            val id = names.next()
            require(idFormat.matches(id))
            val score = quiz.getInt(id)
            require(score in 0..1000)
            scores[id] = score
        }
        val restoredLang = ReadingLanguage.valueOf(json.getString("language"))
        val scale = json.getDouble("textScale")
        require(scale.isFinite() && scale in 1.0..2.0)

        val edit = prefs.edit().clear()
            .putStringSet("done", completedIds)
            .putStringSet("saved", savedIds)
            .putString("lang", restoredLang.name)
            .putFloat("scale", scale.toFloat())
        for ((id, score) in scores) edit.putInt("quiz:$id", score)
        edit.commit()
    }.getOrDefault(false)

    /** Wipes private learning data synchronously and reports persistence success. */
    fun eraseAllLearningData(): Boolean = prefs.edit().clear().commit()
}
