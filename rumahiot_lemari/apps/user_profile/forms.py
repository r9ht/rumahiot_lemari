from django import forms

class UpdateProfileForm(forms.Form):
    full_name = forms.CharField(required=True, max_length=120)
    phone_number = forms.CharField(required=False, max_length=32)


