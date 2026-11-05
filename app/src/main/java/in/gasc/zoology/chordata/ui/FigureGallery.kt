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
    // Overview previews first lesson's figure; lesson page contains its real placement.
    val relevant = plates.filter { it.topicId == topicId && (it.page == page || (page == 0 && it.page == 1)) }
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (page == 0 && requestedCount > relevant.size) {
            Text(
                if (lang == ReadingLanguage.TA)
                    "மேலும் " + (requestedCount - relevant.size) + " உடற்கூறியல் வரைபடங்கள் தயாரிப்பில் உள்ளன."
                else (requestedCount - relevant.size).toString() + " further anatomical diagrams await review.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        relevant.forEach { plate ->
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
                        Text(if (lang == ReadingLanguage.TA) "மூலம்: " + plate.author + " · " + plate.licence
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
    }
}
