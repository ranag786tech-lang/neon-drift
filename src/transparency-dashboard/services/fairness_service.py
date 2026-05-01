"""
Trust & Transparency Dashboard - Fairness Service

Service for detecting bias, calculating fairness metrics, and generating audit reports.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import random
import sys
import os

# Import from local models module
from models import (
    FairnessMetric, FairnessMetricType, FairnessAuditReport,
    Explanation, ImpactType
)


class FairnessService:
    """
    Service for fairness auditing and bias detection.
    
    This service calculates various fairness metrics, detects potential biases,
    and generates comprehensive audit reports for AI models and decisions.
    """
    
    def __init__(self):
        self.metrics_cache = {}
        self.audit_cache = {}
        self.model_summaries = {}
    
    def run_audit(
        self,
        model_name: Optional[str] = None,
        decision_ids: Optional[List[str]] = None,
        metric_types: Optional[List[FairnessMetricType]] = None
    ) -> FairnessAuditReport:
        """
        Run a comprehensive fairness audit on specified models or decisions.
        
        Args:
            model_name: Name of the model to audit
            decision_ids: List of decision IDs to audit
            metric_types: Types of fairness metrics to calculate
            
        Returns:
            FairnessAuditReport with complete audit findings
        """
        audit_id = f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Default to all metric types if not specified
        if metric_types is None:
            metric_types = list(FairnessMetricType)
        
        # Calculate fairness metrics
        metrics = self._calculate_metrics(model_name, decision_ids, metric_types)
        
        # Detect biases
        biases_detected = self._detect_biases(metrics, model_name, decision_ids)
        
        # Calculate overall fairness score
        overall_score = self._calculate_overall_score(metrics)
        
        # Determine compliance status
        compliance_status = self._determine_compliance(metrics, biases_detected)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(biases_detected, metrics)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            model_name, overall_score, compliance_status, len(biases_detected)
        )
        
        # Generate Urdu translation (placeholder)
        executive_summary_urdu = self._translate_to_urdu(executive_summary)
        
        # Generate detailed findings
        detailed_findings = self._generate_detailed_findings(
            metrics, biases_detected, recommendations
        )
        
        report = FairnessAuditReport(
            audit_id=audit_id,
            model_name=model_name,
            decision_ids=decision_ids or [],
            audit_date=datetime.now(timezone.utc),
            overall_fairness_score=overall_score,
            metrics=metrics,
            biases_detected=biases_detected,
            recommendations=recommendations,
            compliance_status=compliance_status,
            auditor="Automated Fairness Service v1.0",
            detailed_findings=detailed_findings,
            executive_summary=executive_summary,
            executive_summary_urdu=executive_summary_urdu
        )
        
        # Cache the report
        self.audit_cache[audit_id] = report
        
        # Update model summary
        if model_name:
            self._update_model_summary(model_name, report)
        
        return report
    
    def _calculate_metrics(
        self,
        model_name: Optional[str],
        decision_ids: Optional[List[str]],
        metric_types: List[FairnessMetricType]
    ) -> List[FairnessMetric]:
        """Calculate fairness metrics for the specified scope."""
        metrics = []
        
        for metric_type in metric_types:
            metric = self._calculate_single_metric(metric_type, model_name, decision_ids)
            metrics.append(metric)
        
        return metrics
    
    def _calculate_single_metric(
        self,
        metric_type: FairnessMetricType,
        model_name: Optional[str],
        decision_ids: Optional[List[str]]
    ) -> FairnessMetric:
        """Calculate a single fairness metric."""
        # Simulated calculation - in production this would use real statistical analysis
        
        demographic_groups = ["group_a", "group_b", "group_c"]
        
        # Generate realistic-looking metrics based on type
        if metric_type == FairnessMetricType.STATISTICAL_PARITY:
            value = random.uniform(0.85, 0.98)
            threshold = 0.80
            breakdown = {
                "group_a": random.uniform(0.80, 0.95),
                "group_b": random.uniform(0.80, 0.95),
                "group_c": random.uniform(0.80, 0.95)
            }
        elif metric_type == FairnessMetricType.EQUAL_OPPORTUNITY:
            value = random.uniform(0.82, 0.97)
            threshold = 0.80
            breakdown = {
                "group_a": random.uniform(0.78, 0.93),
                "group_b": random.uniform(0.78, 0.93),
                "group_c": random.uniform(0.78, 0.93)
            }
        elif metric_type == FairnessMetricType.PREDICTIVE_PARITY:
            value = random.uniform(0.83, 0.96)
            threshold = 0.80
            breakdown = {
                "group_a": random.uniform(0.79, 0.94),
                "group_b": random.uniform(0.79, 0.94),
                "group_c": random.uniform(0.79, 0.94)
            }
        else:  # INDIVIDUAL_FAIRNESS
            value = random.uniform(0.86, 0.99)
            threshold = 0.85
            breakdown = {
                "group_a": random.uniform(0.82, 0.97),
                "group_b": random.uniform(0.82, 0.97),
                "group_c": random.uniform(0.82, 0.97)
            }
        
        passed = value >= threshold
        sample_size = random.randint(1000, 10000)
        confidence_interval = (
            round(value - 0.03, 3),
            round(value + 0.03, 3)
        )
        
        metric = FairnessMetric(
            metric_type=metric_type,
            value=round(value, 3),
            threshold=threshold,
            passed=passed,
            demographic_groups=demographic_groups,
            breakdown={k: round(v, 3) for k, v in breakdown.items()},
            sample_size=sample_size,
            confidence_interval=confidence_interval,
            timestamp=datetime.now(timezone.utc)
        )
        
        return metric
    
    def _detect_biases(
        self,
        metrics: List[FairnessMetric],
        model_name: Optional[str],
        decision_ids: Optional[List[str]]
    ) -> List[Dict[str, Any]]:
        """Detect potential biases in the model or decisions."""
        biases = []
        
        # Check for statistical parity violations
        stat_parity = next(
            (m for m in metrics if m.metric_type == FairnessMetricType.STATISTICAL_PARITY), 
            None
        )
        if stat_parity and not stat_parity.passed:
            biases.append({
                "type": "statistical_parity_violation",
                "severity": "medium",
                "description": "Statistical parity threshold not met across demographic groups",
                "affected_groups": stat_parity.demographic_groups,
                "metric_value": stat_parity.value,
                "threshold": stat_parity.threshold,
                "recommendation": "Review feature selection and consider reweighting"
            })
        
        # Check for equal opportunity violations
        eq_opp = next(
            (m for m in metrics if m.metric_type == FairnessMetricType.EQUAL_OPPORTUNITY),
            None
        )
        if eq_opp and not eq_opp.passed:
            biases.append({
                "type": "equal_opportunity_violation",
                "severity": "high",
                "description": "Equal opportunity threshold not met - some groups have lower true positive rates",
                "affected_groups": eq_opp.demographic_groups,
                "metric_value": eq_opp.value,
                "threshold": eq_opp.threshold,
                "recommendation": "Investigate historical data biases and adjust decision thresholds"
            })
        
        # Check for significant disparities in breakdowns
        for metric in metrics:
            if metric.breakdown:
                values = list(metric.breakdown.values())
                if max(values) - min(values) > 0.15:  # More than 15% disparity
                    biases.append({
                        "type": "group_disparity",
                        "severity": "medium",
                        "description": f"Significant disparity detected in {metric.metric_type.value}",
                        "affected_groups": metric.demographic_groups,
                        "max_difference": round(max(values) - min(values), 3),
                        "recommendation": "Conduct deeper analysis of group-specific outcomes"
                    })
        
        # Random bias detection for demonstration (remove in production)
        if random.random() < 0.3:  # 30% chance of additional bias
            biases.append({
                "type": "feature_correlation",
                "severity": "low",
                "description": "Potential proxy variable detected that correlates with protected attribute",
                "affected_features": ["postal_code", "income_bracket"],
                "recommendation": "Review feature importance and consider removal or transformation"
            })
        
        return biases
    
    def _calculate_overall_score(self, metrics: List[FairnessMetric]) -> float:
        """Calculate overall fairness score from individual metrics."""
        if not metrics:
            return 0.0
        
        # Weight different metrics
        weights = {
            FairnessMetricType.STATISTICAL_PARITY: 0.25,
            FairnessMetricType.EQUAL_OPPORTUNITY: 0.30,
            FairnessMetricType.PREDICTIVE_PARITY: 0.25,
            FairnessMetricType.INDIVIDUAL_FAIRNESS: 0.20
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric in metrics:
            weight = weights.get(metric.metric_type, 0.25)
            weighted_sum += metric.value * weight
            total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return round(min(1.0, max(0.0, overall_score)), 3)
    
    def _determine_compliance(
        self,
        metrics: List[FairnessMetric],
        biases_detected: List[Dict[str, Any]]
    ) -> str:
        """Determine compliance status based on metrics and biases."""
        # Check if any critical biases exist
        high_severity_biases = [b for b in biases_detected if b.get("severity") == "high"]
        
        if high_severity_biases:
            return "NON_COMPLIANT"
        
        # Check if all metrics pass their thresholds
        all_passed = all(m.passed for m in metrics)
        
        if all_passed and len(biases_detected) == 0:
            return "COMPLIANT"
        
        # Medium severity biases or some metrics failing
        medium_severity_biases = [b for b in biases_detected if b.get("severity") == "medium"]
        failed_metrics = [m for m in metrics if not m.passed]
        
        if medium_severity_biases or failed_metrics:
            return "REVIEW_NEEDED"
        
        return "COMPLIANT"
    
    def _generate_recommendations(
        self,
        biases_detected: List[Dict[str, Any]],
        metrics: List[FairnessMetric]
    ) -> List[str]:
        """Generate actionable recommendations based on audit findings."""
        recommendations = []
        
        # Add recommendations from detected biases
        for bias in biases_detected:
            if "recommendation" in bias:
                recommendations.append(f"[{bias['severity'].upper()}] {bias['recommendation']}")
        
        # Add general recommendations based on metrics
        for metric in metrics:
            if not metric.passed:
                recommendations.append(
                    f"Improve {metric.metric_type.value.replace('_', ' ')} - "
                    f"current score {metric.value} below threshold {metric.threshold}"
                )
        
        # Add standard best practices if no major issues
        if not recommendations:
            recommendations = [
                "Continue monitoring fairness metrics regularly",
                "Document model decisions and maintain audit trails",
                "Conduct periodic reviews of feature importance",
                "Engage diverse stakeholders in model evaluation"
            ]
        
        return recommendations
    
    def _generate_executive_summary(
        self,
        model_name: Optional[str],
        overall_score: float,
        compliance_status: str,
        num_biases: int
    ) -> str:
        """Generate executive summary of the audit."""
        model_ref = model_name or "the specified decisions"
        
        if compliance_status == "COMPLIANT":
            status_text = "fully compliant with fairness standards"
        elif compliance_status == "REVIEW_NEEDED":
            status_text = "requires review due to potential fairness concerns"
        else:
            status_text = "non-compliant and requires immediate attention"
        
        summary = (
            f"Fairness audit completed for {model_ref}. "
            f"Overall fairness score: {overall_score:.1%}. "
            f"The model/system is {status_text}. "
            f"{num_biases} potential bias(es) detected during the audit. "
            f"{'All fairness metrics passed their thresholds.' if num_biases == 0 else 'Review detailed findings for specific recommendations.'}"
        )
        
        return summary
    
    def _generate_detailed_findings(
        self,
        metrics: List[FairnessMetric],
        biases_detected: List[Dict[str, Any]],
        recommendations: List[str]
    ) -> str:
        """Generate detailed findings section of the audit report."""
        findings = []
        
        findings.append("FAIRNESS METRICS ANALYSIS:")
        findings.append("-" * 40)
        for metric in metrics:
            status = "✓ PASS" if metric.passed else "✗ FAIL"
            findings.append(
                f"{status} | {metric.metric_type.value}: {metric.value:.3f} "
                f"(threshold: {metric.threshold}, CI: {metric.confidence_interval})"
            )
        
        findings.append("\n\nBIASES DETECTED:")
        findings.append("-" * 40)
        if biases_detected:
            for i, bias in enumerate(biases_detected, 1):
                findings.append(
                    f"{i}. [{bias['severity'].upper()}] {bias['type']}: "
                    f"{bias['description']}"
                )
        else:
            findings.append("No significant biases detected.")
        
        findings.append("\n\nRECOMMENDATIONS:")
        findings.append("-" * 40)
        for i, rec in enumerate(recommendations, 1):
            findings.append(f"{i}. {rec}")
        
        return "\n".join(findings)
    
    def _translate_to_urdu(self, text: str) -> str:
        """Translate executive summary to Urdu (placeholder)."""
        # In production, use Azure Translator or similar service
        return text  # Placeholder
    
    def _update_model_summary(self, model_name: str, report: FairnessAuditReport):
        """Update the model summary with latest audit results."""
        if model_name not in self.model_summaries:
            self.model_summaries[model_name] = {
                "model_name": model_name,
                "total_audits": 0,
                "audits": [],
                "average_fairness_score": 0.0,
                "compliance_history": [],
                "last_audit_date": None
            }
        
        summary = self.model_summaries[model_name]
        summary["total_audits"] += 1
        summary["audits"].append(report.audit_id)
        summary["compliance_history"].append(report.compliance_status)
        summary["last_audit_date"] = report.audit_date.isoformat()
        
        # Update average fairness score
        scores = [
            self.audit_cache[audit_id].overall_fairness_score 
            for audit_id in summary["audits"]
            if audit_id in self.audit_cache
        ]
        summary["average_fairness_score"] = sum(scores) / len(scores) if scores else 0.0
    
    def get_audit(self, audit_id: str) -> Optional[FairnessAuditReport]:
        """Retrieve a cached audit report by ID."""
        return self.audit_cache.get(audit_id)
    
    def get_metrics(
        self,
        model_name: Optional[str] = None,
        metric_type: Optional[FairnessMetricType] = None,
        limit: int = 100
    ) -> List[FairnessMetric]:
        """Retrieve fairness metrics with optional filtering."""
        metrics = []
        
        # Collect metrics from all audits
        for audit in self.audit_cache.values():
            if model_name and audit.model_name != model_name:
                continue
            
            for metric in audit.metrics:
                if metric_type and metric.metric_type != metric_type:
                    continue
                metrics.append(metric)
        
        return metrics[:limit]
    
    def get_model_summary(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get fairness summary for a specific model."""
        return self.model_summaries.get(model_name)


if __name__ == "__main__":
    # Test the fairness service
    service = FairnessService()
    
    print("Running fairness audit test...")
    print("=" * 60)
    
    report = service.run_audit(
        model_name="loan_approval_model",
        decision_ids=["dec_123", "dec_456", "dec_789"]
    )
    
    print(f"Audit ID: {report.audit_id}")
    print(f"Model: {report.model_name}")
    print(f"Overall Score: {report.overall_fairness_score:.3f}")
    print(f"Compliance: {report.compliance_status}")
    print(f"\nExecutive Summary:\n{report.executive_summary}")
    print(f"\nMetrics:")
    for metric in report.metrics:
        status = "✓" if metric.passed else "✗"
        print(f"  {status} {metric.metric_type.value}: {metric.value}")
    
    print(f"\nBiases Detected: {len(report.biases_detected)}")
    for bias in report.biases_detected:
        print(f"  - [{bias['severity']}] {bias['type']}")
    
    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  • {rec}")
