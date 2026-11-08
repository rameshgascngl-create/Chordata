package `in`.gasc.zoology.chordata

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.performTextInput
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onFirst
import androidx.compose.ui.test.isDisplayed
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performScrollToIndex
import androidx.compose.ui.test.captureToImage
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.graphics.asAndroidBitmap
import androidx.test.platform.app.InstrumentationRegistry
import android.graphics.Bitmap
import android.content.ContentValues
import android.provider.MediaStore
import `in`.gasc.zoology.chordata.data.ContentRepository
import `in`.gasc.zoology.chordata.ui.decodePlateBitmap
import org.junit.Rule
import org.junit.Test

class ReaderNavigationTest {

    @Test fun creditedReferenceAssetsAreBundledAndMappedCorrectly() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val images = org.json.JSONArray(context.assets.open("figures.json").bufferedReader().use { it.readText() })
        org.junit.Assert.assertEquals(7, images.length())
        val sourced = (0 until images.length()).map { images.getJSONObject(it) }
            .filter { it.optString("sourceUrl").startsWith("https://commons.wikimedia.org/wiki/File:") }
        org.junit.Assert.assertEquals(4, sourced.size)
        for (plate in sourced) {
            org.junit.Assert.assertTrue(plate.getString("author").isNotBlank())
            org.junit.Assert.assertTrue(plate.getString("license").isNotBlank())
            context.assets.open("figures/" + plate.getString("file")).use { stream ->
                val bmp = android.graphics.BitmapFactory.decodeStream(stream)
                org.junit.Assert.assertNotNull(plate.getString("id"), bmp)
                org.junit.Assert.assertTrue(bmp.width >= 400 && bmp.height >= 500)
                bmp.recycle()
            }
        }
    }

    /**
     * Validate the exact assets shipped in the APK, not just the ZIP/source tree.
     * Decode bounds only to keep peak memory low on API 24 devices.
     * The scientific-review status must remain provisional.
     */
    @Test fun all64ProvisionalPlatesAreBundledAndDecode() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val raw = context.assets.open("pencil_plates/manifest.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val figures = org.json.JSONObject(raw).getJSONArray("figures")
        org.junit.Assert.assertTrue(figures.length() >= 64)
        val ids = mutableSetOf<String>()
        val languages = mutableMapOf<String, MutableSet<String>>()
        val variants = mutableSetOf<String>()
        for (i in 0 until figures.length()) {
            val entry = figures.getJSONObject(i)
            val diagramId = entry.getString("diagramId")
            val language = entry.getString("lang")
            org.junit.Assert.assertTrue(language in setOf("en", "ta", "shared"))
            org.junit.Assert.assertTrue("Duplicate figure variant: $diagramId / $language",
                variants.add("$diagramId:$language"))
            ids.add(diagramId)
            languages.getOrPut(diagramId) { mutableSetOf() }.add(language)
            org.junit.Assert.assertTrue(entry.getString("reviewStatus").startsWith("PROVISIONAL_"))
            // Decode the *exact* path from the manifest. Deriving a basename would
            // hide an obsolete or incorrectly nested directory entry.
            val path = entry.getString("path")
            org.junit.Assert.assertTrue("Noncanonical asset path: $path",
                path.startsWith("pencil_plates/") && path.count { it == '/' } == 1 &&
                    path.substringAfter('/').endsWith(".png"))
            val options = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
            context.assets.open(path).use { input ->
                android.graphics.BitmapFactory.decodeStream(input, null, options)
            }
            org.junit.Assert.assertTrue("Image too small or invalid: $path",
                options.outWidth >= 1200 && options.outHeight >= 600)
        }
        val pack = ContentRepository.load(context)
        val requiredIds = pack.topics.flatMap { it.diagramIds }.toSet()
        org.junit.Assert.assertEquals(64, requiredIds.size)
        org.junit.Assert.assertEquals(requiredIds, ids)
        for (id in requiredIds) {
            org.junit.Assert.assertTrue("No English-labelled plate for: $id",
                languages[id]?.any { it == "en" || it == "shared" } == true)
        }
    }

    /**
     * The preview must remain bounded, while the pinch-zoom bitmap must be
     * the exact, unscaled asset in the APK. Artwork is intentionally replaced
     * during QA: source image dimensions are NOT fixed constants.
     */
    @Test fun lessonPreviewIsBoundedAndZoomAssetIsFullResolution() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val upgraded = listOf(
            "frog_arterial_system_en.png",
            "rana_respiration_en.png",
            "fish_scale_types.png"
        )
        for (filename in upgraded) {
            val path = "pencil_plates/$filename"
            val bounds = android.graphics.BitmapFactory.Options().apply {
                inJustDecodeBounds = true
            }
            context.assets.open(path).use { stream ->
                android.graphics.BitmapFactory.decodeStream(stream, null, bounds)
            }
            org.junit.Assert.assertTrue("No bitmap bounds: $path",
                bounds.outWidth >= 1200 && bounds.outHeight >= 600)

            val preview = requireNotNull(decodePlateBitmap(
                context, "pencil_plates", filename, maxLongestEdgePx = 1200))
            val zoom = requireNotNull(decodePlateBitmap(
                context, "pencil_plates", filename))
            try {
                org.junit.Assert.assertTrue("Unbounded preview: $path",
                    maxOf(preview.width, preview.height) <= 1200)
                org.junit.Assert.assertEquals("Zoom width was downsampled: $path",
                    bounds.outWidth, zoom.width)
                org.junit.Assert.assertEquals("Zoom height was downsampled: $path",
                    bounds.outHeight, zoom.height)
                org.junit.Assert.assertTrue("Preview is not smaller than zoom: $path",
                    preview.width.toLong() * preview.height <
                        zoom.width.toLong() * zoom.height)
            } finally {
                preview.recycle()
                zoom.recycle()
            }
        }
    }

    @Test fun greenTickTamilAiVariantsAreSelectedButHeldOnesFallbackToEnglish() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val entries = org.json.JSONObject(
            context.assets.open("pencil_plates/manifest.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
        ).getJSONArray("figures")
        val byIdAndLanguage = (0 until entries.length()).map { entries.getJSONObject(it) }
            .associateBy { it.getString("diagramId") to it.getString("lang") }

        fun selected(diagramId: String, lang: `in`.gasc.zoology.chordata.domain.ReadingLanguage): String {
            return requireNotNull(
                `in`.gasc.zoology.chordata.ui.selectProvisionalPlate(byIdAndLanguage, diagramId, lang)
            ).getString("path")
        }

        val ta = `in`.gasc.zoology.chordata.domain.ReadingLanguage.TA
        val en = `in`.gasc.zoology.chordata.domain.ReadingLanguage.EN
        org.junit.Assert.assertEquals("pencil_plates/avian_respiration_ta.png",
            selected("u5-flight-adaptations-avian-lung", ta))
        org.junit.Assert.assertEquals("pencil_plates/columba_skeleton_ta.png",
            selected("u5-columba-endoskeleton", ta))
        org.junit.Assert.assertEquals("pencil_plates/avian_respiration_en.png",
            selected("u5-flight-adaptations-avian-lung", en))
        org.junit.Assert.assertEquals("pencil_plates/columba_skeleton_en.png",
            selected("u5-columba-endoskeleton", en))
        // Material errors are not green-ticked: they must not override the
        // alternative, credited English anatomical plates.
        org.junit.Assert.assertEquals("pencil_plates/branchiostoma_en.png",
            selected("u1-cephalochordata-branchiostoma-labelled", ta))
        org.junit.Assert.assertEquals("pencil_plates/rabbit_skeleton_en.png",
            selected("u5-rabbit-endoskeleton", ta))
        // Other already-approved AI PNGs remain accessible through shared/en.
        org.junit.Assert.assertEquals("pencil_plates/amphibian_orders.png",
            selected("u3-amphibia-classification-living-orders", ta))
        org.junit.Assert.assertEquals("pencil_plates/calotes_brain_dorsal_en.png",
            selected("u4-calotes-brain", ta))
    }

    @Test fun tamilCompactHeaderFitsAndBackWorks() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithText("பாடம்").assertIsDisplayed()
        rule.onNodeWithTag("lesson-back").assertIsDisplayed().performClick()
        rule.onNodeWithText("அனைத்துப் பாடங்கள்").assertIsDisplayed()
    }


    @get:Rule val rule = createAndroidComposeRule<MainActivity>()

    private fun selectEnglish() {
        val english = rule.onAllNodesWithText("English")
        if (english.fetchSemanticsNodes().isNotEmpty()) english.onFirst().performClick()
        else rule.onNodeWithText("ஆங்கிலம்").performClick()
    }

    @Test fun opensFirstChapterAndAdvancesToLesson() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onAllNodesWithText("Origin of Chordata").onFirst().assertIsDisplayed()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithText("Next ›").performClick()
        rule.waitUntil(timeoutMillis = 5_000) {
            runCatching { rule.onNodeWithText("Deuterostome ancestry").isDisplayed() }
                .getOrDefault(false)
        }
        rule.onNodeWithText("Deuterostome ancestry").assertIsDisplayed()
    }

    @Test fun scoliodonBrainPlateIsReachableOnItsExactFourthSection() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Scoliodon")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        // The previously rejected synthetic plate is replaced by a source-verified
        // 1878 dogfish comparison; do not imply an exact Scoliodon dissection.
        for (section in 0 until 4) {
            rule.onNodeWithTag("lesson-reader-list")
                .performScrollToIndex(if (section == 0) 3 else 4)
            rule.onNodeWithText("Next ›").performClick()
        }
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-rejected-quality").assertDoesNotExist()
        rule.onNodeWithTag("figure-image-u2-scoliodon-brain-labelled")
            .assertIsDisplayed()
            .performClick()
        rule.onNodeWithText("Close").assertIsDisplayed()
        captureQaScreen("scoliodon-brain-zoom-en-100")
    }

    @Test fun canSwitchTamilAndIncreaseTextSize() {
        selectEnglish()
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("The Chordata Fieldbook").assertDoesNotExist()
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-page-heading").assertTextEquals("முதுகுநாணிகளின் தோற்றம்")
    }
    @Test fun englishReferenceFigureOpensNativeZoom() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Scoliodon")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").assertDoesNotExist()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithText("Next ›").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").assertIsDisplayed().performClick()
        rule.onNodeWithText("Close").assertIsDisplayed()
    }
    /**
     * Emulator evidence is written to MediaStore Pictures so the CI job
     * can extract the exact English/Tamil screen shown by Compose.
     */
    private fun captureQaScreen(name: String) {
        require(Regex("[a-z0-9-]+").matches(name))
        rule.waitForIdle()
        // MediaStore survives Android Gradle's post-test package uninstall.
        // getExternalFilesDir() does not, so adb pull after connectedAndroidTest failed.
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val resolver = context.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, "$name.png")
            put(MediaStore.Images.Media.MIME_TYPE, "image/png")
            put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/ChordataQA/")
            put(MediaStore.Images.Media.IS_PENDING, 1)
        }
        val uri = requireNotNull(resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)) {
            "Unable to create screenshot media entry"
        }
        try {
            val bitmap = rule.onRoot().captureToImage().asAndroidBitmap()
            requireNotNull(resolver.openOutputStream(uri)).use { stream ->
                check(bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream))
            }
            val completed = ContentValues().apply { put(MediaStore.Images.Media.IS_PENDING, 0) }
            check(resolver.update(uri, completed, null, null) > 0)
        } catch (failure: Throwable) {
            resolver.delete(uri, null, null)
            throw failure
        }
    }

    @Test fun englishReaderIsExclusiveAtNormalScale() {
        selectEnglish()
        rule.onNodeWithText("The Chordata Fieldbook").assertIsDisplayed()
        rule.onNodeWithText("முதுகுநாணிகள் கற்றல் களஞ்சியம்").assertDoesNotExist()
        captureQaScreen("home-en-100")
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-page-heading").assertTextEquals("Origin of Chordata")
        rule.onNodeWithText("பாட அமைப்பு").assertDoesNotExist()
        captureQaScreen("origin-overview-en-100")
    }

    @Test fun tamilReaderIsExclusiveAt200Percent() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("The Chordata Fieldbook").assertDoesNotExist()
        rule.onNodeWithText("முதுகுநாணிகள் கற்றல் களஞ்சியம்").assertIsDisplayed()
        captureQaScreen("home-ta-200")
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-page-heading").assertTextEquals("முதுகுநாணிகளின் தோற்றம்")
        rule.onNodeWithText("Chapter outline").assertDoesNotExist()
        captureQaScreen("origin-overview-ta-200")
    }

    @Test fun tamilFigureOpensNativeZoomAt200Percent() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Scoliodon")
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").assertDoesNotExist()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithText("அடுத்து ›").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").assertIsDisplayed()
        captureQaScreen("scoliodon-figure-ta-200")
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").performClick()
        rule.onNodeWithText("மூடுக").assertIsDisplayed()
        captureQaScreen("scoliodon-zoom-ta-200")
    }

    private fun verifyProvisionalExternalFigureLocation(search: String, figureId: String) {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput(search)
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("figure-image-" + figureId).assertDoesNotExist()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithText("Next ›").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-" + figureId).assertIsDisplayed()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithText("Next ›").performClick()
        rule.onNodeWithTag("figure-image-" + figureId).assertDoesNotExist()
    }

    @Test fun pigeonFigureOnlyAppearsOnExternalMorphologyLesson() {
        verifyProvisionalExternalFigureLocation("Columba", "u5-columba-external")
    }

    @Test fun rabbitFigureOnlyAppearsOnExternalMorphologyLesson() {
        verifyProvisionalExternalFigureLocation("Rabbit", "u5-rabbit-external")
    }

    @Test fun all64FigureSlotsAreMappedToActualSectionsInApk() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val pack = ContentRepository.load(context)
        val topicById = pack.topics.associateBy { it.id }
        val raw = context.assets.open("figure_slots.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val slots = org.json.JSONObject(raw).getJSONArray("slots")
        org.junit.Assert.assertEquals(64, slots.length())
        val visited = mutableSetOf<String>()
        var draftLinks = 0
        for (i in 0 until slots.length()) {
            val slot = slots.getJSONObject(i)
            val id = slot.getString("id")
            check(visited.add(id)) { "Duplicate diagram slot" }
            val topic = requireNotNull(topicById[slot.getString("topicId")])
            check(id in topic.diagramIds)
            val page = slot.getInt("page")
            check(page in 1..topic.sections.size)
            check(topic.sections[page - 1].key == slot.getString("sectionKey"))
            check(slot.getString("captionEn").isNotBlank())
            check(slot.getString("captionTa").isNotBlank())
            if (!slot.isNull("provisionalFigureId")) draftLinks++
        }
        org.junit.Assert.assertEquals(pack.topics.flatMap { it.diagramIds }.toSet(), visited)
        org.junit.Assert.assertEquals(7, draftLinks)
    }

}
