import json

from persistence import get_path
from persistence.model.user import User


class UserRepository:
    @staticmethod
    def install():
        UserRepository.__store_all([])

    @staticmethod
    def find_all():
        with open(get_path('users.json'), encoding='utf-8') as file:
            users = []

            for data in json.load(file):
                user = User.create_from_data(data)
                users.append(user)

            return users

    @staticmethod
    def find_by_id(user_id):
        for user in UserRepository.find_all():
            if user.user_id == user_id:
                return user

        return None

    @staticmethod
    def find_by_username(username):
        for user in UserRepository.find_all():
            if user.username.lower() == username.lower():
                return user

        return None

    @staticmethod
    def save(user):
        users = UserRepository.find_all()

        for i in range(len(users)):
            if users[i].username == user.username \
                    and users[i].user_id != user.user_id:
                raise ValueError(f'Duplicate username {user.username}.')

        if user.user_id is None:
            max_id = 0

            for i in range(len(users)):
                if users[i].user_id > max_id:
                    max_id = users[i].user_id

            user.user_id = max_id + 1
            users.append(user)
        else:
            for i in range(len(users)):
                if users[i].user_id == user.user_id:
                    users[i] = user
                    break

        UserRepository.__store_all(users)

        return user

    @staticmethod
    def delete_by_id(user_id):
        users = UserRepository.find_all()

        for i in range(len(users)):
            if users[i].user_id == user_id:
                users.pop(i)
                break

        UserRepository.__store_all(users)

    @staticmethod
    def __store_all(users):
        with open(get_path('users.json'), 'w', encoding='utf-8') as file:
            rows = []

            for user in users:
                row = user.to_data()
                rows.append(row)

            json.dump(rows, file)
