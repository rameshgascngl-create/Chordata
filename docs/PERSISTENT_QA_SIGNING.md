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
