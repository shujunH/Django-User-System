from django.shortcuts import render, HttpResponse, redirect
from io import BytesIO
from app_sys.utils.form import LoginForm
from app_sys import models
from app_sys.utils.code import check_code


def login(request):
    """登录"""

    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {'form': form})
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存七天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")

    return render(request, "login.html", {'form': form})


def image_code(request):
    """ 图片验证码 """

    # 调用pillow函数，生成图片
    img, code_str = check_code()
    print(code_str)

    # 写入到自己的session中（以便后续获取验证码再进行校验）
    request.session['image_code'] = code_str
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()
    return redirect("/login/")
