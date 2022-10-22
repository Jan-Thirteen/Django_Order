#encoding: utf-8

from apps.forms import FormMixin
from django import forms

class EditGoodsCategoryForm(forms.Form):
    pk = forms.IntegerField(error_messages={"required":"必须传入分类的id！"})
    name = forms.CharField(max_length=100)

from apps.goods.models import Goods
class WriteGoodsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = Goods
        exclude = ['category']


class EditGoodsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = Goods
        exclude = ['category']

from apps.goods.models import Banner
class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banner
        fields = ('priority','link_to','image_url')

class EditBannerForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Banner
        fields = ('priority','link_to','image_url')

# class PubCourseForm(forms.ModelForm,FormMixin):
#     category_id = forms.IntegerField()
#     teacher_id = forms.IntegerField()
#     class Meta:
#         model = Course
#         exclude = ("category",'teacher')