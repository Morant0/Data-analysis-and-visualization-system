import shutil

from aerich import Command
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from tortoise.expressions import Q

from app.api import api_router
from app.controllers.api import api_controller
from app.controllers.user import UserCreate, user_controller
from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.log import logger
from app.models.admin import Api, Menu, Role
from app.schemas.menus import MenuType
from app.settings.config import settings

from .middlewares import BackGroundTaskMiddleware, HttpAuditLogMiddleware

import pandas as pd
import json
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(BackGroundTaskMiddleware),
        Middleware(
            HttpAuditLogMiddleware,
            methods=["GET", "POST", "PUT", "DELETE"],
            exclude_paths=[
                "/api/v1/base/access_token",
                "/docs",
                "/openapi.json",
            ],
        ),
    ]
    return middleware


def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


async def init_superuser():
    user = await user_controller.model.exists()
    if not user:
        await user_controller.create_user(
            UserCreate(
                username="admin",
                email="admin@admin.com",
                password="123456",
                is_active=True,
                is_superuser=True,
            )
        )


async def init_menus():
    menus = await Menu.exists()
    if not menus:
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="系统管理",
            path="/system",
            order=1,
            parent_id=0,
            icon="carbon:gui-management",
            is_hidden=True,
            component="Layout",
            keepalive=False,
            redirect="/system/user",
        )
        children_menu = [
            Menu(
                menu_type=MenuType.MENU,
                name="用户管理",
                path="user",
                order=1,
                parent_id=parent_menu.id,
                icon="material-symbols:person-outline-rounded",
                is_hidden=False,
                component="/system/user",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="角色管理",
                path="role",
                order=2,
                parent_id=parent_menu.id,
                icon="carbon:user-role",
                is_hidden=False,
                component="/system/role",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="菜单管理",
                path="menu",
                order=3,
                parent_id=parent_menu.id,
                icon="material-symbols:list-alt-outline",
                is_hidden=False,
                component="/system/menu",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="API管理",
                path="api",
                order=4,
                parent_id=parent_menu.id,
                icon="ant-design:api-outlined",
                is_hidden=False,
                component="/system/api",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="部门管理",
                path="dept",
                order=5,
                parent_id=parent_menu.id,
                icon="mingcute:department-line",
                is_hidden=False,
                component="/system/dept",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="审计日志",
                path="auditlog",
                order=6,
                parent_id=parent_menu.id,
                icon="ph:clipboard-text-bold",
                is_hidden=False,
                component="/system/auditlog",
                keepalive=False,
            ),
        ]
        await Menu.bulk_create(children_menu)
        await Menu.create(
            menu_type=MenuType.MENU,
            name="一级菜单",
            path="/top-menu",
            order=2,
            parent_id=0,
            icon="material-symbols:featured-play-list-outline",
            is_hidden=False,
            component="/top-menu",
            keepalive=False,
            redirect="",
        )


async def init_apis():
    apis = await api_controller.model.exists()
    await api_controller.refresh_api()


async def init_db():
    command = Command(tortoise_config=settings.TORTOISE_ORM, app="models")
    await command.init()  # 仅需初始化一次
    await command.upgrade()  # 每次启动应用时检查并应用迁移


async def init_roles():
    roles = await Role.exists()
    if not roles:
        admin_role = await Role.create(
            name="管理员",
            desc="管理员角色",
        )
        user_role = await Role.create(
            name="普通用户",
            desc="普通用户角色",
        )

        # 分配所有API给管理员角色
        all_apis = await Api.all()
        await admin_role.apis.add(*all_apis)
        # 分配所有菜单给管理员和普通用户
        all_menus = await Menu.all()
        await admin_role.menus.add(*all_menus)
        await user_role.menus.add(*all_menus)

        # 为普通用户分配基本API
        basic_apis = await Api.filter(Q(method__in=["GET"]) | Q(tags="基础模块"))
        await user_role.apis.add(*basic_apis)


def generate_disaster_association_rules(input_file_path, output_file_path, min_support=0.01, min_threshold=1):
    """
    生成灾害类型关联规则并保存为JSON文件
    参数:
        input_file_path (str): 输入Excel文件路径
        output_file_path (str): 输出JSON文件路径
        min_support (float): 最小支持度，默认为0.01
        min_threshold (float): 最小置信度，默认为1
    """
    try:
        # 读取数据
        df = pd.read_csv(input_file_path)
        # 提取灾害类型和相关联的次生灾害类型
        disaster_data = df[['Disaster Type', 'Associated Types']].copy()
        # 处理缺失值
        disaster_data['Associated Types'] = disaster_data['Associated Types'].fillna('None')
        # 将数据转换为适合关联分析的格式
        disaster_data['Disaster Type'] = disaster_data['Disaster Type'].str.strip()
        disaster_data['Associated Types'] = disaster_data['Associated Types'].str.strip()
        # 将关联类型拆分成列表
        disaster_data['Associated Types'] = disaster_data['Associated Types'].apply(
            lambda x: x.split('|') if '|' in x else [x])

        # 创建一个包含所有灾害类型和关联类型的列表
        all_disasters = []
        for _, row in disaster_data.iterrows():
            main_type = row['Disaster Type']
            associated_types = row['Associated Types']
            all_disasters.append([main_type] + associated_types)

        # 将列表转换为适合 Apriori 算法的格式
        te = TransactionEncoder()
        te_ary = te.fit(all_disasters).transform(all_disasters)
        disaster_df = pd.DataFrame(te_ary, columns=te.columns_)

        # 应用 Apriori 算法
        frequent_itemsets = apriori(disaster_df, min_support=min_support, use_colnames=True)

        # 生成关联规则
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)

        # 选择需要的列
        rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

        # 将 frozenset 转换为列表以便序列化为 JSON
        rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
        rules['consequents'] = rules['consequents'].apply(lambda x: list(x))

        # 将结果转换为字典格式
        association_rules_dict = rules.to_dict(orient='records')

        # 保存为 JSON 文件
        with open(output_file_path, 'w') as f:
            json.dump(association_rules_dict, f, indent=4)
        print(f"灾害关联规则已成功生成并保存至 {output_file_path}")

    except Exception as e:
        print(f"生成灾害关联规则时出错: {str(e)}")

async def init_data():
    input_excel_path = 'app/data/emdat.csv'
    output_json_path = 'app/api/v1/association/disaster_association_rules.json'
    generate_disaster_association_rules(input_excel_path, output_json_path)
    await init_db()
    await init_superuser()
    await init_menus()
    await init_apis()
    await init_roles()
