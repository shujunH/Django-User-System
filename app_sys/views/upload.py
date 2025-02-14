import os
from django.shortcuts import render, HttpResponse
from django import forms
from django.conf import settings
from app_sys import models
from app_sys.utils.bootstrap import BootStrapForm, BootStrapModelForm


def upload_list(request):
    """ 文件上传列表 """

    return render(request, "upload_list.html")


# 定义Form
class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """ Form上传 """

    title = "Form上传"
    if request.method == 'GET':
        form = UpForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})

    form = UpForm(request.POST, request.FILES)
    if form.is_valid():
        # 1.读取文件内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get("img")

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)

        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=media_path,
        )

        return HttpResponse("文件已上传")

    return render(request, "upload_form.html", {'form': form, 'title': title})


# 定义ModelForm
class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
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
        return HttpResponse("上传成功")
    return render(request, "upload_form.html", {'form': form, 'title': title})
