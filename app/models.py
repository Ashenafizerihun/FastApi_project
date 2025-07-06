from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, PrimaryKeyConstraint
from app.database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(200), nullable=False)
    published = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="posts")  # Establishing relationship with User model
    created_at = Column(DateTime, server_default=func.now())  # ✅ timestamp with default NOW()



class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # ✅ timestamp with default NOW()
    posts = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True)
    
    __table_args__ = (PrimaryKeyConstraint('user_id', 'post_id'), )