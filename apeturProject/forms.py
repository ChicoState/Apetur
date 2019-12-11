from django import forms
from . import models


class CreateEvent(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['event_type', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['start_time'].widget.attrs['placeholder'] = 'HH:MM:SS'
        self.fields['end_time'].widget.attrs['placeholder'] = 'HH:MM:SS'
