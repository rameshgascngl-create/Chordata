package `in`.gasc.zoology.chordata

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import `in`.gasc.zoology.chordata.data.ContentRepository
import `in`.gasc.zoology.chordata.data.ProgressStore
import `in`.gasc.zoology.chordata.ui.ChordataApp
import `in`.gasc.zoology.chordata.ui.ErrorContent

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val result = runCatching { ContentRepository.load(this) }
        val store = ProgressStore(this)
        setContent {
            if (result.isSuccess) ChordataApp(result.getOrThrow(), store)
            else ErrorContent(result.exceptionOrNull()?.message ?: "Unable to load offline course")
        }
    }
}
