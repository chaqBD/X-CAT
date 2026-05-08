from fastapi import APIRouter

from app.api.analytics import budget, category, geographic, inventory, spend, supplier

router = APIRouter(prefix="/analytics", tags=["analytics"])
router.include_router(spend.router)
router.include_router(category.router)
router.include_router(supplier.router)
router.include_router(inventory.router)
router.include_router(budget.router)
router.include_router(geographic.router)
