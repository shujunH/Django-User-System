from django import forms


class BootStrap:
    # 将不想应用的样式的名称写在里面
    bootstrap_exclude_fields = []

    # 循环找到所有的插件，添加了"class": "form-control"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # HTML中原本含有标签属性时，在原来的基础上再加上BootStrap样式
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            # 为空白时，直接覆盖BootStrap样式
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapForm(BootStrap, forms.Form):
    pass


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass
