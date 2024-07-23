from django import forms
from .models import Product, Version
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Название продукта содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание продукта содержит запрещенные слова.")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'release_date', 'description', 'version_name']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'


