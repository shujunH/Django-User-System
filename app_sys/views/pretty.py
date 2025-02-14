from django.shortcuts import render, redirect
from app_sys import models
from app_sys.utils.pagination import Pagination
from app_sys.utils.form import PrettyModelForm, PrettyEditModelForm


# 靓号管理
def pretty_list(request):
    """靓号列表"""

    data_dict = {}
    # 通过GET请求获取用户搜索的内容，无输入则为空，无搜索条件，默认返回所有数据
    search_data = request.GET.get("q", "")
    if search_data:
        # 搜索包含用户输入内容的数据
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成的页码
    }

    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """新建靓号"""

    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""

    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """删除靓号"""

    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")