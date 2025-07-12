import pytest
from app.services.account_service import AccountService
from app.schemas.account import AccountCreate
from app.models.account import AccountType

def test_create_account():
    """Test account creation"""
    service = AccountService()
    
    account_data = AccountCreate(
        number="1000",
        name="Kasse",
        account_type=AccountType.ASSET
    )
    
    account = service.create_account(account_data)
    
    assert account.number == "1000"
    assert account.name == "Kasse"
    assert account.account_type == AccountType.ASSET
    assert account.balance == 0.0

def test_duplicate_account_error():
    """Test duplicate account number error"""
    service = AccountService()
    
    account_data = AccountCreate(
        number="1000",
        name="Kasse",
        account_type=AccountType.ASSET
    )
    
    # Create first account
    service.create_account(account_data)
    
    # Try to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        service.create_account(account_data)

def test_german_account_validation():
    """Test German account number validation"""
    service = AccountService()
    
    # Asset account with wrong number range
    account_data = AccountCreate(
        number="5000",  # Should be 0000-2999 for assets
        name="Wrong Asset",
        account_type=AccountType.ASSET
    )
    
    with pytest.raises(ValueError, match="Asset accounts must be in range"):
        service.create_account(account_data)
