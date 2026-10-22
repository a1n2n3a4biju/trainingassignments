from urllib import response

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_reports():
    #Act
    response = client.get("/reports")
    #Assert
    assert response.status_code == 200



def test_add_report():
    response = client.post(
        "/reports",
        json={
            "id": 1,
            "title": "Prepare Report",
            "status": "Pending"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Prepare Report"
    assert data["status"] == "Pending"

def test_get_reports_after_add():
    client.post(
        "/reports",
        json={
            "id": 2,
            "title": "Review Invoice",
            "status": "Completed"
        }
    )

    response = client.get("/reports")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_reports_after_add_after_add():
    client.post(
        "/reports",
        json={
            "id": 3,
            "title": "Update Dashboard",
            "status": "Pending"
        }
    )

    response = client.get("/reports")

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_reports_id():
    #Act
    response = client.get("/reports/1")
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_notexist_reports_id():
    #Act
    response = client.get("/reports/999")
    #Assert
    assert response.status_code == 404

def test_get_reports_add_after_add_after_add_after_add():
    response=client.post(
        "/reports",
        json={
            "id": 4,
          "title": "Check server logs",
          "status": "Pending"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "Check server logs"









def test_invalid_report():
    response = client.post(
        "/reports",
        json={
            "id": 3,
            "status": "Pending"
        }
    )

    assert response.status_code == 422

def test_put_report():
    #Act
    response = client.put(
        "/reports/2",
        json={
            "id": 2,
            "title": "Review Invoice",
        "status":"Pending"

        })
    #Assert
    assert response.status_code == 200

def test_delete_report():
    response = client.delete(
        "/reports/3")
    assert response.status_code == 200


def test_get_notexist_reports_id_after_delet():
    #Act
    response = client.get("/reports/3")
    #Assert
    assert response.status_code == 404