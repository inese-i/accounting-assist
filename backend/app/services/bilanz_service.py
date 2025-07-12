from typing import List, Dict, Optional
from datetime import datetime
import logging

from ..models.bilanz import Bilanz
from ..models.account import Account
from ..models.account_categories import (
    AccountCategory, 
    CATEGORY_HIERARCHY, 
    get_main_categories,
    get_subcategories
)

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
    
    def generate_structured_bilanz(self, period_end: Optional[datetime] = None) -> Dict:
        """Generate Bilanz with hierarchical category structure"""
        try:
            # Get all accounts
            accounts_result = self.account_service.get_all_accounts()
            if not accounts_result["success"]:
                raise Exception(f"Failed to get accounts: {accounts_result['error']}")
            
            accounts = accounts_result["data"]
            
            self.logger.info(f"Generating structured Bilanz with {len(accounts)} accounts")
            
            # Group accounts by category
            categorized_accounts = {}
            for account_data in accounts:
                if account_data["account_type"] in ["aktivkonto", "passivkonto"]:
                    category = account_data.get("category")
                    if category:
                        if category not in categorized_accounts:
                            categorized_accounts[category] = []
                        categorized_accounts[category].append(account_data)
            
            # Build hierarchical structure
            aktiva_structure = self._build_category_structure("aktiva", categorized_accounts)
            passiva_structure = self._build_category_structure("passiva", categorized_accounts)
            
            # Calculate totals
            aktiva_total = sum(
                acc["balance"] for acc in accounts 
                if acc["account_type"] == "aktivkonto"
            )
            passiva_total = sum(
                acc["balance"] for acc in accounts 
                if acc["account_type"] == "passivkonto"
            )
            
            result = {
                "aktiva": {
                    "structure": aktiva_structure,
                    "total": aktiva_total
                },
                "passiva": {
                    "structure": passiva_structure, 
                    "total": passiva_total
                },
                "is_balanced": abs(aktiva_total - passiva_total) < 0.01,
                "difference": aktiva_total - passiva_total,
                "period_end": period_end.isoformat() if period_end else datetime.now().isoformat()
            }
            
            self.logger.info(f"Generated structured Bilanz: Aktiva={aktiva_total}, Passiva={passiva_total}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating structured Bilanz: {e}")
            raise
    
    def _build_category_structure(self, bilanz_section: str, categorized_accounts: Dict) -> Dict:
        """Build hierarchical category structure for Bilanz section"""
        structure = {}
        
        # Get main categories for this section
        main_categories = get_main_categories(bilanz_section)
        
        for main_cat in main_categories:
            main_info = CATEGORY_HIERARCHY[main_cat]
            main_cat_key = main_cat.value
            
            # Initialize main category
            structure[main_cat_key] = {
                "name": main_info["name"],
                "subcategories": {},
                "accounts": categorized_accounts.get(main_cat_key, []),
                "total": sum(acc["balance"] for acc in categorized_accounts.get(main_cat_key, []))
            }
            
            # Add subcategories
            subcategories = get_subcategories(main_cat)
            for sub_cat in subcategories:
                sub_info = CATEGORY_HIERARCHY[sub_cat]
                sub_cat_key = sub_cat.value
                
                sub_accounts = categorized_accounts.get(sub_cat_key, [])
                sub_total = sum(acc["balance"] for acc in sub_accounts)
                
                structure[main_cat_key]["subcategories"][sub_cat_key] = {
                    "name": sub_info["name"],
                    "accounts": sub_accounts,
                    "total": sub_total
                }
                
                # Add subcategory total to main category
                structure[main_cat_key]["total"] += sub_total
        
        return structure

# Dependency function for use in endpoints
def get_bilanz_service(account_service) -> BilanzService:
    """Get BilanzService instance with injected account service"""
    return BilanzService(account_service)
