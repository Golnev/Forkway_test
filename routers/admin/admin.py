from fastapi import APIRouter
from routers.admin import customer, order, employee, outlet, visit

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


router.include_router(employee.router)
router.include_router(customer.router)
router.include_router(outlet.router)
router.include_router(order.router)
router.include_router(visit.router)
