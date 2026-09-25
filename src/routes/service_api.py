from fastapi import APIRouter


router = APIRouter(prefix='/api/service', tags=['Service API Endpoints'])

@router.get('/health')
async def health() -> bool:
    return True
