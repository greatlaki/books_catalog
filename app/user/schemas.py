from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None
