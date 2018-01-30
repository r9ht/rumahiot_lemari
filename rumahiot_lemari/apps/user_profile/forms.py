from django import forms

class UpdateProfileForm(forms.Form):
    full_name = forms.CharField(required=True, max_length=70)
    # 15 max standart
    phone_number = forms.CharField(required=False, max_length=15)

class UpdateProfilePictureForm(forms.Form):
    profile_image = forms.ImageField()

