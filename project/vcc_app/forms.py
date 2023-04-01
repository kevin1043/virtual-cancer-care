from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid email address')
        return email
