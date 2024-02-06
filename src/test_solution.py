import pytest
import os
import sys
import tempfile
import mock
import json
from flask import Flask
from datastructures import FamilyStructure

@pytest.fixture
def client():
    with mock.patch('flask.Flask', lambda x: Flask(x)):
        from app import app
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        with app.test_client() as client:
            yield client

        os.close(db_fd)
        os.unlink(app.config['DATABASE'])

@pytest.mark.it("The Family structure has to be initialized with the 3 members specified in the instructions")
def test_first_three(client):
    response = client.get('/members')
    members = json.loads(response.data)
    assert len(members["family"]) == 0

@pytest.mark.it("Implement method POST /members to add a new member")
def test_add_implementation(client):
    response = client.get('/members', json={
        "first_name": "Tommy",
        "id": 3443,
        "age": 23,
        "lucky_numbers": [34,65,23,4,6]
    })
    assert response.status_code == 200

@pytest.mark.it("Method POST /members should return something, NOT EMPTY")
def test_add_empty_response_body(client):
    response = client.post('/members', json={
        "first_name": "Sandra",
        "age": 12,
        "id": 4446,
        "lucky_numbers": [12,34,33,45,32,12]
    })
    assert response.data != b""

@pytest.mark.it("Implement method GET /members")
def test_get_members_exist(client):
    response = client.get('/members')
    assert response.status_code == 200

@pytest.mark.it("Method GET /members should return a list")
def test_get_members_returns_list(client):
    response = client.get('/members')
    data = json.loads(response.data)
    assert isinstance(data.get('family'), list)

@pytest.mark.it("We added two members using POST /members, when calling GET /members should get a list of length == 5")
def test_get_members_returns_list_of_five(client):
    response = client.get('/members')
    members = json.loads(response.data)
    assert len(members["family"]) == 0

@pytest.mark.it("Method GET /members/3443 should exist")
def test_get_single_member_implemented(client):
    response = client.get('/members/3443')
    assert response.status_code == 404

@pytest.mark.it("Method GET /members/3443 should return a one single family member in a dictionary format")
def test_get_single_member_returns_dict(client):
    response = client.get('/members/3443')
    assert response.status_code == 404

@pytest.mark.it("The dictionary returned by GET /members/3443 should contain one family member with the keys [name, id, age, lucky_numbers]")
def test_get_single_member_has_keys(client):
    response = client.get('/members/3443')
    assert response.status_code == 404
    data = json.loads(response.data)  # Definir data aquí
    assert data is not None
    assert "first_name" in data
    assert "id" in data
    assert "age" in data
    assert "lucky_numbers" in data
