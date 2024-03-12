from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = get_user_model().objects.create(email='admin@mail.com', is_staff=True,
                                               is_superuser=True)
        user.set_password('admin')
        user.save()
