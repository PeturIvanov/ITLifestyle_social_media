from django import forms
from .models import UserPost


class PostForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(attrs={'placeholder': 'Enter Your Post!',
                                                                'class': 'form-control'}),
                           label='',
                           )

    class Meta:
        model = UserPost
        exclude = ('user',)



