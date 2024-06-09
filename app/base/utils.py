from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_and_update(plain_password: str, hashed_password: str) -> tuple[bool, str]:
    return password_context.verify_and_update(plain_password, hashed_password)
