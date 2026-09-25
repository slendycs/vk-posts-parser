from httpx import AsyncClient, HTTPError
from typing import Optional, Any
from json import JSONDecodeError

from client.vk_errors import VKError, APICallError, NoItemsError
from configs.config import settings
from parser.data_structures import Post
from parser.parser import parse_posts_from_json

class VKClient:
    def __init__(self, api_url:Optional[str] = None, version:Optional[str] = None, 
                 token:Optional[str] = None):
        """
        Класс для работы с API Вконтакте

        Args:
            api_url (Optional[str]): Базовый URL к API Вконтакте, по умолчанию `https://api.vk.ru/method/`
            version (Optional[str]): Версия API Вконтакте, по умолчанию `5.199`
            token (Optional[str]): Сервисный токен API Вконтакте, по умолчанию берётся из `.env`
        """
        if token is not None:
            self.token:str = token
        else:
            self.token:str = settings.VK_API_KEY
        if api_url is not None:
            self.base_url:str = api_url
        else:
            self.base_url:str = 'https://api.vk.ru/method/'

        if version is not None:
            self.api_version:str = version
        else:
            self.api_version:str = '5.199'
    
    
    async def api_call(self, method:str, params:dict[str, Any]) -> dict[str, Any]:
        """
        Базовый метод для доступа к API Вконтакте

        Args:
            method (str): Название VK API метода, например: `wall.get`
            params (dict[str, Any]): Словарь параметров метода

        Returns:
            dict[str, dict]: JSON ответ от серверов VK
        
        Examples:
        >>> client = VKClient()
        >>> params = {'domain': 'slendycsama', 'count': 1}
        >>> response = await client.api_call('wall.get', params)

        Raises:
            APICallError: При ошибках во время выполнения запроса
        """
        url = self.base_url + method

        params = params.copy()
        params['access_token'] = self.token
        params['v'] = self.api_version

        try:
            async with AsyncClient() as client:
                response = await client.post(url=url,
                                             params=params,
                                             timeout=30)
                response.raise_for_status()
                json_response = response.json()

                # Проверка на ошибки от ВК
                if json_response.get('error') is not None:
                    error_msg = json_response.get('error').get('error_msg')
                    raise VKError(error_msg)

                return json_response

        except HTTPError as e:
            settings.logger.error(f'A network error occurred while executing the request: {e}')
            raise APICallError(e, method) from e
        except VKError as e:
            settings.logger.error(f'Failed to execute method "{method}": {e}')
            raise APICallError(e, method) from e
        except JSONDecodeError as e:
            settings.logger.error(f'Failed to decode JSON response: {e}')
            raise APICallError(e, method) from e
        

    async def get_posts(self, domain:str, count:int, post_text_len:int) -> list[Post]:
        """
        Метод для получения постов со стены

        Args:
            domain (str): Короткий адрес пользователя или сообщества
            count (int): Количество записей, которое необходимо получить. Максимальное значение: `100`
            post_text_len (int): Количество символов до которого нужно сократить текст

        Returns:
            list[Post]: Список данных о постах со стены
        
        Examples:
        >>> client = VKClient()
        >>> response = await client.get_posts(domain='domain', count=3, post_text_len=70)
        >>> print(response[0].post_text) # Some text from latest post

        Raises:
            APICallError: При ошибках во время выполнения запроса
            NoItemsError: Если сервера ВК отправляют пустой ответ, либо не удалось получить нужную информацию
        """
        params = {'domain': domain,
                  'count': count}
        
        response = await self.api_call('wall.get', params)
        if (response['response']['items'] == []):
            err = NoItemsError('VK returned empty posts list', domain)
            settings.logger.error(err)
            raise err
        
        posts = parse_posts_from_json(response['response']['items'], domain, post_text_len)
        if len(posts) == 0:
            err = NoItemsError('Failed to retrieve valid data', domain)
            settings.logger.error(err)
            raise err
        
        return posts
