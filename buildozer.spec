[app]

# عنوان التطبيق
title = Osra AI Social Automation
package.name = osra.social.automation
package.domain = org.example

# إصدار التطبيق
version = 1.0

# متطلبات Python
requirements = python3,kivy,kivymd,playwright,mistralai,python-dotenv,sqlite3

# أيقونة التطبيق (اختياري)
icon.filename = %(source.dir)s/assets/icon.png

# شاشة البداية
orientation = portrait
fullscreen = 0

# إعدادات Android
android.permissions = INTERNET
android.api = 30
android.ndk = 23b
android.sdk = 30
