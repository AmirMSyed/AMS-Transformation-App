[app]
# (str) Title of your application
title = AMS Transformation App

# (str) Package name
package.name = amstransform

# (str) Package domain (needed for android/ios packaging)
package.domain = org.amirmsyed

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.3

# (list) Application requirements
# We only need kivy now, since we are offline.
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) The Android archs to build for.
# arm64-v8a is the modern standard for Android phones.
android.archs = arm64-v8a

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK API to use
android.ndk_api = 21


[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
