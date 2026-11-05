package `in`.gasc.zoology.chordata.ui

import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.rememberTransformableState
import androidx.compose.foundation.gestures.transformable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import `in`.gasc.zoology.chordata.domain.ReadingLanguage
import org.json.JSONArray

/** Syllabus figures are assigned to exact pages, independent of asset availability. */
private data class FigureSlot(
    val diagramId: String, val topicId: String, val page: Int,
    val titleEn: String, val titleTa: String
)
private data class Plate(
    val id: String, val diagramId: String, val topicId: String, val page: Int,
    val filename: String, val captionEn: String, val captionTa: String,
    val author: String, val licence: String
)

@Composable
internal fun FigureGallery(topicId: String, page: Int, lang: ReadingLanguage, requestedCount: Int = 0) {
    val context = LocalContext.current
    val slots = remember(context) {
        val raw = context.assets.open("figure_placements.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val a = JSONArray(raw)
        (0 until a.length()).map { i ->
            a.getJSONObject(i).let { r ->
                FigureSlot(
                    r.getString("diagramId"), r.getString("topicId"), r.getInt("page"),
                    r.getString("titleEn"), r.getString("titleTa")
                )
            }
        }
    }
    val plates = remember(context) {
        val raw = context.assets.open("figures.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val a = JSONArray(raw)
        (0 until a.length()).map { i ->
            a.getJSONObject(i).let { r ->
                Plate(
                    r.getString("id"), r.getString("diagramId"),
                    r.getString("topicId"), r.getInt("page"), r.getString("file"),
                    r.getString("captionEn"), r.getString("captionTa"),
                    r.getString("author"), r.getString("license")
                )
            }
        }
    }
    val inChapter = slots.filter { it.topicId == topicId }
    val inSection = if (page == 0) emptyList() else inChapter.filter { it.page == page }
    val present = inChapter.count { slot ->
        plates.any { it.diagramId == slot.diagramId &&
            it.topicId == topicId && it.page == slot.page }
    }
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (page == 0 && requestedCount > 0) {
            Text(
                if (lang == ReadingLanguage.TA)
                    "இப்பாடத்திற்கான வரைபடங்கள்: " + present + " / " + inChapter.size +
                        ". ஏனைய வரைபடங்கள் இன்னும் அறிவியல் சரிபார்ப்பில் உள்ளன."
                else "Chapter illustrations: " + present + " / " + inChapter.size +
                    ". The remaining anatomical figures are not yet supplied and reviewed.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.testTag("figure-chapter-summary")
            )
        }
        if (page > 0) {
            inSection.forEach { slot ->
                val plate = plates.firstOrNull { it.diagramId == slot.diagramId &&
                    it.topicId == slot.topicId && it.page == slot.page }
                if (plate == null) {
                    Card(modifier = Modifier.fillMaxWidth()
                            .testTag("figure-pending-" + slot.diagramId),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                        Column(Modifier.padding(12.dp),
                            verticalArrangement = Arrangement.spacedBy(5.dp)) {
                            Text(
                                if (lang == ReadingLanguage.TA)
                                    "தேவையான வரைபடம் இன்னும் சேர்க்கப்படவில்லை"
                                else "Required scientific figure not yet available",
                                fontWeight = FontWeight.SemiBold
                            )
                            Text(if (lang == ReadingLanguage.TA) slot.titleTa else slot.titleEn)
                            Text(
                                if (lang == ReadingLanguage.TA)
                                    "உடற்கூறியல் மற்றும் தமிழ்ச் சொற்கள் சரிபார்க்கப்பட்ட பின்னரே சேர்க்கப்படும்."
                                else "This figure requires anatomical and language review before integration.",
                                style = MaterialTheme.typography.labelSmall
                            )
                        }
                    }
                } else {
                    val bitmap = remember(context, plate.filename) {
                        runCatching {
                            context.assets.open("figures/" + plate.filename).use { stream ->
                                BitmapFactory.decodeStream(stream)?.asImageBitmap()
                            }
                        }.getOrNull()
                    }
                    if (bitmap == null) {
                        Text(
                            if (lang == ReadingLanguage.TA)
                                "படக் கோப்பைத் திறக்க இயலவில்லை; கோப்புச் சரிபார்ப்பு தேவை."
                            else "Figure file unavailable; integrity check required.",
                            color = MaterialTheme.colorScheme.error,
                            modifier = Modifier.testTag("figure-error-" + plate.id)
                        )
                    } else {
                        var zoomed by remember(plate.id) { mutableStateOf(false) }
                        Card(modifier = Modifier.fillMaxWidth().testTag("figure-" + plate.id)) {
                            Column(Modifier.padding(12.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text(
                                    if (lang == ReadingLanguage.TA)
                                        "புறத்தோற்ற வரைபடம் · சோதனைப் பதிப்பு"
                                    else "External morphology · provisional QA drawing",
                                    fontWeight = FontWeight.SemiBold
                                )
                                Image(
                                    bitmap = bitmap,
                                    contentDescription = if (lang == ReadingLanguage.TA)
                                        plate.captionTa else plate.captionEn,
                                    contentScale = ContentScale.Fit,
                                    modifier = Modifier.fillMaxWidth()
                                        .heightIn(min = 170.dp, max = 340.dp)
                                        .clickable { zoomed = true }
                                        .testTag("figure-image-" + plate.id)
                                )
                                Text(if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn)
                                Text(
                                    if (lang == ReadingLanguage.TA)
                                        "மூலம்: " + plate.author + " · " + plate.licence
                                    else "Source: " + plate.author + " · " + plate.licence,
                                    style = MaterialTheme.typography.labelSmall
                                )
                                Text(
                                    if (lang == ReadingLanguage.TA) "பெரிதாக்கப் படத்தைத் தொடுக"
                                    else "Tap image to enlarge",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            }
                        }
                        if (zoomed) {
                            var zoom by remember(plate.id) { mutableFloatStateOf(1f) }
                            var offset by remember(plate.id) { mutableStateOf(Offset.Zero) }
                            val transform = rememberTransformableState { change, pan, _ ->
                                zoom = (zoom * change).coerceIn(1f, 5f)
                                offset = if (zoom > 1f) offset + pan else Offset.Zero
                            }
                            Dialog(
                                onDismissRequest = { zoomed = false },
                                properties = DialogProperties(usePlatformDefaultWidth = false)
                            ) {
                                Surface(Modifier.fillMaxSize()) {
                                    Column(Modifier.padding(12.dp)) {
                                        Row(Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.End) {
                                            TextButton(onClick = { zoomed = false }) {
                                                Text(if (lang == ReadingLanguage.TA) "மூடுக" else "Close")
                                            }
                                        }
                                        Box(
                                            Modifier.weight(1f).fillMaxWidth().transformable(transform),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Image(
                                                bitmap,
                                                contentDescription = if (lang == ReadingLanguage.TA)
                                                    plate.captionTa else plate.captionEn,
                                                contentScale = ContentScale.Fit,
                                                modifier = Modifier.fillMaxSize().graphicsLayer {
                                                    scaleX = zoom; scaleY = zoom
                                                    translationX = offset.x; translationY = offset.y
                                                }
                                            )
                                        }
                                        Text(if (lang == ReadingLanguage.TA)
                                            plate.captionTa else plate.captionEn)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
