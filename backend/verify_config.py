import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import Config

print(f"Loading config from: {os.getcwd()}")
print(f"LLM_API_KEY present: {bool(Config.LLM_API_KEY)}")
print(f"ZEP_API_KEY present: {bool(Config.ZEP_API_KEY)}")

errors = Config.validate()
if errors:
    print("Configuration Errors found:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("Configuration is VALID. You are ready to run!")
