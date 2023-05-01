import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey
from ..auth import get_api_key
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

@router.get("/token", tags=['API'])
async def read_token():
    return {
        'TOKEN': {os.getenv('ZEN_API_TOKEN')}
    }