from typing import Optional

from fastapi import Request
from fastapi.security import HTTPBasicCredentials
from fastapi_users import BaseUserManager, IntegerIDMixin, models
from fastapi_users import exceptions

from ..db.adapters.users import UserAdapter
from ..schemas.users import UC
from ..db.models.users import User
from ..conf import SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    user_db: UserAdapter
    {% if cookiecutter.required_username %}
    async def authenticate(
            self, credentials: HTTPBasicCredentials
    ) -> Optional[User]:
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def get_by_username(self, username: str) -> User:
        user = await self.user_db.get_by_username(username)
        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def create(
            self,
            user_create: UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_username(user_create.username)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    {% endif %}