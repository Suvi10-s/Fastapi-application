import os
from motor import motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL")

client=motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database=client.suvidb
collection=database.user_details