import motor.motor_asyncio
from info import Config

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.col = self.db["files"]

    async def save_file(self, file_id, file_name, caption=""):
        data = {
            "file_id": file_id,
            "file_name": file_name,
            "caption": caption
        }
        await self.col.insert_one(data)

    async def get_search_results(self, query):
        regex = {'$regex': query, '$options': 'i'}
        files = self.col.find({"file_name": regex})
        return [file async for file in files]

    async def get_file(self, file_id):
        return await self.col.find_one({"file_id": file_id})
