import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_user_id():
    random_id = str(uuid.uuid4())
    return random_id


def hash(password: str):
    return pwd_context.hash(password)
