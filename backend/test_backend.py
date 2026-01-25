import requests
import json

# Test 1: Simple SELECT query
print("=" * 50)
print("Test 1: Simple SELECT query")
print("=" * 50)

try:
    response = requests.post(
        "http://localhost:5000/consulta",
        headers={"Content-Type": "application/json"},
        json={"sql": "SELECT * FROM usuarios WHERE id = 101"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Test 2: Complex SELECT query (like frontend)")
print("=" * 50)

try:
    sql_query = """SELECT 
    u.id, 
    u.username, 
    u.email
FROM 
    users u
WHERE 
    u.status = 'active';"""
    
    response = requests.post(
        "http://localhost:5000/consulta",
        headers={"Content-Type": "application/json"},
        json={"sql": sql_query}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Test 3: Health check with minimal query")
print("=" * 50)

try:
    response = requests.post(
        "http://localhost:5000/consulta",
        headers={"Content-Type": "application/json"},
        json={"sql": "SELECT * FROM usuarios"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
