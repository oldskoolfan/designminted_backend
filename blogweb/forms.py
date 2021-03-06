from django import forms
from blogapi.models import ContactFormMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = [ 'firstname', 'lastname', 'email', 'message' ]
        widgets = {
            'message': forms.Textarea(),
            'email': forms.EmailInput(),
        }