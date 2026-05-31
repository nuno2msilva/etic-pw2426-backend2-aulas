import html
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not _USERNAME_RE.match(username):
            raise forms.ValidationError(
                "Username must be 3–20 characters: letters, digits, and underscores only."
            )
        return username


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment…"}),
    )

    def clean_comment(self):
        raw = self.cleaned_data["comment"].strip()
        if not raw:
            raise forms.ValidationError("Comment cannot be empty.")
        return html.escape(raw)
