from dataclasses import dataclass

@dataclass
class Post:
    post_text:str
    first_image_url:str
    post_link:str
    title:str = ''
