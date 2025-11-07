# SQL Injection Scanner

A fast and efficient SQL injection vulnerability scanner with parallel testing capabilities for penetration testing and security assessment.

## Features

- **Parallel Testing**: Tests multiple payloads simultaneously for faster scanning
- **Connection Pooling**: Reuses HTTP connections for improved performance  
- **Database Detection**: Identifies specific database types (MySQL, PostgreSQL, SQLite, etc.)
- **Focused Payloads**: Curated set of effective SQL injection test cases
- **Response Time Tracking**: Monitors request performance
- **Clean Output**: Structured results with vulnerability details

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SQL-injection-scanner.git
cd SQL-injection-scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python sql_injection_scanner.py "http://example.com/page?id=1"
```

### Advanced Options
```bash
python sql_injection_scanner.py "http://example.com/page?id=1&name=test" \
    --timeout 15 \
    --workers 10
```

### Command Line Options

- `url`: Target URL with parameters (required)
- `-t, --timeout`: Request timeout in seconds (default: 10)
- `-w, --workers`: Maximum parallel workers (default: 5)

## Example Output

```
[*] Scanning: http://example.com/page?id=1
[*] Testing 4 combinations across 1 parameters
[!] VULNERABLE - Parameter: id, Payload: ' OR 1=1--, DB Type: mysql
[!] Found 1 potential vulnerabilities

[*] Scan completed in 0.85 seconds
[!] Note: Always get permission before testing!
```

## How It Works

1. **URL Parsing**: Extracts parameters from the target URL
2. **Payload Generation**: Creates test cases with SQL injection payloads
3. **Parallel Execution**: Sends requests concurrently using ThreadPoolExecutor
4. **Error Detection**: Analyzes responses for SQL error patterns
5. **Database Identification**: Determines the database type from error messages

## Supported Databases

- MySQL
- PostgreSQL
- SQLite
- Microsoft SQL Server
- Oracle
- Generic SQL databases

## Payloads Tested

- `'` - Basic quote test
- `' OR 1=1--` - Boolean-based injection
- `' UNION SELECT 1--` - Union-based injection
- `'; DROP TABLE users--` - Destructive test (safe in most cases)

## Red Team / Blue Team Usage

**Red Team (Offensive Security):**
- Penetration testing authorized targets
- Bug bounty hunting
- Security assessments
- Vulnerability discovery

**Blue Team (Defensive Security):**
- Testing your own applications
- Validating security fixes
- CI/CD security integration
- Security training and awareness

## Legal Disclaimer

This tool is for educational and authorized testing purposes only.

- Only test applications you own or have explicit written permission to test
- Unauthorized testing may be illegal in your jurisdiction
- Always follow responsible disclosure practices
- The authors are not responsible for misuse of this tool
- Get proper authorization before any security testing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for educational purposes and ethical security testing
- Inspired by common SQL injection testing methodologies
- Thanks to the security research community for payload insights
