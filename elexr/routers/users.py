from fastapi import APIRouter, Depends
from ..models import users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me")
def me(current_user: str = Depends(users.get_current_user)):
    return current_user
