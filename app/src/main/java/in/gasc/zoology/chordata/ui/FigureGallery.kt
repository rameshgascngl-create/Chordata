package `in`.gasc.zoology.chordata.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.BitmapRegionDecoder
import android.graphics.Rect
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
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.sp
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

/**
 * Focus the credited 1878 comparative dogfish engraving without upscaling
 * or changing the source PNG. The full original remains stored unchanged.
 * Region decoding holds only 500 x 941 pixels (~1.8 MiB ARGB_8888), rather
 * than decoding the 1420 x 1010 composite (~5.5 MiB).
 *
 * The historical species was NOT confirmed as Scoliodon laticaudus.
 */
internal fun decodeFocusedHistoricalDogfishBrain(
    context: Context, assetDirectory: String, filename: String
): Bitmap? {
    context.assets.open("$assetDirectory/$filename").use { stream ->
        val decoder = BitmapRegionDecoder.newInstance(stream, false) ?: return null
        return try {
            if (decoder.width != 1420 || decoder.height != 1010) null
            else decoder.decodeRegion(Rect(40, 35, 540, 976), BitmapFactory.Options())
        } finally {
            decoder.recycle()
        }
    }
}

/**
 * Present only Figure 8 (A-D) from the authentic 1905 composite plate on
 * the Ascidia metamorphosis lesson. Figures 9-10 depict Balanoglossus and
 * must not be misread as ascidian stages. Source PNG and source credits stay
 * byte-for-byte intact; these are temporary region decodes, not new assets.
 *
 * Rectangles were verified against the 1488 x 2387 original plate:
 * A/B = free-swimming + attached larvae; C/D = older attached stage + tail.
 */
internal fun decodeFocusedAscidianPanel(
    context: Context, assetDirectory: String, filename: String, panel: Int
): Bitmap? {
    if (assetDirectory != "pencil_plates" || filename != "ascidia_metamorphosis.png") return null
    val bounds = when (panel) {
        0 -> Rect(780, 0, 1488, 540)
        1 -> Rect(1070, 545, 1488, 1190)
        else -> return null
    }
    context.assets.open("$assetDirectory/$filename").use { stream ->
        val decoder = BitmapRegionDecoder.newInstance(stream, false) ?: return null
        return try {
            if (decoder.width != 1488 || decoder.height != 2387) null
            else decoder.decodeRegion(bounds, BitmapFactory.Options())
        } finally {
            decoder.recycle()
        }
    }
}


/** Region-based student views; original credited PNG files are not changed. */
internal fun decodeTeachingPanel(
    context: Context, assetDirectory: String, filename: String, panel: Int
): Bitmap? {
    if (assetDirectory != "pencil_plates") return null
    val (width, height, region) = when (filename) {
        "pigeon_urinogenital_en.png" -> Triple(3360, 1900, when (panel) {
            0 -> Rect(115, 260, 1150, 1540)
            1 -> Rect(1150, 260, 2220, 1540)
            2 -> Rect(2270, 220, 3340, 1730)
            else -> return null
        })
        "columba_skeleton_en.png" -> Triple(1600, 2104, when (panel) {
            0 -> Rect(260, 400, 1530, 1690)
            else -> return null
        })
        "fish_accessory_breathing_en.png" -> Triple(1800, 1120, when (panel) {
            0 -> Rect(0, 0, 1800, 1050)
            else -> return null
        })
        else -> return null
    }
    context.assets.open("$assetDirectory/$filename").use { input ->
        val decoder = BitmapRegionDecoder.newInstance(input, false) ?: return null
        return try {
            if (decoder.width != width || decoder.height != height) null
            else decoder.decodeRegion(region, BitmapFactory.Options())
        } finally { decoder.recycle() }
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

/**
 * Use a Tamil-labelled AI figure only when its exact PNG has received the
 * user's green-tick permission for provisional QA use. Otherwise use the
 * existing English/shared plate (including historical anatomy references).
 * This is a display choice, never independent Biology/Tamil certification.
 */
internal fun selectProvisionalPlate(
    entries: Map<Pair<String, String>, JSONObject>,
    diagramId: String,
    language: ReadingLanguage
): JSONObject? {
    val fallback = entries[diagramId to "en"] ?: entries[diagramId to "shared"]
    val tamil = if (language == ReadingLanguage.TA) entries[diagramId to "ta"] else null
    return tamil?.takeIf {
        it.optString("scientificRiskHold").isBlank() &&
        it.optString("aiQaIntegrationDecision") == "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE" &&
            it.optString("reviewStatus").startsWith("PROVISIONAL_") &&
            it.optString("visualReview") != "USER_REJECTED_REPLACEMENT_REQUIRED"
    } ?: fallback
}

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
    val userRejectedSlots = pageSlots.filter { slot ->
        val entry = pencilPlates[slot.id to "en"] ?: pencilPlates[slot.id to "shared"]
        entry?.optString("visualReview") == "USER_REJECTED_REPLACEMENT_REQUIRED"
    }
    val matchingDraftIds = pageSlots.mapNotNull { it.provisionalFigureId }.toSet()
    val pencilBySlot = pageSlots.mapNotNull { slot ->
        // English-labelled plates remain the default in both readers; a green-ticked
        // Tamil AI PNG may be displayed on the Tamil page without requiring perfect art.
        val entry = selectProvisionalPlate(pencilPlates, slot.id, lang)
            ?: return@mapNotNull null
        // Rejected drawings must not appear as valid anatomical teaching plates.
        // Keep the registered slot and caption visible in the pending section instead.
        if (entry.optString("visualReview") == "USER_REJECTED_REPLACEMENT_REQUIRED")
            return@mapNotNull null
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
            captionEn = listOf(slot.captionEn,
                entry.optString("learnerKeyEn").ifBlank { entry.optString("keyEn") })
                .filter { it.isNotBlank() }.joinToString("\n"),
            captionTa = listOf(slot.captionTa,
                entry.optString("learnerKeyTa").ifBlank { entry.optString("keyTa") })
                .filter { it.isNotBlank() }.joinToString("\n"),
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
    Column(verticalArrangement = Arrangement.spacedBy(7.dp)) {
        if (userRejectedSlots.isNotEmpty()) {
            Text(
                if (lang == ReadingLanguage.TA)
                    "இந்தப் பாடத்திற்கான உடற்கூறியல் விளக்கப்படம் தற்போது கிடைக்கவில்லை."
                else "The anatomical illustration for this section is currently unavailable.",
                modifier = Modifier.testTag("figure-rejected-quality"),
                color = MaterialTheme.colorScheme.error
            )
        }
        if (allSlots == null) {
            Text(
                if (lang == ReadingLanguage.TA) "வரைபட இருப்பிடப் பதிவேடு கிடைக்கவில்லை."
                else "Diagram placement register unavailable.",
                modifier = Modifier.testTag("figure-register-error"),
                color = MaterialTheme.colorScheme.error
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
                    val preview = if (plate.id == "u2-scoliodon-brain-labelled") {
                        decodeFocusedHistoricalDogfishBrain(
                            context, plate.assetDirectory, plate.filename)
                    } else null
                    val bounded = preview ?: decodePlateBitmap(
                        context, plate.assetDirectory, plate.filename,
                        maxLongestEdgePx = 1200)
                    bounded?.asImageBitmap()
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
                var zoomPanel by remember(plate.id) { mutableIntStateOf(-1) }
                var showOriginal by remember(plate.id) { mutableStateOf(false) }
                val isAscidia = plate.id == "u1-urochordata-ascidia-larva-adult"
                val isPigeonUro = plate.id == "u5-columba-urinogenital"
                val isPigeonSkeleton = plate.id == "u5-columba-endoskeleton" &&
                    plate.filename == "columba_skeleton_en.png"
                val isAccessoryFish = plate.id == "u2-accessory-respiration-accessory-organs-comparison"
                val focused = remember(context, plate.assetDirectory, plate.filename) {
                    val count = when {
                        isPigeonUro -> 3
                        isPigeonSkeleton || isAccessoryFish -> 1
                        else -> 0
                    }
                    (0 until count).map { index ->
                        runCatching {
                            decodeTeachingPanel(context, plate.assetDirectory, plate.filename, index)
                                ?.asImageBitmap()
                        }.getOrNull()
                    }
                }
                val ascidiaAB = remember(context, plate.assetDirectory, plate.filename) {
                    if (isAscidia) runCatching {
                        decodeFocusedAscidianPanel(context, plate.assetDirectory, plate.filename, 0)
                            ?.asImageBitmap()
                    }.getOrNull() else null
                }
                val ascidiaCD = remember(context, plate.assetDirectory, plate.filename) {
                    if (isAscidia) runCatching {
                        decodeFocusedAscidianPanel(context, plate.assetDirectory, plate.filename, 1)
                            ?.asImageBitmap()
                    }.getOrNull() else null
                }
                var creditsExpanded by remember(plate.id) { mutableStateOf(false) }
                var captionExpanded by remember(plate.id) { mutableStateOf(false) }
                val fullCaption = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn
                val conciseCaption = fullCaption.substringBefore('\n').trim()
                val extendedCaption = fullCaption.substringAfter('\n', "").trim()
                val previewHeight = when {
                    bitmap.height > bitmap.width * 1.2f -> 470.dp
                    bitmap.width > bitmap.height * 1.6f -> 250.dp
                    else -> 350.dp
                }
                Card(
                    modifier = Modifier.fillMaxWidth().testTag("figure-" + plate.id),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Column(Modifier.padding(10.dp),
                        verticalArrangement = Arrangement.spacedBy(5.dp)) {
                        Text(if (lang == ReadingLanguage.TA) "விளக்கப்படம்" else "Illustration",
                            color = MaterialTheme.colorScheme.primary,
                            fontWeight = FontWeight.SemiBold,
                            style = MaterialTheme.typography.labelMedium)
                        if (ascidiaAB != null && ascidiaCD != null) {
                            Text(
                                if (lang == ReadingLanguage.TA)
                                    "அசிடியன் உருமாற்றம் — வரலாற்றுப் படத்தின் 8A–8D பகுதிகள்"
                                else "Ascidian metamorphosis — historical figures 8A–8D",
                                fontWeight = FontWeight.Bold, fontSize = 15.sp,
                                color = MaterialTheme.colorScheme.primary
                            )
                            Image(bitmap = ascidiaAB,
                                contentDescription = if (lang == ReadingLanguage.TA)
                                    "8A நீந்தும் இளர்வி; 8B பற்றிய இளர்வி"
                                else "Figure 8A free-swimming larva; 8B recently attached larva",
                                contentScale = ContentScale.Fit,
                                modifier = Modifier.fillMaxWidth().height(235.dp)
                                    .clickable { zoomPanel = 0; zoomed = true }
                                    .testTag("figure-image-" + plate.id))
                            Text(if (lang == ReadingLanguage.TA)
                                    "8A: நீந்தும் தலைப்பிரட்டை இளர்வி. 8B: புதிதாகப் பற்றிய நிலை."
                                 else "8A — free-swimming tadpole larva. 8B — recently attached larva.",
                                fontSize = 13.sp, lineHeight = 18.sp)
                            Image(bitmap = ascidiaCD,
                                contentDescription = if (lang == ReadingLanguage.TA)
                                    "8C வளர்ந்த பற்றிய நிலை; 8D வாலின் குறுக்குவெட்டு"
                                else "Figure 8C later attached stage; 8D transverse section of larval tail",
                                contentScale = ContentScale.Fit,
                                modifier = Modifier.fillMaxWidth().height(460.dp)
                                    .clickable { zoomPanel = 1; zoomed = true }
                                    .testTag("figure-ascidia-stages-cd"))
                            Text(if (lang == ReadingLanguage.TA)
                                    "8C: வளர்ந்த பற்றிய நிலை. 8D: இளர்வி வாலின் குறுக்குவெட்டு."
                                 else "8C — later attached stage. 8D — transverse section of the larval tail.",
                                fontSize = 13.sp, lineHeight = 18.sp)
                            TextButton(onClick = { showOriginal = !showOriginal },
                                modifier = Modifier.testTag("figure-ascidia-original-toggle")) {
                                Text(if (showOriginal)
                                    if (lang == ReadingLanguage.TA) "முழுப் படத்தை மறை" else "Hide complete historical plate"
                                else if (lang == ReadingLanguage.TA) "1905 ஆம் ஆண்டின் முழுப் படம்" else "View complete 1905 historical plate")
                            }
                            if (showOriginal) {
                                Image(bitmap = bitmap,
                                    contentDescription = if (lang == ReadingLanguage.TA)
                                        "அசிடியன் மற்றும் பலனோக்ளாசஸ் இணைந்த வரலாற்றுப் படம்"
                                    else "Original composite plate with ascidians and separate Balanoglossus figures",
                                    contentScale = ContentScale.Fit,
                                    modifier = Modifier.fillMaxWidth().height(470.dp)
                                        .clickable { zoomPanel = -1; zoomed = true }
                                        .testTag("figure-ascidia-composite"))
                                Text(if (lang == ReadingLanguage.TA)
                                        "குறிப்பு: முழுப் படத்தின் 9–10 பகுதிகள் பலனோக்ளாசஸ்; அசிடியன் அல்ல."
                                     else "Note: Figures 9–10 in the complete plate depict Balanoglossus, not ascidians.",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 12.sp, lineHeight = 17.sp)
                            }
                        } else {
                            Image(bitmap = bitmap,
                                contentDescription = if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn,
                                contentScale = ContentScale.Fit,
                                modifier = Modifier.fillMaxWidth().height(previewHeight)
                                    .clickable { zoomPanel = -1; zoomed = true }
                                    .testTag("figure-image-" + plate.id))
                        }
                        Text(conciseCaption,
                            fontSize = 14.sp,
                            lineHeight = 19.sp,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = if (captionExpanded) Int.MAX_VALUE else 2,
                            overflow = TextOverflow.Ellipsis)
                        if (extendedCaption.isNotEmpty()) {
                            TextButton(onClick = { captionExpanded = !captionExpanded },
                                modifier = Modifier.testTag("figure-caption-toggle-" + plate.id)) {
                                Text(if (captionExpanded)
                                    if (lang == ReadingLanguage.TA) "விளக்கக் குறிப்பை மறை" else "Hide figure key"
                                else if (lang == ReadingLanguage.TA) "படக் குறியீடுகளைப் படிக்க" else "View labels and figure key")
                            }
                            if (captionExpanded) {
                                Text(extendedCaption, fontSize = 12.sp,
                                    lineHeight = 18.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                        TextButton(
                            onClick = { creditsExpanded = !creditsExpanded },
                            modifier = Modifier.testTag("figure-credits-toggle-" + plate.id)
                        ) {
                            Text(if (lang == ReadingLanguage.TA)
                                (if (creditsExpanded) "பட மூல விவரங்களை மறை" else "பட மூலம் மற்றும் உரிமம்")
                                else (if (creditsExpanded) "Hide image credits" else "Image source and credits"))
                        }
                        if (creditsExpanded) {
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
                                    "பட மூலத் தளம்: " + plate.sourceUrl.substringAfter("://").substringBefore("/") +
                                        " · செய்யப்பட்ட மாற்றங்கள்: " + plate.modifications
                                else "Image source site: " + plate.sourceUrl.substringAfter("://").substringBefore("/") +
                                        " · Changes: " + plate.modifications,
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
                        }
                        Text(if (lang == ReadingLanguage.TA) "பெரிதாகக் காண படத்தைத் தொடுக" else "Tap the illustration to zoom",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    }
                }
                if (zoomed) {
                    // Load the unmodified full-resolution image only inside the dialog.
                    val fullImage = remember(context, plate.assetDirectory, plate.filename, zoomed, zoomPanel) {
                        runCatching {
                            val focused = when {
                                isAscidia && zoomPanel in 0..1 -> decodeFocusedAscidianPanel(
                                    context, plate.assetDirectory, plate.filename, zoomPanel)
                                plate.id == "u2-scoliodon-brain-labelled" ->
                                    decodeFocusedHistoricalDogfishBrain(
                                        context, plate.assetDirectory, plate.filename)
                                else -> null
                            }
                            (focused ?: decodePlateBitmap(context, plate.assetDirectory, plate.filename))
                                ?.asImageBitmap()
                        }.getOrNull()
                    }
                    var scale by remember(plate.id, zoomed) {
                        // The tall historical dogfish engraving needs a wider initial
                        // view on narrow handsets; pan and pinch remain available.
                        mutableFloatStateOf(if (plate.id == "u2-scoliodon-brain-labelled") 1.25f else 1f)
                    }
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
                                // The full image key remains in the lesson card.
                                // Showing it again here previously compressed a tall
                                // engraving into a tiny area on 320 px Android screens.
                                Text(
                                    (if (lang == ReadingLanguage.TA) plate.captionTa else plate.captionEn)
                                        .substringBefore('\n'),
                                    maxLines = 2,
                                    modifier = Modifier.testTag("figure-zoom-caption-" + plate.id)
                                )
                            }
                        }
                    }
                }
            }
        }

    }
}
