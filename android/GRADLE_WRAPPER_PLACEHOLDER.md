# Gradle wrapper JAR placeholder

The Gradle wrapper bootstrap JAR (`gradle/wrapper/gradle-wrapper.jar`) is not
committed to this repository. Before running any Gradle commands, download it by
running:

```bash
python android/scripts/bootstrap_gradle_wrapper.py
```

The script downloads the version referenced in
`android/gradle/wrapper/gradle-wrapper.properties` and writes it to the expected
location. Re-run the script whenever the Gradle distribution is upgraded.
