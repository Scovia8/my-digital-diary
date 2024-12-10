from .models import Comment,Reply
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body','parent')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['parent'].widget = forms.HiddenInput()


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
