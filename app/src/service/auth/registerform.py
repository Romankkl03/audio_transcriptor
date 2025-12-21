from fastapi import Request

class RegisterForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors = []
        self.email: str | None = None
        self.password: str | None = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.email or "@" not in self.email:
            self.errors.append("Некорректный email")

        if not self.password or len(self.password) < 4:
            self.errors.append("Пароль должен быть минимум 4 символа")

        return not self.errors
