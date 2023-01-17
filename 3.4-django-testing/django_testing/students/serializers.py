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
        students = validated_data.pop('students', None)
        course = super().update(instance, validated_data)
        if students:
            student_objs = [Student(**data) for data in students]
            course.students.set(student_objs)
        return course

    @staticmethod
    def validate_students(value):
        students_qty = len(value)
        if students_qty > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Q-ty {students_qty} of students per course must not be greater than '
                                  f'{settings.MAX_STUDENTS_PER_COURSE}!')
        return value
