from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template import loader
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext as _

from dm_apps.utils import custom_send_mail
from . import models

try:
    from dm_apps import my_conf as local_conf
except (ModuleNotFoundError, ImportError):
    from dm_apps import default_conf as local_conf

# from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('position_eng', 'position_fre', 'phone', 'language', 'section')


class UserAccountForm(forms.ModelForm):
    class Meta:
        # fields = ('username','first_name','last_name','email','password1','password2')
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'email': "Username / Email address"
        }


class AccountRequestForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email address')
    reason_for_request = forms.CharField(widget=forms.Textarea)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text=_(
        'Required - a verification email will be sent to you once this form is submitted'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=new_email).count() > 0:
            url_redirect = reverse("password_reset")
            raise forms.ValidationError(mark_safe(
                "This email address already exists in the database. To reset your account credentials click <a href='{}'>HERE</a>".format(
                    url_redirect)))
            # raise forms.ValidationError(_(mark_safe('An account already exists for this email address. <a href="#" class="email_error">Log in instead?</a>')))

        if new_email.lower().endswith("@dfo-mpo.gc.ca") == False:
            raise forms.ValidationError(
                _("Only DFO employees can register for an account. Please enter an email ending with '@DFO-MPO.GC.CA'"))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return new_email


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email")


class RequestAccessForm(forms.Form):
    # we only want the text from the choices of apps
    APPLICATION_CHOICES = [(app_key, local_conf.APP_DICT[app_key]) for app_key in local_conf.APP_DICT]
    APPLICATION_CHOICES.insert(0, (None, "-----"))

    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email address')
    user_id = forms.CharField(widget=forms.HiddenInput())
    application = forms.ChoiceField(label='Requesting access to which app', choices=APPLICATION_CHOICES)
    optional_comment = forms.CharField(required=False, label="Details")

# class SetUserPasswordForm(SetPasswordForm):

# label='Reason for request'

class DMAppsPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        custom_send_mail(
            html_message=body,
            subject=subject,
            from_email=from_email,
            recipient_list=[to_email]
        )

        # email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # if html_email_template_name is not None:
        #     html_email = loader.render_to_string(html_email_template_name, context)
        #     email_message.attach_alternative(html_email, 'text/html')
        #
        # email_message.send()
