# hookdapp

Trusted Web Activity (TWA) project for wrapping [hookd.fish](https://hookd.fish).

## Development setup

1. Install the Bubblewrap CLI:
   ```bash
   npm install -g @bubblewrap/cli
   ```
2. Install JDK 17 and the Android SDK command-line tools. Download the
   `commandlinetools-linux` archive from Google, extract it, and install the
   required platform components:
   ```bash
   export ANDROID_SDK_ROOT="$HOME/.bubblewrap/android_sdk"
   mkdir -p "$ANDROID_SDK_ROOT"
   unzip commandlinetools-linux-*_latest.zip -d "$ANDROID_SDK_ROOT/cmdline-tools"
   mv "$ANDROID_SDK_ROOT/cmdline-tools"/cmdline-tools "$ANDROID_SDK_ROOT/cmdline-tools/latest"
   "$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" \
     "platform-tools" "build-tools;34.0.0" "platforms;android-34"
   ln -s cmdline-tools/latest "$ANDROID_SDK_ROOT/tools"
   ln -s cmdline-tools/latest/bin "$ANDROID_SDK_ROOT/bin"
   ```
   Run `bubblewrap doctor` to confirm Bubblewrap can locate both the JDK and the
   Android SDK.

## Building the Android project

1. Set the Android SDK environment variables (or add a `local.properties` file
   inside `android/` containing `sdk.dir=/path/to/sdk`):
   ```bash
   export ANDROID_HOME="$ANDROID_SDK_ROOT"
   export ANDROID_SDK_ROOT="$ANDROID_SDK_ROOT"
   ```
2. Add the release keystore referenced by Bubblewrap. The repository does not
   include binary signing material; follow the instructions in
   `android/KEYSTORE_PLACEHOLDER.md` to generate or supply a file named
   `android/android.keystore` with the expected credentials.

3. Download the Gradle wrapper bootstrap JAR by running the helper script:
   ```bash
   python android/scripts/bootstrap_gradle_wrapper.py
   ```
   The binary wrapper is ignored by Git; see
   `android/GRADLE_WRAPPER_PLACEHOLDER.md` for more background.

4. Restore the binary artwork. All PNG launch, notification, splash, and store
   icons are ignored by Git so the project ships with XML placeholders instead.
   Consult `android/ASSET_REQUIREMENTS.md` for the list of expected files and
   densities, then export the artwork from your design source before building.

5. Build the release artifacts from the `android/` directory:
   ```bash
   cd android
   bubblewrap build
   ```
   When prompted, use the provided keystore alias `hookd` with password
   `Hookd123` for both the keystore and key.

The build outputs `app-release-signed.apk` and `app-release-bundle.aab` inside
the `android/` directory. Bubblewrap also stores the original TWA configuration
in `android/twa-manifest.json` for future updates.
Capacitor wrapper for the hookd.fish PWA.

## Prerequisites

- Node.js 18+
- npm 9+
- Android Studio (Electric Eel or newer) with the Android SDK installed
- Java 17 (required by the current Android Gradle Plugin)

Install dependencies once after cloning:

```bash
npm install
```

### Restore required binary assets

This repository omits the Gradle wrapper JAR and the generated launcher/splash PNGs to keep the history free of binary blobs. Restore them before opening the Android project by regenerating the platform shell locally:

```bash
npx cap add android
```

Then copy the following outputs back into this repo (see `android/BINARY_ASSETS.md` for the complete list):

- `android/gradle/wrapper/gradle-wrapper.jar`
- All launcher icons under `android/app/src/main/res/mipmap-*/`
- All splash screens under `android/app/src/main/res/drawable*/`

## Build the web assets

1. Build or export the Hookd PWA so that the production assets land in `dist/`.
   - Replace the placeholder `npm run build` script in `package.json` with the build command from the web project if needed.
2. Verify that `dist/index.html` exists and contains the compiled app.

```bash
npm run build
```

## Sync assets into the Capacitor shell

After building the PWA assets, sync them into the native projects:

```bash
npx cap sync android
```

This copies `dist/` into `android/app/src/main/assets/public/` and refreshes the plugin configuration (Camera and Filesystem). If you only need to copy web assets without reinstalling plugins, run `npx cap copy android` instead.

To open the Android project in Android Studio:

```bash
npx cap open android
```

## File-upload metadata handling

- `capacitor.config.ts` configures the Camera plugin to always return URI-based results with editing disabled. This preserves EXIF data when the Hybrid app requests media from the Camera plugin.
- `android/app/src/main/java/fish/hookd/app/MainActivity.java` registers the Camera and Filesystem plugins explicitly and enables file/content access on the underlying WebView so uploads routed through the WebView bridge retain file metadata.
- The project depends on `@capacitor/camera@^5.0.10` and `@capacitor/filesystem@^5.2.2`. Make sure these versions (or newer within the same major) are installed so EXIF metadata is available via `photo.exif` when calling `Camera.getPhoto({ resultType: CameraResultType.Uri })`.

## Testing metadata preservation

1. Build the web bundle and sync it into Android as described above.
2. Run the Android project from Android Studio on a device or emulator.
3. In the app, trigger an upload using a file input or Camera integration that requests `CameraResultType.Uri`.
4. On the receiving backend (or by using `adb pull` on the temporary file path returned by the Filesystem plugin), inspect the uploaded image with `exiftool` and confirm GPS/date metadata is intact.

Example command after pulling the uploaded file from the device:

```bash
exiftool path/to/photo.jpg | grep -E 'Create Date|GPS'
```

If metadata is missing, confirm that the Camera plugin call does **not** request base64 output (`resultType: CameraResultType.Base64`) or enable editing, both of which strip EXIF information on Android.
