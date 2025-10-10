# fix_urllib3.py
# This patch prevents urllib3.contrib.appengine import errors in python-telegram-bot 13.x

import sys, types

# Create a fake module so that telegram.ext can import it without crashing
fake_appengine = types.ModuleType("urllib3.contrib.appengine")
sys.modules["urllib3.contrib.appengine"] = fake_appengine

print("✅ urllib3.contrib.appengine module patched successfully")
