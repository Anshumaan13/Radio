#!/usr/bin/env python3
"""
Backend Test Suite for Global Radio API
Tests all the radio API endpoints including connectivity, countries, stations, and validation.
"""

import asyncio
import httpx
import json
import os
from typing import List, Dict, Any
from datetime import datetime

# Get the backend URL from frontend .env file
def get_backend_url():
    """Get backend URL from frontend .env file"""
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

class RadioAPITester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        self.failed_tests = []
        
    async def close(self):
        await self.client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if not success:
            self.failed_tests.append(test_name)
        print()
    
    async def test_basic_connectivity(self):
        """Test 1: Basic API connectivity"""
        print("=== Testing Basic Connectivity ===")
        
        try:
            response = await self.client.get(f"{API_BASE}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Global Radio API" in data["message"]:
                    self.log_test(
                        "Basic Connectivity - GET /api/", 
                        True, 
                        f"API responded with welcome message: {data['message']}", 
                        data
                    )
                else:
                    self.log_test(
                        "Basic Connectivity - GET /api/", 
                        False, 
                        f"Unexpected response format: {data}"
                    )
            else:
                self.log_test(
                    "Basic Connectivity - GET /api/", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Basic Connectivity - GET /api/", 
                False, 
                f"Connection error: {str(e)}"
            )
    
    async def test_countries_endpoint(self):
        """Test 2: Countries endpoint"""
        print("=== Testing Countries Endpoint ===")
        
        try:
            response = await self.client.get(f"{API_BASE}/countries")
            
            if response.status_code == 200:
                countries = response.json()
                
                if isinstance(countries, list) and len(countries) > 0:
                    # Check structure of first country
                    first_country = countries[0]
                    required_fields = ['code', 'name', 'flag', 'station_count']
                    
                    missing_fields = [field for field in required_fields if field not in first_country]
                    
                    if not missing_fields:
                        # Check for reasonable countries
                        country_codes = [c.get('code', '') for c in countries]
                        expected_countries = ['US', 'GB', 'DE', 'FR', 'CA']
                        found_countries = [code for code in expected_countries if code in country_codes]
                        
                        self.log_test(
                            "Countries Endpoint - Structure", 
                            True, 
                            f"Found {len(countries)} countries with correct structure. Major countries found: {found_countries}",
                            {"total_countries": len(countries), "sample": countries[:3]}
                        )
                        
                        # Test specific country details
                        us_country = next((c for c in countries if c.get('code') == 'US'), None)
                        if us_country:
                            self.log_test(
                                "Countries Endpoint - US Data", 
                                True, 
                                f"US: {us_country['name']}, Flag: {us_country['flag']}, Stations: {us_country['station_count']}",
                                us_country
                            )
                        else:
                            self.log_test(
                                "Countries Endpoint - US Data", 
                                False, 
                                "United States not found in countries list"
                            )
                    else:
                        self.log_test(
                            "Countries Endpoint - Structure", 
                            False, 
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Countries Endpoint - Response", 
                        False, 
                        f"Expected non-empty list, got: {type(countries)} with {len(countries) if isinstance(countries, list) else 'N/A'} items"
                    )
            else:
                self.log_test(
                    "Countries Endpoint - HTTP Status", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Countries Endpoint - Request", 
                False, 
                f"Request error: {str(e)}"
            )
    
    async def test_stations_endpoint(self):
        """Test 3: Stations endpoint"""
        print("=== Testing Stations Endpoint ===")
        
        # Test valid country codes
        test_countries = [
            ('US', 'United States'),
            ('GB', 'United Kingdom'),
            ('DE', 'Germany')
        ]
        
        for country_code, country_name in test_countries:
            try:
                response = await self.client.get(f"{API_BASE}/stations/{country_code}")
                
                if response.status_code == 200:
                    stations = response.json()
                    
                    if isinstance(stations, list):
                        if len(stations) > 0:
                            # Check structure of first station
                            first_station = stations[0]
                            required_fields = ['id', 'name', 'frequency', 'genre', 'url', 'listeners', 'description']
                            
                            missing_fields = [field for field in required_fields if field not in first_station]
                            
                            if not missing_fields:
                                self.log_test(
                                    f"Stations Endpoint - {country_code} Structure", 
                                    True, 
                                    f"Found {len(stations)} stations for {country_name} with correct structure",
                                    {"country": country_code, "station_count": len(stations), "sample": stations[0]}
                                )
                            else:
                                self.log_test(
                                    f"Stations Endpoint - {country_code} Structure", 
                                    False, 
                                    f"Missing required fields: {missing_fields}"
                                )
                        else:
                            self.log_test(
                                f"Stations Endpoint - {country_code} Data", 
                                False, 
                                f"No stations returned for {country_name}"
                            )
                    else:
                        self.log_test(
                            f"Stations Endpoint - {country_code} Response", 
                            False, 
                            f"Expected list, got: {type(stations)}"
                        )
                else:
                    self.log_test(
                        f"Stations Endpoint - {country_code} HTTP Status", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Stations Endpoint - {country_code} Request", 
                    False, 
                    f"Request error: {str(e)}"
                )
    
    async def test_stations_limit_parameter(self):
        """Test 4: Stations endpoint with limit parameter"""
        print("=== Testing Stations Limit Parameter ===")
        
        try:
            response = await self.client.get(f"{API_BASE}/stations/US?limit=10")
            
            if response.status_code == 200:
                stations = response.json()
                
                if isinstance(stations, list):
                    if len(stations) <= 10:
                        self.log_test(
                            "Stations Limit Parameter", 
                            True, 
                            f"Limit parameter working: requested 10, got {len(stations)} stations",
                            {"requested_limit": 10, "actual_count": len(stations)}
                        )
                    else:
                        self.log_test(
                            "Stations Limit Parameter", 
                            False, 
                            f"Limit not respected: requested 10, got {len(stations)} stations"
                        )
                else:
                    self.log_test(
                        "Stations Limit Parameter", 
                        False, 
                        f"Expected list, got: {type(stations)}"
                    )
            else:
                self.log_test(
                    "Stations Limit Parameter", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Stations Limit Parameter", 
                False, 
                f"Request error: {str(e)}"
            )
    
    async def test_invalid_country_code(self):
        """Test 5: Invalid country code handling"""
        print("=== Testing Invalid Country Code ===")
        
        try:
            response = await self.client.get(f"{API_BASE}/stations/INVALID")
            
            if response.status_code == 400:
                self.log_test(
                    "Invalid Country Code", 
                    True, 
                    "Correctly returned HTTP 400 for invalid country code",
                    {"status_code": response.status_code}
                )
            else:
                self.log_test(
                    "Invalid Country Code", 
                    False, 
                    f"Expected HTTP 400, got HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Invalid Country Code", 
                False, 
                f"Request error: {str(e)}"
            )
    
    async def test_station_validation(self):
        """Test 6: Station validation endpoint"""
        print("=== Testing Station Validation ===")
        
        try:
            test_station_id = "test-station-id"
            response = await self.client.get(f"{API_BASE}/stations/{test_station_id}/validate")
            
            if response.status_code == 200:
                validation_data = response.json()
                
                required_fields = ['valid', 'status', 'last_checked']
                missing_fields = [field for field in required_fields if field not in validation_data]
                
                if not missing_fields:
                    self.log_test(
                        "Station Validation", 
                        True, 
                        f"Validation endpoint working: {validation_data}",
                        validation_data
                    )
                else:
                    self.log_test(
                        "Station Validation", 
                        False, 
                        f"Missing required fields in validation response: {missing_fields}"
                    )
            else:
                self.log_test(
                    "Station Validation", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Station Validation", 
                False, 
                f"Request error: {str(e)}"
            )
    
    async def test_error_handling(self):
        """Test 7: Additional error handling scenarios"""
        print("=== Testing Error Handling ===")
        
        # Test single character country code
        try:
            response = await self.client.get(f"{API_BASE}/stations/U")
            
            if response.status_code == 400:
                self.log_test(
                    "Error Handling - Single Char Country", 
                    True, 
                    "Correctly rejected single character country code",
                    {"status_code": response.status_code}
                )
            else:
                self.log_test(
                    "Error Handling - Single Char Country", 
                    False, 
                    f"Expected HTTP 400, got HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Single Char Country", 
                False, 
                f"Request error: {str(e)}"
            )
        
        # Test three character country code
        try:
            response = await self.client.get(f"{API_BASE}/stations/USA")
            
            if response.status_code == 400:
                self.log_test(
                    "Error Handling - Three Char Country", 
                    True, 
                    "Correctly rejected three character country code",
                    {"status_code": response.status_code}
                )
            else:
                self.log_test(
                    "Error Handling - Three Char Country", 
                    False, 
                    f"Expected HTTP 400, got HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Three Char Country", 
                False, 
                f"Request error: {str(e)}"
            )
    
    async def run_all_tests(self):
        """Run all tests"""
        print(f"🚀 Starting Global Radio API Backend Tests")
        print(f"📡 Testing API at: {API_BASE}")
        print("=" * 60)
        
        # Run all test methods
        await self.test_basic_connectivity()
        await self.test_countries_endpoint()
        await self.test_stations_endpoint()
        await self.test_stations_limit_parameter()
        await self.test_invalid_country_code()
        await self.test_station_validation()
        await self.test_error_handling()
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print("\n🔍 FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  • {test}")
        
        print("\n" + "=" * 60)
        
        # Save detailed results to file
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100,
                    'failed_tests': self.failed_tests
                },
                'detailed_results': self.test_results,
                'test_timestamp': datetime.now().isoformat(),
                'api_base_url': API_BASE
            }, f, indent=2)
        
        print(f"📄 Detailed results saved to: /app/backend_test_results.json")
        
        return passed_tests == total_tests

async def main():
    """Main test runner"""
    tester = RadioAPITester()
    try:
        success = await tester.run_all_tests()
        return success
    finally:
        await tester.close()

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)