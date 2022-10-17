from aiohttp import ClientSession


class HttpRequest:
    def __init__(self):
        self.url = None
        self._headers = {"Content-Type": "application/json"}

    async def get(self, url, headers, params=None):
        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as response:
                return await response.json()

    async def post(self, url, headers, body=None):
        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, json=body) as response:
                return await response.json()

    async def put(self, url, headers, body=None):
        async with ClientSession() as session:
            async with session.put(url=url, headers=headers, json=body) as response:
                return await response.json()
