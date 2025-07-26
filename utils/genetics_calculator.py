"""
Genetics Calculator
Implements Mendelian genetics calculations for dragon breeding.
"""

import random
from typing import List, Dict, Tuple, Any
from collections import Counter
import itertools

class GeneticsCalculator:
    """
    Handles genetic calculations based on Mendelian inheritance principles.
    """
    
    def __init__(self):
        # Define dominance relationships for different traits
        self.dominance_hierarchy = {
            'scale_color': {
                'gold': 6,      # Most dominant
                'red': 5,
                'blue': 4,
                'green': 3,
                'silver': 2,
                'black': 1      # Most recessive
            },
            'wing_size': {
                'huge': 4,
                'large': 3,
                'medium': 2,
                'small': 1
            },
            'fire_type': {
                'holy': 5,     # Most dominant
                'lightning': 4,
                'flame': 3,
                'ice': 2,
                'poison': 1    # Most recessive
            }
        }
    
    def calculate_trait_probabilities(self, parent1_alleles: List[str], 
                                    parent2_alleles: List[str], 
                                    trait_name: str) -> Dict[str, float]:
        """
        Calculate the probability of each possible phenotype from a cross.
        
        Args:
            parent1_alleles: List of alleles for parent 1 [dominant, recessive]
            parent2_alleles: List of alleles for parent 2 [dominant, recessive]
            trait_name: Name of the trait being analyzed
            
        Returns:
            Dictionary mapping phenotypes to their probabilities
        """
        
        # Generate all possible offspring genotype combinations
        possible_offspring = []
        
        for p1_allele in parent1_alleles:
            for p2_allele in parent2_alleles:
                offspring_genotype = [p1_allele, p2_allele]
                # Sort by dominance to determine phenotype
                offspring_genotype.sort(
                    key=lambda x: self._get_dominance_value(trait_name, x), 
                    reverse=True
                )
                possible_offspring.append(offspring_genotype)
        
        # Count phenotypes (dominant allele determines phenotype)
        phenotype_counts = Counter()
        for genotype in possible_offspring:
            phenotype = genotype[0]  # Most dominant allele
            phenotype_counts[phenotype] += 1
        
        # Convert counts to probabilities
        total_outcomes = len(possible_offspring)
        probabilities = {}
        for phenotype, count in phenotype_counts.items():
            probabilities[phenotype] = (count / total_outcomes) * 100
        
        return probabilities
    
    def predict_offspring_genotypes(self, parent1_alleles: List[str], 
                                  parent2_alleles: List[str]) -> List[Tuple[str, str, float]]:
        """
        Predict all possible offspring genotypes with their probabilities.
        
        Args:
            parent1_alleles: Alleles from parent 1
            parent2_alleles: Alleles from parent 2
            
        Returns:
            List of tuples (allele1, allele2, probability)
        """
        
        genotype_counts = Counter()
        
        # Calculate all possible combinations
        for p1_allele in parent1_alleles:
            for p2_allele in parent2_alleles:
                # Create genotype tuple (sorted for consistency)
                genotype = tuple(sorted([p1_allele, p2_allele]))
                genotype_counts[genotype] += 1
        
        # Convert to probabilities
        total = sum(genotype_counts.values())
        results = []
        
        for genotype, count in genotype_counts.items():
            probability = (count / total) * 100
            results.append((genotype[0], genotype[1], probability))
        
        # Sort by probability (highest first)
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results
    
    def calculate_punnett_square(self, parent1_alleles: List[str], 
                               parent2_alleles: List[str]) -> Dict[str, Any]:
        """
        Generate a complete Punnett square analysis.
        
        Args:
            parent1_alleles: Alleles from parent 1
            parent2_alleles: Alleles from parent 2
            
        Returns:
            Dictionary containing Punnett square data and analysis
        """
        
        # Create the grid
        grid = []
        for p1_allele in parent1_alleles:
            row = []
            for p2_allele in parent2_alleles:
                offspring = [p1_allele, p2_allele]
                row.append(offspring)
            grid.append(row)
        
        # Flatten for analysis
        all_offspring = [item for row in grid for item in row]
        
        # Count genotypes
        genotype_counts = Counter()
        for offspring in all_offspring:
            genotype_key = tuple(sorted(offspring))
            genotype_counts[genotype_key] += 1
        
        # Calculate genotype ratios
        total_offspring = len(all_offspring)
        genotype_ratios = {}
        for genotype, count in genotype_counts.items():
            ratio = count / total_offspring
            genotype_ratios[f"{genotype[0]}{genotype[1]}"] = {
                'count': count,
                'ratio': ratio,
                'percentage': ratio * 100
            }
        
        return {
            'grid': grid,
            'parent1_alleles': parent1_alleles,
            'parent2_alleles': parent2_alleles,
            'total_offspring': total_offspring,
            'genotype_ratios': genotype_ratios,
            'unique_genotypes': len(genotype_counts)
        }
    
    def determine_trait_dominance(self, trait_name: str, allele1: str, allele2: str) -> str:
        """
        Determine which allele is dominant between two alleles.
        
        Args:
            trait_name: Name of the trait
            allele1: First allele
            allele2: Second allele
            
        Returns:
            The dominant allele
        """
        
        dom1 = self._get_dominance_value(trait_name, allele1)
        dom2 = self._get_dominance_value(trait_name, allele2)
        
        return allele1 if dom1 >= dom2 else allele2
    
    def calculate_inbreeding_coefficient(self, parent1_id: str, parent2_id: str, 
                                       pedigree: Dict[str, List[str]]) -> float:
        """
        Calculate the inbreeding coefficient for offspring of two parents.
        This is a simplified version for demonstration.
        
        Args:
            parent1_id: ID of first parent
            parent2_id: ID of second parent
            pedigree: Dictionary mapping dragon ID to list of parent IDs
            
        Returns:
            Inbreeding coefficient (0.0 to 1.0)
        """
        
        # Find common ancestors (simplified approach)
        p1_ancestors = self._get_ancestors(parent1_id, pedigree, depth=3)
        p2_ancestors = self._get_ancestors(parent2_id, pedigree, depth=3)
        
        common_ancestors = set(p1_ancestors) & set(p2_ancestors)
        
        if not common_ancestors:
            return 0.0
        
        # Simple calculation: more common ancestors = higher inbreeding
        # Real calculation would consider the path lengths
        base_coefficient = len(common_ancestors) * 0.1
        
        # Check for immediate family relationships
        if parent1_id in p2_ancestors or parent2_id in p1_ancestors:
            base_coefficient += 0.25  # Parent-offspring
        
        return min(base_coefficient, 1.0)
    
    def _get_dominance_value(self, trait_name: str, allele: str) -> int:
        """Get the dominance value for an allele (higher = more dominant)."""
        
        if trait_name in self.dominance_hierarchy:
            return self.dominance_hierarchy[trait_name].get(allele, 0)
        else:
            # For unknown traits, use alphabetical order as a fallback
            return ord(allele[0].lower()) if allele else 0
    
    def _get_ancestors(self, dragon_id: str, pedigree: Dict[str, List[str]], depth: int) -> List[str]:
        """
        Get ancestors of a dragon up to specified depth.
        
        Args:
            dragon_id: ID of the dragon
            pedigree: Pedigree dictionary
            depth: How many generations to go back
            
        Returns:
            List of ancestor IDs
        """
        
        if depth <= 0 or dragon_id not in pedigree:
            return []
        
        ancestors = []
        parents = pedigree.get(dragon_id, [])
        
        for parent in parents:
            ancestors.append(parent)
            # Recursively get ancestors of parents
            ancestors.extend(self._get_ancestors(parent, pedigree, depth - 1))
        
        return list(set(ancestors))  # Remove duplicates
    
    def calculate_genetic_diversity(self, population_traits: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate genetic diversity metrics for a population.
        
        Args:
            population_traits: List of trait dictionaries for the population
            
        Returns:
            Dictionary with diversity metrics
        """
        
        if not population_traits:
            return {'overall_diversity': 0.0, 'trait_diversity': {}}
        
        trait_diversity = {}
        
        # Analyze each trait type
        all_trait_names = set()
        for traits in population_traits:
            all_trait_names.update(traits.keys())
        
        for trait_name in all_trait_names:
            trait_values = []
            for traits in population_traits:
                if trait_name in traits:
                    value = traits[trait_name]
                    if isinstance(value, list):
                        trait_values.extend(value)
                    else:
                        trait_values.append(value)
            
            # Calculate diversity as ratio of unique values to total values
            if trait_values:
                unique_values = len(set(trait_values))
                total_values = len(trait_values)
                diversity = unique_values / total_values
                trait_diversity[trait_name] = diversity
        
        # Overall diversity is the average of individual trait diversities
        overall_diversity = sum(trait_diversity.values()) / len(trait_diversity) if trait_diversity else 0.0
        
        return {
            'overall_diversity': overall_diversity,
            'trait_diversity': trait_diversity,
            'population_size': len(population_traits)
        }
