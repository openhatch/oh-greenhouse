from django import forms


class NotesForm(forms.Form):
    notes = forms.CharField(widget=forms.widgets.Textarea(), required=False)


class EditContrib(forms.Form):
    lpid = forms.CharField(label='Launchpad ID: ', required=True)
    email = forms.EmailField(label='Email: ', required=True)
