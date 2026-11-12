# CHORDATA — persistent QA signing (no production keys)

The Android CI runners create an independent default debug signing identity.
The QA APKs from workflows **#388 and #390 have different certificate
SHA-256 fingerprints**, so Android normally rejects an upgrade from one to
the other. Removing the old app deletes its locally stored lesson progress.
This is an actual QA usability issue.

## Safe configuration (repository administrator only)

Generate ONE QA-only signing keystore securely on a trusted computer and keep
a private, backed-up copy **outside GitHub source control**. Do not reuse
Google Play's production/upload signing key.

Example (interactive; DO NOT paste passwords into chat):

```bash
keytool -genkeypair -v -keystore chordata-qa.jks -storetype PKCS12 \
  -alias chordata-qa -keyalg RSA -keysize 3072 -validity 10000
base64 -w 0 chordata-qa.jks > chordata-qa.jks.b64
```

Configure these FOUR **GitHub Actions repository secrets** using
Settings → Secrets and variables → Actions:
- `CHORDATA_QA_KEYSTORE_B64`: full base64 text from the local temporary file
- `CHORDATA_QA_STORE_PASSWORD`: keystore password
- `CHORDATA_QA_KEY_ALIAS`: `chordata-qa`
- `CHORDATA_QA_KEY_PASSWORD`: key password

Delete the temporary base64 text file after the secret is configured.
Never commit the keystore, base64, passwords, or signing key to this public
repository. `.gitignore` already excludes `*.jks` and `*.keystore`.

The workflow uses that identity only for `debug` builds, including
instrumentation and published QA APKs. The `release` build remains unsigned.

## Offline progress transfer in newer QA builds

The native Android Privacy policy screen now provides **Export learning data**
and **Import learning data**, using the Android system file picker without
storage or network permissions. Export produces a readable, unencrypted JSON
file containing lesson completion, bookmarks, quiz scores, language and reader
scale. Import requires a confirmation and schema validation before replacing
existing local progress. Store backup files privately and delete them
separately after use; deleting the app does not remove an exported file.

**Important:** older QA builds (including #402 and #405) do not contain
these export controls. Installing a newer APK signed with a different
certificate over an older build will still be refused by Android. Backing up
through the new in-app UI cannot rescue progress from a previous APK that does
not implement the feature. For existing installations, use an identical
signing identity or obtain an authorised device-level backup before
uninstalling; never promise that unrelated debug builds can upgrade in place.

## Acceptance and limitations

1. Run Android QA twice on successive commits with the SAME encrypted secrets.
2. Confirm the displayed SHA-256 certificate fingerprint is identical.
3. Confirm an installed QA APK upgrades in-place and keeps bookmarks/scores.
4. Before secrets are installed, the workflow deliberately emits an **ephemeral
   key warning** and publishes only a temporary-key debug APK.
5. An installed APK signed using an older, random debug certificate **cannot**
   be upgraded to a different QA signing certificate. Do not suggest
   uninstalling without explaining local-data loss.
6. Increment `versionCode` before eventual store release. QA update signing
   does not satisfy Play production signing, image sign-off or Play declarations.
