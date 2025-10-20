from fastapi import APIRouter

from app.core.dependency import DependPermission

from .apis import apis_router
from .auditlog import auditlog_router
from .base import base_router
from .depts import depts_router
from .menus import menus_router
from .pcb import pcb_router
from .pcb_planning import router as pcb_planning_router
from .pcb_production import router as pcb_production_router
from .raw_material import router as raw_material_router
from .resource_consumption import router as resource_consumption_router
from .roles import roles_router
from .users import users_router
from .process_equipment import router as process_equipment_router
from .pollution_control import router as pollution_control_router
from .solid_waste import router as solid_waste_router
from .self_monitoring import router as self_monitoring_router
from .pcb_report import router as pcb_report_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermission])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermission])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermission])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermission])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermission])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermission])
v1_router.include_router(pcb_router, prefix="/pcb", dependencies=[DependPermission])
v1_router.include_router(pcb_planning_router, prefix="/pcb", dependencies=[DependPermission])
v1_router.include_router(pcb_production_router, prefix="/pcb", dependencies=[DependPermission])
v1_router.include_router(raw_material_router, prefix="/raw-material", dependencies=[DependPermission])
v1_router.include_router(resource_consumption_router, prefix="/resource-consumption", dependencies=[DependPermission])
v1_router.include_router(process_equipment_router, prefix="/process-equipment", dependencies=[DependPermission])
v1_router.include_router(pollution_control_router, prefix="/pollution-control", dependencies=[DependPermission])
v1_router.include_router(solid_waste_router, prefix="/solid-waste", dependencies=[DependPermission])
v1_router.include_router(self_monitoring_router, prefix="/self-monitoring", dependencies=[DependPermission])
v1_router.include_router(pcb_report_router, prefix="/pcb", dependencies=[DependPermission])