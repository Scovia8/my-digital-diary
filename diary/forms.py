from .models import Comment,Post
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body','image','video')
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'})) # Accept only images
    video = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': 'video/*'})) # Accept only videos
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'placeholder': 'Write your comment...'}), label="Comment")



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'video', 'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']  # Include image and video

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))  # Accept only images
    video = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': 'video/*'}))



