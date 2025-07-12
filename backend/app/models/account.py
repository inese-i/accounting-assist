from enum import Enum
from typing import Optional, List
from datetime import datetime

# German Account Types - 4 fundamental types in HGB accounting
class AccountType(str, Enum):
    AKTIVKONTO = "aktivkonto"     # Aktivkonto (Bestandskonto) - Assets
    PASSIVKONTO = "passivkonto"   # Passivkonto (Bestandskonto) - Liabilities & Equity
    AUFWANDSKONTO = "aufwandskonto" # Aufwandskonto (Erfolgskonto) - Expenses
    ERTRAGSKONTO = "ertragskonto"   # Ertragskonto (Erfolgskonto) - Revenue

# Account Entry Model - Represents a single transaction entry in an account
class AccountEntry:
    def __init__(self, amount: float, description: str, date: Optional[datetime] = None):
        self.amount = amount
        self.description = description
        self.date = date or datetime.now()

# Account Model - Database representation (future SQLAlchemy model)
class Account:
    def __init__(
        self,
        number: str,
        name: str,
        account_type: AccountType,
        soll_balance: float = 0.0,
        haben_balance: float = 0.0,
        parent_account: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.number = number
        self.name = name
        self.account_type = account_type
        self.soll_balance = soll_balance
        self.haben_balance = haben_balance
        self.parent_account = parent_account
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.soll_entries: List[AccountEntry] = []
        self.haben_entries: List[AccountEntry] = []

    def debit(self, amount: float, description: str) -> None:
        """Add debit amount to Soll side and record entry."""
        self.soll_balance += amount
        self.soll_entries.append(AccountEntry(amount, description))

    def credit(self, amount: float, description: str) -> None:
        """Add credit amount to Haben side and record entry."""
        self.haben_balance += amount
        self.haben_entries.append(AccountEntry(amount, description))

    def get_balance(self) -> float:
        """
        Calculate account balance based on German accounting principles.
        
        Bestandskonten (Balance Sheet Accounts):
        - Aktivkonto: Soll increases, Haben decreases → Balance = Soll - Haben
        - Passivkonto: Haben increases, Soll decreases → Balance = Haben - Soll
        
        Erfolgskonten (Success Accounts):
        - Aufwandskonto: Soll increases expenses → Balance = Soll - Haben
        - Ertragskonto: Haben increases revenue → Balance = Haben - Soll
        """
        if self.account_type in [AccountType.AKTIVKONTO, AccountType.AUFWANDSKONTO]:
            # Aktivkonto and Aufwandskonto: Soll side increases the balance
            return self.soll_balance - self.haben_balance
        elif self.account_type in [AccountType.PASSIVKONTO, AccountType.ERTRAGSKONTO]:
            # Passivkonto and Ertragskonto: Haben side increases the balance
            return self.haben_balance - self.soll_balance
        else:
            # Fallback (should not occur with the 4 defined types)
            return self.soll_balance - self.haben_balance
