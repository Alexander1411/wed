from django import forms

from .models import RSVPResponse


class RSVPForm(forms.Form):
    attendance = forms.ChoiceField(
        choices=RSVPResponse.ATTENDANCE_CHOICES,
        widget=forms.RadioSelect,
    )
    full_name = forms.CharField(max_length=255)
    drinks = forms.MultipleChoiceField(
        choices=RSVPResponse.DRINK_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Укажите имя и фамилию.")
        return value
