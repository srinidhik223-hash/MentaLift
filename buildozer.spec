[app]
title = MentaLift
package.name = mentalift
package.domain = org.srinidhi
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 0.1
requirements = kivy,requests
icon.filename = icon.png
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
copy_libraries = True
android.archs = arm64-v8a, armeabi-v7a
log_level = 2

[buildozer]
