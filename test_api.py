"""
Example usage of Dragon Farm ML Service API
Run this script after starting the Flask service to test the breeding engine.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

def test_health_check():
    """Test the health check endpoint."""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service is healthy: {data['service']}")
            print(f"   Version: {data['version']}")
            print(f"   Status: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service. Make sure it's running on port 5000.")
        return False

def test_breeding_calculation():
    """Test the breeding calculation endpoint."""
    print("\n🐉 Testing breeding calculation...")
    
    # Sample dragon data
    breeding_data = {
        "parent1": {
            "id": "fire_drake_001",
            "traits": {
                "scale_color": ["red", "gold"],
                "wing_size": ["large", "huge"],
                "fire_type": ["flame", "lightning"],
                "strength": 92,
                "agility": 78,
                "intelligence": 85
            }
        },
        "parent2": {
            "id": "ice_serpent_002",
            "traits": {
                "scale_color": ["blue", "silver"],
                "wing_size": ["medium", "large"],
                "fire_type": ["ice", "holy"],
                "strength": 74,
                "agility": 95,
                "intelligence": 90
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/breeding/calculate",
            json=breeding_data,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            offspring = data["offspring"]
            
            print("✅ Breeding successful!")
            print(f"   Offspring ID: {offspring['dragon_id']}")
            print(f"   Description: {offspring['phenotype_description']}")
            print("   Traits:")
            for trait_name, trait_value in offspring['traits'].items():
                if isinstance(trait_value, list):
                    print(f"     {trait_name}: {trait_value[0]} (dominant), {trait_value[1]} (recessive)")
                else:
                    print(f"     {trait_name}: {trait_value}")
            
            return True
        else:
            print(f"❌ Breeding calculation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during breeding calculation: {e}")
        return False

def test_genetics_analysis():
    """Test the genetics analysis endpoint."""
    print("\n🧬 Testing genetics analysis...")
    
    genetics_data = {
        "parent1_alleles": ["red", "blue"],
        "parent2_alleles": ["gold", "green"],
        "trait_name": "scale_color"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/genetics/analyze",
            json=genetics_data,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            probabilities = data["probabilities"]
            
            print("✅ Genetics analysis successful!")
            print(f"   Trait: {data['trait_name']}")
            print("   Offspring probabilities:")
            for phenotype, probability in probabilities.items():
                print(f"     {phenotype}: {probability:.1f}%")
            
            return True
        else:
            print(f"❌ Genetics analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during genetics analysis: {e}")
        return False

def test_breeding_prediction():
    """Test the breeding success prediction endpoint."""
    print("\n📊 Testing breeding success prediction...")
    
    prediction_data = {
        "parent1": {
            "traits": {
                "fire_type": ["flame", "ice"],
                "wing_size": ["large", "medium"],
                "strength": 88,
                "agility": 76,
                "intelligence": 82
            }
        },
        "parent2": {
            "traits": {
                "fire_type": ["lightning", "holy"],
                "wing_size": ["huge", "large"],
                "strength": 79,
                "agility": 91,
                "intelligence": 87
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/breeding/predict",
            json=prediction_data,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            success_rate = data["breeding_success_rate"]
            
            print("✅ Breeding prediction successful!")
            print(f"   Success rate: {success_rate}%")
            
            if success_rate > 80:
                print("   🟢 Excellent breeding compatibility!")
            elif success_rate > 60:
                print("   🟡 Good breeding compatibility")
            elif success_rate > 40:
                print("   🟠 Moderate breeding compatibility")
            else:
                print("   🔴 Low breeding compatibility")
            
            return True
        else:
            print(f"❌ Breeding prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during breeding prediction: {e}")
        return False

def run_comprehensive_test():
    """Run all tests in sequence."""
    print("🐲 Dragon Farm ML Service - API Test Suite")
    print("=" * 50)
    
    # Wait a moment for service to be ready
    time.sleep(1)
    
    # Run tests
    tests = [
        test_health_check,
        test_breeding_calculation,
        test_genetics_analysis,
        test_breeding_prediction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Dragon Farm ML Service is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Integrate with your .NET backend")
        print("   2. Customize trait systems as needed")
        print("   3. Add more advanced breeding features")
    else:
        print("⚠️  Some tests failed. Check the service logs for details.")
    
    return passed == total

if __name__ == "__main__":
    run_comprehensive_test()
