from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продуктов"""

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с добавлением CSS классов"""
        super().__init__(*args, **kwargs)

        # Добавляем CSS классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'is_published':  # Для checkbox особый стиль
                field.widget.attrs['class'] = 'form-control'

        # Особые настройки для отдельных полей
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-select'

        # Добавляем placeholder'ы
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название продукта'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание продукта'
        self.fields['price'].widget.attrs['placeholder'] = '0.00'

    def clean_name(self):
        """Валидация названия продукта на запрещенные слова"""
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(
                    f'Название продукта содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта на запрещенные слова"""
        description = self.cleaned_data.get('description', '').lower()

        if description:  # Проверяем только если описание не пустое
            for word in self.FORBIDDEN_WORDS:
                if word in description:
                    raise forms.ValidationError(
                        f'Описание продукта содержит запрещенное слово: "{word}"'
                    )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены продукта"""
        price = self.cleaned_data['price']

        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')

        if price == 0:
            raise forms.ValidationError('Цена не может быть нулевой')

        return price