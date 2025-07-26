# Dragon Farm ML Service

A machine learning service for Dragon Farm that implements a breeding engine based on Mendelian genetics. This Flask-based service handles dragon breeding calculations and communicates with the .NET backend.

## 🐉 Features

- **Breeding Engine**: Calculate offspring traits using Mendelian genetics principles
- **Genetics Calculator**: Analyze trait probabilities and genetic patterns
- **REST API**: Clean endpoints for .NET backend communication
- **Trait Modeling**: Comprehensive dragon trait system with dominance hierarchies
- **Success Prediction**: Calculate breeding success rates based on parent compatibility

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)
- .NET backend running (for full integration)

### Installation

1. **Clone and navigate to the project**:

   ```bash
   cd dragon-farm-ml
   ```

2. **Set up virtual environment** (if not already done):

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   # source .venv/bin/activate    # On Unix/MacOS
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the service**:

   ```bash
   # Windows
   start.bat

   # Unix/MacOS
   chmod +x start.sh && ./start.sh

   # Or manually
   python app.py
   ```

The service will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check

```http
GET /health
```

Returns service status and information.

### Calculate Offspring

```http
POST /api/breeding/calculate
Content-Type: application/json

{
  "parent1": {
    "id": "dragon_001",
    "traits": {
      "scale_color": ["red", "blue"],
      "wing_size": ["large", "medium"],
      "fire_type": ["flame", "ice"],
      "strength": 85,
      "agility": 70,
      "intelligence": 90
    }
  },
  "parent2": {
    "id": "dragon_002",
    "traits": {
      "scale_color": ["blue", "green"],
      "wing_size": ["medium", "small"],
      "fire_type": ["ice", "lightning"],
      "strength": 75,
      "agility": 95,
      "intelligence": 80
    }
  }
}
```

### Analyze Genetics

```http
POST /api/genetics/analyze
Content-Type: application/json

{
  "parent1_alleles": ["red", "blue"],
  "parent2_alleles": ["blue", "green"],
  "trait_name": "scale_color"
}
```

### Predict Breeding Success

```http
POST /api/breeding/predict
Content-Type: application/json

{
  "parent1": { ... },
  "parent2": { ... }
}
```

## 🧬 Dragon Traits System

### Categorical Traits (Mendelian Inheritance)

- **Scale Color**: `red`, `blue`, `green`, `gold`, `silver`, `black`
- **Wing Size**: `small`, `medium`, `large`, `huge`
- **Fire Type**: `flame`, `ice`, `lightning`, `poison`, `holy`

### Quantitative Traits (Numerical with Variation)

- **Strength**: 0-100
- **Agility**: 0-100
- **Intelligence**: 0-100
- **Magic Affinity**: 0-100

### Dominance Hierarchy

```
Scale Color: gold > red > blue > green > silver > black
Wing Size: huge > large > medium > small
Fire Type: holy > lightning > flame > ice > poison
```

## 🔧 Configuration

Environment variables for customization:

```bash
# Flask Settings
FLASK_ENV=development
DEBUG=true
HOST=0.0.0.0
PORT=5000

# CORS Settings (for .NET backend)
CORS_ORIGINS=http://localhost:3000,http://localhost:7000

# .NET Backend Integration
DOTNET_BACKEND_URL=http://localhost:7000
DOTNET_API_KEY=your_api_key_here

# Breeding Engine Settings
ENABLE_MUTATIONS=true
MUTATION_RATE=0.05
MIN_BREEDING_SUCCESS_RATE=10.0
MAX_BREEDING_SUCCESS_RATE=95.0
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest test_dragon_farm.py

# Run with verbose output
pytest -v test_dragon_farm.py

# Run specific test class
pytest test_dragon_farm.py::TestBreedingEngine
```

## 🏗️ Project Structure

```
dragon-farm-ml/
├── app.py                 # Main Flask application
├── breeding_engine.py     # Core breeding logic
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── start.bat/start.sh    # Startup scripts
├── test_dragon_farm.py   # Test suite
├── models/
│   ├── __init__.py
│   └── dragon_traits.py  # Dragon trait modeling
└── utils/
    ├── __init__.py
    └── genetics_calculator.py  # Genetics calculations
```

## 🔗 Integration with .NET Backend

This service is designed to work seamlessly with your .NET backend:

1. **CORS Enabled**: Ready for cross-origin requests
2. **RESTful API**: Standard HTTP methods and JSON payloads
3. **Error Handling**: Consistent error responses
4. **Logging**: Comprehensive logging for debugging

### Example .NET Integration

```csharp
// Example C# code to call the breeding service
public async Task<DragonOffspring> BreedDragonsAsync(Dragon parent1, Dragon parent2)
{
    var request = new
    {
        parent1 = new { id = parent1.Id, traits = parent1.Traits },
        parent2 = new { id = parent2.Id, traits = parent2.Traits }
    };

    var response = await httpClient.PostAsJsonAsync(
        "http://localhost:5000/api/breeding/calculate",
        request
    );

    var result = await response.Content.ReadFromJsonAsync<BreedingResponse>();
    return result.Offspring;
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**: Change the `PORT` environment variable
2. **Import errors**: Ensure virtual environment is activated and dependencies installed
3. **CORS errors**: Check `CORS_ORIGINS` configuration
4. **Breeding calculations fail**: Verify parent trait data format

### Logs

Logs are output to console with timestamps. Adjust log level with `LOG_LEVEL` environment variable:

- `DEBUG`: Detailed information
- `INFO`: General information (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only

## 🚧 Future Enhancements

- [ ] Database integration for dragon lineage tracking
- [ ] Advanced genetic algorithms
- [ ] Mutation system implementation
- [ ] Breeding simulation endpoints
- [ ] Machine learning trait prediction
- [ ] gRPC support for high-performance communication
- [ ] Docker containerization

## 📄 License

This project is part of the Dragon Farm application suite.
