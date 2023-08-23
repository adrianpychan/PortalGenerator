import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('PORTAL_USERNAME'))
print(os.getenv('PORTAL_PASSWORD'))