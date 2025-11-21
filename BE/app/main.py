import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.api.v1.api import api_router
from app.models.exam import Exam
from app.models.submission import Submission
from app.models.student import Student

if not os.path.exists("static"):
    os.makedirs("static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kết nối Database khi app khởi động
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.DB_NAME],
        document_models=[Exam, Submission, Student]
    )
    print("✅ MongoDB Connected!")
    yield

app = FastAPI(title="AI Grading API", lifespan=lifespan)

# --- 2. MOUNT STATIC FILES ---
# Giờ thì an toàn rồi vì thư mục đã được tạo ở bước 1
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Backend is running!"}