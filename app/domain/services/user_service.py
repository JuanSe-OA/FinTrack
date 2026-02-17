class UserService:

    @staticmethod
    def can_create_transaction(user) -> bool:
        return user.is_active
