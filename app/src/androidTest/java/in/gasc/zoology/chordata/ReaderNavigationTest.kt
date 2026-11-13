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
import `in`.gasc.zoology.chordata.data.ProgressStore
import `in`.gasc.zoology.chordata.domain.ReadingLanguage
import `in`.gasc.zoology.chordata.ui.decodePlateBitmap
import `in`.gasc.zoology.chordata.ui.decodeFocusedAscidianPanel
import `in`.gasc.zoology.chordata.ui.decodeTeachingPanel
import `in`.gasc.zoology.chordata.ui.selectedPlateNeedsReplacement
import `in`.gasc.zoology.chordata.ui.selectProvisionalPlate
import org.json.JSONObject
import org.junit.Rule
import org.junit.Test

class ReaderNavigationTest {

    @Test fun ownerApprovedProvisionalHeartAndSourcedPlatesAreAvailable() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val raw = context.assets.open("pencil_plates/manifest.json")
            .bufferedReader(Charsets.UTF_8).use { it.readText() }
        val variants = JSONObject(raw).getJSONArray("figures")
        val entries = (0 until variants.length())
            .map { variants.getJSONObject(it) }
            .associateBy { it.getString("diagramId") to it.getString("lang") }
        // Owner accepts minor image imperfections only; not independent anatomy approval.
        for (lang in ReadingLanguage.entries) {
            val heart = requireNotNull(selectProvisionalPlate(entries,
                "u4-calotes-arterial-system", lang))
            org.junit.Assert.assertFalse(selectedPlateNeedsReplacement(entries,
                "u4-calotes-arterial-system", lang))
            org.junit.Assert.assertEquals("AI_RECONSTRUCTION_QA_PROVISIONAL_ACCEPT_MINOR_COSMETIC_ERRORS", heart.getString("visualReview"))
            org.junit.Assert.assertEquals("2c3406c9def947bc61c22203aaa424ce8c9b7133eddd6d0a3163511340d5f7a3", heart.getString("sha256"))
            org.junit.Assert.assertTrue(heart.getString("reviewStatus").startsWith("PROVISIONAL_"))
            org.junit.Assert.assertTrue(heart.getString("editorialCaution").contains("RIGHT atrium"))
        }
        val sourced = listOf(
            "u4-snakes-india-big-four-identification",
            "u5-flight-adaptations-flight-muscles",
            "u5-marsupials-marsupial-life-history"
        )
        for (id in sourced) for (lang in ReadingLanguage.entries) {
            org.junit.Assert.assertFalse("New source plate should be selectable: $id $lang",
                selectedPlateNeedsReplacement(entries, id, lang))
            val entry = requireNotNull(selectProvisionalPlate(entries, id, lang))
            org.junit.Assert.assertEquals("SOURCED_TEACHING_FIGURE_QA_PROVISIONAL",
                entry.getString("visualReview"))
            org.junit.Assert.assertTrue(entry.getString("sourceUrl")
                .startsWith("https://commons.wikimedia.org/wiki/File:"))
        }
        for (lang in ReadingLanguage.entries) {
            val aquatic = requireNotNull(selectProvisionalPlate(entries,
                "u5-aquatic-mammals-aquatic-mammal-groups", lang))
            org.junit.Assert.assertEquals(
                "SOURCED_FOUR_AQUATIC_MAMMAL_PHOTOGRAPHS_QA_PROVISIONAL",
                aquatic.getString("visualReview"))
            org.junit.Assert.assertFalse(selectedPlateNeedsReplacement(entries,
                "u5-aquatic-mammals-aquatic-mammal-groups", lang))
            org.junit.Assert.assertEquals(4, aquatic.getJSONArray("sourceUrls").length())
            org.junit.Assert.assertTrue(aquatic.getString("keyEn")
                .contains("NOT one taxonomic order"))
        }
        for (lang in ReadingLanguage.entries) {
            val monotreme = requireNotNull(selectProvisionalPlate(entries,
                "u5-egg-laying-mammals-monotreme-reproduction", lang))
            org.junit.Assert.assertEquals(
                "SOURCED_REAL_MONOTREME_SPECIMENS_AND_ANATOMY_QA_PROVISIONAL",
                monotreme.getString("visualReview"))
            org.junit.Assert.assertFalse(selectedPlateNeedsReplacement(entries,
                "u5-egg-laying-mammals-monotreme-reproduction", lang))
            org.junit.Assert.assertEquals(3, monotreme.getJSONArray("sourceUrls").length())
            val monotremeKey = monotreme.getString("keyEn")
            org.junit.Assert.assertTrue(
                "Monotreme caption must distinguish platypus from echidna specimens",
                monotremeKey.contains("different species"))
            org.junit.Assert.assertTrue(
                "Photographs must not be presented as a single-species life cycle",
                monotremeKey.contains("not a chronological photographic life-cycle"))
        }
        for (lang in ReadingLanguage.entries) {
            val rabbit = requireNotNull(selectProvisionalPlate(entries, "u5-rabbit-sense-organs", lang))
            org.junit.Assert.assertEquals("SOURCED_REAL_RABBIT_SENSORY_PHOTO_QA_PROVISIONAL",
                rabbit.getString("visualReview"))
            org.junit.Assert.assertFalse(
                selectedPlateNeedsReplacement(entries, "u5-rabbit-sense-organs", lang))
            org.junit.Assert.assertEquals(
                "https://commons.wikimedia.org/wiki/File:Side_view_of_the_head_of_a_pet_rabbit_in_Brussels_(DSCF0830).jpg",
                rabbit.getString("sourceUrl"))
        }
        for (lang in ReadingLanguage.entries) {
            val photo = requireNotNull(selectProvisionalPlate(entries, "u4-calotes-external", lang))
            org.junit.Assert.assertEquals("SOURCED_REAL_SPECIMEN_PHOTO_QA_PROVISIONAL",
                photo.getString("visualReview"))
            org.junit.Assert.assertFalse(
                selectedPlateNeedsReplacement(entries, "u4-calotes-external", lang))
            org.junit.Assert.assertTrue(photo.getString("sourceUrl")
                .endsWith("File:Oriental_Lizard.jpg"))
        }
    }

    @Test fun portableLearningBackupRoundTripsAndRejectsInvalidImport() {
        val store = ProgressStore(InstrumentationRegistry.getInstrumentation().targetContext)
        val chapter = "u1-origin"
        try {
            org.junit.Assert.assertTrue(store.eraseAllLearningData())
            store.saveBookmarks(setOf(chapter))
            store.saveCompleted(setOf(chapter))
            store.saveQuizScore(chapter, 3)
            store.saveLanguage(ReadingLanguage.TA)
            store.saveTextScale(1.75f)

            val backup = store.exportLearningData()
            org.junit.Assert.assertEquals("chordata-learning-progress",
                JSONObject(backup).getString("format"))
            org.junit.Assert.assertFalse(store.importLearningData(
                """{"format":"chordata-learning-progress","version":1,"completed":[],"bookmarks":[],"quizScores":{},"language":"EN","textScale":4.0}"""))
            org.junit.Assert.assertTrue(chapter in store.completed())
            org.junit.Assert.assertFalse(store.importLearningData("{invalid"))
            org.junit.Assert.assertEquals(3, store.quizScore(chapter))

            org.junit.Assert.assertTrue(store.eraseAllLearningData())
            org.junit.Assert.assertTrue(store.importLearningData(backup))
            org.junit.Assert.assertEquals(setOf(chapter), store.bookmarks())
            org.junit.Assert.assertEquals(setOf(chapter), store.completed())
            org.junit.Assert.assertEquals(3, store.quizScore(chapter))
            org.junit.Assert.assertEquals(ReadingLanguage.TA, store.language())
            org.junit.Assert.assertEquals(1.75f, store.textScale(), 0.001f)
        } finally {
            org.junit.Assert.assertTrue(store.eraseAllLearningData())
        }
    }

    @Test fun backupRestoreRequiresConfirmationInEnglish() {
        selectEnglish()
        rule.onNodeWithTag("home-book-layout").performScrollToIndex(2)
        rule.onNodeWithTag("privacy-policy-entry").performClick()
        rule.onNodeWithTag("privacy-policy-page").performScrollToIndex(5)
        rule.onNodeWithTag("privacy-export-entry").assertExists()
        rule.onNodeWithTag("privacy-import-entry").performClick()
        rule.onNodeWithTag("privacy-import-dialog").assertExists()
        rule.onNodeWithTag("privacy-import-cancel").performClick()
        rule.onNodeWithTag("privacy-import-dialog").assertDoesNotExist()
    }

    @Test fun eraseLearningDataRequiresConfirmationAndPersistsDeletion() {
        selectEnglish()
        val store = ProgressStore(InstrumentationRegistry.getInstrumentation().targetContext)
        val chapter = "u1-origin"
        store.saveBookmarks(setOf(chapter))
        store.saveCompleted(setOf(chapter))
        store.saveQuizScore(chapter, 3)
        org.junit.Assert.assertTrue(chapter in store.bookmarks())
        org.junit.Assert.assertEquals(3, store.quizScore(chapter))

        rule.onNodeWithTag("home-book-layout").performScrollToIndex(2)
        rule.onNodeWithTag("privacy-policy-entry").performClick()
        rule.onNodeWithTag("privacy-policy-page").performScrollToIndex(6)
        rule.onNodeWithTag("privacy-erase-entry").performClick()
        rule.onNodeWithTag("privacy-erase-dialog").assertExists()
        rule.onNodeWithTag("privacy-erase-cancel").performClick()
        org.junit.Assert.assertTrue(chapter in store.bookmarks())
        org.junit.Assert.assertEquals(3, store.quizScore(chapter))
        rule.onNodeWithTag("privacy-erase-entry").performClick()
        rule.onNodeWithTag("privacy-erase-confirm").performClick()
        rule.onNodeWithTag("home-book-layout").assertExists()
        org.junit.Assert.assertTrue(store.bookmarks().isEmpty())
        org.junit.Assert.assertTrue(store.completed().isEmpty())
        org.junit.Assert.assertNull(store.quizScore(chapter))
        org.junit.Assert.assertEquals(1f, store.textScale(), 0.0001f)
        org.junit.Assert.assertEquals("EN", store.language().name)
    }

    @Test fun privacyPolicyIsAccessibleInTamilAt200Percent() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithTag("home-book-layout").performScrollToIndex(2)
        rule.onNodeWithTag("privacy-policy-entry").performClick()
        rule.onNodeWithTag("privacy-policy-page").assertExists()
        rule.onNodeWithTag("privacy-policy-heading").assertIsDisplayed()
        captureQaScreen("privacy-ta-200")
        rule.onNodeWithTag("privacy-policy-page").performScrollToIndex(7)
        rule.onNodeWithText("தனியுரிமை தொடர்பான கேள்விகள்").assertIsDisplayed()
        captureQaScreen("privacy-ta-200-footer")
        rule.onNodeWithTag("privacy-policy-back").performClick()
        rule.onNodeWithTag("home-book-layout").assertExists()
    }

    @Test fun privacyPolicyIsAvailableInEnglishWithoutNetwork() {
        selectEnglish()
        rule.onNodeWithTag("home-book-layout").performScrollToIndex(2)
        rule.onNodeWithTag("privacy-policy-entry").performClick()
        rule.onNodeWithTag("privacy-policy-page").assertExists()
        rule.onAllNodesWithText("Privacy policy").onFirst().assertExists()
        rule.onNodeWithTag("privacy-policy-back").performClick()
        rule.onNodeWithTag("home-book-layout").assertExists()
    }



    @Test fun milkSharkPanelExcludesTinyCompositeTextAndKeepsPreviewBounded() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val full = requireNotNull(decodeTeachingPanel(context, "pencil_plates",
            "scoliodon_external_anatomy_en.png", 0))
        val preview = requireNotNull(decodeTeachingPanel(context, "pencil_plates",
            "scoliodon_external_anatomy_en.png", 0, maxLongestEdgePx = 1200))
        try {
            org.junit.Assert.assertEquals(3000, full.width)
            org.junit.Assert.assertEquals(805, full.height)
            org.junit.Assert.assertTrue(maxOf(preview.width, preview.height) <= 1200)
        } finally { full.recycle(); preview.recycle() }
    }

    @Test fun threeOriginalCambridgeAccessoryFiguresAreBundledOfflineAndUnmodified() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val jsonText = context.assets.open("historical_figures/sources.json")
            .bufferedReader().use { it.readText() }
        val figures = org.json.JSONObject(jsonText).getJSONArray("figures")
        org.junit.Assert.assertEquals(3, figures.length())
        val expected = listOf(169, 171, 172)
        expected.forEachIndexed { index, number ->
            val item = figures.getJSONObject(index)
            org.junit.Assert.assertEquals(number, item.getInt("figure"))
            val name = "historical_figures/cnh1904_fig" + number + ".jpg"
            org.junit.Assert.assertEquals(name, item.getString("path"))
            val bytes = context.assets.open(name).use { it.readBytes() }
            org.junit.Assert.assertEquals(item.getInt("byteLength"), bytes.size)
            org.junit.Assert.assertEquals(0xFF, bytes[0].toInt() and 0xff)
            org.junit.Assert.assertEquals(0xD8, bytes[1].toInt() and 0xff)
            val digest = java.security.MessageDigest.getInstance("SHA-1")
            digest.update("blob " .plus(bytes.size).plus("\u0000").toByteArray(Charsets.UTF_8))
            val sha = digest.digest(bytes).joinToString("") {
                "%02x".format(it.toInt() and 0xff)
            }
            org.junit.Assert.assertEquals(item.getString("gitBlobSha1"), sha)
            val bounds = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
            context.assets.open(name).use {
                android.graphics.BitmapFactory.decodeStream(it, null, bounds)
            }
            org.junit.Assert.assertTrue(bounds.outWidth > 500 && bounds.outHeight > 400)
        }
        org.junit.Assert.assertEquals(
            "Saccobranchus singio",
            figures.getJSONObject(2).getString("originalCaptionTaxon")
        )
    }

    @Test fun pigeonSensoryEngravingsAreFocusedAndExcludeInternalReviewFooter() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val directory = "pencil_plates"
        val plate = "pigeon_eye_ear_en.png"
        val eye = requireNotNull(decodeTeachingPanel(context, directory, plate, 0))
        val ear = requireNotNull(decodeTeachingPanel(context, directory, plate, 1))
        try {
            org.junit.Assert.assertEquals(720, eye.width)
            org.junit.Assert.assertEquals(650, eye.height)
            org.junit.Assert.assertEquals(568, ear.width)
            org.junit.Assert.assertEquals(455, ear.height)
        } finally {
            eye.recycle()
            ear.recycle()
        }
        org.junit.Assert.assertNull(decodeTeachingPanel(context, directory, plate, 2))
        val raw = context.assets.open(directory + "/" + plate).use { it.readBytes() }
        val opts = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
        context.assets.open(directory + "/" + plate).use {
            android.graphics.BitmapFactory.decodeStream(it, null, opts)
        }
        org.junit.Assert.assertEquals(1600, opts.outWidth)
        org.junit.Assert.assertEquals(1260, opts.outHeight)
        org.junit.Assert.assertTrue(raw.size > 200_000)
    }

    @Test fun vertebratePhylogenyFigureKeyIsImmediatelyVisible() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Classification of Vertebrata")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-essential-key-u1-vertebrata-classification-vertebrate-phylogeny")
            .assertExists()
    }

    @Test fun greenTickedAiVariantIsNotRejectedBecauseEnglishFallbackWasRejected() {
        val oldEnglish = JSONObject().apply {
            put("visualReview", "USER_REJECTED_REPLACEMENT_REQUIRED")
        }
        val acceptedTamilAi = JSONObject().apply {
            put("aiQaIntegrationDecision", "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE")
            put("reviewStatus", "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING")
            put("visualReview", "ACCEPT_MINOR_COSMETIC_ERRORS")
            put("scientificRiskHold", "")
        }
        val heldTamilAi = JSONObject().apply {
            put("aiQaIntegrationDecision", "HOLD_MATERIAL_ANATOMY_ERROR")
            put("reviewStatus", "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING")
            put("scientificRiskHold", "MATERIAL_ANATOMY_ERROR")
        }
        val id = "u-test-displayed-variant"
        val good = mapOf((id to "en") to oldEnglish,
            (id to "ta") to acceptedTamilAi)
        org.junit.Assert.assertFalse(selectedPlateNeedsReplacement(
            good, id, `in`.gasc.zoology.chordata.domain.ReadingLanguage.TA))
        org.junit.Assert.assertTrue(selectedPlateNeedsReplacement(
            good, id, `in`.gasc.zoology.chordata.domain.ReadingLanguage.EN))
        val materialHold = mapOf((id to "en") to oldEnglish,
            (id to "ta") to heldTamilAi)
        org.junit.Assert.assertTrue(selectedPlateNeedsReplacement(
            materialHold, id, `in`.gasc.zoology.chordata.domain.ReadingLanguage.TA))
    }

    @Test fun focusedTeachingPanelsRespectLegacyAndOwnerApprovedAi10Images() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val assetDirectory = "pencil_plates"

        fun originalDimensions(filename: String): Pair<Int, Int> {
            val bounds = android.graphics.BitmapFactory.Options().apply {
                inJustDecodeBounds = true
            }
            context.assets.open("$assetDirectory/$filename").use {
                android.graphics.BitmapFactory.decodeStream(it, null, bounds)
            }
            return bounds.outWidth to bounds.outHeight
        }

        fun assertPanel(filename: String, panel: Int, expected: Pair<Int, Int>) {
            val focused = requireNotNull(decodeTeachingPanel(
                context, assetDirectory, filename, panel
            )) { "Missing legacy region for $filename/$panel" }
            try {
                org.junit.Assert.assertEquals("$filename width", expected.first, focused.width)
                org.junit.Assert.assertEquals("$filename height", expected.second, focused.height)
            } finally {
                focused.recycle()
            }
        }

        // The columba skeleton is an unchanged legacy figure, so its
        // deliberate, source-preserving crop must continue to decode.
        assertPanel("columba_skeleton_en.png", 0, 1270 to 1290)

        // Both of these files may be a retained historical/legacy plate or
        // the exact owner-approved AI10 PNG, depending on source intake.
        // New 1448x1086 original PNGs must be shown whole, not cropped using
        // the old source's unrelated coordinate system.
        val migratedOrLegacy = listOf(
            Triple("pigeon_urinogenital_en.png", 3360 to 1900,
                listOf(1030 to 1040, 1090 to 1040, 1070 to 1510)),
            Triple("fish_accessory_breathing_en.png", 1800 to 1120,
                listOf(1800 to 1050))
        )
        for ((filename, legacySize, panels) in migratedOrLegacy) {
            val observed = originalDimensions(filename)
            if (observed == legacySize) {
                panels.forEachIndexed { index, size -> assertPanel(filename, index, size) }
            } else {
                org.junit.Assert.assertEquals("$filename AI10 dimensions",
                    1448 to 1086, observed)
                // Legacy crops must be unavailable for the new, different
                // illustration. The reader already falls back to full PNG.
                org.junit.Assert.assertNull(decodeTeachingPanel(
                    context, assetDirectory, filename, 0))
                val full = requireNotNull(decodePlateBitmap(
                    context, assetDirectory, filename))
                try {
                    org.junit.Assert.assertEquals(1448, full.width)
                    org.junit.Assert.assertEquals(1086, full.height)
                } finally {
                    full.recycle()
                }
            }
        }
        org.junit.Assert.assertNull(decodeTeachingPanel(
            context, assetDirectory, "fish_accessory_breathing_en.png", 9))
    }

    @Test fun historicalAscidianFigure8CropsDecodeWithoutAlteringOriginalPlate() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val source = "pencil_plates/ascidia_metamorphosis.png"
        val bounds = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
        context.assets.open(source).use {
            android.graphics.BitmapFactory.decodeStream(it, null, bounds)
        }
        org.junit.Assert.assertEquals(1488, bounds.outWidth)
        org.junit.Assert.assertEquals(2387, bounds.outHeight)
        val stagesAB = requireNotNull(decodeFocusedAscidianPanel(
            context, "pencil_plates", "ascidia_metamorphosis.png", 0))
        val stagesCD = requireNotNull(decodeFocusedAscidianPanel(
            context, "pencil_plates", "ascidia_metamorphosis.png", 1))
        try {
            org.junit.Assert.assertEquals(708, stagesAB.width)
            org.junit.Assert.assertEquals(540, stagesAB.height)
            org.junit.Assert.assertEquals(418, stagesCD.width)
            org.junit.Assert.assertEquals(645, stagesCD.height)
            org.junit.Assert.assertNull(decodeFocusedAscidianPanel(
                context, "pencil_plates", "ascidia_metamorphosis.png", 2))
        } finally {
            stagesAB.recycle()
            stagesCD.recycle()
        }
    }

    @Test fun ascidianMetamorphosisShowsFocusedStagesAndKeepsCompositeOptional() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Urochordata")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-u1-urochordata-ascidia-larva-adult").assertExists()
        rule.onNodeWithTag("figure-ascidia-stages-cd").assertExists()
        rule.onNodeWithTag("figure-ascidia-composite").assertDoesNotExist()
        // The complete source remains an optional expansion, not a required
        // large default image on a short display.
        rule.onNodeWithTag("figure-ascidia-original-toggle").assertExists()
    }

    @Test fun detailedScoliodonTextbookIsBilingualAndPreservesFigureSlots() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val pack = ContentRepository.load(context)
        val specimen = requireNotNull(pack.findTopic("u2-scoliodon"))
        org.junit.Assert.assertEquals(5, specimen.sections.size)
        org.junit.Assert.assertEquals(5, specimen.diagramIds.size)
        org.junit.Assert.assertEquals(1, specimen.textbookChapters.size)
        val chapter = specimen.textbookChapters.single()
        org.junit.Assert.assertEquals(15, chapter.sections.size)
        org.junit.Assert.assertTrue(chapter.sections.all {
            it.body.en.length >= 150 && it.body.ta.length >= 150
        })
        org.junit.Assert.assertTrue(chapter.sections.any {
            it.body.en.contains("laticaudus") && it.body.ta.contains("laticaudus")
        })
        org.junit.Assert.assertTrue(`in`.gasc.zoology.chordata.domain.LearningLogic
            .lastPage(specimen) >
            `in`.gasc.zoology.chordata.domain.LearningLogic.sectionPages(specimen).size)
        org.junit.Assert.assertEquals(127, pack.topics.sumOf { it.sections.size })
        org.junit.Assert.assertEquals(64, pack.topics.sumOf { it.diagramIds.size })
    }

    @Test fun bilingualPointwiseEnrichmentPreservesOriginalChapterStructure() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val pack = ContentRepository.load(context)
        org.junit.Assert.assertEquals(5, pack.units.size)
        org.junit.Assert.assertEquals(39, pack.topics.size)
        org.junit.Assert.assertEquals(127, pack.topics.sumOf { it.sections.size })
        org.junit.Assert.assertEquals(64, pack.topics.sumOf { it.diagramIds.size })
        org.junit.Assert.assertEquals(117, pack.topics.sumOf { it.quiz.size })
        val enriched = pack.topics.flatMap { it.sections }.filter { it.keyPoints.isNotEmpty() }
        org.junit.Assert.assertEquals(39, enriched.size)
        org.junit.Assert.assertEquals(117, enriched.sumOf { it.keyPoints.size })
        org.junit.Assert.assertTrue(enriched.all { section ->
            section.keyPoints.size == 3 && section.keyPoints.all { point ->
                point.en.length >= 50 && point.ta.length >= 45
            }
        })
        val origin = requireNotNull(pack.findTopic("u1-origin")).sections.first()
        org.junit.Assert.assertTrue(origin.keyPoints[0].en.contains("deuterostome"))
        org.junit.Assert.assertTrue(origin.keyPoints[0].ta.contains("முதுகுநாணிகள்"))
    }

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
        // A held historical variant must use its credited English fallback.
        // Once the exact corrected, green-ticked AI PNG is staged, the Tamil
        // reader must use it instead; that transition cannot break QA.
        val lanceletId = "u1-cephalochordata-branchiostoma-labelled"
        val lanceletTamil = requireNotNull(byIdAndLanguage[lanceletId to "ta"])
        val lanceletDecision = lanceletTamil.optString("aiQaIntegrationDecision")
        if (lanceletDecision == "GREEN_TICK_ALLOW_PROVISIONAL_QA_USE") {
            org.junit.Assert.assertEquals("pencil_plates/branchiostoma_ta.png",
                selected(lanceletId, ta))
            org.junit.Assert.assertEquals(
                "2fbd48be62b83309c87214492ea20dfea1995a3e624fca66c17ed995c95d9b1e",
                lanceletTamil.getString("sha256"))
            org.junit.Assert.assertEquals("PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
                lanceletTamil.getString("reviewStatus"))
        } else {
            org.junit.Assert.assertEquals("HOLD_MATERIAL_ANATOMY_ERROR", lanceletDecision)
            org.junit.Assert.assertEquals("pencil_plates/branchiostoma_en.png",
                selected(lanceletId, ta))
        }
        org.junit.Assert.assertEquals("pencil_plates/branchiostoma_en.png",
            selected(lanceletId, en))
        // Owner blanket approval MUST NOT override this material anatomical hold.
        val rabbitHeld = requireNotNull(byIdAndLanguage["u5-rabbit-endoskeleton" to "ta"])
        org.junit.Assert.assertEquals("HOLD_MATERIAL_ANATOMY_ERROR",
            rabbitHeld.optString("aiQaIntegrationDecision"))
        org.junit.Assert.assertEquals("MATERIAL_ANATOMY_ERROR",
            rabbitHeld.optString("scientificRiskHold"))
        org.junit.Assert.assertEquals("OWNER_APPROVAL_EXCLUDED_MATERIAL_ANATOMY_ERROR_2026-11-11",
            rabbitHeld.optString("ownerQaAcceptance"))
        // Rabbit AI anatomy remains held until there is a separate reviewed
        // exact-hash replacement. Never show the rejected Tamil image.
        org.junit.Assert.assertEquals("pencil_plates/rabbit_skeleton_en.png",
            selected("u5-rabbit-endoskeleton", ta))
        // Other already-approved AI PNGs remain accessible through shared/en.
        org.junit.Assert.assertEquals("pencil_plates/amphibian_orders.png",
            selected("u3-amphibia-classification-living-orders", ta))
        org.junit.Assert.assertEquals("pencil_plates/calotes_brain_dorsal_en.png",
            selected("u4-calotes-brain", ta))
    }

    @Test fun tamilPagerRemainsWideAt200Percent() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
        rule.onNodeWithTag("reader-next").assertIsDisplayed()
        val bounds = rule.onNodeWithTag("reader-next").fetchSemanticsNode().boundsInRoot
        org.junit.Assert.assertTrue(
            "Tamil next-page button collapsed: " + bounds, bounds.width > bounds.height * 1.7f)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-page-heading").assertTextEquals("பரிணாமத் தோற்றத்துக்கான ஆதாரங்கள்")
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

    @Test fun lessonHidesBottomNavigationAndRestoresItOnBack() {
        selectEnglish()
        rule.onNodeWithTag("app-bottom-navigation").assertIsDisplayed()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").assertIsDisplayed()
        rule.onNodeWithTag("app-bottom-navigation").assertDoesNotExist()
        rule.onNodeWithTag("lesson-back").performClick()
        rule.onNodeWithTag("app-bottom-navigation").assertIsDisplayed()
        rule.onNodeWithText("All lessons").assertIsDisplayed()
    }

    @Test fun compactChaptersPackBriefSectionsWithoutLosingTextOrFigures() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val pack = ContentRepository.load(context)
        val origin = requireNotNull(pack.findTopic("u1-origin"))
        org.junit.Assert.assertEquals(setOf(1), origin.figurePages)
        org.junit.Assert.assertEquals(
            listOf(listOf(0), listOf(1, 2)),
            `in`.gasc.zoology.chordata.domain.LearningLogic.sectionPages(origin))
        org.junit.Assert.assertEquals(2,
            `in`.gasc.zoology.chordata.domain.LearningLogic.lastPage(origin))
        val illustratedLast = requireNotNull(pack.findTopic("u1-urochordata"))
        org.junit.Assert.assertTrue(3 in illustratedLast.figurePages)
        org.junit.Assert.assertEquals(3,
            `in`.gasc.zoology.chordata.domain.LearningLogic.lastPage(illustratedLast))

        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-page-heading")
            .assertTextEquals("Evidence and hypotheses")
        // Third section is included ON THIS PAGE, not on an empty extra page.
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithTag("packed-section-heading-2")
            .assertTextEquals("Ancestry versus resemblance")
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(6)
        rule.onNodeWithTag("reader-next").performClick()
        rule.onNodeWithTag("lesson-page-heading").assertTextEquals("Practice")
    }

    @Test fun opensFirstChapterAndAdvancesToLesson() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onAllNodesWithText("Origin of Chordata").onFirst().assertIsDisplayed()
        rule.onNodeWithTag("first-section-heading").assertExists()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
        rule.onNodeWithText("Next ›").performClick()
        rule.waitUntil(timeoutMillis = 5_000) {
            runCatching { rule.onNodeWithText("Evidence and hypotheses").isDisplayed() }
                .getOrDefault(false)
        }
        rule.onNodeWithText("Evidence and hypotheses").assertIsDisplayed()
    }

    @Test fun scoliodonBrainPlateIsReachableOnItsExactFourthSection() {
        selectEnglish()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Scoliodon")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        // The previously rejected synthetic plate is replaced by a source-verified
        // 1878 dogfish comparison; do not imply an exact Scoliodon dissection.
        for (section in 0 until 3) {
            rule.onNodeWithTag("lesson-reader-list")
                .performScrollToIndex(if (section == 0) 5 else 4)
            rule.onNodeWithText("Next ›").performClick()
        }
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-rejected-quality").assertDoesNotExist()
        rule.onNodeWithTag("figure-image-u2-scoliodon-brain-labelled")
            .assertIsDisplayed()
            .performClick()
        rule.onNodeWithText("Close").assertIsDisplayed()
        rule.onNodeWithTag("figure-zoom-caption-u2-scoliodon-brain-labelled")
            .assertTextEquals("Shark brain, dorsal view")
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled")
            .assertIsDisplayed().performClick()
        rule.onNodeWithText("Close").assertIsDisplayed()
    }
    /**
     * Emulator evidence is written to MediaStore Pictures so the CI job
     * can extract the exact English/Tamil screen shown by Compose.
     */
    /**
     * A launcher or system ANR dialog can cover a Compose capture while all
     * widget assertions still pass. Such screenshots are invalid QA evidence.
     * UI Automation reads accessibility text directly; no image OCR is used.
     */
    private fun systemAnrDialogVisible(): Boolean {
        val root = InstrumentationRegistry.getInstrumentation().uiAutomation.rootInActiveWindow
            ?: return false
        fun hasAnr(node: android.view.accessibility.AccessibilityNodeInfo?): Boolean {
            if (node == null) return false
            val text = (node.text?.toString().orEmpty() + " " +
                node.contentDescription?.toString().orEmpty()).lowercase()
            if ("isn't responding" in text || "not responding" in text) return true
            return (0 until node.childCount).any { hasAnr(node.getChild(it)) }
        }
        return hasAnr(root)
    }

    private fun captureQaScreen(name: String) {
        require(Regex("[a-z0-9-]+").matches(name))
        rule.waitForIdle()
        check(!systemAnrDialogVisible()) {
            "System/launcher ANR dialog visible; cannot certify screenshot $name"
        }
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
            check(!systemAnrDialogVisible()) {
                "System/launcher ANR appeared during screenshot capture: $name"
            }
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled").assertIsDisplayed()
        val fishBounds = rule.onNodeWithTag("figure-image-u2-scoliodon-external-labelled")
            .fetchSemanticsNode().boundsInRoot
        org.junit.Assert.assertTrue("Wide fish image should not occupy a tall empty frame: $fishBounds",
            fishBounds.width > fishBounds.height * 3f)
        rule.onNodeWithTag("figure-essential-key-u2-scoliodon-external-labelled").assertExists()
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithTag("figure-image-" + figureId).assertIsDisplayed()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(5)
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

