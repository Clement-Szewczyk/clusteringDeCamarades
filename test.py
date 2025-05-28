import requests
from datetime import datetime, timedelta
import os
import sys
import json
import time
import random

# Add the backend/src directory to the Python path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Configuration
API_BASE_URL = "http://localhost:5000"

# Variables for storing important IDs and tokens between tests
student_id = None
teacher_id = None
auth_token = None
formular_id = None

# Configuration globale pour la génération de données de test
NUM_STUDENTS = 30  # Nombre d'étudiants à créer
VOTES_PER_STUDENT = 15  # Nombre moyen de votes par étudiant

# Liste pour stocker les IDs des étudiants créés
student_ids = []

def print_header(title):
    """Print a formatted header for test sections"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_test_result(name, success, details=None):
    """Print formatted test results"""
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"{status} - {name}")
    if details and not success:
        print(f"    Details: {details}")

def test_roles():
    """Test role functionality"""
    print_header("TESTING ROLES")
    
    # Create roles
    roles = ["admin", "teacher", "student"]
    results = []
    
    for role in roles:
        url = f"{API_BASE_URL}/roles"
        role_data = {"role_name": role}
        
        print(f"\nCreating role '{role}'...")
        try:
            response = requests.post(url, json=role_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            success = response.status_code in [201, 409]  # 201=Created, 409=Already exists
            results.append(success)
            print_test_result(f"Create role '{role}'", success)
        except Exception as e:
            print(f"Error creating role: {e}")
            results.append(False)
            print_test_result(f"Create role '{role}'", False, str(e))
    
    # List roles
    try:
        response = requests.get(f"{API_BASE_URL}/roles")
        print(f"\nListing all roles - Status: {response.status_code}")
        roles_data = response.json()
        print(f"Found {len(roles_data)} roles: {roles_data}")
        success = response.status_code == 200 and len(roles_data) >= 3
        results.append(success)
        print_test_result("List all roles", success)
    except Exception as e:
        print(f"Error listing roles: {e}")
        results.append(False)
        print_test_result("List all roles", False, str(e))
    
    return all(results)

def generate_test_data():
    """Génère un grand nombre d'étudiants et de votes pour tester l'algorithme de clustering"""
    print_header("GÉNÉRATION DE DONNÉES DE TEST")
    
    # Créer d'abord le formulaire
    if not test_auth() or not test_formulars():
        print("❌ Échec lors de la création du formulaire. Impossible de continuer.")
        return False
    
    # Créer ensuite de nombreux étudiants
    create_multiple_students()
    
    # Finalement, créer de nombreux votes entre les étudiants
    create_multiple_votes()
    
    print_header("DONNÉES DE TEST GÉNÉRÉES AVEC SUCCÈS")
    print(f"✅ {len(student_ids)} étudiants créés")
    print(f"✅ ~{len(student_ids) * VOTES_PER_STUDENT} votes créés")
    return True

def create_multiple_students():
    """Crée un grand nombre d'étudiants pour les tests"""
    global student_ids
    print_header(f"CRÉATION DE {NUM_STUDENTS} ÉTUDIANTS")
    
    student_ids = []
    
    for i in range(NUM_STUDENTS):
        # Génération d'un email avec un timestamp pour éviter les doublons
        student_email = f"student_{int(time.time())}_{i}@example.com"
        url = f"{API_BASE_URL}/students"
        student_data = {"email": student_email}
        
        try:
            response = requests.post(url, json=student_data)
            if response.status_code == 201:
                new_id = response.json().get("student_id")
                student_ids.append(new_id)
                print(f"✅ Étudiant créé: {student_email} (ID: {new_id})")
            else:
                print(f"❌ Échec création étudiant {student_email}: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'étudiant {i}: {str(e)}")
    
    print(f"\nTotal étudiants créés: {len(student_ids)}/{NUM_STUDENTS}")
    return len(student_ids) > 0

def create_multiple_votes():
    """Crée un grand nombre de votes entre les étudiants"""
    global formular_id, student_ids
    print_header("CRÉATION DE VOTES MULTIPLES")
    
    if not formular_id or not student_ids:
        print("❌ Pas de formulaire ou d'étudiants disponibles. Impossible de créer des votes.")
        return False
    
    votes_created = 0
    total_votes = len(student_ids) * VOTES_PER_STUDENT
    
    print(f"Génération de ~{total_votes} votes...")
    
    # Pour chaque étudiant, créer des votes pour plusieurs autres étudiants
    for voter_id in student_ids:
        # Chaque étudiant vote pour VOTES_PER_STUDENT autres étudiants (ou moins s'il n'y a pas assez d'étudiants)
        # Sélectionnons aléatoirement d'autres étudiants pour voter
        potential_votees = [s_id for s_id in student_ids if s_id != voter_id]
        num_votes = min(VOTES_PER_STUDENT, len(potential_votees))
        votees = random.sample(potential_votees, num_votes)
        
        for votee_id in votees:
            # Générer un poids aléatoire entre 1 et 100
            weight = random.randint(1, 100)
            
            url = f"{API_BASE_URL}/votes"
            vote_data = {
                "userid": 1,  # Utilisateur système
                "idform": formular_id,
                "idstudent": votee_id,
                "weight": weight
            }
            
            try:
                response = requests.post(url, json=vote_data)
                if response.status_code == 201:
                    votes_created += 1
                    if votes_created % 20 == 0:  # Afficher le progrès tous les 20 votes
                        print(f"► {votes_created} votes créés...")
                else:
                    print(f"❌ Échec création vote: {voter_id}->{votee_id} (weight: {weight}): {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur lors de la création du vote: {str(e)}")
    
    print(f"\nTotal votes créés: {votes_created}")
    return votes_created > 0

def test_students():
    """Test student functionality"""
    global student_id
    print_header("TESTING STUDENTS")
    
    results = []
    
    # Create student
    student_email = f"student_{int(time.time())}@example.com"
    url = f"{API_BASE_URL}/students"
    student_data = {"email": student_email}
    
    print(f"\nCreating student with email '{student_email}'...")
    try:
        response = requests.post(url, json=student_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 201
        results.append(success)
        
        if success:
            student_id = response.json().get("student_id")
    except Exception as e:
        print(f"Error creating student: {e}")
        results.append(False)
        print_test_result("Create student", False, str(e))
    
    # List students
    try:
        response = requests.get(f"{API_BASE_URL}/students")
        print(f"\nListing all students - Status: {response.status_code}")
        students_data = response.json()
        print(f"Found {len(students_data)} students")
        success = response.status_code == 200 and len(students_data) > 0
        results.append(success)
        print_test_result("List students", success)
    except Exception as e:
        print(f"Error listing students: {e}")
        results.append(False)
        print_test_result("List students", False, str(e))
    
    # Get specific student
    if student_id:
        try:
            response = requests.get(f"{API_BASE_URL}/students/{student_id}")
            print(f"\nGetting student {student_id} - Status: {response.status_code}")
            print(f"Response: {response.json()}")
            success = response.status_code == 200
            results.append(success)
            print_test_result("Get specific student", success)
        except Exception as e:
            print(f"Error getting student: {e}")
            results.append(False)
            print_test_result("Get specific student", False, str(e))
    
    return all(results)

def test_teachers():
    """Test teacher functionality"""
    global teacher_id
    print_header("TESTING TEACHERS")
    
    results = []
    
    # Create teacher
    teacher_email = f"teacher_{int(time.time())}@example.com"
    url = f"{API_BASE_URL}/teachers"
    teacher_data = {"email": teacher_email}
    
    print(f"\nCreating teacher with email '{teacher_email}'...")
    try:
        response = requests.post(url, json=teacher_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 201
        results.append(success)
        
        if success:
            teacher_id = teacher_email  # For teachers, email is the ID
    except Exception as e:
        print(f"Error creating teacher: {e}")
        results.append(False)
        print_test_result("Create teacher", False, str(e))
    
    # List teachers
    try:
        response = requests.get(f"{API_BASE_URL}/teachers")
        print(f"\nListing all teachers - Status: {response.status_code}")
        teachers_data = response.json()
        print(f"Found {len(teachers_data)} teachers")
        success = response.status_code == 200 and len(teachers_data) > 0
        results.append(success)
        print_test_result("List teachers", success)
    except Exception as e:
        print(f"Error listing teachers: {e}")
        results.append(False)
        print_test_result("List teachers", False, str(e))
    
    # Get specific teacher
    if teacher_id:
        try:
            response = requests.get(f"{API_BASE_URL}/teachers/{teacher_id}")
            print(f"\nGetting teacher {teacher_id} - Status: {response.status_code}")
            print(f"Response: {response.json()}")
            success = response.status_code == 200
            results.append(success)
            print_test_result("Get specific teacher", success)
        except Exception as e:
            print(f"Error getting teacher: {e}")
            results.append(False)
            print_test_result("Get specific teacher", False, str(e))
    
    return all(results)

def test_auth():
    """Test authentication functionality"""
    global auth_token, teacher_id
    print_header("TESTING AUTHENTICATION")
    
    results = []
    
    # Register user (teacher)
    password = "Password123"
    url = f"{API_BASE_URL}/auth/register"
    user_data = {
        "email": teacher_id,
        "password": password,
        "nom": "Test",
        "prenom": "Teacher"
    }
    
    print(f"\nRegistering user with email '{teacher_id}'...")
    try:
        response = requests.post(url, json=user_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 201
        results.append(success)
    except Exception as e:
        print(f"Error registering user: {e}")
        results.append(False)
        print_test_result("Register user", False, str(e))
    
    # Login
    url = f"{API_BASE_URL}/auth/login"
    login_data = {
        "email": teacher_id,
        "password": password
    }
    
    print(f"\nLogging in with email '{teacher_id}'...")
    try:
        response = requests.post(url, json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 200
        results.append(success)
        
        if success:
            auth_token = response.json().get("token")
    except Exception as e:
        print(f"Error logging in: {e}")
        results.append(False)
        print_test_result("Login", False, str(e))
    
    return all(results)

def test_formulars():
    """Test formular functionality"""
    global formular_id, auth_token
    print_header("TESTING FORMULARS")
    
    results = []
    
    # Create formular
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    url = f"{API_BASE_URL}/formulars"
    formular_data = {
        "title": f"Test Formular {int(time.time())}",
        "description": "This is a test formular description",
        "creator_id": 1,  # Assuming ID 1 for first user
        "end_date": end_date,
        "nb_person_group": 3
    }
    
    # Prepare headers with auth token if available
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    print("\nCreating formular...")
    try:
        response = requests.post(url, json=formular_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 201
        results.append(success)
        
        if success:
            formular_id = response.json().get("formular_id")
    except Exception as e:
        print(f"Error creating formular: {e}")
        results.append(False)
        print_test_result("Create formular", False, str(e))
    
    # List formulars
    try:
        response = requests.get(f"{API_BASE_URL}/formulars", headers=headers)
        print(f"\nListing all formulars - Status: {response.status_code}")
        formulars_data = response.json()
        print(f"Found {len(formulars_data)} formulars")
        success = response.status_code == 200
        results.append(success)
        print_test_result("List formulars", success)
    except Exception as e:
        print(f"Error listing formulars: {e}")
        results.append(False)
        print_test_result("List formulars", False, str(e))
    
    # Get specific formular
    if formular_id:
        try:
            response = requests.get(f"{API_BASE_URL}/formulars/{formular_id}", headers=headers)
            print(f"\nGetting formular {formular_id} - Status: {response.status_code}")
            print(f"Response: {response.json()}")
            success = response.status_code == 200
            results.append(success)
            print_test_result("Get specific formular", success)
        except Exception as e:
            print(f"Error getting formular: {e}")
            results.append(False)
            print_test_result("Get specific formular", False, str(e))
    
    return all(results)

def test_votes():
    """Test vote functionality"""
    global formular_id, student_id
    print_header("TESTING VOTES")
    
    results = []
    
    # Create a vote
    url = f"{API_BASE_URL}/votes"
    vote_data = {
        "userid": 1,  # Assuming user ID 1
        "idform": formular_id,
        "idstudent": student_id,
        "weight": 50  # Weight of 50 points
    }
    
    print("\nCreating vote...")
    try:
        response = requests.post(url, json=vote_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        success = response.status_code == 201
        results.append(success)
        print_test_result("Create vote", success)
        
        if success:
            vote_id = response.json().get("vote_idvote")
    except Exception as e:
        print(f"Error creating vote: {e}")
        results.append(False)
        print_test_result("Create vote", False, str(e))
        vote_id = None
    
    # List votes
    try:
        response = requests.get(f"{API_BASE_URL}/votes")
        print(f"\nListing all votes - Status: {response.status_code}")
        votes_data = response.json()
        print(f"Found {len(votes_data)} votes")
        success = response.status_code == 200
        results.append(success)
        print_test_result("List votes", success)
    except Exception as e:
        print(f"Error listing votes: {e}")
        results.append(False)
        print_test_result("List votes", False, str(e))
    
    # Get votes for specific formular
    if formular_id:
        try:
            response = requests.get(f"{API_BASE_URL}/formulars/{formular_id}/votes")
            print(f"\nGetting votes for formular {formular_id} - Status: {response.status_code}")
            formular_votes = response.json()
            print(f"Found {len(formular_votes)} votes for formular")
            success = response.status_code == 200
            results.append(success)
            print_test_result("Get formular votes", success)
        except Exception as e:
            print(f"Error getting formular votes: {e}")
            results.append(False)
            print_test_result("Get formular votes", False, str(e))
    
    return all(results)

def test_clustering():
    """Test clustering functionality"""
    global formular_id
    print_header("TESTING CLUSTERING")
    
    if not formular_id:
        print("⚠️ No formular ID available. Cannot test clustering.")
        return False
    
    # Test clustering API
    try:
        url = f"{API_BASE_URL}/clustering/{formular_id}"
        print(f"\nGenerating clusters for formular {formular_id}...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Clustering result: {json.dumps(result, indent=2)}")
        
        success = response.status_code == 200
        print_test_result("Generate clusters via API", success)
        
        return success
    except Exception as e:
        print(f"Error testing clustering: {e}")
        print_test_result("Generate clusters via API", False, str(e))
        return False

def run_full_test_suite():
    """Run all tests in sequence"""
    results = []
    
    # Store test results
    results.append(("Roles", test_roles()))
    results.append(("Students", test_students()))
    results.append(("Teachers", test_teachers()))
    results.append(("Authentication", test_auth()))
    results.append(("Formulars", test_formulars()))
    results.append(("Votes", test_votes()))
    results.append(("Clustering", test_clustering()))
    
    # Print summary
    print_header("TEST SUMMARY")
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
    
    print("\n" + "="*60)
    print(f"OVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    # Vérifier si on veut juste générer des données de test
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-data":
        generate_test_data()
    else:
        run_full_test_suite()
