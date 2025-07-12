from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.account import AccountType

# Schema for creating new account
class AccountCreate(BaseModel):
    number: str = Field(..., pattern=r"^\d{4}$", description="German account number (4 digits)")
    name: str = Field(..., min_length=2, max_length=100, description="Account name")
    account_type: AccountType = Field(..., description="Type of account")
    balance: Optional[float] = Field(0.0, description="Starting balance")
    parent_account: Optional[str] = Field(None, description="Parent account number")
    is_active: Optional[bool] = Field(True, description="Whether account is active")
    
    @field_validator('number')
    @classmethod
    def validate_german_account_number(cls, v):
        """Validate German account number format"""
        if not v.isdigit():
            raise ValueError('Account number must contain only digits')
        if len(v) != 4:
            raise ValueError('German account number must be exactly 4 digits')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_account_name(cls, v):
        """Validate account name"""
        if not v.strip():
            raise ValueError('Account name cannot be empty')
        return v.strip()

# Schema for account entries in responses
class AccountEntryResponse(BaseModel):
    amount: float
    description: str
    date: datetime

# Schema for account responses
class AccountResponse(BaseModel):
    number: str
    name: str
    account_type: AccountType
    soll_balance: float
    haben_balance: float
    balance: float  # Calculated net balance (soll - haben)
    parent_account: Optional[str]
    is_active: bool
    created_at: datetime
    soll_entries: List[AccountEntryResponse]
    haben_entries: List[AccountEntryResponse]
    
    class Config:
        from_attributes = True

# Schema for updating account
class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    account_type: Optional[AccountType] = None
    is_active: Optional[bool] = None
    parent_account: Optional[str] = None

# Schema for debit/credit operations
class AccountOperation(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = Field(None, description="Transaction description")
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if round(v, 2) != v:
            raise ValueError('Amount cannot have more than 2 decimal places')
        return round(v, 2)

# Schema for operation response
class OperationResponse(BaseModel):
    account: str
    account_name: str
    operation: str  # "debit" or "credit"
    amount: float
    new_balance: float
    account_type: AccountType
