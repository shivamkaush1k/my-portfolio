from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"style": "display:none;", "id": "honeypot"})
    )

    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Project details (optional)",
        })
    )

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "What's your name?",
                "required": "required",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "your.email@example.com",
                "required": "required",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-input textarea",
                "rows": 6,
                "placeholder": "Hi Shivam, I'm interested in...",
                "required": "required",
            }),
        }

    def clean_honeypot(self):
        honeypot = self.cleaned_data.get("honeypot")
        if honeypot:
            raise forms.ValidationError("Spam bot detected.")
        return honeypot

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 10:
            raise forms.ValidationError("Message is too short (minimum 10 characters).")
        return message