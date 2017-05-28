from django import forms

class YearForm(forms.Form):
    Year = forms.NumberInput()
    Name = forms.TextInput()

