# SMS Transactions REST API

A comprehensive REST API implementation built with Python's `http.server` module for managing SMS transaction data. This project demonstrates CRUD operations, authentication, data structure algorithms, and performance analysis.

## 📁 Repository Structure

```
sms-transactions-api/
├── api/                          # API Implementation
│   └── sms_api_server.py        # Main REST API server
├── dsa/                          # Data Structures & Algorithms
│   └── search_algorithms.py     # Search algorithm implementations
├── docs/                         # Documentation
│   └── api_docs.md              # Complete API documentation
├── screenshots/                  # Test case screenshots
├── sms_transactions.json        # SMS transaction dataset
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd sms-transactions-api
   ```

2. **Start the API server:**
   ```bash
   python api/sms_api_server.py
   ```

3. **Test the API:**
   ```bash
   # Test authentication
   curl -u admin:password123 http://localhost:8000/transactions
   
   # Test unauthorized access
   curl http://localhost:8000/transactions
   ```

## 🔑 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/transactions` | List all transactions | ✅ |
| GET | `/transactions/{id}` | Get specific transaction | ✅ |
| POST | `/transactions` | Create new transaction | ✅ |
| PUT | `/transactions/{id}` | Update transaction | ✅ |
| DELETE | `/transactions/{id}` | Delete transaction | ✅ |

## 🔐 Authentication

All endpoints require Basic Authentication:

**Valid Credentials:**
- Username: `admin`, Password: `password123`
- Username: `user`, Password: `userpass456`

**Example:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

## 📊 Data Structures & Algorithms

### Implemented Algorithms

1. **Linear Search** - O(n) time complexity
2. **Dictionary Lookup** - O(1) average time complexity  
3. **Binary Search** - O(log n) time complexity

### Performance Comparison

Run the DSA demonstration:
```bash
python dsa/search_algorithms.py
```

**Sample Output:**
```
🔍 SMS Transactions Search Algorithms Demo
==================================================
Dataset size: 1500 transactions

🔍 Testing search for transaction ID: 1
------------------------------
Linear Search:
  Status: ✅ Found
  Time: 0.000123 seconds
  Complexity: O(n)

Dictionary Lookup:
  Status: ✅ Found
  Time: 0.000001 seconds
  Complexity: O(1)

Binary Search:
  Status: ✅ Found
  Time: 0.000045 seconds
  Complexity: O(log n)

📊 Performance Analysis:
  Fastest: Dictionary Lookup
  Dataset size: 1500
  Speed improvements:
    Dictionary Vs Linear: 123.00x faster
    Binary Vs Linear: 2.73x faster
    Dictionary Vs Binary: 45.00x faster
```

### Why Dictionary Lookup is Fastest

1. **Hash Table Implementation**: Uses Python's built-in hash table
2. **Direct Access**: No iteration or comparison needed
3. **O(1) Average Case**: Constant time regardless of dataset size
4. **Memory Trade-off**: Uses more memory but provides faster access

## 🧪 Testing

### Manual Testing with curl

```bash
# List all transactions
curl -u admin:password123 http://localhost:8000/transactions

# Get specific transaction
curl -u admin:password123 http://localhost:8000/transactions/1

# Create new transaction
curl -X POST -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"address":"Test","body":"Test message","date":"1234567890","type":"1"}' \
  http://localhost:8000/transactions

# Update transaction
curl -X PUT -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"address":"Updated","body":"Updated message","date":"1234567890","type":"1"}' \
  http://localhost:8000/transactions/1

# Delete transaction
curl -X DELETE -u admin:password123 http://localhost:8000/transactions/1
```

### Test Cases Covered

- ✅ **Authentication**: Valid/invalid credentials
- ✅ **CRUD Operations**: Create, Read, Update, Delete
- ✅ **Error Handling**: 400, 401, 404, 500 responses
- ✅ **Input Validation**: Required fields, JSON format
- ✅ **Performance**: Algorithm comparison
- ✅ **CORS**: Cross-origin requests

## 🔒 Security Analysis

### Basic Authentication Limitations

1. **Plain Text Credentials**: Base64 encoding is easily decoded
2. **No Encryption**: Credentials sent with every request
3. **No Session Management**: Cannot revoke access without restart
4. **Replay Attack Vulnerability**: Same credentials can be reused

### Recommended Alternatives

1. **JWT (JSON Web Tokens)**: Stateless, signed tokens with expiration
2. **OAuth 2.0**: Industry standard for authorization
3. **API Keys**: Simple server-to-server authentication

## 📚 Documentation

- **Complete API Documentation**: [`docs/api_docs.md`](docs/api_docs.md)
- **Algorithm Implementation**: [`dsa/search_algorithms.py`](dsa/search_algorithms.py)
- **Server Implementation**: [`api/sms_api_server.py`](api/sms_api_server.py)

## 🎯 Learning Objectives Achieved

✅ **API Implementation**: Complete REST API with Python http.server  
✅ **Authentication**: Basic Auth with security analysis  
✅ **Data Structures**: Linear Search vs Dictionary Lookup comparison  
✅ **Performance Analysis**: Timing measurements and complexity analysis  
✅ **Error Handling**: Comprehensive error responses  
✅ **Testing**: Manual testing with curl commands  
✅ **Documentation**: Complete API documentation  

## 🐛 Troubleshooting

### Common Issues

1. **Server won't start:**
   - Check if port 8000 is available
   - Ensure Python 3.6+ is installed
   - Verify `sms_transactions.json` exists

2. **Authentication fails:**
   - Use correct credentials: `admin:password123`
   - Ensure Basic Auth header is properly formatted

3. **Performance issues:**
   - Large datasets may slow down linear search
   - Dictionary lookup remains fast regardless of dataset size

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the API documentation in `docs/api_docs.md`
3. Test with the provided curl commands
4. Check server logs for error messages

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

**🎉 Ready to submit!** This repository contains everything needed for your assignment submission.