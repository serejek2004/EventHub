from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
        })
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'new-password',
        })
    )

    password_confirm = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if username.lower() and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use.")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self):
        username = self.cleaned_data.get('username')
        user = User.objects.create_user(
            username=username.lower(),
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class UserProfileInfoUpdateForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
        })
    )
    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    age = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Age',
        })
    )
    biography = forms.CharField(
        max_length=2000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Biography',
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Profile Picture',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email:
            if User.objects.filter(email=email).exclude(id=self.user.id).exists():
                raise forms.ValidationError("This email is already in use by another user.")

        return cleaned_data

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        user_profile = user.userprofile
        user_profile.age = self.cleaned_data['age']
        user_profile.biography = self.cleaned_data['biography']

        if self.cleaned_data.get('profile_picture'):
            user_profile.profile_picture = self.cleaned_data['profile_picture']

        user_profile.save()

        return user


class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Old password',
        })
    )
    new_password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password',
        })
    )
    new_password_confirm = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password',
        })
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        if len(new_password) < 8:
            raise forms.ValidationError("New password must be at least 8 characters.")

        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        if old_password and old_password == new_password:
            raise forms.ValidationError("The new password cannot be the same as the old password.")

        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Incorrect old password.")

        return cleaned_data