# fix_urllib3.py
# Patch to prevent urllib3.contrib.appengine errors in python-telegram-bot 13.x

import sys, types

# Create a fake module
fake_appengine = types.ModuleType("urllib3.contrib.appengine")

# Add fake attributes used by python-telegram-bot
def is_appengine_sandbox():
    return False

fake_appengine.is_appengine_sandbox = is_appengine_sandbox

# Register this fake module
sys.modules["urllib3.contrib.appengine"] = fake_appengine

print("✅ urllib3.contrib.appengine module patched successfully with is_appengine_sandbox")
