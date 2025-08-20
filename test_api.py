#!/usr/bin/env python3
"""
Test script for the Symptom Checker API
Run this script to test the API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running!")
        return False
    return True

def test_get_symptoms():
    """Test the get symptoms endpoint"""
    print("\n🔍 Testing get symptoms...")
    try:
        response = requests.get(f"{BASE_URL}/symptoms")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get symptoms passed!")
            print(f"   Available symptoms: {data['count']}")
            print(f"   Sample symptoms: {data['symptoms'][:5]}")
        else:
            print(f"❌ Get symptoms failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing get symptoms: {e}")

def test_check_symptoms(symptoms, expected_urgent=False):
    """Test the check symptoms endpoint"""
    print(f"\n🔍 Testing check symptoms: '{symptoms}'")
    try:
        data = {"input": symptoms}
        response = requests.post(f"{BASE_URL}/check-symptoms", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Check symptoms passed!")
            print(f"   Conditions: {result['conditions']}")
            print(f"   Urgent: {result['urgent']}")
            print(f"   Advice: {result['advice'][:100]}...")
            
            if result['urgent'] == expected_urgent:
                print("✅ Urgency level matches expectation!")
            else:
                print(f"⚠️  Urgency level unexpected. Expected: {expected_urgent}, Got: {result['urgent']}")
        else:
            print(f"❌ Check symptoms failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing check symptoms: {e}")

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test missing input
    try:
        response = requests.post(f"{BASE_URL}/check-symptoms", json={})
        if response.status_code == 400:
            print("✅ Missing input error handled correctly!")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing input: {e}")
    
    # Test empty input
    try:
        response = requests.post(f"{BASE_URL}/check-symptoms", json={"input": ""})
        if response.status_code == 400:
            print("✅ Empty input error handled correctly!")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing empty input: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Symptom Checker API Tests")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ API is not running. Please start the server with: python app.py")
        return
    
    # Test other endpoints
    test_get_symptoms()
    
    # Test various symptom combinations
    test_check_symptoms("I have a headache", expected_urgent=False)
    test_check_symptoms("I have chest pain and shortness of breath", expected_urgent=True)
    test_check_symptoms("I have a fever and cough", expected_urgent=False)
    test_check_symptoms("I have severe abdominal pain", expected_urgent=True)
    test_check_symptoms("I have dizziness and nausea", expected_urgent=False)
    
    # Test unknown symptoms
    test_check_symptoms("I have purple spots on my elbow", expected_urgent=False)
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 