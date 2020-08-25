from .models import Post, Comment, ChildComment, Image
from django import forms
from django.forms import inlineformset_factory
# from tinymce import TinyMCE


# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False

class PostCreateForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'featured', 'category',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'style': 'height:100px'})

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mx-auto col-11',
        'placeholder': 'Type your comment',
        'rows': '4',
        'id': 'comment_input'
        }))
    class Meta:
        model = Comment
        fields = ['comment']

class ChildCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mx-auto col-11',
        'placeholder': 'Type your comment',
        'rows': '4',
        'id': 'child_comment_input'
        }))
    class Meta:
        model = ChildComment
        fields = ['comment']


PostImageFormSet = inlineformset_factory(Post, Image, fields=('thumbnail',), extra=1, max_num=6, can_delete=True)