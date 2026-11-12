package `in`.gasc.zoology.chordata.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import `in`.gasc.zoology.chordata.domain.ReadingLanguage

/** In-app privacy disclosure; all data paths are local to this APK. */
@Composable
fun PrivacyPolicyPage(language: ReadingLanguage, textScale: Float) {
    val scale = textScale.coerceIn(1f, 2f)
    val tamil = language == ReadingLanguage.TA
    fun tr(en: String, ta: String): String = if (tamil) ta else en

    LazyColumn(
        modifier = Modifier.fillMaxSize().testTag("privacy-policy-page"),
        contentPadding = PaddingValues(horizontal = 18.dp, vertical = 20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        item {
            Text(tr("Privacy policy", "தனியுரிமைக் கொள்கை"),
                fontSize = (24f * scale).sp,
                lineHeight = (32f * scale).sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.testTag("privacy-policy-heading"),
                color = MaterialTheme.colorScheme.primary)
            Text(tr("Chordata Atlas · Updated 12 November 2026",
                "Chordata Atlas · புதுப்பிப்பு: 12 நவம்பர் 2026"),
                fontSize = (12f * scale).sp,
                lineHeight = (18f * scale).sp)
        }
        item { PrivacySection(scale,
            tr("About this app", "செயலியைப் பற்றி"),
            tr("Chordata Atlas is an offline Zoology learning app from the Department of Zoology, Government Arts & Science College, Nagercoil. No account or sign-in is required.",
               "Chordata Atlas என்பது நாகர்கோவில் அரசு கலை மற்றும் அறிவியல் கல்லூரியின் விலங்கியல் துறைக்கான இணையமற்ற கற்றல் செயலி. பயனர் கணக்கோ உள்நுழைவோ தேவையில்லை.")
        ) }
        item { PrivacySection(scale,
            tr("Stored on your device", "உங்கள் சாதனத்தில் சேமிக்கப்படும் தரவு"),
            tr("Completed lessons, bookmarks, quiz scores, reading language and text-size preference are stored in the app's private storage on your device. Unsubmitted quiz selections are held in the app's current session.",
               "முடித்த பாடங்கள், சேமித்த பாடங்கள், வினாடி வினா மதிப்பெண்கள், வாசிப்பு மொழி மற்றும் எழுத்தளவுத் தேர்வு ஆகியவை உங்கள் சாதனத்தின் செயலிக்குரிய தனிப்பட்ட சேமிப்பகத்தில் மட்டுமே பதிவாகும். சமர்ப்பிக்காத வினா விடைகள் நடப்பு பயன்பாட்டு அமர்வில் வைத்திருக்கப்படும்.")
        ) }
        item { PrivacySection(scale,
            tr("Collection and sharing", "தரவு சேகரிப்பும் பகிர்வும்"),
            tr("The app does not request Internet access. It does not send learner information to developer servers or third parties, and has no advertising, analytics or user-tracking integration. Educational figures and credits are bundled offline.",
               "இந்தச் செயலி இணைய அணுகல் அனுமதி கோராது. கற்பவரின் தரவு உருவாக்குநரின் சேவையகங்களுக்கோ மூன்றாம் தரப்பினருக்கோ அனுப்பப்படாது. விளம்பரங்கள், பயன்பாட்டுப் பகுப்பாய்வு அல்லது பயனர் கண்காணிப்புச் சேவைகள் இல்லை. கல்விப் படங்களும் அவற்றின் மூல விவரங்களும் செயலியில் உள்ளடக்கப்பட்டுள்ளன.")
        ) }
        item { PrivacySection(scale,
            tr("Protection, retention and deletion", "பாதுகாப்பு, வைத்திருத்தல் மற்றும் நீக்குதல்"),
            tr("Android private app storage is used and Android automatic backup is disabled. Local preferences remain until you uninstall the app or clear its storage in Android Settings > Apps > Chordata Atlas > Storage > Clear storage. No cloud copy is maintained by this app.",
               "Android செயலியின் தனிப்பட்ட சேமிப்பகம் பயன்படுத்தப்படுகிறது; தானியங்கி காப்புப்பிரதி முடக்கப்பட்டுள்ளது. செயலியை நீக்கினாலோ Android அமைப்புகள் > செயலிகள் > Chordata Atlas > சேமிப்பகம் > தரவை அழி என்பதைத் தேர்ந்தெடுத்தாலோ உள்ளூர் பதிவுகள் நீங்கும். இந்தச் செயலி மேகச் சேமிப்பகத்தில் நகல் வைத்திருக்காது.")
        ) }
        item { PrivacySection(scale,
            tr("Privacy enquiries", "தனியுரிமை தொடர்பான கேள்விகள்"),
            tr("For enquiries about this app's privacy practices, use the developer contact details shown on its Google Play listing.",
               "இச்செயலியின் தனியுரிமை நடைமுறைகள் குறித்த கேள்விகளுக்கு Google Play செயலி விவரப் பக்கத்தில் உள்ள உருவாக்குநர் தொடர்புத் தகவலைப் பயன்படுத்தவும்.")
        ) }
        item { Spacer(Modifier.height(8.dp)) }
    }
}

@Composable
private fun PrivacySection(scale: Float, heading: String, body: String) {
    Column(modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Text(heading, fontWeight = FontWeight.Bold,
            fontSize = (17f * scale).sp, lineHeight = (24f * scale).sp,
            color = MaterialTheme.colorScheme.primary)
        Text(body, fontSize = (16f * scale).sp,
            lineHeight = (25f * scale).sp)
    }
}
