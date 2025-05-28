import requests


def add_role(role_name):
    """Add a role to the database"""
    url = "http://localhost:5000/roles"
    role_data = {
        "role_name": role_name
    }
    
    print(f"\nTesting adding role '{role_name}'...")
    response = requests.post(url, json=role_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

    return response.status_code == 200

if __name__ == "__main__":

    add_role("admin")
    add_role("teacher")
    add_role("student")
