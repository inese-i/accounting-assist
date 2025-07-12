from typing import List, Dict, Optional
from datetime import datetime
from .account import Account, AccountType

class BilanzPosition:
    """Individual position in the Bilanz (Balance Sheet)"""
    def __init__(
        self,
        name: str,
        amount: float,
        accounts: List[Account],
        position_type: str  # "aktiva" or "passiva"
    ):
        self.name = name
        self.amount = amount
        self.accounts = accounts
        self.position_type = position_type

class Bilanz:
    """German Balance Sheet (Bilanz) - HGB compliant"""
    
    def __init__(self, accounts: List[Account], period_end: Optional[datetime] = None):
        self.accounts = accounts
        self.period_end = period_end or datetime.now()
        self.created_at = datetime.now()
        
        # Calculate positions
        self._calculate_positions()
    
    def _calculate_positions(self):
        """Calculate all balance sheet positions from accounts"""
        
        # Initialize position dictionaries
        self.aktiva_positions = {}
        self.passiva_positions = {}
        
        # Group accounts by type and calculate balances
        for account in self.accounts:
            if not account.is_active:
                continue
                
            balance = account.get_balance()
            
            # Only handle explicit German account types
            if account.account_type == AccountType.AKTIVKONTO:
                self._add_to_aktiva(account, balance)
            elif account.account_type == AccountType.PASSIVKONTO:
                self._add_to_passiva(account, balance)
    
    def _add_to_aktiva(self, account: Account, balance: float):
        """Add account to Aktiva side - only for AKTIVKONTO"""
        category = account.account_type.value
        
        if category not in self.aktiva_positions:
            self.aktiva_positions[category] = []
        
        self.aktiva_positions[category].append({
            "account": account,
            "balance": balance
        })
    
    def _add_to_passiva(self, account: Account, balance: float):
        """Add account to Passiva side - only for PASSIVKONTO"""
        category = account.account_type.value
        
        if category not in self.passiva_positions:
            self.passiva_positions[category] = []
        
        self.passiva_positions[category].append({
            "account": account,
            "balance": abs(balance)  # Passiva balances are shown as positive
        })
    
    def get_aktiva_total(self) -> float:
        """Calculate total Aktiva"""
        total = 0.0
        for category, accounts in self.aktiva_positions.items():
            for item in accounts:
                total += item["balance"]
        return total
    
    def get_passiva_total(self) -> float:
        """Calculate total Passiva"""
        total = 0.0
        for category, accounts in self.passiva_positions.items():
            for item in accounts:
                total += item["balance"]
        return total
    
    def is_balanced(self) -> bool:
        """Check if Bilanz is balanced (Aktiva = Passiva)"""
        return abs(self.get_aktiva_total() - self.get_passiva_total()) < 0.01
    
    def get_balance_difference(self) -> float:
        """Get difference between Aktiva and Passiva"""
        return self.get_aktiva_total() - self.get_passiva_total()
    
    def to_dict(self) -> Dict:
        """Convert Bilanz to dictionary representation"""
        return {
            "period_end": self.period_end.isoformat(),
            "created_at": self.created_at.isoformat(),
            "aktiva": {
                "positions": {
                    category: [
                        {
                            "account_number": item["account"].number,
                            "account_name": item["account"].name,
                            "balance": item["balance"]
                        }
                        for item in accounts
                    ]
                    for category, accounts in self.aktiva_positions.items()
                },
                "total": self.get_aktiva_total()
            },
            "passiva": {
                "positions": {
                    category: [
                        {
                            "account_number": item["account"].number,
                            "account_name": item["account"].name,
                            "balance": item["balance"]
                        }
                        for item in accounts
                    ]
                    for category, accounts in self.passiva_positions.items()
                },
                "total": self.get_passiva_total()
            },
            "is_balanced": self.is_balanced(),
            "balance_difference": self.get_balance_difference()
        }
    
    def print_bilanz(self):
        """Print formatted Bilanz to console"""
        print(f"\n{'='*60}")
        print(f"BILANZ (Balance Sheet) - {self.period_end.strftime('%Y-%m-%d')}")
        print(f"{'='*60}")
        
        print(f"\n{'AKTIVA':<30} {'PASSIVA':<30}")
        print(f"{'-'*30} {'-'*30}")
        
        # Get max number of lines for parallel display
        aktiva_lines = []
        passiva_lines = []
        
        # Build Aktiva lines
        for category, accounts in self.aktiva_positions.items():
            aktiva_lines.append(f"{category}")
            for item in accounts:
                aktiva_lines.append(f"  {item['account'].name}: €{item['balance']:,.2f}")
        
        aktiva_lines.append(f"")
        aktiva_lines.append(f"TOTAL AKTIVA: €{self.get_aktiva_total():,.2f}")
        
        # Build Passiva lines
        for category, accounts in self.passiva_positions.items():
            passiva_lines.append(f"{category}")
            for item in accounts:
                passiva_lines.append(f"  {item['account'].name}: €{item['balance']:,.2f}")
        
        passiva_lines.append(f"")
        passiva_lines.append(f"TOTAL PASSIVA: €{self.get_passiva_total():,.2f}")
        
        # Print side by side
        max_lines = max(len(aktiva_lines), len(passiva_lines))
        for i in range(max_lines):
            aktiva_line = aktiva_lines[i] if i < len(aktiva_lines) else ""
            passiva_line = passiva_lines[i] if i < len(passiva_lines) else ""
            print(f"{aktiva_line:<30} {passiva_line:<30}")
        
        print(f"\n{'='*60}")
        if self.is_balanced():
            print("✅ BILANZ IS BALANCED")
        else:
            print(f"❌ BILANZ NOT BALANCED - Difference: €{self.get_balance_difference():,.2f}")
        print(f"{'='*60}")
