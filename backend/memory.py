from datetime import datetime
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    favorite_color = Column(String, nullable=True)
    favorite_sport = Column(String, nullable=True)
    favorite_anime = Column(String, nullable=True)
    favorite_food = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)

    messages = relationship('Message', back_populates='user', cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='messages')

class MemoryStore:
    def __init__(self, db_url: str = "sqlite:///memory.db"):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_or_create_user(self, user_id: str) -> User:
        with self.Session() as s:
            u = s.get(User, user_id)
            if not u:
                u = User(id=user_id)
                s.add(u)
                s.commit()
                s.refresh(u)
            return u

    def update_profile(self, user_id: str, updates: dict):
        with self.Session() as s:
            u = s.get(User, user_id)
            if not u:
                u = User(id=user_id)
                s.add(u)
            for k in ["name", "location", "favorite_color", "favorite_sport", "favorite_anime", "favorite_food"]:
                if k in updates and updates[k]:
                    setattr(u, k, updates[k])
            u.last_seen = datetime.utcnow()
            s.commit()

    def add_message(self, user_id: str, role: str, content: str):
        with self.Session() as s:
            m = Message(user_id=user_id, role=role, content=content)
            s.add(m)
            u = s.get(User, user_id)
            if u:
                u.last_seen = datetime.utcnow()
            s.commit()

    def get_recent_messages(self, user_id: str, limit: int = 8) -> List[Message]:
        with self.Session() as s:
            return (
                s.query(Message)
                .filter(Message.user_id == user_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
                .all()
            )[::-1]

    def get_user_profile(self, user_id: str) -> dict:
        with self.Session() as s:
            u = s.get(User, user_id)
            if not u:
                return {}
            return {
                "name": u.name,
                "location": u.location,
                "favorite_color": u.favorite_color,
                "favorite_sport": u.favorite_sport,
                "favorite_anime": u.favorite_anime,
                "favorite_food": u.favorite_food,
                "summary": u.summary,
            }

    def set_summary(self, user_id: str, summary: str):
        with self.Session() as s:
            u = s.get(User, user_id)
            if u:
                u.summary = summary
                s.commit()
