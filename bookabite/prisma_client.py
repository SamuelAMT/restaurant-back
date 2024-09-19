import os
from dotenv import load_dotenv
from prisma import Prisma

load_dotenv()

database_url = os.getenv('DATABASE_URL')

prisma = Prisma()
prisma.connect()