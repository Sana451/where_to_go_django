import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point
from maps.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Load place data from JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL to JSON file')

    def handle(self, *args, **options):
        json_url = options['json_url']

        try:
            response = requests.get(json_url)
            response.raise_for_status()
            place_data = response.json()

            place, created = Place.objects.get_or_create(
                title=place_data['title'],
                defaults={
                    'description_short': place_data.get('description_short', ''),
                    'description_long': place_data.get('description_long', ''),
                    'point': Point(
                        place_data['coordinates']['lng'],
                        place_data['coordinates']['lat']
                    )
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created place: {place.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Place already exists: {place.title}')
                )

            for img_url in place_data.get('imgs', []):
                self.load_image(place, img_url)

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching JSON from {json_url}: {e}')
            )
        except KeyError as e:
            self.stdout.write(
                self.style.ERROR(f'Missing required field in JSON: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )

    def load_image(self, place, img_url):
        """Загружает изображение по URL и связывает с местом"""
        try:
            response = requests.get(img_url)
            response.raise_for_status()

            # Получаем имя файла из URL
            filename = img_url.split('/')[-1]

            # Создаем объект изображения
            place_image = PlaceImage(place=place)
            place_image.image.save(
                filename,
                ContentFile(response.content),
                save=True
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded image: {filename}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading image {img_url}: {e}')
            )