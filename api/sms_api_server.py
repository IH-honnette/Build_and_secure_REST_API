#!/usr/bin/env python3

import json
import base64
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Optional, Tuple
import os


class SMSAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for SMS Transactions API"""

    VALID_CREDENTIALS = {
        "admin": "password123",
        "user": "userpass456"
    }
    
    def __init__(self, *args, **kwargs):
        self.transactions = []
        self.transactions_dict = {}  # For dictionary lookup optimization
        self.load_transactions()
        super().__init__(*args, **kwargs)
    
    def load_transactions(self):
        """Load transactions from JSON file"""
        try:
            with open('sms_transactions.json', 'r', encoding='utf-8') as f:
                self.transactions = json.load(f)
                # Create dictionary for O(1) lookup
                for i, transaction in enumerate(self.transactions):
                    transaction['id'] = i + 1  # Add ID field
                    self.transactions_dict[transaction['id']] = transaction
            print(f"Loaded {len(self.transactions)} transactions")
        except FileNotFoundError:
            print("sms_transactions.json not found. Starting with empty dataset.")
            self.transactions = []
            self.transactions_dict = {}
    
    def authenticate(self) -> bool:
        """Check Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        try:
            # Decode base64 credentials
            encoded_credentials = auth_header[6:]  # Remove 'Basic '
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            return self.VALID_CREDENTIALS.get(username) == password
        except Exception:
            return False
    
    def send_auth_error(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="SMS API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        error_response = {
            "error": "Unauthorized",
            "message": "Invalid credentials. Please provide valid Basic Auth credentials.",
            "status_code": 401
        }
        self.wfile.write(json.dumps(error_response).encode())
    
    def send_json_response(self, data: dict, status_code: int = 200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error_response(self, message: str, status_code: int = 400):
        """Send error response"""
        error_response = {
            "error": "Bad Request" if status_code == 400 else "Not Found" if status_code == 404 else "Internal Server Error",
            "message": message,
            "status_code": status_code,
            "timestamp": time.time()
        }
        self.send_json_response(error_response, status_code)
    
    def linear_search(self, transaction_id: int) -> Optional[dict]:
        """Linear search implementation - O(n) time complexity"""
        start_time = time.time()
        for transaction in self.transactions:
            if transaction.get('id') == transaction_id:
                end_time = time.time()
                print(f"Linear search took {end_time - start_time:.6f} seconds")
                return transaction
        end_time = time.time()
        print(f"Linear search (not found) took {end_time - start_time:.6f} seconds")
        return None
    
    def dictionary_lookup(self, transaction_id: int) -> Optional[dict]:
        """Dictionary lookup implementation - O(1) time complexity"""
        start_time = time.time()
        result = self.transactions_dict.get(transaction_id)
        end_time = time.time()
        print(f"Dictionary lookup took {end_time - start_time:.6f} seconds")
        return result
    
    def parse_path(self) -> Tuple[str, Optional[int]]:
        """Parse URL path to extract endpoint and ID"""
        path = self.path.split('?')[0]  # Remove query parameters
        parts = path.strip('/').split('/')
        
        if len(parts) == 1 and parts[0] == 'transactions':
            return 'transactions', None
        elif len(parts) == 2 and parts[0] == 'transactions':
            try:
                return 'transaction', int(parts[1])
            except ValueError:
                return 'invalid', None
        else:
            return 'invalid', None
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            self.send_auth_error()
            return
        
        endpoint, transaction_id = self.parse_path()
        
        if endpoint == 'transactions':
            # GET /transactions - List all transactions
            response = {
                "message": "All SMS transactions retrieved successfully",
                "count": len(self.transactions),
                "transactions": self.transactions[:100],  # Limit to first 100 for performance
                "search_performance": {
                    "note": "For individual lookups, dictionary lookup is O(1) vs linear search O(n)"
                }
            }
            self.send_json_response(response)
            
        elif endpoint == 'transaction' and transaction_id:
            # GET /transactions/{id} - Get specific transaction
            # Compare both search methods
            linear_result = self.linear_search(transaction_id)
            dict_result = self.dictionary_lookup(transaction_id)
            
            if dict_result:
                response = {
                    "message": f"Transaction {transaction_id} retrieved successfully",
                    "transaction": dict_result,
                    "search_comparison": {
                        "linear_search_result": linear_result is not None,
                        "dictionary_lookup_result": dict_result is not None,
                        "note": "Dictionary lookup is significantly faster for large datasets"
                    }
                }
                self.send_json_response(response)
            else:
                self.send_error_response(f"Transaction with ID {transaction_id} not found", 404)
        else:
            self.send_error_response("Invalid endpoint. Use /transactions or /transactions/{id}")
    
    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            self.send_auth_error()
            return
        
        endpoint, _ = self.parse_path()
        
        if endpoint != 'transactions':
            self.send_error_response("Invalid endpoint for POST. Use /transactions")
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_transaction = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['address', 'body', 'date']
            for field in required_fields:
                if field not in new_transaction:
                    self.send_error_response(f"Missing required field: {field}")
                    return
            
            # Add ID and timestamp
            new_transaction['id'] = len(self.transactions) + 1
            new_transaction['created_at'] = time.time()
            
            # Add to both data structures
            self.transactions.append(new_transaction)
            self.transactions_dict[new_transaction['id']] = new_transaction
            
            response = {
                "message": "Transaction created successfully",
                "transaction": new_transaction,
                "total_transactions": len(self.transactions)
            }
            self.send_json_response(response, 201)
            
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON in request body")
        except Exception as e:
            self.send_error_response(f"Error creating transaction: {str(e)}", 500)
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self.authenticate():
            self.send_auth_error()
            return
        
        endpoint, transaction_id = self.parse_path()
        
        if endpoint != 'transaction' or not transaction_id:
            self.send_error_response("Invalid endpoint for PUT. Use /transactions/{id}")
            return
        
        # Check if transaction exists
        existing_transaction = self.dictionary_lookup(transaction_id)
        if not existing_transaction:
            self.send_error_response(f"Transaction with ID {transaction_id} not found", 404)
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_data = json.loads(put_data.decode('utf-8'))
            
            # Preserve ID and add update timestamp
            updated_data['id'] = transaction_id
            updated_data['updated_at'] = time.time()
            
            # Update in both data structures
            for i, transaction in enumerate(self.transactions):
                if transaction.get('id') == transaction_id:
                    self.transactions[i] = updated_data
                    break
            
            self.transactions_dict[transaction_id] = updated_data
            
            response = {
                "message": f"Transaction {transaction_id} updated successfully",
                "transaction": updated_data
            }
            self.send_json_response(response)
            
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON in request body")
        except Exception as e:
            self.send_error_response(f"Error updating transaction: {str(e)}", 500)
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self.authenticate():
            self.send_auth_error()
            return
        
        endpoint, transaction_id = self.parse_path()
        
        if endpoint != 'transaction' or not transaction_id:
            self.send_error_response("Invalid endpoint for DELETE. Use /transactions/{id}")
            return
        
        # Check if transaction exists
        existing_transaction = self.dictionary_lookup(transaction_id)
        if not existing_transaction:
            self.send_error_response(f"Transaction with ID {transaction_id} not found", 404)
            return
        
        # Remove from both data structures
        self.transactions = [t for t in self.transactions if t.get('id') != transaction_id]
        del self.transactions_dict[transaction_id]
        
        response = {
            "message": f"Transaction {transaction_id} deleted successfully",
            "deleted_transaction": existing_transaction,
            "remaining_transactions": len(self.transactions)
        }
        self.send_json_response(response)
    
    def log_message(self, format, *args):
        """Override to customize log format"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port: int = 8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SMSAPIHandler)
    
    print(f"SMS Transactions API Server starting...")
    print(f"Server running on http://localhost:{port}")
    print(f"Available endpoints:")
    print(f"  GET    /transactions           - List all transactions")
    print(f"  GET    /transactions/{{id}}      - Get specific transaction")
    print(f"  POST   /transactions           - Create new transaction")
    print(f"  PUT    /transactions/{{id}}      - Update transaction")
    print(f"  DELETE /transactions/{{id}}      - Delete transaction")
    print(f"\nAuthentication required for all endpoints.")
    print(f"Valid credentials: admin/password123 or user/userpass456")
    print(f"\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\nServer stopped.")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
