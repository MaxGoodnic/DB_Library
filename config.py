import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_CONFIG = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': int(os.getenv('POSTGRES_PORT', 5432)),
        'database': os.getenv('POSTGRES_DB', 'university_db'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password')
    }
    
    SQLITE_DB = os.getenv('SQLITE_DB', 'university.db')
