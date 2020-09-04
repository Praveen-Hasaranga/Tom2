from .models import Job
from django.forms import ModelForm


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['job_id', 'customer_name', 'description', 'quantity', 'value', 'sales_person', 'category']
