# fix_urllib3.py -- fixes missing urllib3.contrib.appengine for PTB 13.x
import sys, types

fake_appengine = types.ModuleType("urllib3.contrib.appengine")
def is_appengine_sandbox():
    return False
fake_appengine.is_appengine_sandbox = is_appengine_sandbox
sys.modules["urllib3.contrib.appengine"] = fake_appengine

print("✅ urllib3.contrib.appengine patched")
