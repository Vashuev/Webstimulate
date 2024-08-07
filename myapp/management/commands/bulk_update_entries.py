import csv
from django.core.management.base import BaseCommand
from myapp.models import Entry

class Command(BaseCommand):
    help = 'Bulk update Entries from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to read data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry, created = Entry.objects.update_or_create(
                    name=row['Name'],
                    defaults={
                        'place': row['Place'],
                        'number': row['Number'],
                        'category': row['Category'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created entry: {entry.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated entry: {entry.name}'))
