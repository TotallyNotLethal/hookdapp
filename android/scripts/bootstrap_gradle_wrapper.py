#!/usr/bin/env python3
"""Download the Gradle wrapper JAR referenced by gradle-wrapper.properties.

This repository intentionally excludes binary artifacts. Contributors should run
this script before invoking any Gradle tasks so that the wrapper JAR is
available locally.
"""
from __future__ import annotations

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

WRAPPER_JAR_RELATIVE_PATH = "gradle/wrapper/gradle-wrapper.jar"
# Keep this in sync with distributionUrl in gradle/wrapper/gradle-wrapper.properties.
GRADLE_VERSION = "8.1.1"
DISTRIBUTION_URL = f"https://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip"


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    jar_path = project_root / WRAPPER_JAR_RELATIVE_PATH

    if jar_path.exists():
        print(f"Gradle wrapper JAR already present at {jar_path}.")
        return 0

    print(f"Downloading Gradle {GRADLE_VERSION} wrapper from {DISTRIBUTION_URL}...")
    with urllib.request.urlopen(DISTRIBUTION_URL) as response:
        if response.status != 200:
            print(
                f"Failed to download distribution: HTTP {response.status}",
                file=sys.stderr,
            )
            return 1
        archive_data = response.read()

    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        jar_entry = None
        for name in archive.namelist():
            if name.endswith("gradle-wrapper.jar") or \
               name.endswith(f"gradle-wrapper-{GRADLE_VERSION}.jar"):
                jar_entry = name
                break

        if jar_entry is None:
            print(
                "Could not locate gradle-wrapper artifact in downloaded archive.",
                file=sys.stderr,
            )
            return 1

        with archive.open(jar_entry) as jar_file:
            jar_path.parent.mkdir(parents=True, exist_ok=True)
            with open(jar_path, "wb") as output:
                output.write(jar_file.read())

    print(f"Saved wrapper JAR to {jar_path} from archive entry {jar_entry}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
