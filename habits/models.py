from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='user', null=True, blank=True)
    place_to_do = models.CharField(max_length=255, verbose_name='Место',
                                   null=True, blank=True)
    time_to_do = models.TimeField(verbose_name='Время',
                                  null=True, blank=True)
    action = models.CharField(max_length=255, verbose_name='Действие',
                              null=True, blank=True)  # Действие
    is_good = models.BooleanField(verbose_name='Признак приятной привычки',
                                  null=True, blank=True,
                                  default=None)  # Признак приятной привычки
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE,
                                      null=True, blank=True,
                                      related_name='other_habit',
                                      verbose_name='Связанная привычка')
    periodicity = models.IntegerField(verbose_name='Периодичность', default=1)
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение',
                              null=True, blank=True)
    time_required = models.DurationField(verbose_name='Время на выполнение',
                                         null=True,
                                         blank=True)
    is_public = models.BooleanField(verbose_name='Признак публичности',
                                    default=False)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
