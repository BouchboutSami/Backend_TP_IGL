from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_annonce_info_by_id():
    response = client.get("/annonce/24")
    assert response.status_code == 200
    assert response.json() == [24,   "loca",   "f4",   150,   "ffff",   100,   10,   "ainoussara",   "ff",   "ddd",   "ddd",   "dd",   "2022-12-28"  ]

def test_messages_utilisateur():
    response = client.get("/message/0")
    assert response.status_code == 200
    assert response.json() == [   [     10,     4,     0,     "string",     "2022-12-30T22:33:24",     0   ],   [     9,     3,     0,     "string",     "2022-12-30T22:33:20",     0   ],   [     8,     2,     0,     "string",     "2022-12-30T22:33:16",     0   ],   [     7,     1,     0,     "string",     "2022-12-30T22:33:09",     0   ] ]

def test_annonces_by_mot_cle():
    response = client.get("/annonces_motcle/loca")
    assert response.status_code == 200
    assert response.json() == [   [     24,     "loca",     "f4",     150,     "ffff",     100,     10,     "ainoussara",     "ff",     "ddd",     "ddd",     "dd",     "2022-12-28"   ] ]