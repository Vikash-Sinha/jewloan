from django import forms
from .models import *


class LoanInfoForm(forms.ModelForm):
    class Meta:
        model = LoanInfo
        fields = (
            'sr_no',
            'name',
            'product_id',
            'weight',
            'amount',
            'rate_of_interest',
            )


class LoanDetailForm(forms.ModelForm):
    class Meta:
        model = LoanDetail
        fields = (
            'Notes',
            'TodayRate',
            'Active',)