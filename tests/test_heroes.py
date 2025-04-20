from fastapi import status
from sqlmodel import select
from src.models.heroes import Hero


def test_create_hero(client, db_session):
    # given
    payload = {"name": "Iron Man", "secret_name": "Tony Stark"}
    # when
    response = client.post("/heroes", json=payload)
    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]
    # Verify persisted
    hero_in_db = db_session.exec(
        select(Hero).where(Hero.id == data["id"])
    ).one()
    assert hero_in_db.name == "Iron Man"


def test_read_hero(client, db_session):
    # given
    hero = Hero(name="Hulk", secret_name="Bruce Banner")
    db_session.add(hero)
    db_session.commit()
    db_session.refresh(hero)
    # when
    response = client.get(f"/heroes/{hero.id}")
    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == hero.id


def test_read_hero_not_found(client):
    # when
    response = client.get("/heroes/9999")
    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_hero(client, db_session):
    # given
    hero = Hero(name="Thor", secret_name="Thor Odinson", age=25)
    db_session.add(hero)
    db_session.commit()
    db_session.refresh(hero)
    update_payload = {"name": "Thor, God of Thunder"}
    # when
    response = client.patch(f"/heroes/{hero.id}", json=update_payload)
    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data['age'] == 25 # unchanged
    # Verify in DB
    updated = db_session.get(Hero, hero.id)
    assert updated.name == update_payload["name"]


def test_update_hero_not_found(client):
    # given
    payload = {"name": "Doesn't Matter"}
    # when
    response = client.patch("/heroes/9999", json=payload)
    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Hero not found"


def test_delete_hero(client, db_session):
    # given
    hero = Hero(name="Black Widow", secret_name="Natasha Romanoff")
    db_session.add(hero)
    db_session.commit()
    db_session.refresh(hero)
    # when
    response = client.delete(f"/heroes/{hero.id}")
    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ok": True}
    # Verify deletion
    assert db_session.get(Hero, hero.id) is None


def test_delete_hero_not_found(client):
    # when
    response = client.delete("/heroes/9999")
    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Hero not found"


