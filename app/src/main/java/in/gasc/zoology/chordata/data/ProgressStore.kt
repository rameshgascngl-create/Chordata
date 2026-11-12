package `in`.gasc.zoology.chordata.data

import android.content.Context
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

    /** Wipes private learning data synchronously and reports persistence success. */
    fun eraseAllLearningData(): Boolean = prefs.edit().clear().commit()
}
