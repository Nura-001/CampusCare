from django import forms

from .models import Complaint, ComplaintCategory


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'title',
            'description',
            'category',
            'location',
            'room_number',
            'priority',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only active categories in the dropdown
        self.fields['category'].queryset = ComplaintCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = 'Select a category'