from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


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
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтверждение пароля'
        self.fields['email'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'
        self.fields['password1'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'
        self.fields['password2'].widget.attrs['class'] = 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'


class ProfileForm(forms.ModelForm):
    # TODO: Сделать валидацию email
    #       Почему-то email не меняется в личном кабинете

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'form-control fs_24 ps-2 SelfStorage__input',
            'disabled': True
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control fs_24 ps-2 SelfStorage__input'
        self.fields['email'].disabled = True

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        user = super().save(commit=False)
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
