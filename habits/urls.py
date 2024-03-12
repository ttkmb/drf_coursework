from django.urls import path
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, HabitPublicView, HabitPublicDetailView

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(r'', HabitViewSet, basename='habits')

urlpatterns = [
    path('public/', HabitPublicView.as_view(), name='list-public-habits'),
    path('public/<int:pk>/', HabitPublicDetailView.as_view(),
         name='detail-public-habit'),
              ]+router.urls
