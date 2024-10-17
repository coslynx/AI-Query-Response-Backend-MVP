# Specify version and import
from sqlalchemy.orm import Session  # Version: 2.0.36
from api.src.core.db.models import User, QueryResponse  # Version: 2.0.36
from api.src.core.db.utils.db_utils import get_db  # Version: 2.9.2
from api.src.config.settings import Settings  # Version: 2.9.2

settings = Settings()

#  Function Definitions
def seed_users(db: Session):
    """Seeds the database with initial user data."""
    users = [
        User(email="user1@example.com", hashed_password=settings.HASH_PASSWORD("user1")),
        User(email="user2@example.com", hashed_password=settings.HASH_PASSWORD("user2")),
    ]
    db.add_all(users)
    db.commit()
    db.refresh(users)


def seed_query_responses(db: Session):
    """Seeds the database with initial query response data."""
    query_responses = [
        QueryResponse(user_id=1, query="What is the meaning of life?", model="text-davinci-003", response="The meaning of life is 42."),
        QueryResponse(user_id=2, query="What is the capital of France?", model="text-davinci-003", response="Paris"),
    ]
    db.add_all(query_responses)
    db.commit()
    db.refresh(query_responses)


def seed_db(db: Session):
    """Seeds the database with initial data for users and query responses."""
    seed_users(db)
    seed_query_responses(db)


if __name__ == "__main__":
    db = get_db()
    seed_db(db)