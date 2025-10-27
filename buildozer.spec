cat > buildozer.spec <<'INIF'
[app]

# (str) Title of your application
title = MentaLift

# (str) Package name
package.name = mentalift

# (str) Package domain
package.domain = org.srinidhi

# (str) Source dir
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,txt

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = kivy,requests

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target API
android.api = 31

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Copy libraries instead of linking
copy_libraries = True

# (str) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Log level
log_level = 2

[buildozer]
INIF
