"""
Trust & Transparency Dashboard - REST API Layer

FastAPI-based REST endpoints for exposing explainer service functionality.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    Explanation, Factor, DecisionTrace, FairnessMetric, 
    FairnessAuditReport, FairnessMetricType
)
from explainer_service import ExplainerService
from services.fairness_service import FairnessService

# Initialize FastAPI app
app = FastAPI(
    title="Trust & Transparency Dashboard API",
    description="REST API for AI decision explanations and fairness auditing",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
explainer_service = ExplainerService()
fairness_service = FairnessService()


# Dependency for API key authentication (placeholder)
async def verify_api_key(api_key: str = Query(None, alias="X-API-Key")):
    """Verify API key for authentication."""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    # In production, validate against stored keys
    return api_key


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "explainer": "operational",
            "fairness": "operational"
        }
    }


@app.post("/api/v1/explain", response_model=Explanation, tags=["Explanations"])
async def generate_explanation(
    decision_id: str,
    model_name: str,
    model_version: str,
    outcome: str,
    confidence: float,
    input_features: Dict[str, Any],
    model_weights: Optional[Dict[str, float]] = None,
    context: Optional[Dict[str, Any]] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate a comprehensive explanation for an AI decision.
    
    - **decision_id**: Unique identifier for the decision
    - **model_name**: Name of the AI model
    - **model_version**: Version of the model
    - **outcome**: The decision outcome
    - **confidence**: Model's confidence score (0-1)
    - **input_features**: Input features used in the decision
    - **model_weights**: Optional feature importance weights
    - **context**: Additional context about the decision
    
    Returns a complete explanation with factors, alternatives, and fairness assessment.
    """
    try:
        explanation = explainer_service.generate_explanation(
            decision_id=decision_id,
            model_name=model_name,
            model_version=model_version,
            outcome=outcome,
            confidence=confidence,
            input_features=input_features,
            model_weights=model_weights,
            context=context
        )
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/explain/{decision_id}", response_model=Explanation, tags=["Explanations"])
async def get_explanation(decision_id: str, api_key: str = Depends(verify_api_key)):
    """
    Retrieve a previously generated explanation by decision ID.
    
    - **decision_id**: The unique identifier of the decision to retrieve
    """
    explanation = explainer_service.get_explanation(decision_id)
    if not explanation:
        raise HTTPException(status_code=404, detail="Explanation not found")
    return explanation


@app.get("/api/v1/explanations", response_model=List[Explanation], tags=["Explanations"])
async def list_explanations(api_key: str = Depends(verify_api_key)):
    """
    List all cached explanations.
    
    Returns a list of all explanations currently in the cache.
    """
    return explainer_service.list_explanations()


@app.get("/api/v1/trace/{decision_id}", response_model=DecisionTrace, tags=["Traces"])
async def get_decision_trace(decision_id: str, api_key: str = Depends(verify_api_key)):
    """
    Retrieve the complete decision trace for a specific decision.
    
    Shows all intermediate steps in the decision-making process.
    """
    trace = explainer_service.get_trace(decision_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace


@app.post("/api/v1/audit/run", response_model=FairnessAuditReport, tags=["Audits"])
async def run_fairness_audit(
    model_name: Optional[str] = None,
    decision_ids: Optional[List[str]] = None,
    metric_types: Optional[List[FairnessMetricType]] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Run a fairness audit on specified models or decisions.
    
    - **model_name**: Optional model name to audit
    - **decision_ids**: Optional list of decision IDs to audit
    - **metric_types**: Types of fairness metrics to calculate
    
    At least one of model_name or decision_ids must be provided.
    """
    if not model_name and not decision_ids:
        raise HTTPException(
            status_code=400, 
            detail="Either model_name or decision_ids must be provided"
        )
    
    try:
        report = fairness_service.run_audit(
            model_name=model_name,
            decision_ids=decision_ids or [],
            metric_types=metric_types
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/audit/{audit_id}", response_model=FairnessAuditReport, tags=["Audits"])
async def get_audit_report(audit_id: str, api_key: str = Depends(verify_api_key)):
    """
    Retrieve a previously generated audit report.
    
    - **audit_id**: The unique identifier of the audit report
    """
    report = fairness_service.get_audit(audit_id)
    if not report:
        raise HTTPException(status_code=404, detail="Audit report not found")
    return report


@app.get("/api/v1/metrics/fairness", response_model=List[FairnessMetric], tags=["Metrics"])
async def get_fairness_metrics(
    model_name: Optional[str] = None,
    metric_type: Optional[FairnessMetricType] = None,
    limit: int = Query(100, ge=1, le=1000),
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve fairness metrics for models or decisions.
    
    - **model_name**: Filter by model name
    - **metric_type**: Filter by specific metric type
    - **limit**: Maximum number of results to return
    """
    metrics = fairness_service.get_metrics(
        model_name=model_name,
        metric_type=metric_type,
        limit=limit
    )
    return metrics


@app.get("/api/v1/models/{model_name}/fairness-summary", tags=["Models"])
async def get_model_fairness_summary(model_name: str, api_key: str = Depends(verify_api_key)):
    """
    Get a fairness summary for a specific model.
    
    Includes overall fairness score, recent audits, and compliance status.
    """
    summary = fairness_service.get_model_summary(model_name)
    if not summary:
        raise HTTPException(status_code=404, detail="Model not found")
    return summary


@app.post("/api/v1/trace/capture", tags=["Traces"])
async def capture_decision_trace(
    decision_id: str,
    model_name: str,
    initial_input: Dict[str, Any],
    final_output: Dict[str, Any],
    steps: List[Dict[str, Any]],
    total_processing_time_ms: float,
    data_sources_used: List[str] = None,
    preprocessing_applied: List[str] = None,
    postprocessing_applied: List[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Capture and store a decision trace for later analysis.
    
    This endpoint allows external AI systems to submit their decision traces
    for storage and later explanation generation.
    """
    try:
        trace = explainer_service.capture_trace(
            decision_id=decision_id,
            model_name=model_name,
            initial_input=initial_input,
            final_output=final_output,
            steps=steps,
            total_processing_time_ms=total_processing_time_ms,
            data_sources_used=data_sources_used or [],
            preprocessing_applied=preprocessing_applied or [],
            postprocessing_applied=postprocessing_applied or []
        )
        return {"status": "success", "decision_id": decision_id, "trace_id": decision_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
