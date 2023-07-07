from django import forms


class CodeErrorForm(forms.Form):
    code = forms.CharField(max_length=500)
    error = forms.CharField(max_length=500)
