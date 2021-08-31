from django import forms
from .models import Comment, Post, Category


class CommentForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', "placeholder": "title"})
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', "placeholder": "body"})
    )

    class Meta:
        model = Comment
        fields = (
            'title'
            , 'body'
        )


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', "placeholder": "title"})
    )
    subtitle = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', "placeholder": "subtitle"})
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'editable form-control', "placeholder": "body"})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
        , widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = (
            'title'
            , 'subtitle'
            , 'body'
            , 'category'
        )

