# CHORDATA — manually gated Google Play upload-candidate workflow

This is an **optional release-candidate workflow**, not an automatic store submission.
It does not use a QA/debug certificate. It is intentionally blocked until the full
human scientific/editorial review, privacy, and publisher checks are complete.

## Release prerequisites (all required)

1. An existing **successful Native QA Debug APK workflow for the identical commit**.
2. The 64-row review register: **64/64** independent scientific and Tamil reviewer
   decisions ACCEPTED with names and evidence. Owner's provisional AI green ticks
   do not fulfil this requirement. Any changed artwork invalidates earlier approval.
3. The public **HTTPS** privacy-policy page must display HTML, be accessible worldwide,
   and identify Chordata Atlas. The file in docs/ is only the source template; a
   repository raw-file/download link is not a Play privacy-policy webpage.
4. Play Console Data safety declaration, target age, relevant content rating and
   publisher/privacy contact must be reviewed by the publisher.
5. Configure the GitHub Actions environment **play-upload-review** with required
   reviewer approval and these **environment secrets**, generated locally:
   - CHORDATA_PLAY_UPLOAD_KEYSTORE_B64
   - CHORDATA_PLAY_UPLOAD_STORE_PASSWORD
   - CHORDATA_PLAY_UPLOAD_KEY_ALIAS
   - CHORDATA_PLAY_UPLOAD_KEY_PASSWORD

These secrets must be a dedicated **Play upload key**, *not* the application
signing key managed by Google Play and *not* the persistent QA debug key.
Do not share keys or passwords in chat or commit them to the repository.

## Workflow

1. Open **Actions → CHORDATA gated Play upload candidate → Run workflow**.
2. Select the reviewed QA branch; provide a fresh, increasing numeric versionCode,
   a release-style versionName such as 1.0.0, and the hosted privacy-policy URL.
3. Explicitly confirm publisher contact and Play declarations.
4. The workflow checks that exact commit's QA pass, independent review status,
   privacy URL, source and image integrity, release lint and bundle compilation.
5. It signs the AAB with the private upload key and verifies the JAR signature.
6. The signed AAB is retained for seven days as a downloadable GitHub Actions
   artifact. **No Play Console upload or publication occurs automatically.**

The QA Gradle build retains its existing version code/name when no release
environment overrides are provided. The bundle is not signed by the QA debug
key. Without all four Play secrets, signoff and a hosted privacy page,
the manual workflow **must fail** rather than silently publish an invalid AAB.

## Important currently open blockers

The review register has not received 64 independent dual acceptances.
A live public privacy-policy URL and confirmed privacy enquiry contact have
not been supplied. Production upload secrets have not been verified.
The next valid deliverable remains a tested QA APK until these requirements
are actually satisfied.

Official reference: https://developer.android.com/build/building-cmdline
Official policy: https://support.google.com/googleplay/android-developer/answer/9859455
