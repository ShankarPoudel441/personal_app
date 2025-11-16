from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Ask me something about Shankar...'  # can be changed
    }))
