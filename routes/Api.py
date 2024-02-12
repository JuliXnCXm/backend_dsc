from fastapi import APIRouter
from endpoints import Index, User , Auth , Task


router = APIRouter()
router.include_router(Index.router)
router.include_router(Auth.router)
router.include_router(User.router)
router.include_router(Task.router)