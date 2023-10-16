import json

from django.core.management import BaseCommand
from recipes.models import Tag

from api_foodgram.settings import UPLOAD_FILES_DIR


class Command(BaseCommand):
    help = 'Загружает теги в базу данных из json файла'

    def handle(self, *args, **options):
        with open(
                f'{UPLOAD_FILES_DIR}/tags.json',
                encoding='utf-8'
        ) as json_file:
            json_data = json.load(json_file)

            tags = [
                Tag(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug']
                )
                for tag in json_data
            ]

            Tag.objects.bulk_create(tags)
