from datetime import timedelta
from django.core.exceptions import ValidationError


class CheckRelatedHabitReward:
    """
    Исключить одновременный выбор связанной привычки и указания вознаграждения.
    В модели не должно быть заполнено
    одновременно и поле вознаграждения,
    и поле связанной привычки.
    Можно заполнить только одно из двух полей.
    """

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        related_habit = value.get(self.related_habit)
        reward = value.get(self.reward)
        if not value['is_good']:
            if reward and related_habit:
                raise ValidationError('Должно быть заполнено только одно поле')

            if not reward and not related_habit:
                raise ValidationError('Должно быть заполнено хотя '
                                      'бы одно поле')
        # У приятной привычки не может быть
        # вознаграждения или связанной привычки.
        elif reward or related_habit:
            raise ValidationError(
                'У приятной привычки не может быть '
                'вознаграждения или связанной привычки')


def check_time_to_do(value):
    """
    Время выполнения должно быть не больше 120 секунд.
    """
    time_required = value.get('time_required')
    if time_required and time_required > timedelta(seconds=120):
        raise ValidationError('Время выполнения не может быть больше '
                              '120 секунд')


def check_related_habit_with_is_good(value):
    related_habit = value.get('related_habit')
    if related_habit and not related_habit.is_good:
        raise ValidationError('В связанные привычки могут попадать только '
                              'привычки с признаком приятной привычки.')


def habit_periodicity_validator(value):
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    periodicity = value.get('periodicity')
    if periodicity and periodicity > 7:
        raise ValidationError('Нельзя выполнять привычку реже,'
                              'чем 1 раз в 7 дней')
