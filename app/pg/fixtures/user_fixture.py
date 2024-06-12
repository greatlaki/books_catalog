from base.utils import get_hashed_password
from pg.repositories.user_repository import UserRepository

users = {
    'repository': UserRepository,
    'data': [
        {'id': 1, 'email': 'user1@example.com', 'hashed_password': get_hashed_password('pass@words')},
        {'id': 2, 'email': 'user2@example.com', 'hashed_password': get_hashed_password('pass@words')},
        {'id': 3, 'email': 'user3@example.com', 'hashed_password': get_hashed_password('pass@words')},
        {'id': 4, 'email': 'user4@example.com', 'hashed_password': get_hashed_password('pass@words')},
        {'id': 5, 'email': 'user5@example.com', 'hashed_password': get_hashed_password('pass@words')},
    ],
}
