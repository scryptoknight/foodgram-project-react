from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsOwnerOrReadOnly
from users.models import Follow
from users.serializers import (FollowReadSerializer, FollowSerializer,
                               UserSerializer)

User = get_user_model()


class FollowReadViewSet(ReadOnlyModelViewSet):
    serializer_class = FollowReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = User.ext_objects.follow_recipes(user=self.request.user).all()
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class AuthorViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, author_id):
        user = request.user
        data = {
            'user': user.id,
            'author': author_id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        user = request.user
        follow = get_object_or_404(
            Follow, user_id=user.id, author_id=author_id
        )
        follow.delete()
        return Response('Вы успешно отписаны',
                        status=status.HTTP_204_NO_CONTENT)
