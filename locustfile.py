from locust import HttpUser, task, between, TaskSet
from requests.auth import HTTPBasicAuth

class ThingsBehavior(TaskSet):
    def on_start(self) -> None:
        login_url = "/api/users/login"
        username = "admin"
        password = "admin"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = self.client.post(login_url, auth=HTTPBasicAuth(username, password), headers=headers)
        if response.status_code == 200:
            self.token = response.json().get("tokenValue")
            self.item_id = None
        else:
            print("Login failed:", response.text)
            self.token = None
            self.item_id = None

    @task
    def health_check(self):
        with self.client.get("/", name="health_check", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Failed to get health check")

    @task(1)
    def get_all_things(self):
        if not self.item_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            with self.client.get(
                "/api/things",
                headers=headers,
                catch_response=True,
            ) as response:
                if response.status_code != 200:
                    response.failure("Failed to get things")
                else: 
                    items = response.json().get("items")
                    if items:
                        self.item_id = items[0].get("id")
                    else:
                        print("Failed to get items:", response.text)
                        self.item_id = None

    @task(2)
    def create_things(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        with self.client.post(
            "/api/things",
            headers=headers,
            json={"title": "Thing"},
            name="create_thing",
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure("Failed to create thing")
            else:
                self.get_all_things()
    
    @task(2)
    def get_thing(self):
        if self.item_id:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            with self.client.get(
                f"/api/things/{self.item_id}",
                headers=headers,
                catch_response=True,
            ) as response:
                if response.status_code != 200:
                    response.failure("Failed to get thing")

    @task(2)
    def delete_thing(self):
        if self.item_id:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            with self.client.delete(
                f"/api/things/{self.item_id}",
                headers=headers,
                catch_response=True,
            ) as response:
                if response.status_code != 204:
                    response.failure("Failed to delete thing")
                else:
                    self.item_id = None

    @task(2)
    def update_thing(self):
        if self.item_id:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            with self.client.put(
                f"/api/things/{self.item_id}",
                headers=headers,
                json={"title": "Updated Thing"},
                name="update_thing",
                catch_response=True
            ) as response:
                if response.status_code != 200:
                    response.failure("Failed to update thing")

class APIUser(HttpUser):
    tasks = [ThingsBehavior]
    wait_time = between(1, 5)