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
