from django.db import models


# Create your models here.

class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 有约束
    # - to 与哪张表关联
    # - to_field 与表中哪列数据关联
    # - on_delete 级联删除(关联的数据列被删除（如部门id被删除），关联的用户也一起删除)
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # 设置约束后数据库会自动加上与其关联的字段后缀，所以此处数据在数据库中的列名为depart_id

    # 关联用户不删除，数据列置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在Django中自定义的约束
    gender_choices = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="号码", max_length=11)
    price = models.IntegerField(verbose_name="价格")

    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)

    status_choices = (
        (0, "未占用"),
        (1, "已占用"),
    )
    status = models.SmallIntegerField(verbose_name="占用情况", choices=status_choices, default=0)


class Order(models.Model):
    """ 订单 """

    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (0, "待支付"),
        (1, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)
    admin = models.ForeignKey(verbose_name="管理员", to=Admin, on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """

    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """ 城市 """

    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    # 本质上数据库里的数据也是CharField,能够自动帮你保存数据，并且可以指定保存的路径
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')
