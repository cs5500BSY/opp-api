from fastapi import Path, Query, HTTPException, APIRouter
from pydantic import BaseModel, Field
from starlette import status

import models


router = APIRouter()


@router.get("/api/")
async def api_query_param(
        query_param: str = Query(min_length=2, max_length=100)):
    return {"message": 'Hello World', "query_param": query_param}
