from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.article = kwargs.pop('article', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.article = self.article
        comment.save()

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'onfocus': 'commentFocus()',
                                             'onfocusout': 'commentFocusOut()'}),
        }
