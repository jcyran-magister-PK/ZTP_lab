def build_product_payload(name: str = "TestProduct") -> dict:
    return {
        "name": name,
        "category_id": 1, 
        "price": 9.09,
        "stock": 10
    }

def test_post_products_creates_product_successfully(client):
    payload = build_product_payload()
    
    response = client.post("/api/v1/products", json=payload)
    
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]

def test_post_products_rejects_invalid_data(client):
    payload = build_product_payload()
    payload["price"] = "invalid_string_price" 
    
    response = client.post("/api/v1/products", json=payload)
    
    assert response.status_code == 422 

def test_put_products_updates_successfully(client):
    create_payload = build_product_payload()
    create_response = client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]
    
    update_payload = {
        "name": "Updated Product",
        "category_id": 2,
        "price": 14.00,
        "stock": 20
    }
    
    update_response = client.put(f"/api/v1/products/{product_id}", json=update_payload)
    
    assert update_response.status_code == 201
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Product"
    assert updated_data["price"] == 14.00

def test_get_product_history_records_changes(client):
    create_payload = build_product_payload()
    create_response = client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]
    
    update_payload = build_product_payload(name="History Test Update")
    update_response = client.put(f"/api/v1/products/{product_id}", json=update_payload)
    
    history_response = client.get(f"/api/v1/products/{product_id}/history")
    
    assert history_response.status_code == 200
    history = history_response.json()
    
    assert len(history) >= 2
    
    latest_entry = history[0]
    oldest_entry = history[-1]
    
    assert latest_entry["action"] in "update"
    assert latest_entry["current_state"]["name"] == "History Test Update"
    
    assert oldest_entry["action"] == "create"
    assert oldest_entry["previous_state"] == {}
