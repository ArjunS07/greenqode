from django.db import models
from django import forms
from django.forms import ModelForm, TextInput
from .models import CommunityItem

class ItemForm(ModelForm):
    class Meta:
        model = CommunityItem
        labels = {
            'name': 'Name',
            'location' : 'Location',
            'description': 'Description',
            'quantity': 'Number of items',

        }
        # placeholders = {
        #     'name': ,
        #     'location' : 'Locations of item',
        #     'description': 'A description for people to see',
        #     'image': ''
        # }
        fields = ['name', 'location', 'description', 'quantity']
        # widgets = {

        #     'name': forms.TextInput(attrs={
        #         'class': 'col-xs-12 md-6 smallbox name form-control'
        #     }),
            
        #     'location': forms.TextInput(attrs={
        #         'class': 'col-xs-12 md-6 location smallbox form-control'
        #     }),
        #     'description': forms.TextInput(attrs= {
        #         'class': 'col-xs-12 description form-control'
        #     }),

        #     'image': forms.FileField(required=False, attrs = {
        #         'class': 'image-input form-control'
        #     })

        # }   

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Tree or plant name', 'id': 'item-detail-name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item location in community'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What people will see when they scan the code'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of these items in community', 'value': '1'}),
        }

#     name = forms.CharField(max_length=40, widget = forms.TextInput(attrs={
#         'class': 'col-sm-6 col-xs-12 form-small-text',
#         'placeholder': 'Tree or plant name',
#         'label': ''
#     }))
#     location = forms.CharField(max_length=40, widget = forms.TextInput(attrs={
#         'class': 'col-sm-6 col-xs-12 form-small-text',
#         'placeholder': 'Tree or plant name'
#     }))
#     description = forms.CharField(widget = forms.Textarea)
