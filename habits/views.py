from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import DefaultPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner, CanSeePublic
from habits.tasks import habit_sender


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = DefaultPagination

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def send_habits(self, request, *args, **kwargs):
        habits = habit_sender()
        return Response({'habits': habits})


class HabitPublicView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, CanSeePublic]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitPublicDetailView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, CanSeePublic]
