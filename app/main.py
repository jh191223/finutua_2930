from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, photos, avatars, logs, predictions
from app.database import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI HealthCare API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(photos.router, prefix="/api/photos", tags=["photos"])
app.include_router(avatars.router, prefix="/api/avatars", tags=["avatars"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])

@app.get("/")
def read_root():
    return {"message": "AI HealthCare API is running"}

@app.get("/health")
def health_check():
