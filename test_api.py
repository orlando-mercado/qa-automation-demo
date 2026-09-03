import requests

BASE_URL = "https://dummyjson.com"

def test_get_products_list():
    resp = requests.get(f"{BASE_URL}/products", params={"limit": 10})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["products"]) > 0
    for p in data["products"]:
        assert "id" in p and "title" in p and "price" in p

def test_get_single_product():
    resp = requests.get(f"{BASE_URL}/products/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert isinstance(data["price"], (int, float))
    assert data["price"] > 0

def test_get_selected_fields_only():
    resp = requests.get(f"{BASE_URL}/products/1", params={"select": "title,price"})
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data and "price" in data
    assert "description" not in data
    assert "category" not in data

def test_search_product_by_title():
    resp = requests.get(f"{BASE_URL}/products/search", params={"q": "mascara"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert all("mascara" in p["title"].lower() for p in data["products"])

def test_create_product():
    payload = {"title": "test product", "price": 19.99}
    resp = requests.post(f"{BASE_URL}/products/add", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "test product"
    assert "id" in data

def test_update_product():
    resp = requests.put(f"{BASE_URL}/products/1", json={"title": "updated title"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "updated title"

def test_delete_product():
    resp = requests.delete(f"{BASE_URL}/products/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["isDeleted"] is True
    assert "deletedOn" in data

def test_get_nonexistent_product():
    resp = requests.get(f"{BASE_URL}/products/9999")
    # Check what dummyjson actually returns before asserting — some fake APIs
    # return 200 with an error message instead of a real 404. Assert on the
    # real observed behavior, not an assumption.
    assert resp.status_code in (404,)
    assert "message" in resp.json()