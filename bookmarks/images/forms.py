from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description', 'user')
        widgets = {'url': forms.HiddenInput,
                   'user': forms.HiddenInput}


    def clean_url(self):
        #Проверка значения поля url
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL does not match valid image extensions")
        return url

    #Переопределение метода save
    def save(self, force_insert=False, force_update=False, commit=True):
        #Создание объекта image
        image = super(ImageCreateForm, self).save(commit=True)
        #получаем URL из атрибута cleaned_data формы
        image_url = self.cleaned_data['url']
        #генерируем название изображения, совмещая слаг и расширение картинки
        image_name = '{} {}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())
        #Скачаиваем изображение по указанному адресу
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
