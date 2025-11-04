import json
import random

from django.views import View
from django.http import Http404, JsonResponse
from django.shortcuts import render
from faker import Faker

from .models import Place


def index(request):
    places = Place.objects.all().prefetch_related('images')
    places_data = [place.to_dict() for place in places]

    context = {
        'places_data': json.dumps(places_data)
    }

    return render(request, template_name="maps/index.html", context=context)


def place_detail(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise Http404("Place not found")

    return JsonResponse(place.to_dict(), json_dumps_params={'ensure_ascii': False})


class RandomPlaceView(View):
    def get(self, request):
        fake = Faker('ru_RU')

        # Генерируем полностью случайные данные
        random_data = {
            "title": self.generate_title(fake),
            "imgs": self.generate_image_urls(),
            "description_short": self.generate_short_description(fake),
            "description_long": self.generate_long_description(fake),
            "coordinates": self.generate_moscow_coordinates()
        }

        return JsonResponse(
            random_data,
            json_dumps_params={'ensure_ascii': False, 'indent': 2}
        )

    def generate_title(self, fake):
        prefixes = ["Экскурсионная компания", "Музей", "Парк", "Галерея", "Исторический центр"]
        names = [
            "«Легенды Москвы»", "«Московские истории»", "«Старая Москва»",
            "«Арт-пространство»", "«Культурный код»", "«Наследие»"
        ]
        return f"{random.choice(prefixes)} {random.choice(names)}"

    def generate_image_urls(self):
        base_urls = [
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/4f793576c79c1cbe68b73800ae06f06f.jpg",
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/7a7631bab8af3e340993a6fb1ded3e73.jpg",
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/a55cbc706d764c1764dfccf832d50541.jpg",
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/65153b5c595345713f812d1329457b54.jpg",
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/0a79676b3d5e3b394717b4bf2e610a57.jpg",
            "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1e27f507cb72e76b604adbe5e7b5f315.jpg"
        ]
        return random.sample(base_urls, random.randint(3, 6))

    def generate_short_description(self, fake):
        templates = [
            "Неважно, живёте ли вы в Москве всю жизнь или впервые оказались в столице, {}",
            "Уникальное место, которое {}",
            "Одно из самых популярных мест, где {}",
            "Идеальное место для тех, кто {}"
        ]

        fillers = [
            "хочет познакомиться с богатой историей города",
            "ищет вдохновение и новые впечатления",
            "ценит архитектуру и культурное наследие",
            "хочет провести время с пользой и удовольствием"
        ]

        return random.choice(templates).format(random.choice(fillers))

    def generate_long_description(self, fake):
        paragraphs = [
            f"<p>{fake.paragraph()}</p>",
            f"<p>{fake.paragraph()}</p>",
            f"<p>Подробности узнавайте <a class=\"external-link\" href=\"https://example.com\" target=\"_blank\">на сайте</a>.</p>",
            f"<p>За обновлениями удобно следить <a class=\"external-link\" href=\"https://vk.com/example\" target=\"_blank\">«ВКонтакте»</a>.</p>"
        ]

        return "".join(random.sample(paragraphs, random.randint(2, 4)))

    def generate_moscow_coordinates(self):
        return {
            "lng": round(random.uniform(37.37, 37.85), 6),
            "lat": round(random.uniform(55.57, 55.90), 6)
        }
