from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class OrderForm(forms.Form):
    name = forms.CharField(
        label='Ім\'я'
    )
    last_name = forms.CharField(
        required=False,
        label='Прізвище')
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        label='Телефон',
        help_text='*По цьому номері з вами звяжеться наш менеджер',

    )
    address = forms.CharField(
        required=False,
        label='Адреса доставки',
        help_text='*Обовязково вкажіть місто'
    )
    comments = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Коментарі до замовлення',
        help_text='Доставка відбувається в районі декількох днів після замовлення. ' \
                  'Менеджер заздалегіть з вами звяжеться'
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логін'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Перевірте правильнісь даних')


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логін',
        min_length=6,
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
    )
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'first_name',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = ''
        self.fields['password'].label = 'Пароль'
        self.fields['password2'].label = 'Повторіть пароль'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'Ім\'я'
        self.fields['last_name'].label = 'Прізвище'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Паролі не співпадають')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Користувач із таким логіном вже зареєстрований')

