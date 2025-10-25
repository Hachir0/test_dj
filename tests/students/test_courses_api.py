import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from students.models import Course, Student
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user("admin")


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_courses(client, user, course_factory):

    courses = course_factory(_quantity=10)


    response = client.get("/api/v1/courses/")
    data = response.json()

    assert len(data) == len(courses)
    assert response.status_code == 200

    for i, course in enumerate(data):
        assert course["name"] == courses[i].name




@pytest.mark.django_db
def test_post_courses(client, user):
    cnt = Course.objects.count()

    response = client.post("/api/v1/courses/",
                           data={"name": "Python"} )

    # response = client.get("/api/v1/courses/")

    assert response.status_code == 201
    assert Course.objects.count() == cnt + 1
