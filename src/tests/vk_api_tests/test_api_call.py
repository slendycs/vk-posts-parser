import allure
import pytest

from client.vk_client import VKClient
from client.vk_errors import APICallError
from tests.test_data import one_post_response
from tests.fixtures.vk_api_fixtures import vk_client


@pytest.mark.need_mock
@pytest.mark.vk
@pytest.mark.unit
@pytest.mark.asyncio
class TestApiCall:
    basic_method = 'wall.get'
    basic_group_domain = 'club238077517'
    basic_params = {'domain': basic_group_domain,
                    'count': 1}
    

    @allure.title('VK API Invalid link')
    async def test_api_call_invalid_link(self, caplog):
        with allure.step('#1. Set invalid link for VK client'):
            invalid_link = 'https://api.vkk.com/method'
            client = VKClient(api_url=invalid_link)
        with allure.step('#2. Try to call API method and check that method raised APICallError'):
            with pytest.raises(APICallError):
                response = await client.api_call(self.basic_method, 
                                                 self.basic_params)
        with allure.step('#3. Check logs'):
            assert 'A network error occurred while executing the request: [Errno -2] Name or service not known' in caplog.text, \
                   'No error message found in logs'


    @allure.title('VK API Invalid token')
    async def test_api_call_invalid_token(self, caplog):
        with allure.step('#1. Set invalid token for VK client'):
            invalid_token = 'dwdwdqwqdwqd'
            client = VKClient(token=invalid_token)
        with allure.step('#2. Try to call API method and check that method raised APICallError'):
            with pytest.raises(APICallError):
                response = await client.api_call(self.basic_method, 
                                                 self.basic_params)
        with allure.step('#3. Check logs'):
            assert 'Failed to execute method "wall.get": Some error from VK servers: User authorization failed: invalid access_token (4)' in caplog.text, \
                   'No error message found in logs'


    @allure.title('VK API wrong method')
    async def test_api_call_invalid_method(self, caplog, vk_client):
        with allure.step('#1. Try to call API with invalid method and check that method raised APICallError'):
            with pytest.raises(APICallError):
                response = await vk_client.api_call('bebra', self.basic_params)
        with allure.step('#2. Check logs'):
            assert 'Failed to execute method "bebra": Some error from VK servers: Unknown method passed' in caplog.text, \
                   'No error message found in logs'


    @allure.title('VK API Standart call')
    async def test_api_call_standart_call(self, caplog, vk_client):
        with allure.step('#1. Try to call API'):
            response = await vk_client.api_call(self.basic_method, 
                                                self.basic_params)
        with allure.step('#2. Check that logs is empty'):
            assert caplog.text == '', f'Some errors in logs: {caplog.text}'
        with allure.step('#3. Assert response'):
            response["response"]["items"][0]["track_code"] = ''
            response["response"]["items"][0]["views"]["count"] = 0
            response["response"]["items"][0]["attachments"][0]["photo"]["web_view_token"] = ''
            response["response"]["items"][0]["attachments"][0]["photo"]["access_key"] = ''
            response["response"]["reaction_sets"] = ''
            assert response == one_post_response, 'The response from the server does not match the expected one'
