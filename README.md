# hookdapp

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
