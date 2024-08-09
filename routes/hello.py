from fastapi import APIRouter
from fastapi.responses import JSONResponse
from functools import lru_cache


router = APIRouter()


# @log_cache
@lru_cache(maxsize=128)
@router.get("/")
async def hello():
    try:
        return {"Hello": "World!"}
    except Exception as err:
        return JSONResponse({"error": str(err)}, 500)
