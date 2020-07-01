from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PostModel
from django import forms


class RegistationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super(RegistationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()


class PostCreationForm(forms.ModelForm):
    title = forms.TextInput()
    content = forms.Textarea()
    author = forms.HiddenInput()
    image = forms.FileInput()

    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",
            "author",
            "image",
        ]