from django import forms

Genre_choices = (('Action','Action'),('Adventure','Adventure'),('Animation','Animation'),('Comedy','Comedy'),
                 ('Drama','Drama'),('Horror','Horror'),('Romance','Romance'),('Thriller','Thriller'),)

class MainForm(forms.Form):
    Year = forms.NumberInput()
    Name = forms.TextInput()



class GenreForm(forms.Form):
    Genre = forms.ChoiceField(choices=Genre_choices)
