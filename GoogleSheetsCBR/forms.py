from django.forms import ModelForm
from .models import ModelSort

class Form_sort(ModelForm):
    class Meta:
        model = ModelSort
        fields = ['sorts_Model', 'ASC_DESK_Model']