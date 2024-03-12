from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from habits.models import Habit


class TestCrudHabit(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='testuser@mail.ru',
                                                    password='1234')
        self.user.save()
        self.client.force_authenticate(self.user)
        related_habit = Habit.objects.create(user=self.user,
                                             place_to_do='дома',
                                             time_to_do='20:00',
                                             action='читать книгу',
                                             is_good=True,
                                             periodicity=2,
                                             reward='посмотреть сериал',
                                             time_required='01:30',
                                             is_public=False)
        related_habit.save()

        self.data = {
            'place_to_do': 'улица',
            'time_to_do': '10:00',
            'action': 'поесть',
            'is_good': False,
            'periodicity': 1,
            'reward': 'выпить чай с лимоном',
            'time_required': '01:00',
            'is_public': True,
        }

        copy_data = self.data.copy()
        copy_data['is_good'] = True
        self.habit_no_is_pleasant = Habit.objects.create(**copy_data)
        self.habit_no_is_pleasant.save()
        self.count_habits = Habit.objects.count()

    def test_create_good(self):
        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), self.count_habits + 1)

    def test_create_habits_is_good(self):
        self.data['is_good'] = True
        self.data['reward'] = ''
        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), self.count_habits + 1)

    def test_create_habits_no_is_good_and_reward(self):
        self.data['is_good'] = False
        self.data['reward'] = '123'

        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), self.count_habits + 1)

    def test_create_validator_is_good_and_no_reward(self):
        self.data['is_good'] = True

        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'][0],
            'У приятной привычки не может '
            'быть вознаграждения или связанной привычки'
        )
        self.assertEqual(Habit.objects.count(), self.count_habits)

    def test_create_time_to_complete(self):
        self.data['time_required'] = 121

        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'][0],
            'Время выполнения не может быть больше 120 секунд'
        )
        self.assertEqual(Habit.objects.count(), self.count_habits)

    def test_create_save_owner(self):
        url = reverse('habits:habits-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), self.count_habits + 1)
        self.assertEqual(Habit.objects.last().user, self.user)
        self.assertEqual(response.data['user'], self.user.id)
