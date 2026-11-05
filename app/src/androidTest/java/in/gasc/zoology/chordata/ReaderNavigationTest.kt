package `in`.gasc.zoology.chordata

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onFirst
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
        rule.onAllNodesWithText("Read chapter  ›").onFirst().performClick()
        rule.onAllNodesWithText("Origin of Chordata").onFirst().assertIsDisplayed()
        rule.onNodeWithTag("lesson-reader-list").performScrollToIndex(4)
        rule.onNodeWithText("Next ›").performClick()
        rule.onNodeWithText("Deuterostome ancestry").assertIsDisplayed()
    }

    @Test fun canSwitchTamilAndIncreaseTextSize() {
        rule.onNodeWithText("தமிழ்").performClick()
        rule.onNodeWithText("200%").performClick()
        rule.onNodeWithText("Explore all lessons").performClick()
        rule.onAllNodesWithText("Read chapter  ›").onFirst().performClick()
        rule.onNodeWithText("முதுகுநாணிகளின் தோற்றம்").assertIsDisplayed()
    }
}
