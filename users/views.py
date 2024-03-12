from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        password = serializer.validated_data.get('password')
        user = get_user_model().objects.get(id=serializer.data.get('id'))
        user.set_password(password)
        user.is_active = True
        user.save()
        return Response(
            status=Response.status_code,
            headers=headers,
            data=UserSerializer(user).data
        )
