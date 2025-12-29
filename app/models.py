from sqlalchemy import Column, Integer, String, Date, DateTime, Decimal, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String(100))
    gender = Column(String(10))
    birth_date = Column(Date)
    height = Column(Decimal(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    photos = relationship("UserPhoto", back_populates="user")
    avatars = relationship("Avatar", back_populates="user")
    food_logs = relationship("FoodLog", back_populates="user")
    exercise_logs = relationship("ExerciseLog", back_populates="user")

class UserPhoto(Base):
    __tablename__ = "user_photos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    photo_url = Column(Text, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    measurements = Column(JSON)
    is_primary = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="photos")

class Avatar(Base):
    __tablename__ = "avatars"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    photo_id = Column(Integer, ForeignKey("user_photos.id"))
    avatar_url = Column(Text, nullable=False)
    body_metrics = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="avatars")

class FoodLog(Base):
    __tablename__ = "food_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    log_date = Column(Date, nullable=False)
    meal_type = Column(String(20))
    food_name = Column(String(255))
    calories = Column(Integer)
    protein = Column(Decimal(5, 2))
    carbs = Column(Decimal(5, 2))
    fat = Column(Decimal(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="food_logs")

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    log_date = Column(Date, nullable=False)
    exercise_type = Column(String(100))
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer)
    intensity = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
