from django import forms
from .models import Brand, Account, Cart, HandSize
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BrandForm(forms.ModelForm):
    # 設定提示字 row顯現為1
    brand_name = forms.CharField(label="品牌名稱", widget=forms.Textarea(attrs={"placeholder": "品牌名稱",  "rows": 1}))
    description = forms.CharField(label="敘述", widget=forms.Textarea(attrs={"placeholder": "描述", "rows": 5}))
    email = forms.EmailField(label="電子信箱", widget=forms.Textarea(attrs={"placeholder": "連絡信箱", "rows": 1}))
    phone_number = forms.CharField(label="聯絡電話", widget=forms.Textarea(attrs={"placeholder": "聯絡電話", "rows": 1}))
    tax_ID_number = forms.CharField(
        label="統一編號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入地址", 'class': 'form-control'}),
        required=False
    )
    address = forms.CharField(
        label="地址",
        widget=forms.TextInput(attrs={"placeholder": "請輸入地址", 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Brand
        fields = [
            'brand_name',
            'description',
            'email',
            'phone_number',
            'tax_ID_number',
            'address'
        ]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not (email.endswith("com") or email.endswith("tw")):
            raise forms.ValidationError("This is not a valid email")
        return email


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []


class Test(forms.ModelForm):
    testing = forms.TextInput()

    class Meta:
        model = Cart
        fields = []


class HSCreateForm(forms.ModelForm):
    class Meta:
        model = HandSize
        fields = []


class HandSizeForm(forms.ModelForm):
    thumb_length = forms.DecimalField(label="拇指長", max_value=30, min_value=0.0, initial=1.0)
    index_length = forms.DecimalField(label="食指長", max_value=30, min_value=0.0, initial=1.0)
    middle_length = forms.DecimalField(label="中指長", max_value=30, min_value=0.0, initial=1.0)
    ring_length = forms.DecimalField(label="無名長", max_value=30, min_value=0.0, initial=1.0)
    little_length = forms.DecimalField(label="小指長", max_value=30, min_value=0.0, initial=1.0)

    thumb_width = forms.DecimalField(label="拇指寬", max_value=4, min_value=0.0, initial=1.0)
    index_width = forms.DecimalField(label="食指寬", max_value=4, min_value=0.0, initial=1.0)
    middle_width = forms.DecimalField(label="中指寬", max_value=4, min_value=0.0, initial=1.0)
    ring_width = forms.DecimalField(label="無名寬", max_value=4, min_value=0.0, initial=1.0)
    little_width = forms.DecimalField(label="小指寬", max_value=4, min_value=0.0, initial=1.0)

    palm_length = forms.DecimalField(label="手掌長", max_value=20, min_value=0.0, initial=7.0)
    palm_width = forms.DecimalField(label="手掌寬", max_value=20, min_value=0.0, initial=7.0)

    class Meta:
        model = HandSize
        fields = [
            'thumb_length', 'index_length', 'middle_length', 'ring_length', 'little_length',
            'thumb_width', 'index_width', 'middle_width', 'ring_width', 'little_width',
            'palm_length', 'palm_width'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入帳號", 'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"placeholder": "請輸入密碼", 'class': 'form-control'})
    )


class RegisterForm(UserCreationForm):
    iden = ((0, '顧客'), (1, '廠商'))
    identity = forms.ChoiceField(label='身份別', widget=forms.Select, choices=iden)
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入帳號", 'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="名稱",
        widget=forms.TextInput(attrs={"placeholder": "請輸入名稱", 'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"placeholder": "請輸入密碼", 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={"placeholder": "請再次輸入密碼", 'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={"placeholder": "請輸入電子信箱", 'class': 'form-control'})
    )

    phone_number = forms.CharField(
        label="電話號碼",
        widget=forms.TextInput(attrs={"placeholder": "請輸入電話號碼", 'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ('identity', 'username', 'last_name', 'password1', 'password2', 'email', 'phone_number')


class consumer_registerForm(UserCreationForm):
    iden = ((0, '顧客'), (1, '廠商'))
    identity = forms.ChoiceField(label='身份別', widget=forms.Select, choices=iden)
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入帳號", 'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="名稱",
        widget=forms.TextInput(attrs={"placeholder": "請輸入名稱", 'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"placeholder": "請輸入密碼", 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={"placeholder": "請再次輸入密碼", 'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={"placeholder": "請輸入電子信箱", 'class': 'form-control'})
    )

    YEARS = [str(x) for x in range(1920, 2021)]
    MONTHS = {
        1: '一月', 2: '二月', 3: '三月', 4: '四月',
        5: '五月', 6: '六月', 7: '七月', 8: '八月',
        9: '九月', 10: '十月', 11: '十一月', 12: '十二月'
    }
    date_of_birth = forms.DateField(
        label='生日',
        widget=forms.SelectDateWidget(years=YEARS, months=MONTHS),
        error_messages={
            'invalid': '請輸入有效生日日期',
            'required': '請輸入生日',
        }
    )

    sex_choice = ((0, '生理女'), (1, '生理男'))
    gender = forms.ChoiceField(label='性别', widget=forms.Select, choices=sex_choice)
    phone_number = forms.CharField(
        label="電話號碼",
        widget=forms.TextInput(attrs={"placeholder": "請輸入電話號碼", 'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ('identity', 'username', 'last_name', 'password1', 'password2', 'email', 'date_of_birth',
                  'gender', 'phone_number')


class UpdateForm(forms.ModelForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入帳號", 'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="名稱",
        widget=forms.TextInput(attrs={"placeholder": "請輸入名稱", 'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"placeholder": "請輸入密碼", 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={"placeholder": "請再次輸入密碼", 'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={"placeholder": "請輸入電子信箱", 'class': 'form-control'})
    )

    phone_number = forms.CharField(
        label="電話號碼",
        widget=forms.TextInput(attrs={"placeholder": "請輸入電話號碼", 'class': 'form-control'})
    )

    tax_ID_number = forms.CharField(
        label="統一編號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入地址", 'class': 'form-control'})
    )
    address = forms.CharField(
        label="地址",
        widget=forms.TextInput(attrs={"placeholder": "請輸入地址", 'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ('username', 'last_name', 'password1', 'password2', 'email', 'tax_ID_number', 'address', 'phone_number')


class consumer_updateForm(forms.ModelForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"placeholder": "請輸入帳號", 'class': 'form-control'})
    )
    email = forms.EmailField(
         label='電子信箱',
         widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
         error_messages={
             'invalid': '請輸入有效電子信箱',
             'required': '尚未輸入電子信箱',
         }
     )
    YEARS = [str(x) for x in range(1920, 2021)]
    MONTHS = {
         1: '一月', 2: '二月', 3: '三月', 4: '四月',
         5: '五月', 6: '六月', 7: '七月', 8: '八月',
         9: '九月', 10: '十月', 11: '十一月', 12: '十二月'
     }
    date_of_birth = forms.DateField(
         label='生日',
         widget=forms.SelectDateWidget(years=YEARS, months=MONTHS),
         error_messages={
            'invalid': '請輸入有效生日日期',
            'required': '請輸入生日',
         }
      )
    password1 = forms.CharField(
         label='密碼',
         strip=False,
         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
         error_messages={'required': '尚未輸入密碼'},
      )
    password2 = forms.CharField(
         label='確認密碼',
         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
         strip=False,
         error_messages={'required': '尚未輸入確認密碼'},
     )
    error_messages = {
         'password_mismatch': '兩次密碼輸入不同',
     }

    sex_choice = ((0, '生理女'), (1, '生理男'))

    gender = forms.ChoiceField(label='性别', widget=forms.Select, choices=sex_choice)

    phone_number=forms.CharField(
        label="電話號碼",
        widget=forms.TextInput(attrs={"placeholder": "請輸入電話號碼", 'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2', 'phone_number', 'gender')


"""
class RawPartnerForm(forms.Form):
    company_name = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Company Name", "rows": 1}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Description", "rows": 5}))
    email = forms.EmailField(widget=forms.Textarea(attrs={"placeholder": "Contact Email", "rows": 1}))
    phone_number = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Phone Number", "rows": 1}))
"""
