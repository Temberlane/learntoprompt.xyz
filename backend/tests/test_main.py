def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_prompts_empty(client):
    response = client.get("/prompts")
    assert response.status_code == 200
    assert response.json() == []


def test_create_prompt(client):
    payload = {"title": "My first prompt", "content": "Tell me a joke."}
    response = client.post("/prompts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first prompt"
    assert data["content"] == "Tell me a joke."
    assert "id" in data
    assert "created_at" in data


def test_list_prompts_after_create(client):
    client.post("/prompts", json={"title": "Prompt A", "content": "Content A"})
    client.post("/prompts", json={"title": "Prompt B", "content": "Content B"})
    response = client.get("/prompts")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_prompt(client):
    created = client.post(
        "/prompts", json={"title": "Test", "content": "Test content"}
    ).json()
    prompt_id = created["id"]
    response = client.get(f"/prompts/{prompt_id}")
    assert response.status_code == 200
    assert response.json()["id"] == prompt_id


def test_get_prompt_not_found(client):
    response = client.get("/prompts/9999")
    assert response.status_code == 404
