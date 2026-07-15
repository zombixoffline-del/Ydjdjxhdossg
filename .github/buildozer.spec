[app]
title = Test
package.name = mytestgame
package.domain = org.mytestgame
version = 0.3

source.dir = .
source.include_exts = py

requirements = python3,kivy

orientation = landscape

android.api = 34
android.minapi = 26
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2