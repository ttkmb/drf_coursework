from celery import shared_task
from django.contrib.auth import get_user_model

from habits.services import send_msg_tg


@shared_task
def habit_sender():
    users = get_user_model().objects.filter(
        is_active=True, telegram_id__isnull=False)
    for user in users:
        habits = user.user.all()
        for habit in habits:
            send_msg_tg(
                f'Привет, в {habit.time_to_do} на '
                f'{habit.place_to_do} нужно '
                f'{habit.action} за '
                f'{habit.time_required}!',
                user.telegram_id)
