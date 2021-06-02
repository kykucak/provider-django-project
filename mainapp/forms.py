from django import forms


class OrderSubmissionForm(forms.Form):
    """Form for filling info about customer's details for order"""

    plan = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    city = forms.CharField()
    street = forms.CharField()
    house_num = forms.IntegerField()
    apartment_num = forms.IntegerField()

