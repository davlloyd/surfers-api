import pytest
from main import create_app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture(scope='module')
def new_feed(app):
    from main.data.models import Feed
    _feed = Feed(name='BOM',
                location='sydney',
                category='weather',
                url='http://weather')
    return _feed


@pytest.fixture(scope='module')
def test_client(app):
    testing_client = TestClient(app)
    yield testing_client  # this is where the testing happens
