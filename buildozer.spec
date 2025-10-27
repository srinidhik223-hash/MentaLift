[app]
title = MentaLift
package.name = mentalift
package.domain = org.srinidhi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.api = 32
android.minapi = 21
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk
android.entrypoint = launcher.py
android.icon = icon.png
log_level = 2
copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
