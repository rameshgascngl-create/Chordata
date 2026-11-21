# CHORDATA — Publisher-controlled Android release signing

**App package:** `in.gasc.zoology.chordata`  
**Native source branch:** `qa/chordata-textbook-unit2-continuation-20261113`  
**Last verified source before signing-workflow preparation:** `dc87849ca737241faf1246cbea80d64b0cd189a7`

## Before creating a signing key

**First check whether CHORDATA has ever been published with this exact package name.**
If yes, identify the existing Android *upload/signing* certificate:

- **An existing APK marketplace listing:** updates MUST be signed using its **original app-signing keystore**. Creating a new key can make updates impossible under the same package name.
- **Google Play App Signing listing:** the upload key must match the certificate registered in Play Console (or be reset via Play's authorised upload-key reset process). The Play app-signing key and upload key can differ.
- **A brand-new app with no published signing identity:** the publisher may create a new upload keystore.

Do not send the keystore, passwords, base64 contents or private signing keys in a ChatGPT message, email, issue, commit or pull request. No signing keys belong in the application source tree.

## Generate an upload keystore on the publisher's Windows computer (only for a new app)

Open **PowerShell**, with **JDK 17** `keytool` on PATH (Android Studio's bundled JDK is also suitable):

```powershell
$dir = Join-Path $env:USERPROFILE 'Documents\CHORDATA-signing'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$key = Join-Path $dir 'chordata-upload.jks'
if (Test-Path $key) { throw "A keystore already exists. Do not overwrite it." }
keytool -genkeypair -v -keystore "$key" -storetype PKCS12 `
  -alias chordata-upload -keyalg RSA -keysize 3072 -validity 10000 `
  -dname "CN=CHORDATA Atlas, OU=Department of Zoology, O=Government Arts and Science College, L=Nagercoil, ST=Tamil Nadu, C=IN"
```

**Choose and securely retain the prompted strong store password.** With a PKCS12 keystore, use the same password for the key and store. Keep at least **two encrypted, independently held backups** of the keystore and password; the old signing key may be required for years of updates.

Confirm the keystore/certificate **locally**:

```powershell
keytool -list -v -keystore "$key" -alias chordata-upload
```

The resulting SHA-256 certificate fingerprint is public and can be recorded as a release identifier. Never publish the keystore or passwords.

## Configure the protected GitHub environment

Open: https://github.com/rameshgascngl-create/Chordata/settings/environments

Create or use environment `play-upload-review` with the appropriate human reviewer protections. Under its **Environment secrets**, configure the following values:

| Secret name | Content |
| --- | --- |
| `CHORDATA_PLAY_UPLOAD_KEYSTORE_B64` | Base64 of the original or newly created `.jks` bytes |
| `CHORDATA_PLAY_UPLOAD_STORE_PASSWORD` | Store password |
| `CHORDATA_PLAY_UPLOAD_KEY_ALIAS` | Existing alias, or `chordata-upload` for a new key |
| `CHORDATA_PLAY_UPLOAD_KEY_PASSWORD` | Password for that alias |

To temporarily copy the keystore as Base64 to the Windows clipboard for pasting into a GitHub secret (no file created):

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes($key)) | Set-Clipboard
```

Clear the clipboard promptly after inserting that one secret:

```powershell
Set-Clipboard -Value ''
```

Enter the remaining **password secrets directly in GitHub's secret fields**; do not paste them into public logs.

## Generate the candidates after formal reviews

The protected manual workflow is:
`.github/workflows/play-upload-candidate.yml` → GitHub **Actions → CHORDATA gated Play upload candidate → Run workflow**.

Before starting, record:

1. An **unused, monotonically increasing versionCode** (check any existing marketplace listing; never reuse a published code), and numeric `versionName` such as `1.0.0`.
2. A publicly accessible HTML privacy-policy HTTPS URL, and a verified publisher support/privacy contact and accurate Data safety declaration.
3. Completion of all **64 independently reviewed Biology/Tamil figure entries** and any outstanding source-licence checks in `docs/FIGURE_REVIEW_REGISTER_64.csv`.
4. Successful native QA and Android instrumentation on the **exact** source revision.

The release workflow enforces these gates, verifies the current sources/figure hashes, compiles both **unsigned release AAB and unsigned release APK**, then signs and verifies **both with the publisher's key**. It checks the installed APK's source asset digests, **16 KiB native-library alignment**, and prints the public signing-certificate fingerprint and output SHA-256 hashes.

Resulting GitHub Action artifacts (manually downloadable, **not automatically sent to a marketplace**):

- `CHORDATA_Manual_Signed_Play_Upload_Candidate` — upload-key-signed `.aab`, for **Google Play**.
- `CHORDATA_Manual_Signed_Store_APK_Candidate` — `zipalign` + Android APK Signature Scheme signed `.apk`, for a marketplace accepting APK files **subject to certificate continuity**.

**Current release status:** successful QA compilation alone is not formal academic approval. Do not falsify or bypass pending independent reviews. A debug-signed APK is not a substitute for either store artifact.
