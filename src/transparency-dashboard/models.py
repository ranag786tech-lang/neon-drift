"""
Trust & Transparency Dashboard - Core Data Models

This module defines the data structures for AI decision explanations,
decision traces, and fairness metrics.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ImpactType(Enum):
    """Impact of a factor on the decision outcome."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class FairnessMetricType(Enum):
    """Types of fairness metrics to track."""
    STATISTICAL_PARITY = "statistical_parity"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    PREDICTIVE_PARITY = "predictive_parity"
    INDIVIDUAL_FAIRNESS = "individual_fairness"


@dataclass
class Factor:
    """Represents a single factor influencing an AI decision."""
    name: str
    weight: float  # 0.0 to 1.0
    impact: ImpactType
    value: Any
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor": self.name,
            "weight": self.weight,
            "impact": self.impact.value,
            "value": self.value,
            "description": self.description
        }


@dataclass
class AlternativeOutcome:
    """Represents a possible alternative decision outcome."""
    outcome: str
    probability: float
    condition: str
    confidence_interval: Optional[tuple] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "outcome": self.outcome,
            "probability": self.probability,
            "condition": self.condition,
            "confidence_interval": self.confidence_interval
        }


@dataclass
class Explanation:
    """Complete explanation of an AI decision."""
    decision_id: str
    model_name: str
    model_version: str
    outcome: str
    confidence: float
    top_factors: List[Factor]
    alternative_outcomes: List[AlternativeOutcome]
    fairness_score: float
    explanation_text: str
    explanation_urdu: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "top_factors": [f.to_dict() for f in self.top_factors],
            "alternative_outcomes": [a.to_dict() for a in self.alternative_outcomes],
            "fairness_score": self.fairness_score,
            "explanation_text": self.explanation_text,
            "explanation_urdu": self.explanation_urdu,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class DecisionStep:
    """A single step in the decision-making process."""
    step_number: int
    operation: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_number": self.step_number,
            "operation": self.operation,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class DecisionTrace:
    """Complete trace of how a decision was made."""
    decision_id: str
    model_name: str
    initial_input: Dict[str, Any]
    final_output: Dict[str, Any]
    steps: List[DecisionStep]
    total_processing_time_ms: float
    data_sources_used: List[str]
    preprocessing_applied: List[str]
    postprocessing_applied: List[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "model_name": self.model_name,
            "initial_input": self.initial_input,
            "final_output": self.final_output,
            "steps": [s.to_dict() for s in self.steps],
            "total_processing_time_ms": self.total_processing_time_ms,
            "data_sources_used": self.data_sources_used,
            "preprocessing_applied": self.preprocessing_applied,
            "postprocessing_applied": self.postprocessing_applied,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class FairnessMetric:
    """A single fairness metric measurement."""
    metric_type: FairnessMetricType
    value: float
    threshold: float
    passed: bool
    demographic_groups: List[str]
    breakdown: Dict[str, float]
    sample_size: int
    confidence_interval: tuple
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_type": self.metric_type.value,
            "value": self.value,
            "threshold": self.threshold,
            "passed": self.passed,
            "demographic_groups": self.demographic_groups,
            "breakdown": self.breakdown,
            "sample_size": self.sample_size,
            "confidence_interval": self.confidence_interval,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class FairnessAuditReport:
    """Complete fairness audit report for a model or set of decisions."""
    audit_id: str
    model_name: Optional[str]
    decision_ids: List[str]
    audit_date: datetime
    overall_fairness_score: float
    metrics: List[FairnessMetric]
    biases_detected: List[Dict[str, Any]]
    recommendations: List[str]
    compliance_status: str  # "COMPLIANT", "NON_COMPLIANT", "REVIEW_NEEDED"
    auditor: str  # Human or automated system
    detailed_findings: str
    executive_summary: str
    executive_summary_urdu: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "model_name": self.model_name,
            "decision_ids": self.decision_ids,
            "audit_date": self.audit_date.isoformat(),
            "overall_fairness_score": self.overall_fairness_score,
            "metrics": [m.to_dict() for m in self.metrics],
            "biases_detected": self.biases_detected,
            "recommendations": self.recommendations,
            "compliance_status": self.compliance_status,
            "auditor": self.auditor,
            "detailed_findings": self.detailed_findings,
            "executive_summary": self.executive_summary,
            "executive_summary_urdu": self.executive_summary_urdu
        }


# Example usage and test data
def create_sample_explanation() -> Explanation:
    """Create a sample explanation for testing purposes."""
    return Explanation(
        decision_id="dec_123456",
        model_name="loan_approval_model",
        model_version="v2.3.1",
        outcome="approved",
        confidence=0.87,
        top_factors=[
            Factor(
                name="credit_score",
                weight=0.45,
                impact=ImpactType.POSITIVE,
                value=750,
                description="Excellent credit history"
            ),
            Factor(
                name="income_stability",
                weight=0.32,
                impact=ImpactType.POSITIVE,
                value="5 years continuous employment",
                description="Stable income source"
            ),
            Factor(
                name="debt_to_income",
                weight=0.23,
                impact=ImpactType.NEUTRAL,
                value=0.35,
                description="Moderate debt level"
            )
        ],
        alternative_outcomes=[
            AlternativeOutcome(
                outcome="rejected",
                probability=0.13,
                condition="if credit score was below 650"
            )
        ],
        fairness_score=0.94,
        explanation_text="This loan was approved primarily due to excellent credit history and stable income.",
        explanation_urdu="یہ قرض بنیادی طور پر بہترین کریڈٹ کی تاریخ اور مستحکم آمدنی کی وجہ سے منظور کیا گیا۔"
    )


if __name__ == "__main__":
    # Test the models
    sample = create_sample_explanation()
    print("Sample Explanation:")
    print(sample.to_dict())
