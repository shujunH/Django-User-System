from django.shortcuts import render, HttpResponse, redirect
from app_sys import models
from app_sys.utils.bootstrap import BootStrapModelForm


def city_list(request):
    """ 城市列表 """

    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ 上传文件和数据(ModelForm) """

    title = "ModelForm上传"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_form.html", {'form': form, 'title': title})
