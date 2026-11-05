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

private data class Plate(
    val id: String, val topicId: String, val page: Int, val filename: String,
    val captionEn: String, val captionTa: String, val author: String, val licence: String
)

private data class DiagramSlot(
    val id: String, val topicId: String, val page: Int,
    val captionEn: String, val captionTa: String, val provisionalFigureId: String?
)

@Composable
internal fun FigureGallery(topicId: String, page: Int, lang: ReadingLanguage, requestedCount: Int = 0) {
    val context = LocalContext.current
    val plates = remember(context) {
        runCatching {
            val raw = context.assets.open("figures.json").bufferedReader().use { it.readText() }
            val array = JSONArray(raw)
            (0 until array.length()).map { index ->
                array.getJSONObject(index).let { entry ->
                    Plate(entry.getString("id"), entry.getString("topicId"),
                        entry.getInt("page"), entry.getString("file"),
                        entry.getString("captionEn"), entry.getString("captionTa"),
                        entry.getString("author"), entry.getString("license"))
                }
            }
        }.getOrDefault(emptyList())
    }
    val allSlots: List<DiagramSlot>? = remember(context) {
        runCatching {
            val raw = context.assets.open("figure_slots.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val array = org.json.JSONObject(raw).getJSONArray("slots")
            (0 until array.length()).map { index ->
                array.getJSONObject(index).let { entry ->
                    DiagramSlot(entry.getString("id"), entry.getString("topicId"),
                        entry.getInt("page"), entry.getString("captionEn"),
                        entry.getString("captionTa"),
                        if (entry.isNull("provisionalFigureId")) null
                        else entry.getString("provisionalFigureId"))
                }
            }
        }.getOrNull()
    }
    // On the chapter overview, show only the status; a figure belongs to
    // exactly one section page, never to both the overview and the section.
    val topicSlots = allSlots?.filter { it.topicId == topicId }.orEmpty()
    val pageSlots = if (page > 0) topicSlots.filter { it.page == page } else emptyList()
    val relevant = if (page > 0) plates.filter { it.topicId == topicId && it.page == page }
                   else emptyList()
    val matchingDraftIds = pageSlots.mapNotNull { it.provisionalFigureId }.toSet()
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (allSlots == null) {
            Text(
                if (lang == ReadingLanguage.TA) "வரைபட இருப்பிடப் பதிவேடு கிடைக்கவில்லை."
                else "Diagram placement register unavailable.",
                modifier = Modifier.testTag("figure-register-error"),
                color = MaterialTheme.colorScheme.error
            )
        }
        if (page == 0 && requestedCount > 0) {
            Text(
                if (lang == ReadingLanguage.TA)
                    "இந்தப் பாடத்தில் " + topicSlots.size + (if (topicSlots.size == 1) " வரைபடம்" else " வரைபடங்கள்") + " திட்டமிடப்பட்டுள்ளன. ஒப்புதல் பெற்ற உடற்கூறியல் வரைபடங்கள் இன்னும் சேர்க்கப்படவில்லை. வரைபடங்கள் உரிய பாடப் பக்கங்களில் மட்டுமே காட்டப்படும்."
                else "This chapter has " + topicSlots.size + (if (topicSlots.size == 1) " planned diagram." else " planned diagrams.") + " No anatomical plate is academically approved yet. Available draft drawings appear only in the relevant lesson sections.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.testTag("figure-overview-status")
            )
        }
        val unexpected = relevant.filter { it.id !in matchingDraftIds }
        if (unexpected.isNotEmpty()) {
            Text(
                if (lang == ReadingLanguage.TA)
                    "படத்திற்கும் பாடப்பகுதிக்கும் பொருத்தமின்மை கண்டறியப்பட்டது."
                else "Figure-to-lesson placement mismatch detected.",
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.testTag("figure-placement-error")
            )
        }
        relevant.filter { it.id in matchingDraftIds }.forEach { plate ->
            val bitmap = remember(context, plate.filename) {
                runCatching {
                    context.assets.open("figures/" + plate.filename).use { stream ->
                        BitmapFactory.decodeStream(stream)?.asImageBitmap()
                    }
                }.getOrNull()
            }
            if (bitmap == null) {
                Text(if (lang == ReadingLanguage.TA)
                    "படக் கோப்பைத் திறக்க இயலவில்லை; சரிபார்ப்பு தேவை."
                else "Figure file unavailable; integrity check required.",
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.testTag("figure-error-" + plate.id))
            } else {
                var zoomed by remember(plate.id) { mutableStateOf(false) }
                Card(modifier = Modifier.fillMaxWidth().testTag("figure-" + plate.id)) {
                    Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(if (lang == ReadingLanguage.TA) "ஆதாரப் படம் · சோதனைப் பதிப்பு"
                            else "Reference figure · QA draft",
                            fontWeight = FontWeight.SemiBold)
                        Image(bitmap = bitmap, contentDescription = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn,
                            contentScale = ContentScale.Fit,
                            modifier = Modifier.fillMaxWidth().heightIn(min = 170.dp, max = 340.dp)
                                .clickable { zoomed = true }.testTag("figure-image-" + plate.id))
                        Text(if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn)
                        Text(if (lang == ReadingLanguage.TA)
                            "மூலம்: Chordata QA project · கணினி உதவியுடன் உருவாக்கப்பட்ட தற்காலிகக் கோட்டோவியம் · அறிவியல் மதிப்பாய்வு நிலுவையில் உள்ளது"
                            else "Source: " + plate.author + " · " + plate.licence,
                            style = MaterialTheme.typography.labelSmall)
                        Text(if (lang == ReadingLanguage.TA) "பெரிதாக்கப் படத்தைத் தொடுக" else "Tap image to enlarge",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    }
                }
                if (zoomed) {
                    var scale by remember(plate.id) { mutableFloatStateOf(1f) }
                    var offset by remember(plate.id) { mutableStateOf(Offset.Zero) }
                    val transforms = rememberTransformableState { zoomChange, panChange, _ ->
                        scale = (scale * zoomChange).coerceIn(1f, 5f)
                        offset = if (scale > 1f) offset + panChange else Offset.Zero
                    }
                    Dialog(onDismissRequest = { zoomed = false },
                        properties = DialogProperties(usePlatformDefaultWidth = false)) {
                        Surface(Modifier.fillMaxSize()) {
                            Column(Modifier.padding(12.dp)) {
                                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                                    TextButton(onClick = { zoomed = false }) {
                                        Text(if (lang == ReadingLanguage.TA) "மூடுக" else "Close")
                                    }
                                }
                                Box(Modifier.weight(1f).fillMaxWidth().transformable(transforms),
                                    contentAlignment = Alignment.Center) {
                                    Image(bitmap, contentDescription = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn,
                                        contentScale = ContentScale.Fit,
                                        modifier = Modifier.fillMaxSize().graphicsLayer {
                                            scaleX = scale; scaleY = scale
                                            translationX = offset.x; translationY = offset.y
                                        })
                                }
                                Text(if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn)
                            }
                        }
                    }
                }
            }
        }
        if (page > 0 && pageSlots.isNotEmpty()) {
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                ),
                modifier = Modifier.fillMaxWidth().testTag("figure-pending-page")
            ) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(
                        if (lang == ReadingLanguage.TA) "சரிபார்ப்பிலுள்ள வரைபடங்கள்"
                        else "Scientific diagrams awaiting approval",
                        fontWeight = FontWeight.SemiBold
                    )
                    pageSlots.forEach { slot ->
                        Text("• " + if (lang == ReadingLanguage.TA) slot.captionTa else slot.captionEn,
                            style = MaterialTheme.typography.bodySmall)
                    }
                    Text(
                        if (lang == ReadingLanguage.TA)
                            "தற்காலிகக் கோட்டோவியங்கள் பெயரிடப்பட்ட உடற்கூறியல் வரைபடங்களுக்கு மாற்றாகாது."
                        else "Provisional outline drawings do not replace labelled anatomical plates.",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
