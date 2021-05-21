from django import forms


class OrderSubmissionForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    city = forms.CharField()
    street = forms.CharField()
    house = forms.CharField()
