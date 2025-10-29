# Hookd Android Shells

This repository contains the Android wrappers that publish the existing [hookd.fish](https://hookd.fish) Progressive Web App in
two different forms:

- A **Trusted Web Activity (TWA)** generated with Bubblewrap that launches Chrome in full-screen mode and serves the production
  site directly from the network.
- A minimal **Capacitor shell** that can host a locally built copy of the PWA when native plugins (Camera/Filesystem) are
  required to preserve photo metadata during uploads.

The web experience remains the source of truth. The Android projects here focus on meeting Play Store requirements, verifying
the Digital Asset Links association, and keeping optional native integrations isolated from the web codebase.

## Repository layout

| Path | Purpose |
| --- | --- |
| `android/` | Bubblewrap-generated Android project. Contains Gradle build files, the TWA launcher activity, and placeholders for signing material and icons. |
| `android/scripts/bootstrap_gradle_wrapper.py` | Helper that restores the Gradle wrapper JAR without committing binaries. |
| `android/ASSET_REQUIREMENTS.md` | List of binary launch/splash assets that must be provided locally before shipping. |
| `android/BINARY_ASSETS.md` | Checklist of Gradle wrapper and icon binaries that are ignored by Git. |
| `android/KEYSTORE_PLACEHOLDER.md` | Instructions for supplying the release keystore referenced by Bubblewrap. |
| `capacitor.config.ts` | Capacitor configuration that keeps Camera uploads as URI-based files so EXIF data is not stripped. |
| `package.json` | NPM metadata and scripts for syncing Capacitor platforms. |
| `web-manifest.json` | Snapshot of the production web manifest used by Bubblewrap when regenerating the Android project. |

## Prerequisites

Install the following tooling once on your workstation:

- **Node.js 18+** and **npm 9+** for the Capacitor CLI.
- **Java Development Kit (JDK) 17** – required by the current Android Gradle Plugin and Bubblewrap.
- **Android SDK command-line tools** with API 34 or newer platforms.
- **Bubblewrap CLI** (`npm install -g @bubblewrap/cli`) for generating and updating the TWA project.
- Optional: **Android Studio Electric Eel or newer** for editing and running the native project.

## Android SDK and Bubblewrap environment

Bubblewrap expects the Android SDK to be present and referenced via environment variables. The following example installs the
SDK to `~/.bubblewrap/android_sdk`:

```bash
export ANDROID_SDK_ROOT="$HOME/.bubblewrap/android_sdk"
mkdir -p "$ANDROID_SDK_ROOT"
# Download the latest command-line tools ZIP from Google before running these commands.
unzip commandlinetools-linux-*_latest.zip -d "$ANDROID_SDK_ROOT/cmdline-tools"
mv "$ANDROID_SDK_ROOT/cmdline-tools"/cmdline-tools "$ANDROID_SDK_ROOT/cmdline-tools/latest"
"$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" \
  "platform-tools" "build-tools;34.0.0" "platforms;android-34"
```

After installing, run `bubblewrap doctor` to confirm Bubblewrap can locate both the JDK and the Android SDK. Either export
`ANDROID_SDK_ROOT`/`ANDROID_HOME` in your shell profile or create `android/local.properties` with
`sdk.dir=/absolute/path/to/android_sdk` so Gradle knows where to find the SDK.

## Trusted Web Activity workflow

1. **Install/upgrade Bubblewrap**
   ```bash
   npm install -g @bubblewrap/cli
   ```

2. **Keep the TWA manifest in sync**
   The current configuration is stored in `android/twa-manifest.json`. To refresh the Android project after changing the web
   manifest, run:
   ```bash
   cd android
   bubblewrap update --manifest=https://hookd.fish/manifest.json
   ```
   Review the generated diff before committing.

3. **Restore ignored binaries**
   - Download the Gradle wrapper JAR once per machine:
     ```bash
     python android/scripts/bootstrap_gradle_wrapper.py
     ```
   - Provide launcher/splash/notification icons for every density listed in `android/ASSET_REQUIREMENTS.md`. The repository only
     contains XML placeholders so binary artwork must be copied in locally before building.

4. **Add signing material**
   Place a keystore named `android/android.keystore` using the credentials from `android/KEYSTORE_PLACEHOLDER.md`. The same SHA256
   fingerprint must appear in `https://hookd.fish/.well-known/assetlinks.json` so the Play Store build can verify the association.

5. **Build release artifacts**
   ```bash
   cd android
   bubblewrap build
   ```
   Bubblewrap produces `app-release-signed.apk` and `app-release-bundle.aab` inside `android/`. Install the APK on a device to
   confirm Chrome launches the verified origin (the overflow menu should show “Hookd” instead of Chrome controls).

## Capacitor workflow (metadata-preserving uploads)

The Capacitor shell is optional but provides a WebView with the Camera and Filesystem plugins pre-registered. When the web app
requests `Camera.getPhoto({ resultType: CameraResultType.Uri, allowEditing: false })`, EXIF/GPS metadata remains intact because
Capacitor returns a file URI instead of base64 data.

1. **Install JavaScript dependencies**
   ```bash
   npm install
   ```

2. **Build the web assets**
   Replace the placeholder build script in `package.json` with the real PWA build command if necessary, then run:
   ```bash
   npm run build
   ```
   Ensure the compiled app lands in `dist/` (or update `capacitor.config.ts` to point `webDir` at the correct folder).

3. **Sync native platforms**
   ```bash
   npx cap sync android
   ```
   This copies `dist/` into `android/app/src/main/assets/public/`, refreshes plugin registries, and regenerates any Capacitor
   resource files. Use `npx cap copy android` for incremental asset-only updates.

4. **Open the project in Android Studio (optional)**
   ```bash
   npx cap open android
   ```

5. **Test metadata retention**
   Deploy the app to a device or emulator, capture/upload a photo from a component that requests `CameraResultType.Uri`, and then
   inspect the resulting file with `exiftool` or a similar utility to verify GPS and timestamp fields remain present.

   ```bash
   exiftool /path/to/photo.jpg | grep -E 'Create Date|GPS'
   ```

If you need to regenerate the Android platform from scratch, run `npx cap add android`. The command restores the binary launcher
icons and splash images described in `android/BINARY_ASSETS.md` before you copy them into version control.

## Digital Asset Links checklist

To publish on the Play Store, make sure the app and site association is valid:

1. Choose a package name (this project uses `fish.hookd.app`).
2. Generate or reuse the signing keystore; retrieve its SHA256 fingerprint with `keytool -list -v -keystore android/android.keystore`.
3. Host `https://hookd.fish/.well-known/assetlinks.json` with an entry that matches the package name and fingerprint.
4. Install a release build on a device and verify the Chrome overflow menu shows the app name, indicating the association
   succeeded.

Following the sections above keeps the Android wrapper lightweight while ensuring the web experience remains installable and can
access native upload APIs when necessary.
