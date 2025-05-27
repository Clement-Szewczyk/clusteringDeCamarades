import requests

# Test single student creation
def test_add_single_student():
    url = "http://localhost:5000/students"
    data = {"email": "student@example.com"}
    
    print("Testing single student creation...")
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    
    try:
        print(f"Response JSON: {response.json()}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")
    
    return response.json().get('id') if response.status_code == 201 else None

# Test batch student creation
def test_add_multiple_students():
    url = "http://localhost:5000/students/batch"
    data = [
        {"email": "student1@example.com"},
        {"email": "student2@example.com"},
        {"email": "invalid-email"},  # Should fail validation
        {"email": "student3@example.com"}
    ]
    
    print("\nTesting batch student creation...")
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    
    try:
        print(f"Response JSON: {response.json()}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")

# Test retrieving all students
def test_get_all_students():
    url = "http://localhost:5000/students"
    
    print("\nTesting get all students...")
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    
    try:
        students = response.json()
        print(f"Number of students retrieved: {len(students)}")
        if students:
            print("First few students:")
            for student in students[:3]:
                print(f"  - {student}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")
    
    return students[0]['id'] if students and len(students) > 0 else None

# Test updating a student
def test_update_student(student_id):
    if not student_id:
        print("\nSkipping update test - no student ID available")
        return
    
    url = f"http://localhost:5000/students/{student_id}"
    data = {"email": f"updated{student_id}@example.com"}
    
    print(f"\nTesting student update for ID {student_id}...")
    response = requests.put(url, json=data)
    print(f"Status code: {response.status_code}")
    
    try:
        print(f"Response JSON: {response.json()}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")

# Test deleting a student
def test_delete_student():
    # First create a student to delete
    url = "http://localhost:5000/students"
    data = {"email": "to-be-deleted@example.com"}
    
    print("\nCreating a student to delete...")
    response = requests.post(url, json=data)
    
    student_id = None
    if response.status_code == 201:
        try:
            student_id = response.json().get('id')
            print(f"Created student with ID {student_id}")
        except:
            print("Failed to get student ID from response")
            return
    else:
        print(f"Failed to create student - Status code: {response.status_code}")
        return
    
    # Now delete the student
    delete_url = f"http://localhost:5000/students/{student_id}"
    print(f"\nTesting student deletion for ID {student_id}...")
    delete_response = requests.delete(delete_url)
    print(f"Delete status code: {delete_response.status_code}")
    
    if delete_response.status_code == 204:
        print("Student deleted successfully (204 No Content)")
    else:
        try:
            print(f"Response JSON: {delete_response.json()}")
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response text: {delete_response.text}")
    
    # Verify deletion by trying to retrieve the student
    get_response = requests.get(delete_url)
    if get_response.status_code == 404:
        print("Verification successful: Student no longer exists (404 Not Found)")
    else:
        print(f"Verification failed - Status code: {get_response.status_code}")

if __name__ == "__main__":
    created_id = test_add_single_student()
    test_add_multiple_students()
    existing_id = test_get_all_students()
    
    # Use an existing ID for update test
    test_update_student(existing_id or created_id)
    
    # Test deletion
    test_delete_student()