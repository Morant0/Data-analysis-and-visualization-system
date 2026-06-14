from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class User(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=20, unique=True, description="用户名称", index=True)
    alias = fields.CharField(max_length=30, null=True, description="姓名", index=True)
    email = fields.CharField(max_length=255, unique=True, description="邮箱", index=True)
    phone = fields.CharField(max_length=20, null=True, description="电话", index=True)
    password = fields.CharField(max_length=128, null=True, description="密码")
    is_active = fields.BooleanField(default=True, description="是否激活", index=True)
    is_superuser = fields.BooleanField(default=False, description="是否为超级管理员", index=True)
    last_login = fields.DatetimeField(null=True, description="最后登录时间", index=True)
    roles = fields.ManyToManyField("models.Role", related_name="user_roles")
    dept_id = fields.IntField(null=True, description="部门ID", index=True)

    class Meta:
        table = "user"


class Role(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="角色名称", index=True)
    desc = fields.CharField(max_length=500, null=True, description="角色描述")
    menus = fields.ManyToManyField("models.Menu", related_name="role_menus")
    apis = fields.ManyToManyField("models.Api", related_name="role_apis")

    class Meta:
        table = "role"


class Api(BaseModel, TimestampMixin):
    path = fields.CharField(max_length=100, description="API路径", index=True)
    method = fields.CharEnumField(MethodType, description="请求方法", index=True)
    summary = fields.CharField(max_length=500, description="请求简介", index=True)
    tags = fields.CharField(max_length=100, description="API标签", index=True)

    class Meta:
        table = "api"


class Menu(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, description="菜单名称", index=True)
    remark = fields.JSONField(null=True, description="保留字段")
    menu_type = fields.CharEnumField(MenuType, null=True, description="菜单类型")
    icon = fields.CharField(max_length=100, null=True, description="菜单图标")
    path = fields.CharField(max_length=100, description="菜单路径", index=True)
    order = fields.IntField(default=0, description="排序", index=True)
    parent_id = fields.IntField(default=0, description="父菜单ID", index=True)
    is_hidden = fields.BooleanField(default=False, description="是否隐藏")
    component = fields.CharField(max_length=100, description="组件")
    keepalive = fields.BooleanField(default=True, description="存活")
    redirect = fields.CharField(max_length=100, null=True, description="重定向")

    class Meta:
        table = "menu"


class Dept(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="部门名称", index=True)
    desc = fields.CharField(max_length=500, null=True, description="备注")
    is_deleted = fields.BooleanField(default=False, description="软删除标记", index=True)
    order = fields.IntField(default=0, description="排序", index=True)
    parent_id = fields.IntField(default=0, max_length=10, description="父部门ID", index=True)

    class Meta:
        table = "dept"


class DeptClosure(BaseModel, TimestampMixin):
    ancestor = fields.IntField(description="父代", index=True)
    descendant = fields.IntField(description="子代", index=True)
    level = fields.IntField(default=0, description="深度", index=True)


class AuditLog(BaseModel, TimestampMixin):
    user_id = fields.IntField(description="用户ID", index=True)
    username = fields.CharField(max_length=64, default="", description="用户名称", index=True)
    module = fields.CharField(max_length=64, default="", description="功能模块", index=True)
    summary = fields.CharField(max_length=128, default="", description="请求描述", index=True)
    method = fields.CharField(max_length=10, default="", description="请求方法", index=True)
    path = fields.CharField(max_length=255, default="", description="请求路径", index=True)
    status = fields.IntField(default=-1, description="状态码", index=True)
    response_time = fields.IntField(default=0, description="响应时间(单位ms)", index=True)
    request_args = fields.JSONField(null=True, description="请求参数")
    response_body = fields.JSONField(null=True, description="返回数据")

# -------------------------------------------------------------------------
# ----------------------------灾害数据相关-----------------------------------
# -------------------------------------------------------------------------

class Disaster(BaseModel, TimestampMixin):
    id = None
    dis_no = fields.CharField(pk=True, max_length=20, description="灾害编号")
    classification_key = fields.CharField(max_length=15, description="分类键")
    disaster_group = fields.CharField(max_length=100, description="灾害组")
    disaster_subgroup = fields.CharField(max_length=100, description="灾害子组")
    disaster_type = fields.CharField(max_length=100, description="灾害类型")
    disaster_subtype = fields.CharField(max_length=100, description="灾害子类型")
    event_name = fields.CharField(max_length=255, null=True, description="事件名称")
    iso = fields.CharField(max_length=3, description="ISO代码")
    country = fields.CharField(max_length=255, description="国家名称")
    subregion = fields.CharField(max_length=255, description="子区域")
    region = fields.CharField(max_length=255, description="区域")
    location = fields.TextField(null=True, description="地理位置")
    origin = fields.TextField(null=True, description="起源")
    ofda_response = fields.BooleanField(description="OFDA响应")
    appeal = fields.BooleanField(description="国际援助请求")
    declaration = fields.BooleanField(description="紧急状态声明")
    magnitude = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="强度")
    magnitude_scale = fields.CharField(max_length=100, null=True, description="强度单位")
    latitude = fields.DecimalField(max_digits=9, decimal_places=6, null=True, description="纬度")
    longitude = fields.DecimalField(max_digits=9, decimal_places=6, null=True, description="经度")
    river_basin = fields.TextField(null=True, description="流域")
    start_year = fields.IntField(null=True, description="起始年")
    start_month = fields.IntField(null=True, description="起始月")
    start_day = fields.IntField(null=True, description="起始日")
    end_year = fields.IntField(null=True, description="结束年")
    end_month = fields.IntField(null=True, description="结束月")
    end_day = fields.IntField(null=True, description="结束日")
    start_date = fields.DateField(null=True, description="起始日期")
    end_date = fields.DateField(null=True, description="结束日期")
    duration_days = fields.IntField(null=True, description="持续天数")

    class Meta:
        table = "disasters"

class Country(BaseModel, TimestampMixin):
    id = None
    iso = fields.CharField(max_length=3, pk=True, description="ISO3代码")
    country = fields.CharField(max_length=255, description="国家名称")
    subregion = fields.CharField(max_length=255, description="子区域")
    region = fields.CharField(max_length=255, description="区域")

    class Meta:
        table = "countries"

class EconomicLoss(BaseModel, TimestampMixin):
    id = None
    dis_no = fields.CharField(pk=True, max_length=20, description="灾害编号")
    disaster_type = fields.CharField(max_length=100, description="灾害类型")
    country = fields.CharField(max_length=255, description="国家名称")
    reconstruction_adjusted = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="调整后重建费用（千美元）")
    insured_adjusted = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="调整后保险损失（千美元）")
    total_adjusted = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="调整后总损失（千美元）")
    cpi = fields.DecimalField(max_digits=15, decimal_places=8, null=True, description="消费者价格指数")
    start_year = fields.IntField(null=True, description="起始年")
    start_date = fields.DateField(null=True, description="起始日期")
    end_date = fields.DateField(null=True, description="结束日期")

    class Meta:
        table = "economic_loss"

class HumanImpact(BaseModel, TimestampMixin):
    id = None
    dis_no = fields.CharField(pk=True, max_length=20, description="灾害编号")
    disaster_type = fields.CharField(max_length=100, description="灾害类型")
    country = fields.CharField(max_length=255, description="国家名称")
    total_deaths = fields.IntField(null=True, description="总死亡人数")
    num_injured = fields.IntField(null=True, description="受伤人数")
    num_affected = fields.IntField(null=True, description="受影响人数")
    num_homeless = fields.IntField(null=True, description="无家可归人数")
    total_affected = fields.IntField(null=True, description="总受影响人数")
    start_year = fields.IntField(null=True, description="起始年")
    start_date = fields.DateField(null=True, description="起始日期")
    end_date = fields.DateField(null=True, description="结束日期")

    class Meta:
        table = "human_impact"
#
# class AssociatedType(BaseModel, TimestampMixin):
#     dis_no = fields.ForeignKeyField("models.Disaster", related_name="associated_types", description="灾害编号")
#     type_name = fields.CharField(max_length=255, description="关联灾害类型名称")
#
#     class Meta:
#         table = "associated_types"

