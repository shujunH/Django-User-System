from django.shortcuts import render, redirect
from app_sys.models import Admin
from app_sys.utils.pagination import Pagination
from app_sys.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app_sys import models


def admin_list(request):
    """ 管理员列表 """

    # 检查用户是否已登录，已经登录则继续往下走，未登录则跳转回登录页面
    # 用户发来请求，获取cookie随机字符串，拿着随机字符串去session中检索是否含有
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    # 搜索
    data_dict = {}
    # 通过GET请求获取用户搜索的内容，无输入则为空，无搜索条件，默认返回所有数据
    search_data = request.GET.get("q", "")
    if search_data:
        # 搜索包含用户输入内容的数据
        data_dict["username__contains"] = search_data

    queryset = Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """添加管理员"""

    title = "添加管理员"

    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    """编辑管理员"""

    row_object = models.Admin.objects.filter(id=nid).first()
    # 判断对象是否存在
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})

    title = "编辑管理员"

    form = AdminEditModelForm(instance=row_object)

    return render(request, 'change.html', {"title": title, 'form': form})


def admin_delete(request, nid):
    """删除管理员"""

    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    """ 重置密码 """

    row_object = models.Admin.objects.filter(id=nid).first()
    # 判断对象是否存在
    if not row_object:
        return redirect('/admin/list/')

    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})

