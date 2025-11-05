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
def test_create_first_course(client, course_factory, user):
    response = client.post("/api/v1/courses/", data={"name": "Python course" })
    assert response.status_code == 201
    assert response.data["name"] == "Python course"

@pytest.mark.django_db
def test_get_courses_list(client, user, course_factory):

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
    data = response.json()

    assert response.status_code == 201
    assert Course.objects.count() == cnt + 1
    assert data["name"] == "Python"

@pytest.mark.django_db
def test_filter_id_courses(client, user, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get("/api/v1/courses/?id=1")
    data = response.json()

    assert len(data) == 1
    assert response.status_code == 200

    for i, course in enumerate(data):
        assert course["id"] == courses[i].id

@pytest.mark.django_db
def test_filter_name_courses(client, user, course_factory):
    course_factory(name="Python course")

    response = client.get("/api/v1/courses/?name=Python course")
    data = response.json()

    assert len(data) == 1
    assert response.status_code == 200
    assert data[0]["name"] == "Python course"

@pytest.mark.django_db
def test_update_courses(client, user, course_factory):
    course = course_factory(name="Python course")

    response = client.put(f"/api/v1/courses/{course.id}/", data={"name": "Python"})

    assert response.status_code == 200
    assert response.data["name"] == "Python"

@pytest.mark.django_db
def test_delete_courses(client, user, course_factory):
    course = course_factory(name="Python course")

    response = client.delete(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 204