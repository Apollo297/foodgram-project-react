import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Ingredient'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Ingredient "{row[0]}" created'
                        )
                    )
                else:
                    self.stdout.write(f'Ingredient "{row[0]}" already exists')
