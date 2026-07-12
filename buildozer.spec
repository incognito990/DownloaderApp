[app]
# 🔥 ඇප් එක ඉන්ස්ටෝල් කළාම ෆෝන් එකේ පෙන්වන නම
title = PH Downloader

# 📌 ඇප් එකේ පැකේජ් නම (මෙතනත් phdownloader කියලා හැදුවා)
package.name = phdownloader
package.domain = org.test
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🖼️ ඔයා අප්ලෝඩ් කරන Logo එක සම්බන්ධ කරන තැන
icon.filename = icon.png

requirements = python3,kivy,kivymd,yt-dlp,certifi,idna,urllib3,setuptools,pillow
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
