from fastapi import APIRouter

from app.core.dependency import DependPermisson

from .apis import apis_router
from .auditlog import auditlog_router
from .base import base_router
from .depts import depts_router
from .menus import menus_router
from .roles import roles_router
from .users import users_router
from .countries import countries_router
from .disasters import disasters_router
from .economic_loss import economic_loss_router
from .human_impact import human_impact_router
from .association import association_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermisson])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermisson])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermisson])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermisson])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermisson])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermisson])
v1_router.include_router(countries_router, prefix="/country", dependencies=[DependPermisson])
v1_router.include_router(disasters_router, prefix="/disaster", dependencies=[DependPermisson])
v1_router.include_router(economic_loss_router, prefix="/economic_loss", dependencies=[DependPermisson])
v1_router.include_router(human_impact_router, prefix="/human_impact", dependencies=[DependPermisson])
v1_router.include_router(association_router, prefix="/association", dependencies=[DependPermisson])


