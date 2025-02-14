from django.shortcuts import render, redirect
from app_sys import models
from app_sys.utils.pagination import Pagination
from app_sys.utils.form import UserModelForm


# 用户管理
def user_list(request):
    """用户管理"""

    queryset = models.UserInfo.objects.all()

    search_data = request.GET.get("q", "")
    # 分页
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成的页码
    }

    return render(request, "user_list.html", context)


def user_add(request):
    """添加用户(ModelForm)"""

    if request.method == "GET":
        # 获取ModelForm对象
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    # 用户提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """编辑用户"""

    # 根据ID去数据库获取要编辑的那一行数据
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再保存除了用户输入以外的值
        #  form.instance.字段名 = 值
        form.save()
        return redirect("/user/list/")

    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """删除用户"""

    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
