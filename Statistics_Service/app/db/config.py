mport os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "../data/raw")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "../data/cleaned")
DATABASE_URI = os.getenv("DATABASE_URI")
