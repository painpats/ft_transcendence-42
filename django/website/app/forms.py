from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *
import re

################################################################################################
# SIGN UP FORM                                                                                #
################################################################################################

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if not re.search(r'[A-Z]', password1):
                self.add_error('password1', _('Password must contain at least one uppercase letter.'))
            if not re.search(r'[a-z]', password1):
                self.add_error('password1', _('Password must contain at least one lowercase letter.'))
            if not re.search(r'[0-9]', password1):
                self.add_error('password1', _('Password must contain at least one digit.'))
            if not re.search(r'[^a-zA-Z0-9]', password1):
                self.add_error('password1', _('Password must contain at least one special character.'))
        return password1
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and Member.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Username already in use.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Member.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email already in use.'))
        return email

################################################################################################
# SIGN IN FORM                                                                                #
################################################################################################

class SignInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            pass
        return cleaned_data

################################################################################################
# CHANGE AVATAR FORM                                                                          #
################################################################################################

class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['avatar']

################################################################################################
# CHANGE PSEUDO FORM                                                                          #
################################################################################################

class ChangePseudoForm(forms.ModelForm):
    current_password_pseudo = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Member
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('This field is required.'))
        if Member.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Username already in use.'))
        return username

    def clean(self):
        cleaned_data = super().clean()
        current_password_pseudo = cleaned_data.get('current_password_pseudo')
        if not current_password_pseudo:
            self.add_error('current_password_pseudo', _('This field is required.'))
        elif not self.instance.check_password(current_password_pseudo):
            self.add_error('current_password_pseudo', _('The current password is incorrect.'))
        if self.errors:
            cleaned_data['username'] = self.instance.username
        return cleaned_data

################################################################################################
# CHANGE EMAIL FORM                                                                           #
################################################################################################

class ChangeEmailForm(forms.ModelForm):
    current_password_email = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Member
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_('This field is required.'))
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email already in use.'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        current_password_email = cleaned_data.get('current_password_email')
        if not current_password_email:
            self.add_error('current_password_email', _('This field is required.'))
        elif not self.instance.check_password(current_password_email):
            self.add_error('current_password_email', _('The current password is incorrect.'))
        if self.errors:
            cleaned_data['email'] = self.instance.email
        return cleaned_data

################################################################################################
# CHANGE PASSWORD FORM                                                                        #
################################################################################################

class ChangePasswordForm(forms.Form):
    current_password_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password_password = cleaned_data.get('current_password_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if not self.user.check_password(current_password_password):
            self.add_error('current_password_password', _('The current password is incorrect.'))
        if self.user.check_password(new_password):
            self.add_error('new_password', _('The new password must be different from the current password.'))
        if new_password and len(new_password) < 8:
            self.add_error('new_password', _('Password must be at least 8 characters long.'))
        if not re.search(r'[A-Z]', new_password):
            self.add_error('new_password', _('Password must contain at least one uppercase letter.'))
        if not re.search(r'[a-z]', new_password):
            self.add_error('new_password', _('Password must contain at least one lowercase letter.'))
        if not re.search(r'[0-9]', new_password):
            self.add_error('new_password', _('Password must contain at least one digit.'))
        if not re.search(r'[^a-zA-Z0-9]', new_password):
            self.add_error('new_password', _('Password must contain at least one special character.'))
        if new_password != confirm_new_password:
            self.add_error('confirm_new_password', _('The new passwords do not match.'))

        return cleaned_data
    
################################################################################################
# ADD FRIEND FORM                                                                             #
################################################################################################

class AddFriendForm(forms.Form):
    add_friend = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        friend_username = cleaned_data.get('add_friend')

        friend = Member.objects.filter(username=friend_username).first()
        if not friend:
            self.add_error('add_friend', _("User not found"))
        elif friend == self.user:
            self.add_error('add_friend', _("You can't add yourself"))
        elif Friend.objects.filter(user=self.user, friend=friend, status='P').exists() or \
             Friend.objects.filter(user=friend, friend=self.user, status='P').exists():
            self.add_error('add_friend', _("An invitation with this user is already pending"))
        elif Friend.objects.filter(user=self.user, friend=friend, status='A').exists():
            self.add_error('add_friend', _("Already friends"))

        cleaned_data['add_friend'] = friend
        return cleaned_data
