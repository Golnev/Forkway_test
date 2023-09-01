from faker import Faker
from fastapi.testclient import TestClient

from main import app


fake = Faker('ru_RU')
client = TestClient(app)
