"""
Dragon Farm ML Service - Breeding Engine
Main Flask application for handling dragon breeding calculations based on Mendelian genetics.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os

from breeding_engine import DragonBreedingEngine
from models.dragon_traits import DragonTraits
from utils.genetics_calculator import GeneticsCalculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for .NET backend communication

# Initialize breeding engine
breeding_engine = DragonBreedingEngine()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the ML service."""
    return jsonify({
        'status': 'healthy',
        'service': 'Dragon Farm ML Service',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/breeding/calculate', methods=['POST'])
def calculate_offspring():
    """
    Calculate offspring traits based on parent dragons using Mendelian genetics.
    
    Expected JSON payload:
    {
        "parent1": {
            "id": "dragon_id_1",
            "traits": {
                "scale_color": ["red", "blue"],  # dominant, recessive alleles
                "wing_size": ["large", "small"],
                "fire_type": ["flame", "ice"],
                "strength": 85,
                "agility": 70,
                "intelligence": 90
            }
        },
        "parent2": {
            "id": "dragon_id_2", 
            "traits": {
                "scale_color": ["blue", "green"],
                "wing_size": ["medium", "large"],
                "fire_type": ["ice", "flame"],
                "strength": 75,
                "agility": 95,
                "intelligence": 80
            }
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'parent1' not in data or 'parent2' not in data:
            return jsonify({'error': 'Missing parent data'}), 400
        
        parent1_data = data['parent1']
        parent2_data = data['parent2']
        
        # Create DragonTraits objects
        parent1 = DragonTraits(
            dragon_id=parent1_data.get('id'),
            traits=parent1_data.get('traits', {})
        )
        
        parent2 = DragonTraits(
            dragon_id=parent2_data.get('id'),
            traits=parent2_data.get('traits', {})
        )
        
        # Calculate offspring
        offspring = breeding_engine.breed_dragons(parent1, parent2)
        
        logger.info(f"Breeding calculation completed for parents {parent1.dragon_id} and {parent2.dragon_id}")
        
        return jsonify({
            'success': True,
            'offspring': offspring.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in breeding calculation: {str(e)}")
        return jsonify({'error': f'Breeding calculation failed: {str(e)}'}), 500

@app.route('/api/genetics/analyze', methods=['POST'])
def analyze_genetics():
    """
    Analyze genetic probability for specific trait combinations.
    
    Expected JSON payload:
    {
        "parent1_alleles": ["red", "blue"],
        "parent2_alleles": ["blue", "green"], 
        "trait_name": "scale_color"
    }
    """
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['parent1_alleles', 'parent2_alleles', 'trait_name']):
            return jsonify({'error': 'Missing required genetics data'}), 400
        
        calculator = GeneticsCalculator()
        probabilities = calculator.calculate_trait_probabilities(
            data['parent1_alleles'],
            data['parent2_alleles'],
            data['trait_name']
        )
        
        return jsonify({
            'success': True,
            'trait_name': data['trait_name'],
            'probabilities': probabilities,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in genetics analysis: {str(e)}")
        return jsonify({'error': f'Genetics analysis failed: {str(e)}'}), 500

@app.route('/api/breeding/predict', methods=['POST'])
def predict_breeding_success():
    """
    Predict breeding success rate based on parent compatibility.
    """
    try:
        data = request.get_json()
        
        if not data or 'parent1' not in data or 'parent2' not in data:
            return jsonify({'error': 'Missing parent data'}), 400
        
        success_rate = breeding_engine.calculate_breeding_success_rate(
            data['parent1'], 
            data['parent2']
        )
        
        return jsonify({
            'success': True,
            'breeding_success_rate': success_rate,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in breeding prediction: {str(e)}")
        return jsonify({'error': f'Breeding prediction failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Dragon Farm ML Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
