"""
Dragon Breeding Engine
Implements Mendelian genetics for dragon breeding calculations.
"""

import random
import logging
from typing import Dict, List, Any
from models.dragon_traits import DragonTraits
from utils.genetics_calculator import GeneticsCalculator

logger = logging.getLogger(__name__)

class DragonBreedingEngine:
    """Main breeding engine for calculating dragon offspring traits."""
    
    def __init__(self):
        self.genetics_calculator = GeneticsCalculator()
        
        # Define trait inheritance patterns
        self.trait_patterns = {
            'scale_color': 'mendelian',  # Simple dominant/recessive
            'wing_size': 'mendelian',
            'fire_type': 'mendelian',
            'strength': 'quantitative',  # Numerical traits with some randomness
            'agility': 'quantitative',
            'intelligence': 'quantitative',
            'magic_affinity': 'quantitative'
        }
    
    def breed_dragons(self, parent1: DragonTraits, parent2: DragonTraits) -> DragonTraits:
        """
        Breed two dragons and return offspring with calculated traits.
        
        Args:
            parent1: First parent dragon
            parent2: Second parent dragon
            
        Returns:
            DragonTraits object representing the offspring
        """
        logger.info(f"Breeding dragons {parent1.dragon_id} and {parent2.dragon_id}")
        
        offspring_traits = {}
        
        # Get all possible traits from both parents
        all_traits = set(parent1.traits.keys()) | set(parent2.traits.keys())
        
        for trait_name in all_traits:
            offspring_traits[trait_name] = self._calculate_offspring_trait(
                trait_name,
                parent1.traits.get(trait_name),
                parent2.traits.get(trait_name)
            )
        
        # Generate new offspring dragon
        offspring = DragonTraits(
            dragon_id=f"offspring_{random.randint(10000, 99999)}",
            traits=offspring_traits
        )
        
        logger.info(f"Generated offspring {offspring.dragon_id} with traits: {offspring_traits}")
        return offspring
    
    def _calculate_offspring_trait(self, trait_name: str, parent1_trait: Any, parent2_trait: Any) -> Any:
        """Calculate a specific trait for offspring based on inheritance pattern."""
        
        if parent1_trait is None or parent2_trait is None:
            # If one parent is missing this trait, use the available one
            return parent1_trait or parent2_trait
        
        pattern = self.trait_patterns.get(trait_name, 'mendelian')
        
        if pattern == 'mendelian':
            return self._calculate_mendelian_trait(trait_name, parent1_trait, parent2_trait)
        elif pattern == 'quantitative':
            return self._calculate_quantitative_trait(trait_name, parent1_trait, parent2_trait)
        else:
            # Default to simple averaging for unknown patterns
            return self._calculate_average_trait(parent1_trait, parent2_trait)
    
    def _calculate_mendelian_trait(self, trait_name: str, parent1_alleles: List[str], parent2_alleles: List[str]) -> List[str]:
        """Calculate Mendelian inheritance for traits with dominant/recessive alleles."""
        
        if not isinstance(parent1_alleles, list) or not isinstance(parent2_alleles, list):
            # Convert single values to allele pairs if needed
            parent1_alleles = [parent1_alleles, parent1_alleles] if not isinstance(parent1_alleles, list) else parent1_alleles
            parent2_alleles = [parent2_alleles, parent2_alleles] if not isinstance(parent2_alleles, list) else parent2_alleles
        
        # Each parent contributes one random allele
        parent1_contribution = random.choice(parent1_alleles)
        parent2_contribution = random.choice(parent2_alleles)
        
        offspring_alleles = [parent1_contribution, parent2_contribution]
        
        # Sort to put dominant allele first (basic dominance hierarchy)
        offspring_alleles.sort(key=lambda x: self._get_allele_dominance(trait_name, x), reverse=True)
        
        return offspring_alleles
    
    def _calculate_quantitative_trait(self, trait_name: str, parent1_value: float, parent2_value: float) -> float:
        """Calculate quantitative traits (numerical values) with genetic variation."""
        
        # Average of parents with some random variation (±10%)
        average = (parent1_value + parent2_value) / 2
        variation = random.uniform(-0.1, 0.1) * average
        result = average + variation
        
        # Ensure result stays within reasonable bounds (0-100 for most traits)
        result = max(0, min(100, result))
        
        return round(result, 1)
    
    def _calculate_average_trait(self, trait1: Any, trait2: Any) -> Any:
        """Simple averaging for unknown trait types."""
        if isinstance(trait1, (int, float)) and isinstance(trait2, (int, float)):
            return (trait1 + trait2) / 2
        else:
            return random.choice([trait1, trait2])
    
    def _get_allele_dominance(self, trait_name: str, allele: str) -> int:
        """Get dominance value for allele ordering (higher = more dominant)."""
        
        dominance_hierarchy = {
            'scale_color': {
                'red': 5, 'blue': 4, 'green': 3, 'gold': 6, 'silver': 2, 'black': 1
            },
            'wing_size': {
                'large': 3, 'medium': 2, 'small': 1, 'huge': 4
            },
            'fire_type': {
                'flame': 3, 'ice': 2, 'lightning': 4, 'poison': 1, 'holy': 5
            }
        }
        
        trait_hierarchy = dominance_hierarchy.get(trait_name, {})
        return trait_hierarchy.get(allele, 0)
    
    def calculate_breeding_success_rate(self, parent1_data: Dict, parent2_data: Dict) -> float:
        """
        Calculate the probability of successful breeding based on parent compatibility.
        
        Args:
            parent1_data: Parent 1 data dictionary
            parent2_data: Parent 2 data dictionary
            
        Returns:
            Success rate as a percentage (0-100)
        """
        
        # Base success rate
        base_rate = 75.0
        
        # Factors that affect breeding success
        parent1_traits = parent1_data.get('traits', {})
        parent2_traits = parent2_data.get('traits', {})
        
        # Compatibility bonus for complementary traits
        compatibility_bonus = self._calculate_compatibility_bonus(parent1_traits, parent2_traits)
        
        # Health and vitality factors
        health_factor = self._calculate_health_factor(parent1_traits, parent2_traits)
        
        # Calculate final success rate
        success_rate = base_rate + compatibility_bonus + health_factor
        
        # Ensure rate stays within 0-100 range
        success_rate = max(10, min(95, success_rate))
        
        return round(success_rate, 1)
    
    def _calculate_compatibility_bonus(self, traits1: Dict, traits2: Dict) -> float:
        """Calculate compatibility bonus based on trait complementarity."""
        bonus = 0.0
        
        # Example: Different fire types create interesting combinations
        fire1 = traits1.get('fire_type', ['none'])[0] if isinstance(traits1.get('fire_type'), list) else traits1.get('fire_type', 'none')
        fire2 = traits2.get('fire_type', ['none'])[0] if isinstance(traits2.get('fire_type'), list) else traits2.get('fire_type', 'none')
        
        if fire1 != fire2:
            bonus += 5.0  # Different fire types = more interesting offspring
        
        # Size compatibility
        size1 = traits1.get('wing_size', ['medium'])[0] if isinstance(traits1.get('wing_size'), list) else traits1.get('wing_size', 'medium')
        size2 = traits2.get('wing_size', ['medium'])[0] if isinstance(traits2.get('wing_size'), list) else traits2.get('wing_size', 'medium')
        
        if size1 == size2:
            bonus += 3.0  # Similar sizes = better compatibility
        
        return bonus
    
    def _calculate_health_factor(self, traits1: Dict, traits2: Dict) -> float:
        """Calculate health factor based on parent vitality."""
        factor = 0.0
        
        # Higher strength and agility = healthier dragons
        strength1 = traits1.get('strength', 50)
        strength2 = traits2.get('strength', 50)
        avg_strength = (strength1 + strength2) / 2
        
        agility1 = traits1.get('agility', 50)
        agility2 = traits2.get('agility', 50)
        avg_agility = (agility1 + agility2) / 2
        
        # Bonus for high vitality parents
        if avg_strength > 80:
            factor += 5.0
        if avg_agility > 80:
            factor += 5.0
        
        # Penalty for low vitality parents
        if avg_strength < 30:
            factor -= 10.0
        if avg_agility < 30:
            factor -= 10.0
        
        return factor
