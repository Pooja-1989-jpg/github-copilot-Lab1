import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_and_unregister():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: Sign up
    response_signup = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Signup successful
    assert response_signup.status_code == 200
    assert f"Signed up {email}" in response_signup.json()["message"]

    # Act: Unregister
    response_unregister = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert: Unregister successful
    assert response_unregister.status_code == 200
    assert f"Unregistered {email}" in response_unregister.json()["message"]

    # Act: Unregister again (should fail)
    response_unregister_again = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert: Should return error
    assert response_unregister_again.status_code == 400
    assert "Student not registered" in response_unregister_again.json()["detail"]

    # Act: Sign up again
    response_signup_again = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Signup successful
    assert response_signup_again.status_code == 200
    assert f"Signed up {email}" in response_signup_again.json()["message"]

    # Act: Sign up duplicate (should fail)
    response_signup_duplicate = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Should return error
    assert response_signup_duplicate.status_code == 400
    assert "Student already signed up" in response_signup_duplicate.json()["detail"]
