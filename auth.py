import os 
from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()
def get_auth():   
    client = Groq(
        api_key=os.environ.get("GROQ_API"),  # This is the default and can be omitted
    )
    tl_token = os.getenv("TELEGRAM_TOKEN")

    return client, tl_token


