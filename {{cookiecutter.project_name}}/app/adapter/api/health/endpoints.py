from fastapi import APIRouter

router = APIRouter(
    prefix=""
)


@router.get("/")
async def health():
    return {"message": "healthy"}