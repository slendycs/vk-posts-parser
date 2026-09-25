import re
import emoji

from parser.data_structures import Post

def prepare_post_text(raw_text:str, number_of_characters:int = 15) -> str:
    """
    Обрабатывает исходный текст поста, удаляя из него эмодзи, цензуру и сокращая его 
    до `number_of_characters` символов

    Args:
        raw_text (str): Исходный текст из JSON
        number_of_characters (int): Количество символов до которого нужно сократить текст, по умолчанию - `15`
    
    Returns:
        str: Обработанный текст поста
    """
    post_text = emoji.replace_emoji(raw_text, '') # Удаление эмодзи
    post_text = re.sub(r'\[#blur\|([^|]+)\|[^]]+\]', r'\1', post_text) # Удаление цензуры
    
    # Сокращение текста
    if len(post_text) > number_of_characters:
        post_text = post_text[:number_of_characters] + '...'
    
    return post_text


def get_post_url(owner_id:str, id:str, domain:str) -> str:
    """
    Подготавливает ссылку на пост
    """ 
    return f'https://vk.com/{domain}?w=wall{owner_id}_{id}'


def get_first_image(attachments:list[dict]) -> str:
    """
    Среди прикреплённых медиа ищет первое изображение и возвращает ссылку на него
    """
    first_image_link = ''

    for attachment in attachments:
        if attachment.get('type') == 'photo':
            first_image_link = attachment.get('photo', {}).get('orig_photo', {}).get('url', '')
            break
    
    return first_image_link


def parse_posts_from_json(json_response: list[dict], domain:str, post_text_len:int = 70) -> list[Post]:
        """
        Получает из JSON списка постов их текст и первое изображение\n
        Текст ограничен только первыми 70-ю символами

        Args:
            json_response (list[dict]): Список постов из поля `items` JSON-ответа сервера
            domain (str): Домен откуда был получен JSON
            post_text_len (str): Количество символов до которого нужно сократить текст, по умолчанию - `70`
        
        Returns:
            list[Post]: Список объектов класса `Post`
        
        Examples:
        >>> post_list = self._parse_posts_from_json(response['response']['items'], domain)
        """
        posts: list[Post] = []

        for item in json_response:
            # URl поста
            post_url = get_post_url(item.get('owner_id', ''), item.get('id', ''), domain)

            # Текст поста (Обрезается до 70 символов, удаляются эмодзи и цензура)
            post_text = prepare_post_text(item.get('text', ''), post_text_len)
            
            # Поиск первого изображения
            attachments = item.get('attachments') or []
            first_image = get_first_image(attachments)

            # Добавляем только если присутствует изображение или текст
            if post_text == '' and first_image == '':
                continue
                
            posts.append(Post(post_text, first_image, post_url))

        return posts