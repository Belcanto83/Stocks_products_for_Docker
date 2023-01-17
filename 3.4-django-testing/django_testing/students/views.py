from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

    def partial_update(self, request, *args, **kwargs):
        """В настоящий момент HTTP-метод PATCH не поддерживается. Подробности смотри в serializers.py"""
        return Response({'detail': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)
