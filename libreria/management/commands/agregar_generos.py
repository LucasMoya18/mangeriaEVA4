import requests
from django.core.management.base import BaseCommand
from libreria.models import Genero

class Command(BaseCommand):
    help = 'Popula la base de datos con los géneros de la API de Jikan'

    def handle(self, *args, **kwargs):
        # Obtener los géneros desde la API de Jikan
        response = requests.get('https://api.jikan.moe/v4/genres/manga')
        genres_data = response.json()['data']

        # Crear los géneros en la base de datos
        for genre in genres_data:
            name = genre['name']

            # Verifica si el género ya existe para no crear duplicados
            if not Genero.objects.filter(nombre=name).exists():
                Genero.objects.create(nombre=name)  # Solo usar el nombre
                self.stdout.write(self.style.SUCCESS(f'Género "{name}" creado exitosamente'))
            else:
                self.stdout.write(self.style.SUCCESS(f'El género "{name}" ya existe'))

        self.stdout.write(self.style.SUCCESS('Todos los géneros han sido importados'))
