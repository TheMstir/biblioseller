from django import forms
from .models import Library, LibImages, Money


class MoneyForm(forms.ModelForm):
    """форма добавления цифр на экран общей суммы"""
    class Meta:
        model = Money
        fields = ('now', )
        widgets = {
            'now': forms.NumberInput(),
             }

        def __init__(self, *args, **kwargs):
            super(Money, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.required = False



class LibImagesForm(forms.ModelForm):
    """Форма добавления дополнительного изображения"""
    class Meta:
        model = LibImages
        fields = ('name', 'image')


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(),
            'stock': forms.NumberInput(),
            'sale': forms.NumberInput(),
            'price': forms.NumberInput(),
            'in_pc_link': forms.TextInput(),
            'in_room_place': forms.TextInput(),
            'archived': forms.CheckboxInput(),
            'category': forms.Select(),
        }

        # Добавляем параметр required=False для каждого поля
        def __init__(self, *args, **kwargs):
            super(LibraryForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.required = False
