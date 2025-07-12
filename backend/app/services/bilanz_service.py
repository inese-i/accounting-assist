from typing import List, Dict, Optional
from datetime import datetime
import logging

from ..models.bilanz import Bilanz
from ..models.account import Account

class BilanzService:
    """Service for managing Bilanz (Balance Sheet) operations"""
    
    def __init__(self, account_service):
        self.logger = logging.getLogger(__name__)
        self.account_service = account_service
    
    def generate_bilanz(self, period_end: Optional[datetime] = None) -> Bilanz:
        """Generate a Bilanz from all active accounts"""
        try:
            # Get all accounts
            accounts = self.account_service.get_all_accounts()
            
            # All accounts returned by get_all_accounts are already active
            active_accounts = accounts
            
            self.logger.info(f"Generating Bilanz with {len(active_accounts)} active accounts")
            
            # Create Bilanz
            bilanz = Bilanz(active_accounts, period_end)
            
            return bilanz
            
        except Exception as e:
            self.logger.error(f"Error generating Bilanz: {e}")
            raise e
    
    def get_bilanz_summary(self, period_end: Optional[datetime] = None) -> Dict:
        """Get Bilanz summary as dictionary"""
        bilanz = self.generate_bilanz(period_end)
        return bilanz.to_dict()
    
    def validate_bilanz(self, period_end: Optional[datetime] = None) -> Dict:
        """Validate that the Bilanz is balanced"""
        bilanz = self.generate_bilanz(period_end)
        
        return {
            "is_balanced": bilanz.is_balanced(),
            "aktiva_total": bilanz.get_aktiva_total(),
            "passiva_total": bilanz.get_passiva_total(),
            "difference": bilanz.get_balance_difference(),
            "period_end": bilanz.period_end.isoformat()
        }
    
    def get_account_resolution(self, account_number: str) -> Dict:
        """Get how a specific account contributes to the Bilanz"""
        account = self.account_service.get_account_by_number(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found")
        
        # Determine Bilanz side and category using simplified logic
        if account.account_type.value == 'aktivkonto':
            side = "aktiva"
            category = account.account_type.value
            contributes_amount = account.get_balance()
        elif account.account_type.value == 'passivkonto':
            side = "passiva"
            category = account.account_type.value
            contributes_amount = abs(account.get_balance())
        else:
            # Account type not supported in Bilanz
            side = "unknown"
            category = "unknown"
            contributes_amount = 0.0
        
        return {
            "account_number": account.number,
            "account_name": account.name,
            "account_type": account.account_type.value,
            "soll_balance": account.soll_balance,
            "haben_balance": account.haben_balance,
            "net_balance": account.get_balance(),
            "bilanz_side": side,
            "bilanz_category": category,
            "contributes_amount": contributes_amount
        }

# Dependency function for use in endpoints
def get_bilanz_service(account_service) -> BilanzService:
    """Get BilanzService instance with injected account service"""
    return BilanzService(account_service)
