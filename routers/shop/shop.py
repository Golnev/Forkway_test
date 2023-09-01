from fastapi import APIRouter
from routers.shop import status_order, outlets_by_phone, order_crud, visit_crud

router = APIRouter(
    prefix='',
    tags=['Shop']
)


router.include_router(status_order.router)
router.include_router(outlets_by_phone.router)
router.include_router(order_crud.router)
router.include_router(visit_crud.router)
