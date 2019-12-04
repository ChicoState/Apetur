from django import forms
from . import models


class CreateEvent(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['event_type','start_time','end_time']