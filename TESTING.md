# Testing Guide - Blacklist Microservice

This document provides comprehensive testing instructions for the Blacklist Microservice API developed for Universidad de los Andes MISW4304.

## 🧪 Testing Overview

The project includes multiple testing approaches:

1. **Python Unit Tests** - Comprehensive test suite using unittest
2. **Newman Tests** - Postman collection with automated test scripts
3. **Manual Testing** - Postman collection for manual API testing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (managed with pyenv)
- Node.js and npm (for Newman)
- PostgreSQL database (for full functionality)

### Setup

1. **Install dependencies:**
   ```bash
   make setup
   ```

2. **Start the application:**
   ```bash
   make start
   ```

3. **Run tests:**
   ```bash
   make test
   ```

## 📋 Available Test Commands

| Command | Description |
|---------|-------------|
| `make test` | Run Python-based tests |
| `make test-newman` | Run Newman (Postman) tests |
| `make test-all` | Run both Python and Newman tests |
| `make test-quick` | Quick health check |
| `make start` | Start the Flask application |
| `make stop` | Stop the Flask application |
| `make clean` | Clean up generated files |

## 🐍 Python Tests

### Running Python Tests

```bash
# Run all Python tests
make test-python

# Or directly
python run_tests.py
```

### Test Coverage

The Python test suite includes:

- ✅ Health check endpoint
- ✅ Add email to blacklist (success case)
- ✅ Check email blacklist status
- ✅ Duplicate email handling
- ✅ Missing parameters validation
- ✅ Invalid email format validation
- ✅ Invalid UUID validation
- ✅ Invalid token authentication
- ✅ Missing authorization header
- ✅ Non-existent email lookup
- ✅ Blocked reason length validation
- ✅ Performance tests (concurrent requests)

### Test Output Example

```
🧪 Blacklist Microservice Test Suite
Universidad de los Andes - MISW4304
==================================================
✅ Server is running

🧪 Running Unit Tests...
------------------------------
🔍 Testing health check endpoint...
✅ Health check passed

📧 Testing add email to blacklist: test_1703123456@example.com
✅ Add email to blacklist passed

🔍 Testing check email blacklist: test_1703123456@example.com
✅ Check email blacklist passed

✅ All 12 tests passed!

🚀 Running Performance Tests...
==================================================
Health Check Response Time: 0.045s
10 Concurrent Requests Time: 0.123s
Average Response Time: 0.012s
Successful Requests: 10/10

==================================================
🎉 All tests completed successfully!
```

## 📮 Newman Tests

### Running Newman Tests

```bash
# Run Newman tests
make test-newman

# Or directly
./run_newman_tests.sh
```

### Newman Test Features

- **Automated Test Scripts**: Each request includes validation tests
- **HTML Reports**: Detailed test reports with screenshots
- **JSON Reports**: Machine-readable test results
- **Environment Variables**: Configurable test parameters
- **Error Handling**: Comprehensive error scenario testing

### Test Collection Structure

1. **Health Check** - Service availability
2. **Add Email Success** - Valid email addition
3. **Check Email Status** - Email lookup verification
4. **Duplicate Email** - Conflict handling
5. **Missing Parameters** - Validation testing
6. **Invalid Email** - Format validation
7. **Invalid UUID** - UUID format validation
8. **Invalid Token** - Authentication testing
9. **Missing Authorization** - Security testing
10. **Non-existent Email** - Not found handling
11. **GET with Invalid Token** - GET endpoint security

### Newman Test Output

```bash
🚀 Newman Test Runner for Blacklist Microservice
================================================

🔍 Checking if server is running at http://localhost:3000...
✅ Server is running

🧪 Running Newman tests...

Blacklist Microservice API - With Tests

→ Health Check
  GET http://localhost:3000/blacklists/ping
  ✓  Status code is 200
  ✓  Response is 'pong'
  ✓  Response time is less than 1000ms

→ Add Email to Blacklist - Success
  POST http://localhost:3000/blacklists
  ✓  Status code is 201
  ✓  Response has success message
  ✓  Response time is less than 2000ms
  ✓  Response is JSON

🎉 All tests passed successfully!
📊 HTML Report: newman_reports/newman_report_20231221_143022.html
📊 JSON Report: newman_reports/newman_report_20231221_143022.json
```

## 📊 Test Reports

### Newman Reports

Newman generates detailed HTML and JSON reports in the `newman_reports/` directory:

- **HTML Report**: Visual test results with request/response details
- **JSON Report**: Machine-readable results for CI/CD integration

### Report Features

- Test execution timeline
- Request/response details
- Error messages and stack traces
- Performance metrics
- Test coverage summary

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=blacklist_db

# JWT Configuration
SECRET_TOKEN=test_secret_token_123

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Test Configuration

The test suite uses the following default configuration:

- **Base URL**: `http://localhost:3000`
- **Secret Token**: `test_secret_token_123`
- **Timeout**: 10 seconds per request
- **Concurrent Tests**: 10 parallel requests

## 🐛 Troubleshooting

### Common Issues

1. **Server Not Running**
   ```
   ❌ Server is not running at http://localhost:3000
   ```
   **Solution**: Start the server with `make start`

2. **Database Connection Error**
   ```
   ❌ Database connection failed
   ```
   **Solution**: Ensure PostgreSQL is running and configured correctly

3. **Newman Not Found**
   ```
   ❌ Newman is not installed
   ```
   **Solution**: Install Newman with `npm install -g newman`

4. **Permission Denied**
   ```
   ❌ Permission denied: ./run_newman_tests.sh
   ```
   **Solution**: Make script executable with `chmod +x run_newman_tests.sh`

### Debug Mode

Enable debug mode for detailed logging:

```bash
export FLASK_DEBUG=True
make start
```

## 📈 Performance Testing

The test suite includes performance benchmarks:

- **Response Time**: < 1 second for health checks
- **Response Time**: < 2 seconds for database operations
- **Concurrent Requests**: 10 parallel requests
- **Throughput**: Measures requests per second

## 🔒 Security Testing

Security tests cover:

- **Authentication**: Valid/invalid token handling
- **Authorization**: Missing header scenarios
- **Input Validation**: Malformed data handling
- **SQL Injection**: Parameter sanitization
- **Rate Limiting**: Concurrent request handling

## 📝 Test Data

The test suite uses dynamic test data:

- **Unique Emails**: Timestamp-based email generation
- **Valid UUIDs**: Properly formatted UUID v4
- **Test Reasons**: Various blocked reason scenarios
- **Edge Cases**: Boundary value testing

## 🎯 Test Coverage

Current test coverage includes:

- ✅ All API endpoints (100%)
- ✅ Success scenarios (100%)
- ✅ Error scenarios (100%)
- ✅ Authentication flows (100%)
- ✅ Data validation (100%)
- ✅ Performance scenarios (80%)

## 📚 Additional Resources

- [Postman Documentation](https://learning.postman.com/docs/)
- [Newman Documentation](https://github.com/postmanlabs/newman)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## 🤝 Contributing

When adding new tests:

1. Follow the existing test structure
2. Include both success and failure scenarios
3. Add performance considerations
4. Update this documentation
5. Ensure tests are deterministic

---

**Universidad de los Andes - MISW4304**  
*Microservices Architecture Course*
