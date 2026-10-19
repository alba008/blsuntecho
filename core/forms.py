from django import forms
from .models import BusinessInquiry


class BusinessInquiryForm(forms.ModelForm):
    # Hidden honeypot field: normal visitors should leave it empty.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = BusinessInquiry
        fields = [
            "name",
            "email",
            "company",
            "service",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Your full name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@example.com"}
            ),
            "company": forms.TextInput(
                attrs={"placeholder": "Company (optional)"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Tell us about your project...",
                    "rows": 6,
                }
            ),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Invalid submission.")
        return value

    def clean_message(self):
        value = self.cleaned_data["message"].strip()
        if len(value) < 20:
            raise forms.ValidationError(
                "Please provide at least 20 characters."
            )
        return value
