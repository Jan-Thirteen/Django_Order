from django import forms
from apps.forms import FormMixin

class PublicCommentForm(forms.Form,FormMixin):
    content = forms.CharField()
    goods_id = forms.IntegerField()