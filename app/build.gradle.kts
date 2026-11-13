plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

// A stable QA signing identity is optional and comes exclusively from local
// environment variables / GitHub Actions encrypted secrets. Never commit keys.
// Without it, Android's standard temporary debug key remains the fallback.
val qaStorePath = System.getenv("CHORDATA_QA_KEYSTORE_PATH")
val qaStorePassword = System.getenv("CHORDATA_QA_STORE_PASSWORD")
val qaKeyAlias = System.getenv("CHORDATA_QA_KEY_ALIAS")
val qaKeyPassword = System.getenv("CHORDATA_QA_KEY_PASSWORD")
val persistentQaSigning = listOf(
    qaStorePath, qaStorePassword, qaKeyAlias, qaKeyPassword
).all { !it.isNullOrBlank() }

// Production metadata may be provided only as a paired explicit override.
// Normal QA runs retain the original version and remain debug-signed.
val releaseVersionCodeEnv = System.getenv("CHORDATA_RELEASE_VERSION_CODE")
val releaseVersionNameEnv = System.getenv("CHORDATA_RELEASE_VERSION_NAME")
require((releaseVersionCodeEnv == null) == (releaseVersionNameEnv == null)) {
    "Release version code and name must be provided together"
}
if (releaseVersionCodeEnv != null) {
    require(releaseVersionCodeEnv.toIntOrNull()?.let { it in 1..2100000000 } == true) {
        "Release version code must be a positive Android-compatible integer"
    }
    require(Regex("""[0-9]+\.[0-9]+\.[0-9]+""").matches(requireNotNull(releaseVersionNameEnv))) {
        "Release version name must be numeric major.minor.patch without a QA suffix"
    }
}

android {
    namespace = "in.gasc.zoology.chordata"
    compileSdk = 37

    defaultConfig {
        applicationId = "in.gasc.zoology.chordata"
        minSdk = 24
        targetSdk = 36
        versionCode = releaseVersionCodeEnv?.toInt() ?: 1
        versionName = releaseVersionNameEnv ?: "0.1.0-qa"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
    signingConfigs {
        if (persistentQaSigning) {
            create("persistentQa") {
                storeFile = file(requireNotNull(qaStorePath))
                storePassword = requireNotNull(qaStorePassword)
                keyAlias = requireNotNull(qaKeyAlias)
                keyPassword = requireNotNull(qaKeyPassword)
            }
        }
    }
    buildTypes {
        debug {
            isDebuggable = true
            if (persistentQaSigning) {
                signingConfig = signingConfigs.getByName("persistentQa")
            }
        }
        release {
            // QA source only; do not generate/distribute a production release.
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        create("compactQa") {
            // Optional smaller *installable* QA APK: exactly the same app ID,
            // code, images and lesson assets as the full QA build.
            // R8/resource shrinking mirrors release; never sign for Play here.
            initWith(getByName("release"))
            isDebuggable = false
            signingConfig = if (persistentQaSigning)
                signingConfigs.getByName("persistentQa")
            else signingConfigs.getByName("debug")
            matchingFallbacks += listOf("release")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    packaging {
        resources.excludes += "/META-INF/{AL2.0,LGPL2.1}"
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2026.09.00")
    implementation(composeBom)
    androidTestImplementation(composeBom)
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    androidTestImplementation("androidx.test:runner:1.6.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
}
