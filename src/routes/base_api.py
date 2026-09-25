from fastapi import APIRouter, Query, HTTPException

from client.vk_client import VKClient
from client.vk_errors import APICallError, NoItemsError
from configs.config import settings


router = APIRouter(prefix='/api', tags=['Base API Endpoints'])

@router.get('/get-posts')
async def get_posts(domain:str = Query(default=settings.VK_GROUP_DOMAIN, description='VK Group domain'), 
                    count:int = Query(default=3, le=100, ge=1, description='Count of posts to get (1-100)'),
                    post_text_len:int = Query(default=70, ge=1, description='Post text length')):
    try:
        client = VKClient()
        return await client.get_posts(domain, count, post_text_len)
    except APICallError as e:
        raise HTTPException(status_code=502, detail="An error on VK's part. For more information, see the logs") from e
    except NoItemsError as e:
        raise HTTPException(status_code=415, detail="Failed to retrieve valid posts") from e
