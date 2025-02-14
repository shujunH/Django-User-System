from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """ 中间件（身份验证） """

    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已经登录过，可以继续向后执行
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect("/login/")

