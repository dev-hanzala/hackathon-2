"""Database access service patterns."""

from uuid import UUID

from sqlalchemy.orm import Session
from sqlmodel import select

from src.db.models import Session as SessionModel
from src.db.models import Task, User


class DBService:
    """Database access service."""

    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID) -> User | None:
        """Get user by ID."""
        return session.exec(select(User).where(User.id == user_id)).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User | None:
        """Get user by email."""
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Task | None:
        """Get task by ID."""
        return session.exec(select(Task).where(Task.id == task_id)).first()

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: UUID, user_id: UUID) -> Task | None:
        """Get task by ID and verify it belongs to user."""
        return session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()

    @staticmethod
    def get_user_tasks(
        session: Session,
        user_id: UUID,
        completed: bool | None = None,
        archived: bool | None = None,
    ) -> list[Task]:
        """Get tasks for a user with optional filtering."""
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        if archived is not None:
            query = query.where(Task.is_archived == archived)

        return session.exec(query).all()

    @staticmethod
    def create_user(session: Session, email: str, password_hash: str) -> User:
        """Create a new user."""
        user = User(email=email, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def create_task(session: Session, user_id: UUID, title: str) -> Task:
        """Create a new task."""
        task = Task(user_id=user_id, title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task(session: Session, task: Task, **kwargs) -> Task:
        """Update task fields."""
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task: Task) -> None:
        """Delete a task."""
        session.delete(task)
        session.commit()

    @staticmethod
    def get_session_by_token(session: Session, token: str) -> SessionModel | None:
        """Get session by token."""
        return session.exec(select(SessionModel).where(SessionModel.token == token)).first()

    @staticmethod
    def create_session(session: Session, user_id: UUID, token: str, expires_at) -> SessionModel:
        """Create a new session."""
        db_session = SessionModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        session.add(db_session)
        session.commit()
        session.refresh(db_session)
        return db_session

    @staticmethod
    def delete_session(session: Session, token: str) -> None:
        """Delete a session by token."""
        db_session = DBService.get_session_by_token(session, token)
        if db_session:
            session.delete(db_session)
            session.commit()
