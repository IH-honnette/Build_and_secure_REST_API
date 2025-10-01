# SMS Transactions REST API Documentation

## Overview
This REST API provides CRUD operations for SMS transaction data using Python's `http.server` module. The API includes Basic Authentication, performance comparison between search algorithms, and comprehensive error handling.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require Basic Authentication. Include the `Authorization` header with base64-encoded credentials.

**Valid Credentials:**
- Username: `admin`, Password: `password123`
- Username: `user`, Password: `userpass456`

**Example:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

## Endpoints

### 1. List All Transactions
**GET** `/transactions`

Retrieves all SMS transactions (limited to first 100 for performance).

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

**Response:**
```json
{
  "message": "All SMS transactions retrieved successfully",
  "count": 1500,
  "transactions": [
    {
      "id": 1,
      "protocol": "0",
      "address": "M-Money",
      "date": "1715351458724",
      "type": "1",
      "subject": "null",
      "body": "You have received 2000 RWF from Jane Smith...",
      "toa": "null",
      "sc_toa": "null",
      "service_center": "+250788110381",
      "read": "1",
      "status": "-1",
      "locked": "0",
      "date_sent": "1715351451000",
      "sub_id": "6",
      "readable_date": "10 May 2024 4:30:58 PM",
      "contact_name": "(Unknown)"
    }
  ],
  "search_performance": {
    "note": "For individual lookups, dictionary lookup is O(1) vs linear search O(n)"
  }
}
```

### 2. Get Specific Transaction
**GET** `/transactions/{id}`

Retrieves a specific transaction by ID and compares search algorithm performance.

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions/1
```

**Response:**
```json
{
  "message": "Transaction 1 retrieved successfully",
  "transaction": {
    "id": 1,
    "protocol": "0",
    "address": "M-Money",
    "date": "1715351458724",
    "type": "1",
    "subject": "null",
    "body": "You have received 2000 RWF from Jane Smith...",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "+250788110381",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1715351451000",
    "sub_id": "6",
    "readable_date": "10 May 2024 4:30:58 PM",
    "contact_name": "(Unknown)"
  },
  "search_comparison": {
    "linear_search_result": true,
    "dictionary_lookup_result": true,
    "note": "Dictionary lookup is significantly faster for large datasets"
  }
}
```

### 3. Create New Transaction
**POST** `/transactions`

Creates a new SMS transaction.

**Request:**
```bash
curl -X POST -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "M-Money",
    "body": "Test transaction message",
    "date": "1715351458724",
    "type": "1",
    "subject": "Test",
    "service_center": "+250788110381"
  }' \
  http://localhost:8000/transactions
```

**Response:**
```json
{
  "message": "Transaction created successfully",
  "transaction": {
    "id": 1501,
    "address": "M-Money",
    "body": "Test transaction message",
    "date": "1715351458724",
    "type": "1",
    "subject": "Test",
    "service_center": "+250788110381",
    "created_at": 1703123456.789
  },
  "total_transactions": 1501
}
```

### 4. Update Transaction
**PUT** `/transactions/{id}`

Updates an existing transaction by ID.

**Request:**
```bash
curl -X PUT -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "M-Money",
    "body": "Updated transaction message",
    "date": "1715351458724",
    "type": "1",
    "subject": "Updated",
    "service_center": "+250788110381"
  }' \
  http://localhost:8000/transactions/1
```

**Response:**
```json
{
  "message": "Transaction 1 updated successfully",
  "transaction": {
    "id": 1,
    "address": "M-Money",
    "body": "Updated transaction message",
    "date": "1715351458724",
    "type": "1",
    "subject": "Updated",
    "service_center": "+250788110381",
    "updated_at": 1703123456.789
  }
}
```

### 5. Delete Transaction
**DELETE** `/transactions/{id}`

Deletes a transaction by ID.

**Request:**
```bash
curl -X DELETE -u admin:password123 http://localhost:8000/transactions/1
```

**Response:**
```json
{
  "message": "Transaction 1 deleted successfully",
  "deleted_transaction": {
    "id": 1,
    "protocol": "0",
    "address": "M-Money",
    "date": "1715351458724",
    "type": "1",
    "subject": "null",
    "body": "You have received 2000 RWF from Jane Smith...",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "+250788110381",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1715351451000",
    "sub_id": "6",
    "readable_date": "10 May 2024 4:30:58 PM",
    "contact_name": "(Unknown)"
  },
  "remaining_transactions": 1499
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials. Please provide valid Basic Auth credentials.",
  "status_code": 401
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Transaction with ID 9999 not found",
  "status_code": 404,
  "timestamp": 1703123456.789
}
```

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Missing required field: body",
  "status_code": 400,
  "timestamp": 1703123456.789
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Error creating transaction: Database connection failed",
  "status_code": 500,
  "timestamp": 1703123456.789
}
```

## Data Structures & Algorithms Analysis

### Linear Search Implementation
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Implementation:** Iterates through all transactions sequentially
- **Use Case:** Simple but inefficient for large datasets

### Dictionary Lookup Implementation
- **Time Complexity:** O(1) average case
- **Space Complexity:** O(n)
- **Implementation:** Uses Python dictionary with transaction ID as key
- **Use Case:** Fast retrieval for individual transactions

### Performance Comparison
For datasets with 20+ records:
- **Dictionary Lookup:** ~0.000001 seconds
- **Linear Search:** ~0.0001-0.001 seconds (varies with position)

**Why Dictionary Lookup is Faster:**
1. **Hash Table:** Dictionary uses hash table internally for O(1) average access
2. **Direct Access:** No need to iterate through elements
3. **Memory Trade-off:** Uses more memory but provides faster access

### Alternative Data Structures
1. **Binary Search Tree:** O(log n) search time, maintains sorted order
2. **B-Tree:** O(log n) search time, optimized for disk storage
3. **Trie:** O(m) search time where m is key length, good for string keys
4. **Hash Table with Chaining:** O(1) average, O(n) worst case

## Security Analysis

### Basic Authentication Limitations
1. **Credentials in Plain Text:** Base64 encoding is easily decoded
2. **No Encryption:** Credentials sent with every request
3. **No Session Management:** No way to revoke access
4. **Vulnerable to Replay Attacks:** Same credentials can be reused

### Recommended Alternatives
1. **JWT (JSON Web Tokens):**
   - Stateless authentication
   - Can include expiration and claims
   - Signed/encrypted for security

2. **OAuth 2.0:**
   - Industry standard for authorization
   - Supports multiple grant types
   - Better for third-party integrations

3. **API Keys:**
   - Simple for server-to-server communication
   - Can be rotated and revoked
   - Better than Basic Auth for APIs

## Running the Server

1. **Start the server:**
```bash
python sms_api_server.py
```

2. **Test with curl:**
```bash
# Test authentication
curl -u admin:password123 http://localhost:8000/transactions

# Test unauthorized access
curl http://localhost:8000/transactions
```

3. **Test with Postman:**
   - Set Authorization to "Basic Auth"
   - Username: `admin`, Password: `password123`
   - Test all CRUD operations

## CORS Support
The API includes CORS headers for cross-origin requests:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`
