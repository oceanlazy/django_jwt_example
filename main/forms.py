from django.forms import EmailField, ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from main import models


class SignUpForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True, help_text=_("Required."))

    class Meta:
        model = models.CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PostForm(ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "text", "slug")
