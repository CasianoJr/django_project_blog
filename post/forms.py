from .models import Post
from django import forms

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'featured', 'category',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'style': 'height:100px'})