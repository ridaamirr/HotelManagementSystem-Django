from django import forms

class LoginForm(forms.Form):
    login_type = forms.ChoiceField(
        choices=[('user', 'User Login'), ('admin', 'Admin Login')],
        widget=forms.RadioSelect(attrs={'class': 'radio'}),
        initial='user',  # Set the initial choice
    )
