from fastapi import APIRouter

router = APIRouter(
    prifix='/',
    tags=['authentication']
)

# @router.get('/login')
# def login()