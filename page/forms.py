from django import forms

class ProposeForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)