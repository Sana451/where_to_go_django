from django.contrib import admin
from django.utils.html import format_html
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import PlaceImage, Place


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 3
    fields = ('image', 'preview')

    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            image_url = obj.image.url
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 50px; cursor: pointer;"/></a>',
                image_url, image_url
            )
        return ""

    preview.short_description = "Превью"


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'url', 'preview')
    search_fields = ('place__title',)

    def preview(self, obj):
        if obj.image:
            image_url = obj.image.url
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 50px; cursor: pointer;"/></a>',
                image_url, image_url
            )
        return ""

    preview.short_description = "Превью"


class PlaceAdminForm(forms.ModelForm):
    description_long = forms.CharField(
        widget=CKEditorWidget(),
        required=False
    )

    lat = forms.FloatField(required=False, label="Широта")
    lng = forms.FloatField(required=False, label="Долгота")

    class Meta:
        model = Place
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('lat')
        lng = cleaned_data.get('lng')
        if lat is not None and lng is not None:
            from django.contrib.gis.geos import Point
            cleaned_data['point'] = Point(lng, lat)  # порядок: x=lng, y=lat
        return cleaned_data


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):

    form = PlaceAdminForm
    list_display = ('title', 'id', 'description_short', 'lat', 'lng')
    search_fields = ('title',)

    inlines = [PlaceImageInline]  # в меню админки для создания этой модели сразу создавать к ней изображения
