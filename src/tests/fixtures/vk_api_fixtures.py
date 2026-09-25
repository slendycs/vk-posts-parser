import pytest

from client.vk_client import VKClient


@pytest.fixture
def vk_client(request):
    yield VKClient()