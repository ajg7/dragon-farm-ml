"""
Basic tests for Dragon Farm ML Service
"""

import pytest
import json
from app import app
from models.dragon_traits import DragonTraits
from utils.genetics_calculator import GeneticsCalculator
from breeding_engine import DragonBreedingEngine

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_dragon_data():
    """Sample dragon data for testing."""
    return {
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

class TestFlaskApp:
    """Test the Flask application endpoints."""
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_breeding_calculation(self, client, sample_dragon_data):
        """Test the breeding calculation endpoint."""
        response = client.post('/api/breeding/calculate', 
                             json=sample_dragon_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'offspring' in data
        assert 'dragon_id' in data['offspring']
        assert 'traits' in data['offspring']
    
    def test_genetics_analysis(self, client):
        """Test the genetics analysis endpoint."""
        genetics_data = {
            "parent1_alleles": ["red", "blue"],
            "parent2_alleles": ["blue", "green"],
            "trait_name": "scale_color"
        }
        
        response = client.post('/api/genetics/analyze',
                             json=genetics_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'probabilities' in data
        assert data['trait_name'] == 'scale_color'
    
    def test_breeding_prediction(self, client, sample_dragon_data):
        """Test the breeding success prediction endpoint."""
        response = client.post('/api/breeding/predict',
                             json=sample_dragon_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'breeding_success_rate' in data
        assert 0 <= data['breeding_success_rate'] <= 100

class TestDragonTraits:
    """Test the DragonTraits model."""
    
    def test_dragon_traits_creation(self):
        """Test creating a DragonTraits instance."""
        traits = {
            "scale_color": ["red", "blue"],
            "strength": 85,
            "agility": 70
        }
        
        dragon = DragonTraits("test_dragon", traits)
        
        assert dragon.dragon_id == "test_dragon"
        assert dragon.get_dominant_trait("scale_color") == "red"
        assert dragon.get_trait_value("strength") == 85
    
    def test_trait_normalization(self):
        """Test that traits are normalized correctly."""
        traits = {
            "scale_color": "red",  # Should become ["red", "red"]
            "wing_size": ["large"]  # Should become ["large", "large"]
        }
        
        dragon = DragonTraits("test_dragon", traits)
        
        assert dragon.traits["scale_color"] == ["red", "red"]
        assert dragon.traits["wing_size"] == ["large", "large"]
    
    def test_homozygous_detection(self):
        """Test detection of homozygous traits."""
        traits = {
            "scale_color": ["red", "red"],  # Homozygous
            "wing_size": ["large", "small"]  # Heterozygous
        }
        
        dragon = DragonTraits("test_dragon", traits)
        
        assert dragon.is_homozygous("scale_color") is True
        assert dragon.is_homozygous("wing_size") is False

class TestGeneticsCalculator:
    """Test the genetics calculator."""
    
    def test_trait_probability_calculation(self):
        """Test calculating trait probabilities."""
        calculator = GeneticsCalculator()
        
        probabilities = calculator.calculate_trait_probabilities(
            ["red", "blue"],
            ["blue", "green"],
            "scale_color"
        )
        
        assert isinstance(probabilities, dict)
        assert sum(probabilities.values()) == 100.0  # Should sum to 100%
    
    def test_punnett_square_generation(self):
        """Test Punnett square generation."""
        calculator = GeneticsCalculator()
        
        result = calculator.calculate_punnett_square(
            ["A", "a"],
            ["A", "a"]
        )
        
        assert 'grid' in result
        assert 'genotype_ratios' in result
        assert result['total_offspring'] == 4

class TestBreedingEngine:
    """Test the breeding engine."""
    
    def test_dragon_breeding(self):
        """Test breeding two dragons."""
        engine = DragonBreedingEngine()
        
        parent1 = DragonTraits("parent1", {
            "scale_color": ["red", "blue"],
            "strength": 85,
            "agility": 70
        })
        
        parent2 = DragonTraits("parent2", {
            "scale_color": ["blue", "green"],
            "strength": 75,
            "agility": 95
        })
        
        offspring = engine.breed_dragons(parent1, parent2)
        
        assert offspring.dragon_id.startswith("offspring_")
        assert "scale_color" in offspring.traits
        assert "strength" in offspring.traits
        assert "agility" in offspring.traits
    
    def test_breeding_success_calculation(self):
        """Test breeding success rate calculation."""
        engine = DragonBreedingEngine()
        
        parent1_data = {
            "traits": {
                "fire_type": ["flame", "ice"],
                "strength": 85,
                "agility": 70
            }
        }
        
        parent2_data = {
            "traits": {
                "fire_type": ["ice", "lightning"],
                "strength": 75,
                "agility": 95
            }
        }
        
        success_rate = engine.calculate_breeding_success_rate(parent1_data, parent2_data)
        
        assert 10 <= success_rate <= 95

if __name__ == '__main__':
    pytest.main([__file__])
