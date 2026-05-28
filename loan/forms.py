from django import forms

class NewLoanForm(forms.Form):
    book_id = forms.ChoiceField(label='ID du livre', required=True)
    date_retour = forms.DateField(
        label='Date de retour', 
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        book_choices = kwargs.pop('book_choices', [])
        super(NewLoanForm, self).__init__(*args, **kwargs)
        self.fields['book_id'].choices = book_choices

class ReturnLoanForm(forms.Form):
    emprunt_id = forms.ChoiceField(label='ID de l\'emprunt', required=True)

    def __init__(self, *args, **kwargs):
        emprunt_choices = kwargs.pop('emprunt_choices', [])
        super(ReturnLoanForm, self).__init__(*args, **kwargs)
        self.fields['emprunt_id'].choices = emprunt_choices
