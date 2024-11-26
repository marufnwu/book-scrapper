import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

CONFIG = {
    "DEBUG" : os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
}
