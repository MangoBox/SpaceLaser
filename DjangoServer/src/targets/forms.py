from django import forms

class SearchForm(forms.Form):
    item = forms.CharField(label="item", max_length=100)

    def is_valid(self):
        return True