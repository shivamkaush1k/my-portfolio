from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "What's your name?",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "your.email@example.com",
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "Project details (optional)",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control rounded-3",
                "rows": 6,
                "placeholder": "Hi Shivam, I'm interested in...",
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            raise forms.ValidationError("Message is too short.")
        return message