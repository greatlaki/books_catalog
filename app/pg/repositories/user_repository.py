from base.repository import PgRepository
from user.models import User


class UserRepository(PgRepository):
    model = User
