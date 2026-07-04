import os
from dotenv import load_dotenv

load_dotenv()

print("API KEY:")
print(os.getenv("ELEVENLABS_API_KEY"))