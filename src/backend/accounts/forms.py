from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    """
    This class is used to create a form for user registration.
    we have validated the fields and added the necessary css here as well.
    
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }), min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password did not match'
            )
        email = self.cleaned_data.get('email')
        try:
            Account.objects.get(email=email)
            raise forms.ValidationError(
                'Email already exists'
            )
        except Account.DoesNotExist:
            pass

    def __init__(self, *args, **kargs):
        super(RegistrationForm, self).__init__(*args, **kargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'example@domain.com'})
