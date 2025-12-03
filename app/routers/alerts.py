from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from app.database import get_db
from app.services.alert_service import AlertService
from app.services.document_service import DocumentService
from app.schemas import Alert, AlertCreate, AlertUpdate

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("/", response_model=Dict[str, List[Alert]])
async def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    acknowledged: bool = Query(None, description="Filter by acknowledged status. None returns all."),
    db: Session = Depends(get_db)
):
    """Get list of alerts with pagination. By default, returns unacknowledged alerts first."""
    try:
        alert_service = AlertService(db)
        generated_alerts: List[Alert] = []

        if acknowledged is None or acknowledged is False:
            document_service = DocumentService(db)
            generated_alerts = document_service.generate_unlinked_alerts()

        if acknowledged is None:
            # Default: Get unacknowledged alerts first, then acknowledged
            unacknowledged = alert_service.get_alerts(skip=0, limit=limit, acknowledged=False)
            if len(unacknowledged) < limit:
                acknowledged_alerts = alert_service.get_alerts(
                    skip=0, 
                    limit=limit - len(unacknowledged), 
                    acknowledged=True
                )
                alerts = unacknowledged + acknowledged_alerts
            else:
                alerts = unacknowledged
            alerts = generated_alerts + alerts
        else:
            alerts = alert_service.get_alerts(skip=skip, limit=limit, acknowledged=acknowledged)
            if not acknowledged:
                alerts = generated_alerts + alerts

        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

@router.get("/{alert_id}", response_model=Alert)
async def get_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific alert by ID"""
    try:
        alert_service = AlertService(db)
        alert = alert_service.get_alert(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alert: {str(e)}")

@router.post("/", response_model=Alert)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    try:
        alert_service = AlertService(db)
        return alert_service.create_alert(alert)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create alert: {str(e)}")

@router.put("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_id: str,
    alert: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert"""
    try:
        alert_service = AlertService(db)
        updated_alert = alert_service.update_alert(alert_id, alert)
        if not updated_alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return updated_alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update alert: {str(e)}")

@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """Delete an alert"""
    try:
        alert_service = AlertService(db)
        success = alert_service.delete_alert(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete alert: {str(e)}")
