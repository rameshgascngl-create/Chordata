package `in`.gasc.zoology.chordata

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertDoesNotExist
import androidx.compose.ui.test.performTextInput
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onFirst
import androidx.compose.ui.test.isDisplayed
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performScrollToIndex
import org.junit.Rule
import org.junit.Test

class ReaderNavigationTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()

    @Test fun opensFirstChapterAndAdvancesToLesson() {
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
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("The Chordata Fieldbook").assertDoesNotExist()
        rule.onNodeWithText("அனைத்துப் பாடங்களையும் காண்க").performClick()
        rule.onAllNodesWithText("பாடத்தைப் படிக்க ›").onFirst().performClick()
        rule.onNodeWithText("முதுகுநாணிகளின் தோற்றம்").assertIsDisplayed()
    }
    @Test fun englishReferenceFigureOpensNativeZoom() {
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onNodeWithTag("lesson-search").performTextInput("Scoliodon")
        rule.onAllNodesWithText("Read chapter ›").onFirst().performClick()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(3)
        rule.onNodeWithTag("figure-image-scoliodon-external").performClick()
        rule.onNodeWithText("Close").assertIsDisplayed()
    }
}
