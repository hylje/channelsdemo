from django import forms

from channelsdemo.main.models import Thread, Post

class ThreadForm(forms.ModelForm):
    class Meta:
        fields = ["title"]
        model = Thread
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"})
        }

class PostForm(forms.ModelForm):
    class Meta:
        fields = ["text", "image"]
        model = Post
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"})
        }

    def clean(self):
        cleaned_data = super(PostForm, self).clean()

        if not any([cleaned_data.get("text"), cleaned_data.get("image")]):
            raise forms.ValidationError("text or image plz")

        return cleaned_data
