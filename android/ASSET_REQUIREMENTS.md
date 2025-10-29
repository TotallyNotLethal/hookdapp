# Android asset requirements

The Android Trusted Web Activity project ships without binary image assets. Replace the placeholder XML drawables with production-ready binaries before publishing or running `bubblewrap build` for release.

| Asset | Target location | Notes |
| --- | --- | --- |
| Launcher icon set | `android/app/src/main/res/mipmap-*/ic_launcher.png` and `ic_maskable.png` variants | Generate density-specific launcher icons (usually 48–192 px) using Android Studio's **Image Asset** wizard. Update `AndroidManifest.xml` to point back to `@mipmap/ic_launcher` if you restore the generated assets. |
| Notification icon | `android/app/src/main/res/drawable-*/ic_notification_icon.png` | Supply a white, transparent-background notification icon that follows Android notification guidelines. Remove `drawable/ic_notification_icon.xml` once the binaries are in place. |
| Splash image | `android/app/src/main/res/drawable-*/splash.png` | Provide full-bleed splash artwork sized for each density. Replace the placeholder shape at `drawable/splash.xml`. |
| Play Store icon | `android/store_icon.png` | 512×512 marketing icon used for the Play Store listing. |
| Web manifest icons | `icon-512.png`, `icon-maskable-512.png` in the repository root | These feed Bubblewrap's `iconUrl` and `maskableIconUrl` fields when updating the TWA manifest. |

Refer to the README for instructions on regenerating these assets locally. All binary images are ignored by Git so they remain local to your workstation.
