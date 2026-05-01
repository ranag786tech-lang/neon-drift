"""
Trust & Transparency Dashboard - Explainer Service

Core service for generating explanations of AI decisions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import random

from models import (
    Explanation, Factor, AlternativeOutcome, ImpactType,
    DecisionTrace, DecisionStep, FairnessMetric, 
    FairnessMetricType, FairnessAuditReport
)


class ExplainerService:
    """
    Service for generating human-readable explanations of AI decisions.
    
    This service takes raw AI model outputs and converts them into
    understandable explanations with factor weights, alternative outcomes,
    and fairness assessments.
    """
    
    def __init__(self):
        self.explanation_cache = {}
        self.trace_cache = {}
    
    def generate_explanation(
        self,
        decision_id: str,
        model_name: str,
        model_version: str,
        outcome: str,
        confidence: float,
        input_features: Dict[str, Any],
        model_weights: Optional[Dict[str, float]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Explanation:
        """
        Generate a comprehensive explanation for an AI decision.
        
        Args:
            decision_id: Unique identifier for the decision
            model_name: Name of the AI model
            model_version: Version of the model
            outcome: The decision outcome
            confidence: Model's confidence score (0-1)
            input_features: Input features used in the decision
            model_weights: Optional feature importance weights
            context: Additional context about the decision
            
        Returns:
            Explanation object with detailed breakdown
        """
        # Calculate factor influences
        factors = self._calculate_factors(
            input_features, 
            model_weights or {},
            outcome
        )
        
        # Generate alternative outcomes
        alternatives = self._generate_alternatives(
            factors, outcome, confidence
        )
        
        # Calculate fairness score
        fairness_score = self._assess_fairness(factors, context)
        
        # Generate natural language explanation
        explanation_text = self._generate_natural_language(
            factors, outcome, model_name
        )
        
        # Generate Urdu translation (placeholder - would use translation API)
        explanation_urdu = self._translate_to_urdu(explanation_text)
        
        explanation = Explanation(
            decision_id=decision_id,
            model_name=model_name,
            model_version=model_version,
            outcome=outcome,
            confidence=confidence,
            top_factors=factors,
            alternative_outcomes=alternatives,
            fairness_score=fairness_score,
            explanation_text=explanation_text,
            explanation_urdu=explanation_urdu,
            timestamp=datetime.now(timezone.utc),
            metadata=context or {}
        )
        
        # Cache for future retrieval
        self.explanation_cache[decision_id] = explanation
        
        return explanation
    
    def _calculate_factors(
        self,
        features: Dict[str, Any],
        weights: Dict[str, float],
        outcome: str
    ) -> List[Factor]:
        """Calculate the influence of each factor on the decision."""
        factors = []
        
        # Normalize weights
        total_weight = sum(weights.values()) if weights else 1.0
        if total_weight == 0:
            total_weight = 1.0
        
        for feature_name, feature_value in features.items():
            weight = weights.get(feature_name, 1.0 / len(features))
            normalized_weight = weight / total_weight
            
            # Determine impact direction (simplified logic)
            impact = self._determine_impact(feature_name, feature_value, outcome)
            
            # Generate description
            description = self._generate_factor_description(
                feature_name, feature_value, impact
            )
            
            factor = Factor(
                name=feature_name,
                weight=round(normalized_weight, 2),
                impact=impact,
                value=feature_value,
                description=description
            )
            factors.append(factor)
        
        # Sort by weight and return top factors
        factors.sort(key=lambda f: f.weight, reverse=True)
        return factors[:5]  # Top 5 factors
    
    def _determine_impact(
        self,
        feature_name: str,
        feature_value: Any,
        outcome: str
    ) -> ImpactType:
        """Determine if a factor had positive, negative, or neutral impact."""
        # Simplified logic - in production this would come from model internals
        if isinstance(feature_value, (int, float)):
            if feature_value > 0:
                return ImpactType.POSITIVE
            elif feature_value < 0:
                return ImpactType.NEGATIVE
            else:
                return ImpactType.NEUTRAL
        elif isinstance(feature_value, str):
            positive_keywords = ['excellent', 'good', 'high', 'stable', 'approved']
            negative_keywords = ['poor', 'bad', 'low', 'unstable', 'rejected']
            
            value_lower = feature_value.lower()
            if any(kw in value_lower for kw in positive_keywords):
                return ImpactType.POSITIVE
            elif any(kw in value_lower for kw in negative_keywords):
                return ImpactType.NEGATIVE
        
        return ImpactType.NEUTRAL
    
    def _generate_factor_description(
        self,
        feature_name: str,
        feature_value: Any,
        impact: ImpactType
    ) -> str:
        """Generate human-readable description of a factor's influence."""
        descriptions = {
            'credit_score': {
                ImpactType.POSITIVE: "Excellent credit history",
                ImpactType.NEGATIVE: "Poor credit history",
                ImpactType.NEUTRAL: "Average credit history"
            },
            'income_stability': {
                ImpactType.POSITIVE: "Stable income source",
                ImpactType.NEGATIVE: "Unstable income source",
                ImpactType.NEUTRAL: "Moderate income stability"
            },
            'debt_to_income': {
                ImpactType.POSITIVE: "Low debt burden",
                ImpactType.NEGATIVE: "High debt burden",
                ImpactType.NEUTRAL: "Moderate debt level"
            }
        }
        
        if feature_name in descriptions:
            return descriptions[feature_name].get(
                impact, 
                f"{feature_name}: {feature_value}"
            )
        
        return f"{feature_name}: {feature_value}"
    
    def _generate_alternatives(
        self,
        factors: List[Factor],
        outcome: str,
        confidence: float
    ) -> List[AlternativeOutcome]:
        """Generate possible alternative outcomes with conditions."""
        alternatives = []
        
        # Calculate probability of alternative outcome
        alt_probability = round(1.0 - confidence, 2)
        
        if alt_probability > 0.05:  # Only show if significant probability
            # Find the most influential factor
            if factors:
                top_factor = factors[0]
                
                # Generate condition for alternative outcome
                if top_factor.impact == ImpactType.POSITIVE:
                    condition = f"if {top_factor.name} was less favorable"
                elif top_factor.impact == ImpactType.NEGATIVE:
                    condition = f"if {top_factor.name} was more favorable"
                else:
                    condition = f"if {top_factor.name} had different value"
                
                # Determine alternative outcome
                alt_outcome = "rejected" if outcome == "approved" else "approved"
                
                alternative = AlternativeOutcome(
                    outcome=alt_outcome,
                    probability=alt_probability,
                    condition=condition,
                    confidence_interval=(
                        max(0, alt_probability - 0.05),
                        min(1, alt_probability + 0.05)
                    )
                )
                alternatives.append(alternative)
        
        return alternatives
    
    def _assess_fairness(
        self,
        factors: List[Factor],
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """Assess the fairness of the decision (0-1 scale)."""
        # Simplified fairness assessment
        # In production, this would use statistical parity, equal opportunity, etc.
        
        base_score = 0.85
        
        # Adjust based on factor diversity
        if len(factors) >= 3:
            base_score += 0.05
        
        # Adjust based on weight distribution (avoid single factor dominance)
        if factors and factors[0].weight < 0.6:
            base_score += 0.05
        
        # Check for sensitive attributes (simplified)
        sensitive_attrs = ['age', 'gender', 'race', 'ethnicity', 'religion']
        for factor in factors:
            if any(attr in factor.name.lower() for attr in sensitive_attrs):
                base_score -= 0.15  # Penalty for using sensitive attributes
        
        return min(1.0, max(0.0, base_score))
    
    def _generate_natural_language(
        self,
        factors: List[Factor],
        outcome: str,
        model_name: str
    ) -> str:
        """Generate natural language explanation."""
        if not factors:
            return f"The {model_name} model determined this outcome based on multiple factors."
        
        top_factor = factors[0]
        
        if len(factors) == 1:
            return (
                f"This decision was primarily influenced by {top_factor.name}. "
                f"{top_factor.description}."
            )
        elif len(factors) == 2:
            return (
                f"This decision was influenced by {top_factor.name} and {factors[1].name}. "
                f"{top_factor.description}, and {factors[1].description.lower()}."
            )
        else:
            factor_names = [f.name for f in factors[:3]]
            return (
                f"This decision was primarily influenced by {', '.join(factor_names)}. "
                f"{top_factor.description}."
            )
    
    def _translate_to_urdu(self, text: str) -> str:
        """
        Translate explanation to Urdu.
        
        Note: In production, this would call a translation API.
        For now, returns placeholder translations.
        """
        # Simple placeholder translations
        translations = {
            "This decision was primarily influenced by": "یہ فیصلہ بنیادی طور پر متاثر ہوا",
            "Excellent credit history": "بہترین کریڈٹ کی تاریخ",
            "Stable income source": "مستحکم آمدنی کا ذریعہ",
            "Low debt burden": "کم قرض کا بوجھ",
            "approved": "منظور شدہ",
            "rejected": "رد شد"
        }
        
        # In production, use proper translation service
        return text  # Placeholder
    
    def get_explanation(self, decision_id: str) -> Optional[Explanation]:
        """Retrieve a cached explanation by decision ID."""
        return self.explanation_cache.get(decision_id)
    
    def list_explanations(self) -> List[Explanation]:
        """List all cached explanations."""
        return list(self.explanation_cache.values())


# Example usage
if __name__ == "__main__":
    service = ExplainerService()
    
    # Simulate an AI decision
    explanation = service.generate_explanation(
        decision_id="dec_789012",
        model_name="loan_approval_model",
        model_version="v2.3.1",
        outcome="approved",
        confidence=0.87,
        input_features={
            "credit_score": 750,
            "income_stability": "5 years continuous employment",
            "debt_to_income": 0.35,
            "employment_status": "full-time"
        },
        model_weights={
            "credit_score": 0.45,
            "income_stability": 0.32,
            "debt_to_income": 0.23
        },
        context={"user_id": "user_123", "request_date": "2024-01-15"}
    )
    
    print("Generated Explanation:")
    print("=" * 50)
    print(explanation.to_dict())
    print("\n" + "=" * 50)
    print(f"English: {explanation.explanation_text}")
    print(f"Urdu: {explanation.explanation_urdu}")
