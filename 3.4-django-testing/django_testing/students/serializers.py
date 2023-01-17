from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "birth_date"]


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def create(self, validated_data):
        students = validated_data.pop('students', None)
        course = super().create(validated_data)
        if students:
            student_objs = [Student(**data) for data in students]
            Student.objects.bulk_create(student_objs)
            course.students.add(*student_objs)
        return course

    def update(self, instance, validated_data):
        """
        В настоящий момент данный метод адаптирован под HTTP-запрос PUT.
        PATCH запрос возможен, но под PATCH запрос данный метод не адаптирован,
        т.к. ВСЕ старые студенты обновляемого курса удаляются
        и сразу же создаются ВСЕ новые студенты курса, согласно параметрам запроса
        """
        students = validated_data.pop('students', None)
        course = super().update(instance, validated_data)
        if students:
            student_objs = [Student(**data) for data in students]
            # Удаляем сразу ВСЕХ старых студентов курса
            Student.objects.filter(id__in=[student.id for student in course.students.all()]).delete()
            # Создаем сразу ВСЕХ новых студентов курса
            new_students = Student.objects.bulk_create(student_objs)
            course.students.set(new_students, clear=True)
        return course

    @staticmethod
    def validate_students(value):
        students_qty = len(value)
        if students_qty > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Q-ty {students_qty} of students per course must not be greater than '
                                  f'{settings.MAX_STUDENTS_PER_COURSE}!')
        return value
