from rest_framework import serializers

from habits.models import Habit
from habits.validators import (CheckRelatedHabitReward,
                               check_time_to_do,
                               check_related_habit_with_is_good,
                               habit_periodicity_validator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            CheckRelatedHabitReward('related_habit', 'reward'),
            check_time_to_do,
            check_related_habit_with_is_good,
            habit_periodicity_validator,
        ]
