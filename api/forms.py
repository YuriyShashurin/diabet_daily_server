from typing import List, Optional


class UserSignUpForm:

    def __init__(self, request):
        self.requset: request
        self.error: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.email: Optional[str] = None

    async def load_data(self):
        pass

    async def is_valid(self):
        pass
