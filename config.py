import os

from dotenv import load_dotenv

load_dotenv('..\\..\\.env')


class Config:
    MS_API_KEY = os.getenv('MS_API_KEY')
    MS_STORE_ID = os.getenv('MS_STORE_ID')
    GOOGLE_DOCUMENT_ID = os.getenv('GOOGLE_DOCUMENT_ID')