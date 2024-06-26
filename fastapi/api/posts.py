from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db, Post, Board, Tag, PostTag, Comment
import logging
from typing import List, Optional
from datetime import datetime
import pytz
# from .scheduler import update_trending_boards

router = APIRouter()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 요청 모델 정의
class PostCreateRequest(BaseModel):
    board_id: str
    content: str
    delete_key: str
    hashtags: list[str]


# 응답 모델 정의
class PostCreateResponse(BaseModel):
    id: int
    board_id: str
    board_post_number: int
    content: str
    created_at: str
    hashtags: list[str]


class CommentCreateRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    user_ip: str
    upvotes: int
    created_at: str

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    board_id: str
    board_post_number: int
    content: str
    created_at: str
    views: int
    upvotes: int
    hashtags: List[str]
    comments: List[CommentResponse]

    class Config:
        orm_mode = True


class PostListResponse(BaseModel):
    message: Optional[str] = None
    posts: List[PostResponse]


class CommentListResponse(BaseModel):
    comments: List[CommentResponse]


class PostDeleteRequest(BaseModel):
    delete_key: str


@router.post("/posts", response_model=PostCreateResponse)
async def create_post(request: PostCreateRequest, http_request: Request, db: Session = Depends(get_db)):
    logger.info(f"Received request: {request.model_dump()}")
    try:
        board_id = request.board_id
        board = db.query(Board).filter(Board.id == board_id).first()

        if not board:
            logger.error(f"Board not found for board_id: {board_id}")
            raise HTTPException(status_code=404, detail="Board not found")

        last_post = db.query(Post).filter(Post.board_id == board_id).order_by(
            Post.board_post_number.desc()).first()
        if last_post:
            board_post_number = last_post.board_post_number + 1
        else:
            board_post_number = 1

        new_post = Post(
            board_id=board.id,
            board_post_number=board_post_number,
            content=request.content,
            user_ip=http_request.client.host,
            delete_key=request.delete_key,
            created_at=datetime.now(pytz.timezone('Asia/Seoul'))
        )

        db.add(new_post)
        db.commit()  # 첫 번째 커밋
        logger.info(f"New post committed with ID: {new_post.id}")
        db.refresh(new_post)

        # 태그 처리
        tags = []
        for tag_name in request.hashtags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
                tag.usage_count = 1
                logger.info(f"New tag created and committed: {tag.name}")
            else:
                tag.usage_count += 1
                logger.info(f"Tag {tag.name} usage count updated to {
                            tag.usage_count}")
            tags.append(tag)
            # PostTag 테이블에 관계 추가
            post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
            db.add(post_tag)

        db.commit()  # 두 번째 커밋
        logger.info(f"Tags associated with post ID: {new_post.id} committed")

        # # 세션 새로 고침
        # db.refresh(new_post)

        # # 트렌드 게시판 업데이트
        # update_trending_boards()

        return PostCreateResponse(
            id=new_post.id,
            board_id=str(new_post.board_id),
            board_post_number=new_post.board_post_number,
            content=new_post.content,
            created_at=new_post.created_at.isoformat(),
            hashtags=[tag.name for tag in tags]
        )
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        db.rollback()  # 예외 발생 시 롤백
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the post")
    finally:
        db.close()


@router.get("/posts/all", response_model=PostListResponse)
async def get_all_posts(db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching all posts")
        posts = db.query(Post).order_by(Post.created_at.desc()).all()

        if not posts:
            return PostListResponse(message="No posts found", posts=[])

        return PostListResponse(posts=[PostResponse(
            id=post.id,
            board_id=post.board_id,
            board_post_number=post.board_post_number,
            content=post.content,
            created_at=post.created_at.isoformat(),
            views=post.views,
            upvotes=post.upvotes,
            hashtags=[tag.name for tag in post.tags],
            comments=[
                CommentResponse(
                    id=comment.id,
                    post_id=comment.post_id,
                    content=comment.content,
                    user_ip=comment.user_ip,
                    upvotes=comment.upvotes,
                    created_at=comment.created_at.isoformat()
                ) for comment in post.comments
            ]
        ) for post in posts])
    finally:
        db.close()


@router.get("/posts/board/{board_id}", response_model=PostListResponse)
async def get_posts(board_id: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching posts for board_id: {board_id}")
        if board_id:
            posts = db.query(Post).filter(Post.board_id == board_id).order_by(
                Post.created_at.desc()).all()
        else:
            posts = db.query(Post).order_by(Post.created_at.desc()).all()

        if not posts:
            return PostListResponse(message="No posts found for this board", posts=[])
        return PostListResponse(posts=[PostResponse(
            id=post.id,
            board_id=post.board_id,
            board_post_number=post.board_post_number,
            content=post.content,
            created_at=post.created_at.isoformat(),
            views=post.views,
            upvotes=post.upvotes,
            hashtags=[tag.name for tag in post.tags],
            comments=[
                CommentResponse(
                    id=comment.id,
                    post_id=comment.post_id,
                    content=comment.content,
                    user_ip=comment.user_ip,
                    upvotes=comment.upvotes,
                    created_at=comment.created_at.isoformat()
                ) for comment in post.comments
            ]
        ) for post in posts])
    finally:
        db.close()


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostResponse(
            id=post.id,
            board_id=post.board_id,
            content=post.content,
            board_post_number=post.board_post_number,
            created_at=post.created_at.isoformat(),
            views=post.views,
            upvotes=post.upvotes,
            hashtags=[tag.name for tag in post.tags],
            comments=[
                CommentResponse(
                    id=comment.id,
                    post_id=comment.post_id,
                    content=comment.content,
                    user_ip=comment.user_ip,
                    upvotes=comment.upvotes,
                    created_at=comment.created_at.isoformat()
                ) for comment in post.comments
            ]
        )
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching the post")
    finally:
        db.close()


@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(post_id: int, request: CommentCreateRequest, http_request: Request, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        client_ip = http_request.headers.get('X-Forwarded-For')
        if client_ip:
            client_ip = client_ip.split(',')[0]
        else:
            client_ip = http_request.client.host

        new_comment = Comment(
            post_id=post.id,
            content=request.content,
            user_ip=client_ip,
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        return CommentResponse(
            id=new_comment.id,
            post_id=new_comment.post_id,
            content=new_comment.content,
            user_ip=new_comment.user_ip,
            upvotes=new_comment.upvotes,
            created_at=new_comment.created_at.isoformat()
        )
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the comment")
    finally:
        db.close()


@router.get("/posts/{post_id}/comments", response_model=CommentListResponse)
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    try:
        comments = db.query(Comment).filter(
            Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()
        return CommentListResponse(comments=[
            CommentResponse(
                id=comment.id,
                post_id=comment.post_id,
                content=comment.content,
                user_ip=comment.user_ip,
                upvotes=comment.upvotes,
                created_at=comment.created_at.isoformat()
            ) for comment in comments
        ])
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching comments")
    finally:
        db.close()


@router.post("/posts/{post_id}/upvote")
async def upvote_post(post_id: int, http_request: Request, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.upvotes += 1
        db.commit()
        db.refresh(post)

        return {"upvotes": post.upvotes}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred while upvoting the post")
    finally:
        db.close()


@router.post("/posts/{post_id}/downvote")
async def downvote_post(post_id: int, http_request: Request, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.upvotes -= 1
        db.commit()
        db.refresh(post)

        return {"upvotes": post.upvotes}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred while downvoting the post")
    finally:
        db.close()


@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int, request: PostDeleteRequest, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.delete_key != request.delete_key:
            raise HTTPException(status_code=403, detail="Invalid delete key")

        # 관련 태그 사용 수 감소 및 태그 삭제
        post_tags = db.query(PostTag).filter(PostTag.post_id == post_id).all()
        for post_tag in post_tags:
            tag = db.query(Tag).filter(Tag.id == post_tag.tag_id).first()
            if tag:
                tag.usage_count -= 1
                if tag.usage_count <= 0:
                    db.delete(tag)

        # 관련 태그 및 댓글 삭제
        db.query(PostTag).filter(PostTag.post_id == post_id).delete()
        db.query(Comment).filter(Comment.post_id == post_id).delete()

        # 게시물 삭제
        db.delete(post)
        db.commit()
        logger.info(">>>>>>post was deleted.\n")

        # # 트렌드 게시판 업데이트
        # update_trending_boards()

        # 세션 새로 고침
        db.commit()

        return {"message": "Post deleted successfully\n"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the post")
    finally:
        db.close()
