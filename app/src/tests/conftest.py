import pytest
from httpx import AsyncClient
from fastapi import FastAPI

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from api import app


import pytest
from httpx import AsyncClient
from httpx import ASGITransport


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

