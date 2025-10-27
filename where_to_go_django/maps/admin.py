from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


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


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description_short', 'lat', 'lng')
    search_fields = ('title',)

    inlines = [PlaceImageInline]  # в меню админки для создания этой модели сразу создавать к ней изображения
