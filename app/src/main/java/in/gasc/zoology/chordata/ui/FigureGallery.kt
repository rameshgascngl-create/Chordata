package `in`.gasc.zoology.chordata.ui

import android.content.Context
import android.graphics.Bitmap
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
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import `in`.gasc.zoology.chordata.domain.ReadingLanguage
import org.json.JSONArray
import org.json.JSONObject

/**
 * A bounded preview decode prevents full-size PNGs being allocated on every lesson
 * page. The full original is decoded only while the pinch-zoom dialog is open.
 * This does not resize or modify the bundled PNG artwork.
 */
internal fun decodePlateBitmap(
    context: Context,
    assetDirectory: String,
    filename: String,
    maxLongestEdgePx: Int? = null
): Bitmap? {
    val assetPath = "$assetDirectory/$filename"
    val options = BitmapFactory.Options()
    if (maxLongestEdgePx != null) {
        require(maxLongestEdgePx > 0)
        options.inJustDecodeBounds = true
        context.assets.open(assetPath).use { input ->
            BitmapFactory.decodeStream(input, null, options)
        }
        if (options.outWidth <= 0 || options.outHeight <= 0) return null
        var sample = 1
        while ((options.outWidth / sample > maxLongestEdgePx ||
                    options.outHeight / sample > maxLongestEdgePx) && sample < 32) {
            sample *= 2
        }
        options.inSampleSize = sample
        options.inJustDecodeBounds = false
    }
    return context.assets.open(assetPath).use { input ->
        BitmapFactory.decodeStream(input, null, options)
    }
}

private data class Plate(
    val id: String, val topicId: String, val page: Int, val filename: String,
    val captionEn: String, val captionTa: String, val author: String, val licence: String,
    val sourceUrl: String, val licenceUrl: String, val modifications: String,
    val assetDirectory: String = "figures",
    val referenceOnly: Boolean = false,
    val secondarySourceUrl: String = ""
)

private data class DiagramSlot(
    val id: String, val topicId: String, val page: Int,
    val captionEn: String, val captionTa: String, val provisionalFigureId: String?
)

@Composable
internal fun FigureGallery(topicId: String, page: Int, lang: ReadingLanguage, requestedCount: Int = 0) {
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    val plates = remember(context) {
        runCatching {
            val raw = context.assets.open("figures.json").bufferedReader().use { it.readText() }
            val array = JSONArray(raw)
            (0 until array.length()).map { index ->
                array.getJSONObject(index).let { entry ->
                    Plate(entry.getString("id"), entry.getString("topicId"),
                        entry.getInt("page"), entry.getString("file"),
                        entry.getString("captionEn"), entry.getString("captionTa"),
                        entry.getString("author"), entry.getString("license"),
                        entry.optString("sourceUrl", ""),
                        entry.optString("licenseUrl", ""),
                        entry.optString("modifications", ""))
                }
            }
        }.getOrDefault(emptyList())
    }
    val pencilPlates = remember(context) {
        val raw = context.assets.open("pencil_plates/manifest.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val entries = JSONObject(raw).getJSONArray("figures")
        (0 until entries.length()).map { entries.getJSONObject(it) }
            .associateBy { it.getString("diagramId") to it.getString("lang") }
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
    val pencilBySlot = pageSlots.mapNotNull { slot ->
        // English-labeled anatomical plates are intentionally shared across language
        // modes. The translated lesson narrative and caption remain language-specific.
        val entry = pencilPlates[slot.id to "en"] ?: pencilPlates[slot.id to "shared"]
            ?: return@mapNotNull null
        // Use the registered canonical asset path. Discarding the parent folder
        // previously concealed 25 incorrect `figures/` manifest entries.
        val assetPath = entry.getString("path")
        val assetDirectory = assetPath.substringBefore('/')
        val filename = assetPath.substringAfter('/')
        if (assetDirectory != "pencil_plates" || filename.contains('/') ||
            filename.startsWith('.') || !filename.endsWith(".png")) return@mapNotNull null
        slot to Plate(
            id = slot.id, topicId = slot.topicId, page = slot.page,
            filename = filename,
            captionEn = listOf(slot.captionEn, entry.optString("keyEn")).filter { it.isNotBlank() }.joinToString("\n"),
            captionTa = listOf(slot.captionTa, entry.optString("keyTa")).filter { it.isNotBlank() }.joinToString("\n"),
            author = entry.getString("author"),
            licence = entry.optString("license", ""),
            sourceUrl = entry.optString("sourceUrl", "").ifBlank {
                entry.optJSONArray("referenceUrls")?.optString(0)
                    ?: entry.optString("referenceUrl", "")
            },
            licenceUrl = entry.optString("licenseUrl", ""),
            modifications = entry.optString("modifications", ""),
            assetDirectory = assetDirectory,
            referenceOnly = entry.optString("sourceUrl", "").isBlank(),
            secondarySourceUrl = entry.optJSONArray("sourceUrls")?.optString(1) ?: ""
        )
    }
    val replacedIds = pencilBySlot.mapNotNull { it.first.provisionalFigureId }.toSet()
    val visiblePlates = pencilBySlot.map { it.second } +
        relevant.filter { it.id in matchingDraftIds && it.id !in replacedIds }
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
        visiblePlates.forEach { plate ->
            val bitmap = remember(context, plate.assetDirectory, plate.filename) {
                runCatching {
                    decodePlateBitmap(context, plate.assetDirectory, plate.filename,
                        maxLongestEdgePx = 1200)?.asImageBitmap()
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
                        Text(if (plate.assetDirectory == "pencil_plates")
                            (if (lang == ReadingLanguage.TA)
                                "வரைவுப் படம் · உடற்கூறியல் சரிபார்ப்பு நிலுவையில் உள்ளது"
                             else "Draft anatomical plate · scientific review pending")
                            else if (plate.sourceUrl.isNotEmpty())
                            (if (lang == ReadingLanguage.TA)
                                "பட உரிமையாளர் குறிப்பிடப்பட்ட ஆதாரம் · அறிவியல் ஒப்புதல் நிலுவை"
                             else "Source-credited reference · anatomical approval pending")
                            else (if (lang == ReadingLanguage.TA)
                                "தற்காலிகக் கோட்டோவியம் · அறிவியல் ஒப்புதல் நிலுவை"
                             else "Provisional outline · anatomical approval pending"),
                            fontWeight = FontWeight.SemiBold)
                        Image(bitmap = bitmap, contentDescription = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn,
                            contentScale = ContentScale.Fit,
                            modifier = Modifier.fillMaxWidth().heightIn(min = 170.dp, max = 340.dp)
                                .clickable { zoomed = true }.testTag("figure-image-" + plate.id))
                        Text(if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn)
                        Text(
                            if (lang == ReadingLanguage.TA)
                                "படத்தை உருவாக்கியது: " + plate.author +
                                    if (plate.licence.isEmpty()) "" else " · உரிமம்: " + plate.licence
                            else "Image creator: " + plate.author +
                                    if (plate.licence.isEmpty()) "" else " · Licence: " + plate.licence,
                            style = MaterialTheme.typography.labelSmall
                        )
                        if (plate.sourceUrl.isNotEmpty()) {
                            Text(
                                if (plate.referenceOnly)
                                    if (lang == ReadingLanguage.TA)
                                        "உடற்கூறியல் தகவல் ஆதாரம்; மூலப் படம் நகலெடுக்கப்படவில்லை."
                                    else "Anatomical reference only; source image not reproduced."
                                else if (lang == ReadingLanguage.TA)
                                    "பட மூலம்: Wikimedia Commons · மாற்றங்கள்: " + plate.modifications
                                else "Image source: Wikimedia Commons · Changes: " + plate.modifications,
                                style = MaterialTheme.typography.labelSmall
                            )
                            TextButton(
                                onClick = { uriHandler.openUri(plate.sourceUrl) },
                                modifier = Modifier.testTag("figure-source-link-" + plate.id)
                            ) {
                                Text(if (plate.referenceOnly)
                                    if (lang == ReadingLanguage.TA) "உடற்கூறியல் ஆதாரம்" else "Anatomical reference"
                                else if (lang == ReadingLanguage.TA)
                                    "படத்தின் மூலப் பக்கமும் உரிமையாளரும்"
                                else "Original image and creator")
                            }
                            if (plate.secondarySourceUrl.isNotEmpty()) {
                                TextButton(onClick = { uriHandler.openUri(plate.secondarySourceUrl) }) {
                                    Text(if (lang == ReadingLanguage.TA)
                                        "இரண்டாவது பட மூலமும் உரிமையாளரும்"
                                    else "Second original image and creator")
                                }
                            }
                            if (!plate.referenceOnly && plate.licenceUrl.isNotEmpty()) {
                                TextButton(onClick = { uriHandler.openUri(plate.licenceUrl) }) {
                                    Text(if (lang == ReadingLanguage.TA)
                                        "பயன்பாட்டு உரிம விவரங்கள்" else "Image reuse licence")
                                }
                            }
                        }
                        Text(if (lang == ReadingLanguage.TA) "பெரிதாக்கப் படத்தைத் தொடுக" else "Tap image to enlarge",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    }
                }
                if (zoomed) {
                    // Load the unmodified full-resolution image only inside the dialog.
                    val fullImage = remember(context, plate.assetDirectory, plate.filename, zoomed) {
                        runCatching {
                            decodePlateBitmap(context, plate.assetDirectory, plate.filename)
                                ?.asImageBitmap()
                        }.getOrNull()
                    }
                    var scale by remember(plate.id, zoomed) { mutableFloatStateOf(1f) }
                    var offset by remember(plate.id, zoomed) { mutableStateOf(Offset.Zero) }
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
                                    if (fullImage == null) {
                                        Text(if (lang == ReadingLanguage.TA)
                                            "முழு அளவிலான படத்தைத் திறக்க இயலவில்லை."
                                        else "Full-resolution image could not be opened.",
                                            color = MaterialTheme.colorScheme.error)
                                    } else {
                                        Image(fullImage,
                                            contentDescription = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn,
                                            contentScale = ContentScale.Fit,
                                            modifier = Modifier.fillMaxSize().graphicsLayer {
                                                scaleX = scale; scaleY = scale
                                                translationX = offset.x; translationY = offset.y
                                            })
                                    }
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
                            "இவை தற்காலிகப் படங்கள்; உடற்கூறியல் அமைப்பு, பெயரிடல், விகிதங்கள் ஆகியவற்றின் துல்லியம் சரிபார்க்கப்பட வேண்டும்."
                        else "These figures are provisional: morphology, labelling and proportions require scientific verification.",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
