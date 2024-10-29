from typing import Literal
from ..models.users import User
from redis.asyncio import Redis


class RedisClient(Redis):

    service = '{{cookiecutter.project_slug}}'

    async def broadcast_user_cud_actions(self, user: User, action: Literal['create', 'update', 'delete']):
        await self.xadd(f'{self.service}.{action}', {'user_id': user.id})
