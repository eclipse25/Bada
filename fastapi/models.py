from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)

    posts = relationship("Post", back_populates="board")
    favorited_by = relationship("FavoriteBoard", back_populates="board")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey('boards.id'))
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime)
    content = Column(String)
    views = Column(Integer, default=0)
    user_ip = Column(String)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

    board = relationship("Board", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(String)
    user_ip = Column(String)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

    post = relationship("Post", back_populates="comments")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=False, unique=True)  # 사용자 닉네임
    password = Column(String(128), nullable=False)  # 사용자 비밀번호
    favorite_boards = relationship("FavoriteBoard", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")

    def __repr__(self):
        return f"<User(nickname={self.nickname})>"


class PostLike(Base):
    __tablename__ = 'post_likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    remaining_likes = Column(Integer, default=3)  # 남은 좋아요 가능 횟수

    user = relationship("User", back_populates="post_likes")
    post = relationship("Post")


class FavoriteBoard(Base):
    __tablename__ = 'favorite_boards'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    board_id = Column(Integer, ForeignKey('boards.id'))
    user = relationship("User", back_populates="favorite_boards")
    board = relationship("Board", back_populates="favorited_by")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    posts = relationship("Post", secondary="post_tags")


# Tag와 Post 사이의 연결 테이블
class PostTag(Base):
    __tablename__ = 'post_tags'
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


# 데이터베이스 엔진 생성
engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()