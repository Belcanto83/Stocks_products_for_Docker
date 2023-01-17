import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=5)
    course = course_factory(students=students)

    # Action
    url = reverse('courses-detail', args=[course.pk])
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resp_json = response.json()
    assert resp_json['name'] == course.name
    assert course.students.count() == 5
    for ind, student in enumerate(resp_json['students']):
        assert student['name'] == students[ind].name


@pytest.mark.django_db
def test_list_course(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Action
    url = reverse('courses-list')
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resp_json = response.json()
    for ind, course in enumerate(courses):
        assert resp_json[ind]['name'] == course.name


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course = courses[3]

    # Action
    url = reverse('courses-list')
    response = api_client.get(url, data={'id': course.pk})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resp_json = response.json()
    assert resp_json[0]['id'] == course.pk


@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_name = courses[3].name

    # Action
    url = reverse('courses-list')
    response = api_client.get(url, data={'name': course_name})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resp_json = response.json()
    for course in resp_json:
        assert course['name'] == course_name


@pytest.mark.django_db
def test_create_course_success(api_client, settings):
    # Arrange
    courses_count = Course.objects.count()
    students_count = Student.objects.count()
    students = [
            {'name': 'Inna'},
            {'name': 'Ivan'},
        ]
    settings.MAX_STUDENTS_PER_COURSE = 2

    # Action
    url = reverse('courses-list')
    response = api_client.post(url, data={
        'name': 'Python',
        'students': students
    }
                               )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == courses_count + 1
    resp_json = response.json()
    assert resp_json['name'] == 'Python'
    assert Student.objects.count() == students_count + 2
    students_iter = iter(students)
    for student in Student.objects.all():
        assert student.name == next(students_iter)['name']


@pytest.mark.django_db
def test_create_course_failure(api_client, settings):
    # Arrange
    count = Course.objects.count()
    settings.MAX_STUDENTS_PER_COURSE = 2

    # Action
    url = reverse('courses-list')
    response = api_client.post(url, data={
        'name': 'Python',
        'students': [
            {'name': 'Inna'},
            {'name': 'Ivan'},
            {'name': 'Sveta'}
        ]
    }
                               )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Course.objects.count() == count


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    courses = course_factory(_quantity=1)
    course = courses[0]

    url = reverse('courses-detail', args=[course.pk])
    response = api_client.put(url, data={'name': 'Python', 'students': []})

    assert response.status_code == status.HTTP_200_OK
    obj = Course.objects.get(pk=course.pk)
    assert obj.name == 'Python'
    resp_json = response.json()
    assert resp_json['name'] == 'Python'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    courses = course_factory(_quantity=1)
    course = courses[0]
    count = Course.objects.count()

    print(course.students)

    url = reverse('courses-detail', args=[course.pk])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == count - 1
    try:
        obj = Course.objects.get(pk=course.pk)
    except:
        obj = None
    assert obj is None
