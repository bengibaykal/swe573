import json
import django
import django_jsonforms
from django import forms
from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField
from django.contrib.postgres.fields import JSONField

from .models import Post2, Community, DataType, DataTypeObject, Field

class PostForm(forms.ModelForm):

    class Meta:
        model = Post2
        fields = ('title', 'content', 'draft')

class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'summary', 'image')

class DataTypeForm(forms.ModelForm):

    class Meta:
        model = DataType
        fields = ('name', 'community', 'extra_fields')



class CustomForm(forms.Form):
    data_type_name = {
        "type": "object",
        "required": ["Data Type Name"],
        "properties": {
            "Data Type Name": {
                "type": "string",
                "maxLength": 30
            }
        }
    }

    data_type_type = {
        "type": "object",
        "required": ["Data Type Type"],
        "properties": {
            "Data Type Type": {
                "type": "string",
                "enum": ["Sting", "Boolean", "Integer"],
                "maxLength": 30,
            }
        }
    }

    is_required = {
        "type": "object",
        "required": ["Is Required?"],
        "properties": {
            "Is Required?": {
                "type": "boolean",
            }
        }
    }

    data_type_schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Community",
        "type": "object",
        "properties": {
            "Data Field Name": {
                "type": "string",
            },
            "Data Field Type": {
                "type": "string",
                "enum": ["String", "Integer", "Boolean", "Image"]
            },
            "is required": {
                "type": "string",
                "enum": ["True", "False"]

            }

        }
    }

    options =  {
        "format":"html",
        "wysiwyg": True,
        "no_additional_properties": True,
        "disable_collapse": False,
        "disable_edit_json": False,
        "disable_properties": False,
}
    data_type = JSONSchemaField(schema=data_type_schema, options=options)
    #data_type_name = JSONSchemaField(schema = data_type_name, options = options)
    #data_type_type = JSONSchemaField(schema=data_type_type, options=options)
    #is_required = JSONSchemaField(schema=is_required, options=options)



#TODO: Create dynamic field
#######create dynamic field#######

class DataTypeForm2(forms.ModelForm):

    class Meta:
        model = DataType
        fields = ('name', 'extra_fields')

class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = ('name', 'field_type', 'required', 'community', 'data_type')

class PostTypeForm(forms.Form):

    FieldName = forms.CharField(max_length=200, required=True),


