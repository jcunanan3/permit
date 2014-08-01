__author__ = 'joaquincunanan'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from permit_app.models import PermitUser, Permit

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class EmailUserCreationForm(UserCreationForm):
        email = forms.EmailField(required=True)

        helper = FormHelper()
        # helper.form_method= 'POST'
        helper.add_input(Submit('login','login', css_class='btn-primary'))

        class Meta:
            model = PermitUser
            fields = ("username", "first_name","last_name","phone","email", "address_1","address_2","city","state","zip_code","password1", "password2")

        def clean_username(self):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            username = self.cleaned_data["username"]
            try:
                PermitUser.objects.get(username=username)
            except PermitUser.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )


class PermitCreationForm(forms.ModelForm):

    class Meta:
        model = Permit
        fields = ("street_address","city","state","zip","date","resident_comments")


    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # self.helper.add_input(Submit('submit', 'Submit'))

    #    self.user = kwargs.pop('user','')
    #    super(PermitCreationForm, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #
    #     super(PermitCreationForm, self).save(commit=commit)

        # self.fields['user_defined_code']=forms.ModelChoiceField(queryset=UserDefinedCode.objects.filter(owner=user))


        # def clean_username(self):
        #     # Since User.username is unique, this check is redundant,
        #     # but it sets a nicer error message than the ORM. See #13147.
        #     username = self.cleaned_data["username"]
        #     try:
        #         Permit.objects.get(username=username)
        #     except Permit.DoesNotExist:
        #         return street_address
        #     raise forms.ValidationError(
        #         self.error_messages['duplicate_username'],
        #         code='duplicate_username',)

class PermitApprovalForm(forms.ModelForm):

    class Meta:
        model = Permit
        fields = ("street_address","city","state","zip","date","resident_comments","MTA_comments","approved","rejected")
