from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class BilanzAccountItem(BaseModel):
    """Individual account item in Bilanz"""
    account_number: str = Field(..., description="Account number")
    account_name: str = Field(..., description="Account name")
    balance: float = Field(..., description="Account balance contribution to Bilanz")

class BilanzCategory(BaseModel):
    """Bilanz category (aktivkonto or passivkonto)"""
    positions: Dict[str, List[BilanzAccountItem]] = Field(..., description="Account positions by category")
    total: float = Field(..., description="Total amount for this side")

class BilanzResponse(BaseModel):
    """Complete Bilanz response"""
    period_end: datetime = Field(..., description="Period end date")
    created_at: datetime = Field(..., description="Bilanz creation timestamp")
    aktiva: BilanzCategory = Field(..., description="Assets side of Bilanz")
    passiva: BilanzCategory = Field(..., description="Liabilities and Equity side of Bilanz")
    is_balanced: bool = Field(..., description="Whether Aktiva equals Passiva")
    balance_difference: float = Field(..., description="Difference between Aktiva and Passiva")

class BilanzValidationResponse(BaseModel):
    """Bilanz validation result"""
    is_balanced: bool = Field(..., description="Whether the Bilanz is balanced")
    aktiva_total: float = Field(..., description="Total Aktiva amount")
    passiva_total: float = Field(..., description="Total Passiva amount") 
    difference: float = Field(..., description="Difference between Aktiva and Passiva")
    period_end: datetime = Field(..., description="Period end date")

class AccountResolutionResponse(BaseModel):
    """How an account resolves into the Bilanz"""
    account_number: str = Field(..., description="Account number")
    account_name: str = Field(..., description="Account name")
    account_type: str = Field(..., description="Account type")
    soll_balance: float = Field(..., description="Soll (debit) balance")
    haben_balance: float = Field(..., description="Haben (credit) balance")
    net_balance: float = Field(..., description="Net balance (Soll - Haben)")
    bilanz_side: str = Field(..., description="Which side of Bilanz (aktiva/passiva)")
    bilanz_category: str = Field(..., description="Bilanz category")
    contributes_amount: float = Field(..., description="Amount contributed to Bilanz")

class BilanzSummaryResponse(BaseModel):
    """Summary of Bilanz"""
    total_accounts: int = Field(..., description="Total number of accounts")
    aktiva_total: float = Field(..., description="Total Aktiva")
    passiva_total: float = Field(..., description="Total Passiva") 
    is_balanced: bool = Field(..., description="Whether balanced")
    period_end: datetime = Field(..., description="Period end date")
