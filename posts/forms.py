from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'thumbnail', 
        'categories', 'featured', 'breaking')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content', )

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control',
            'placeholder': 'Type your comment',
            'id': 'usercomment',
            'rows': '4'})
            }