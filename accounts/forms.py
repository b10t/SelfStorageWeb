from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


# class CustomAuthenticationForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={
#         'placeholder': 'E-mail',
#         'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
#     }))
#     password = forms.CharField(label='Логин', strip=False, widget=forms.PasswordInput(attrs={
#         'placeholder': 'Пароль',
#         'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
#     }),
#     )


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail',
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            }),
            'password': forms.PasswordInput(attrs={'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'}),
        }

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['email'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #
    #     if email is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, email=email, password=password
    #         )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, label='email', help_text='Add a valid email address')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        # self.fields['email'].widget.attrs['type'] = 'email'
        # self.fields['email'].widget.attrs['name'] = 'EMAIL_CREATE'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтверждение пароля'
        self.fields['email'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'
        self.fields['password1'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'
        self.fields['password2'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'


class ProfileForm(forms.ModelForm):
    error_messages = {
        'password_mismatch": "The two password fields didn’t match.',
    }
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Enter the same password as before, for verification.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['first_name'].required = True
        self.fields['username'].required = True
        # self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        # fields = ['first_name', 'username']
        fields = ['username']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Введенные пароли не совпадают.')
            password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        user = super().save(commit=False)
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
