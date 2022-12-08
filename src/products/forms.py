from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # product_name = forms.CharField(label="品名", widget=forms.Textarea(attrs={"placeholder": "請輸入品名", "rows": 1}))
    # # brand = forms.MultipleChoiceField(queryset=None)
    # material_color = forms.CharField(label="材質及配色", required=False, widget=forms.Textarea(attrs={"placeholder": "概要", "rows": 1}))
    # description = forms.CharField(label="描述", widget=forms.Textarea(attrs={"placeholder": "描述", "rows": 3}))
    # price = forms.IntegerField(label="價格", initial=0.0)
    # # picture = forms.ImageField(label="商品圖片", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    # # threeD_model = forms.FileField(label="商品3D模型", required=False)

    class Meta:
        model = Product
        fields = [
            'brand',
            'product_name',
            'material',
            'color',
            'description',
            'price',
            'size',
            'picture',
            'threeD_model'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("product_name")
        if "asd" in title:
            raise forms.ValidationError("This is not a valid title")
        return title


class RawProductForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "品名", "rows": 1}))
    description = forms.CharField( widget=forms.Textarea(attrs={"placeholder": "描述", "rows": 5}))
    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "概要", "rows": 5}))
    price = forms.DecimalField(initial=0.0)




