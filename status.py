"""
Dragon Farm ML Service Status Dashboard
A simple script to check the status of the ML service and show available endpoints.
"""

import os
import sys
import time
from datetime import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the service header."""
    print("🐲" + "="*60 + "🐲")
    print("         DRAGON FARM ML SERVICE - STATUS DASHBOARD")
    print("🐲" + "="*60 + "🐲")
    print()

def print_service_info():
    """Print basic service information."""
    print("📊 SERVICE INFORMATION")
    print("-" * 30)
    print(f"🌐 URL: http://localhost:5000")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print()

def print_endpoints():
    """Print available API endpoints."""
    print("🔗 AVAILABLE ENDPOINTS")
    print("-" * 30)
    endpoints = [
        ("GET", "/health", "Service health check"),
        ("POST", "/api/breeding/calculate", "Calculate dragon offspring"),
        ("POST", "/api/genetics/analyze", "Analyze trait genetics"),
        ("POST", "/api/breeding/predict", "Predict breeding success")
    ]
    
    for method, endpoint, description in endpoints:
        print(f"  {method:4} {endpoint:25} - {description}")
    print()

def print_example_usage():
    """Print example usage instructions."""
    print("💡 QUICK START")
    print("-" * 30)
    print("1. Start the service:")
    print("   Windows: start.bat")
    print("   Unix:    ./start.sh")
    print("   Manual:  python app.py")
    print()
    print("2. Test the API:")
    print("   python test_api.py")
    print()
    print("3. Check health:")
    print("   curl http://localhost:5000/health")
    print()

def print_integration_info():
    """Print .NET integration information."""
    print("🔗 .NET BACKEND INTEGRATION")
    print("-" * 30)
    print("• CORS enabled for cross-origin requests")
    print("• JSON request/response format")
    print("• RESTful API design")
    print("• Error handling with HTTP status codes")
    print()
    print("Example C# request:")
    print("  var response = await httpClient.PostAsJsonAsync(")
    print("    \"http://localhost:5000/api/breeding/calculate\", request);")
    print()

def print_trait_system():
    """Print information about the trait system."""
    print("🧬 DRAGON TRAIT SYSTEM")
    print("-" * 30)
    print("Categorical Traits (Mendelian):")
    print("  • Scale Color: red, blue, green, gold, silver, black")
    print("  • Wing Size: small, medium, large, huge")
    print("  • Fire Type: flame, ice, lightning, poison, holy")
    print()
    print("Quantitative Traits (0-100):")
    print("  • Strength, Agility, Intelligence, Magic Affinity")
    print()
    print("Dominance Hierarchy:")
    print("  • Gold > Red > Blue > Green > Silver > Black")
    print("  • Huge > Large > Medium > Small")
    print("  • Holy > Lightning > Flame > Ice > Poison")
    print()

def print_footer():
    """Print footer information."""
    print("🔧 TROUBLESHOOTING")
    print("-" * 30)
    print("• Port in use: Change PORT environment variable")
    print("• Import errors: Activate virtual environment")
    print("• CORS issues: Check CORS_ORIGINS setting")
    print()
    print("📚 For detailed documentation, see README.md")
    print()
    print("🐲" + "="*60 + "🐲")

def main():
    """Main dashboard display."""
    clear_screen()
    print_header()
    print_service_info()
    print_endpoints()
    print_example_usage()
    print_integration_info()
    print_trait_system()
    print_footer()

if __name__ == "__main__":
    main()
