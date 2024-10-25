import csv
from django.core.management.base import BaseCommand
from main.models import Product 

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Product.objects.create(
                    name=row['name'],
                    kategori=row['kategori'],
                    harga=row['harga'],
                    toko=row['toko'],
                    alamat=row['alamat'],
                    kontak=row['kontak'],
                    gambar=row['path-gambar']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
