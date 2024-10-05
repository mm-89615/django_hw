import random

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


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
def test_get_first_course(api_client, course_factory):
    course = course_factory(_quantity=1)
    response = api_client.get(f"/api/v1/courses/{course[0].id}/")
    assert response.status_code == 200
    assert response.data["name"] == course[0].name


@pytest.mark.django_db
def test_get_list_of_courses(api_client, course_factory):
    courses = course_factory(_quantity=10)
    response = api_client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for idx, course in enumerate(data):
        assert course["name"] == courses[idx].name


@pytest.mark.django_db
def test_get_filtered_list_of_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=10)
    random_course_id = random.choice(courses).id
    response = api_client.get(f"/api/v1/courses/?id={random_course_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == random_course_id


@pytest.mark.django_db
def test_get_filtered_list_of_courses_by_name(api_client, course_factory):
    courses = course_factory(_quantity=10)
    random_course_name = random.choice(courses).name
    response = api_client.get(f"/api/v1/courses/?name={random_course_name}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == random_course_name


@pytest.mark.django_db
def test_create_new_course(api_client, course_factory, student_factory):
    course_name = "New course"
    students = student_factory(_quantity=3)
    response = api_client.post(
        "/api/v1/courses/",
        data={
            "name": course_name,
            "students": [student.id for student in students],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == course_name
    assert set(data["students"]) == set([student.id for student in students])


@pytest.mark.django_db
def test_update_course(api_client, course_factory,student_factory):
    course = course_factory(_quantity=1)
    new_name = "New updated course"
    students = student_factory(_quantity=3)
    response = api_client.patch(
        f"/api/v1/courses/{course[0].id}/",
        data={
            "name": new_name,
            "students": [student.id for student in students],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name
    assert set(data["students"]) == set([student.id for student in students])


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    courses = course_factory(_quantity=5)
    random_course_id = random.choice(courses).id
    response = api_client.delete(f"/api/v1/courses/{random_course_id}/")
    assert response.status_code == 204
    response = api_client.get(f"/api/v1/courses/{random_course_id}/")
    assert response.status_code == 404


