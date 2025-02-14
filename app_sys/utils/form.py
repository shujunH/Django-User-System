from django import forms
from app_sys import models
from django.core.validators import RegexValidator, ValidationError
from app_sys.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app_sys.utils.encrypt import md5


# ModelForm
# 用户
class UserModelForm(BootStrapModelForm):
    """ModelForm类"""

    # 创建在HTML文件中要显示的字段
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]


# 靓号
class PrettyModelForm(BootStrapModelForm):
    # 验证输入值是否合法：（方式1：字段 + 正则表达式）
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']  # 写什么字段就生成什么标签
        # fields = "__all__"                                    # 所选类中所有字段
        # exclude = ['mobile']                                  # 排除哪个字段

    # 方式2：钩子方法
    # def clean_mobile(self):
    #     # 获取用户输入的所有数据中的mobile字段的内容
    #     txt_mobile = self.cleaned_data["mobile"]
    #
    #     if len(txt_mobile) != 11:
    #         # 验证不通过
    #         raise ValidationError("格式错误")
    #
    #     return txt_mobile

    def clean_mobile(self):
        # 获取用户输入的所有数据中的mobile字段的内容
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 不允许修改手机号
    # mobile = forms.CharField(disabled=True)

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 编辑手机号提交时检验除了自身以外是否有其他mobile与自身相同
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


# 管理员
class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        # 用户输入密码加密
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库的就是什么
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        # 用户输入密码加密
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd)
        if exists:
            raise ValidationError("不能与以前的密码相同")

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库的就是什么
        return confirm


# 登录
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


# 订单
class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["oid", "admin"]
