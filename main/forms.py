from django import forms
from django.forms import ModelForm
from .models import CommunityItem

class ItemForm(ModelForm):
    class Meta:
        model = CommunityItem
        labels = {
            'name': 'Name',
            'description': 'Description',
            'quantity': 'Number of items',
        }

        fields = ['name', 'description', 'quantity']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input ', 'placeholder' : 'Tree or plant name', 'id': 'item-detail-name'}),
            'description': forms.Textarea(attrs={'class': 'input textarea ', 'placeholder': 'What people will see when they scan the code. You could talk about the uses of this tree or plant - cultural, medicinal, religious, and more. You could also include interesting facts, like the history of this species or a story you have about this particular tree or plant. ', 'rows' : '5', 'cols': '50'}),
            'quantity': forms.NumberInput(attrs={'class': 'input ', 'placeholder': 'Number of these items in community', 'value': '1'}),
        }