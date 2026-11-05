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
import org.junit.Rule
import org.junit.Test

class ReaderNavigationTest {
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithText("Next ›").performClick()
        rule.waitUntil(timeoutMillis = 5_000) {
            runCatching { rule.onNodeWithText("Deuterostome ancestry").isDisplayed() }
                .getOrDefault(false)
        }
        rule.onNodeWithText("Deuterostome ancestry").assertIsDisplayed()
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-scoliodon-external").performClick()
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
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-scoliodon-external").assertIsDisplayed()
        captureQaScreen("scoliodon-figure-ta-200")
        rule.onNodeWithTag("figure-image-scoliodon-external").performClick()
        rule.onNodeWithText("மூடுக").assertIsDisplayed()
        captureQaScreen("scoliodon-zoom-ta-200")
    }

}
