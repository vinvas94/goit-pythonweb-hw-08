from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)

    contacts = relationship("Contact", back_populates="user", cascade="all, delete")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=False)
    extra_info = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="contacts")
