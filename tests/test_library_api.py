# The pytest import is needed for test discovery, but we should use it
# to avoid linting errors by adding a pytest.mark or fixture
import pytest
from fastapi.testclient import TestClient
from typing import Any

# Type annotations to satisfy Pylance
@pytest.mark.usefixtures("client")
def test_create_library(client: TestClient) -> None:
    library_data = {
        "name": "Central Library",
        "location": "Downtown"
    }
    response = client.post("/library", json=library_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == library_data["name"]
    assert data["location"] == library_data["location"]
    assert "id" in data

def test_get_libraries(client: TestClient, sample_library: Any) -> None:
    response = client.get("/library")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Use a cast to explicitly tell the type checker what we know about the data
    from typing import cast
    libraries = cast(list[dict[str, Any]], data)
    assert len(libraries) >= 1

def test_get_library(client: TestClient, sample_library: Any) -> None:
    response = client.get(f"/library/{sample_library.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_library.id
    assert data["name"] == sample_library.name
    assert data["location"] == sample_library.location

def test_get_nonexistent_library(client: TestClient) -> None:
    response = client.get("/library/999999")
    assert response.status_code == 404









