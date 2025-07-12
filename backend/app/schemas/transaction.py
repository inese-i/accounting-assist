from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class TransactionCreate(BaseModel):
    from_account: str = Field(..., description="Source account number (will be debited)")
    to_account: str = Field(..., description="Target account number (will be credited)")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    description: Optional[str] = Field(None, description="Transaction description")
    
    @field_validator('from_account', 'to_account')
    @classmethod
    def validate_account_numbers(cls, v):
        """Validate account number format"""
        if not v.isdigit():
            raise ValueError('Account number must contain only digits')
        if len(v) != 4:
            raise ValueError('German account number must be exactly 4 digits')
        return v
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if round(v, 2) != v:
            raise ValueError('Amount cannot have more than 2 decimal places')
        return round(v, 2)

class TransactionResponse(BaseModel):
    from_account: str
    to_account: str
    amount: float
    description: str
    debit_account_balance: float
    credit_account_balance: float
    validation_warnings: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True
