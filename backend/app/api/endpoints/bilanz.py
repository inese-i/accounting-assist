from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime
from typing import Optional
import logging

from ...schemas.bilanz import (
    BilanzResponse, 
    BilanzValidationResponse, 
    AccountResolutionResponse,
    BilanzSummaryResponse
)
from ...services.bilanz_service import get_bilanz_service
from .accounts import get_account_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bilanz", tags=["bilanz"])

@router.get("/", response_model=BilanzResponse)
def get_bilanz(
    period_end: Optional[str] = Query(None, description="Period end date (YYYY-MM-DD format)"),
    account_service = Depends(get_account_service)
):
    """
    Generate complete Bilanz (Balance Sheet) from all accounts
    
    Returns the German HGB-compliant Balance Sheet with:
    - Aktiva: All Aktivkonto accounts
    - Passiva: All Passivkonto accounts
    """
    try:
        bilanz_service = get_bilanz_service(account_service)
        
        # Parse period_end if provided
        period_end_date = None
        if period_end:
            try:
                period_end_date = datetime.fromisoformat(period_end)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Generate Bilanz
        bilanz_dict = bilanz_service.get_bilanz_summary(period_end_date)
        
        logger.info(f"Generated Bilanz for period ending {period_end_date or 'current'}")
        
        return BilanzResponse(**bilanz_dict)
        
    except Exception as e:
        logger.error(f"Error generating Bilanz: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating Bilanz: {str(e)}")

@router.get("/validate", response_model=BilanzValidationResponse)
def validate_bilanz(
    period_end: Optional[str] = Query(None, description="Period end date (YYYY-MM-DD format)"),
    account_service = Depends(get_account_service)
):
    """
    Validate that the Bilanz is balanced (Aktiva = Passiva)
    
    Returns validation status and totals for both sides
    """
    try:
        bilanz_service = get_bilanz_service(account_service)
        
        # Parse period_end if provided
        period_end_date = None
        if period_end:
            try:
                period_end_date = datetime.fromisoformat(period_end)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Validate Bilanz
        validation_result = bilanz_service.validate_bilanz(period_end_date)
        
        logger.info(f"Bilanz validation: {'Balanced' if validation_result['is_balanced'] else 'Not balanced'}")
        
        return BilanzValidationResponse(**validation_result)
        
    except Exception as e:
        logger.error(f"Error validating Bilanz: {e}")
        raise HTTPException(status_code=500, detail=f"Error validating Bilanz: {str(e)}")

@router.get("/account/{account_number}/resolution", response_model=AccountResolutionResponse)
def get_account_resolution(
    account_number: str,
    account_service = Depends(get_account_service)
):
    """
    Show how a specific account contributes to the Bilanz
    
    Returns the account's position in the Bilanz structure:
    - Which side (Aktiva/Passiva)
    - Which category (Anlagevermögen, Eigenkapital, etc.)
    - Contributing amount
    """
    try:
        bilanz_service = get_bilanz_service(account_service)
        
        # Get account resolution
        resolution = bilanz_service.get_account_resolution(account_number)
        
        logger.info(f"Retrieved Bilanz resolution for account {account_number}")
        
        return AccountResolutionResponse(**resolution)
        
    except ValueError as e:
        logger.warning(f"Account not found: {account_number}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting account resolution: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting account resolution: {str(e)}")

@router.get("/summary", response_model=BilanzSummaryResponse)
def get_bilanz_summary(
    period_end: Optional[str] = Query(None, description="Period end date (YYYY-MM-DD format)")
):
    """
    Get a summary of the Bilanz without detailed account breakdowns
    """
    try:
        bilanz_service = get_bilanz_service()
        
        # Parse period_end if provided
        period_end_date = None
        if period_end:
            try:
                period_end_date = datetime.fromisoformat(period_end)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Generate Bilanz
        bilanz = bilanz_service.generate_bilanz(period_end_date)
        
        summary = {
            "total_accounts": len([acc for acc in bilanz.accounts if acc.is_active]),
            "aktiva_total": bilanz.get_aktiva_total(),
            "passiva_total": bilanz.get_passiva_total(),
            "is_balanced": bilanz.is_balanced(),
            "period_end": bilanz.period_end
        }
        
        logger.info(f"Generated Bilanz summary for period ending {period_end_date or 'current'}")
        
        return BilanzSummaryResponse(**summary)
        
    except Exception as e:
        logger.error(f"Error generating Bilanz summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating Bilanz summary: {str(e)}")
