import sys
import os

sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    with TestClient(app) as client:
        print("--- [TEST START] UAS Part 1 Verification ---")

        # 0. Health check
        res = client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("[OK] Health check passed.")

        # 1. Login as Admin
        res = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
        assert res.status_code == 200, f"Admin login failed: {res.text}"
        admin_data = res.json()
        admin_token = admin_data["access_token"]
        assert admin_data["user"]["role"] == "admin"
        print("[OK] Step 1: Log in as admin successful.")

        # 2. From admin account, create two new accounts: User A and User B
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        # User A
        res_a = client.post("/users", json={
            "username": "usera",
            "password": "usera123",
            "full_name": "User A (Trainer)",
            "role": "user"
        }, headers=admin_headers)
        if res_a.status_code == 400 and "sudah digunakan" in res_a.text:
            print("[INFO] User A already exists.")
        else:
            assert res_a.status_code == 201, f"Create User A failed: {res_a.text}"
            print("[OK] Created User A.")

        # User B
        res_b = client.post("/users", json={
            "username": "userb",
            "password": "userb123",
            "full_name": "User B (Staff)",
            "role": "user"
        }, headers=admin_headers)
        if res_b.status_code == 400 and "sudah digunakan" in res_b.text:
            print("[INFO] User B already exists.")
        else:
            assert res_b.status_code == 201, f"Create User B failed: {res_b.text}"
            print("[OK] Created User B.")

        # Verify non-admin CANNOT create accounts (Authorization check 1)
        res_fail = client.post("/users", json={
            "username": "attacker",
            "password": "password123",
            "full_name": "Attacker",
            "role": "user"
        })
        assert res_fail.status_code in [401, 403], "Unauthorized user was able to create account!"
        print("[OK] Authorization check 1 passed: Non-admin cannot create accounts.")

        # 3. Log out / Log in as User A
        res_login_a = client.post("/auth/login", json={"username": "usera", "password": "usera123"})
        assert res_login_a.status_code == 200, f"User A login failed: {res_login_a.text}"
        user_a_token = res_login_a.json()["access_token"]
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}
        print("[OK] Step 3: Log in as User A successful.")

        # 4. User A creates and updates their own data
        res_create_session = client.post("/sessions", json={
            "title": "Machine Learning Workshop by User A",
            "trainer": "User A",
            "department": "Engineering",
            "date": "2026-11-20",
            "duration_hours": 4,
            "capacity": 30,
            "status": "Scheduled"
        }, headers=user_a_headers)
        assert res_create_session.status_code == 201, f"User A create session failed: {res_create_session.text}"
        user_a_session_id = res_create_session.json()["id"]
        print(f"[OK] User A created session with ID {user_a_session_id}.")

        # User A updates their own session
        res_update_a = client.put(f"/sessions/{user_a_session_id}", json={
            "title": "Updated ML Workshop by User A",
            "duration_hours": 5
        }, headers=user_a_headers)
        assert res_update_a.status_code == 200, f"User A update session failed: {res_update_a.text}"
        assert res_update_a.json()["title"] == "Updated ML Workshop by User A"
        print("[OK] Step 4: User A successfully updated their own data.")

        # 5. Log in as User B
        res_login_b = client.post("/auth/login", json={"username": "userb", "password": "userb123"})
        assert res_login_b.status_code == 200, f"User B login failed: {res_login_b.text}"
        user_b_token = res_login_b.json()["access_token"]
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}
        print("[OK] Log in as User B successful.")

        # User B attempts to modify User A's session -> MUST be 403 Forbidden!
        res_attack_put = client.put(f"/sessions/{user_a_session_id}", json={
            "title": "Hacked by User B!"
        }, headers=user_b_headers)
        assert res_attack_put.status_code == 403, f"Expected 403 Forbidden, got {res_attack_put.status_code}: {res_attack_put.text}"
        print(f"[OK] Step 5: User B cannot modify User A's data (Got HTTP 403 Forbidden: {res_attack_put.json()['detail']}).")

        # User B attempts to delete User A's session -> MUST be 403 Forbidden!
        res_attack_del = client.delete(f"/sessions/{user_a_session_id}", headers=user_b_headers)
        assert res_attack_del.status_code == 403, f"Expected 403 Forbidden, got {res_attack_del.status_code}: {res_attack_del.text}"
        print(f"[OK] Step 5 (Bonus): User B cannot delete User A's data (Got HTTP 403 Forbidden: {res_attack_del.json()['detail']}).")

        print("--- [ALL TESTS PASSED SUCCESSFULLY!] ---")

if __name__ == "__main__":
    run_tests()
