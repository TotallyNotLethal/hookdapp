# Android Keystore Placeholder

The release keystore used by Bubblewrap is not stored in this repository.

To build signed release artifacts, add a keystore file named `android.keystore`
to this directory with the following credentials:

- **Alias:** `hookd`
- **Keystore password:** `Hookd123`
- **Key password:** `Hookd123`

You can generate the keystore with Bubblewrap using:

```bash
bubblewrap init --manifest=https://hookd.fish/.well-known/assetlinks.json
```

or by running `keytool` manually:

```bash
keytool -genkeypair \
  -alias hookd \
  -keyalg RSA \
  -keysize 2048 \
  -validity 20000 \
  -keystore android.keystore \
  -storepass Hookd123 \
  -keypass Hookd123 \
  -dname "CN=hookd.fish, OU=Hookd, O=Hookd, L=San Francisco, S=CA, C=US"
```

Place the generated `android.keystore` file alongside this placeholder.
