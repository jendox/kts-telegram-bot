import asyncio
from datetime import datetime, timedelta

from jose import jwt
from jose.constants import ALGORITHMS


class TokenManager:
    def __init__(self, secret: str, renew_every: int = 300):
        self._secret = secret
        self._lock = asyncio.Lock()
        self._token: str | None = None
        self._renew_every = renew_every

    async def _generate_token(self):
        payload = {
            "sub": "bot",
            "role": "bot",
            "exp": datetime.now() + timedelta(seconds=self._renew_every),
            "iat": datetime.now(),
        }
        return jwt.encode(payload, self._secret, algorithm=ALGORITHMS.HS256)

    async def start(self):
        while True:
            async with self._lock:
                self._token = await self._generate_token()
            await asyncio.sleep(self._renew_every // 2)

    @property
    async def token(self):
        async with self._lock:
            return self._token
