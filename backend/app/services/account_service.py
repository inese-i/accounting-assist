from typing import List, Optional
from app.models.account import Account, AccountType
from app.models.standard_accounts import get_standard_account, search_accounts, get_starter_accounts
from app.schemas.account import AccountCreate, AccountUpdate
import logging

class AccountService:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing AccountService with empty account list")
        # In-memory storage for now (will be replaced with database)
        self._accounts: List[Account] = []
    
    def create_account(self, account_data: AccountCreate) -> Account:
        self.logger.debug(f"Creating account with data: {account_data}")
        # Check if account number already exists
        if self.get_account_by_number(account_data.number):
            self.logger.error(f"Account with number '{account_data.number}' already exists")
            raise ValueError(f"Account with number '{account_data.number}' already exists")
        
        # Validate German account number rules
        self._validate_german_account_rules(account_data)
        
        # Create account with proper initial balance
        initial_balance = account_data.balance or 0.0
        
        # Determine where initial balance goes based on German accounting rules
        if account_data.account_type == AccountType.AKTIVKONTO:
            # For Aktivkonto: positive balance goes to Soll (debit side)
            soll_balance = max(0.0, initial_balance)
            haben_balance = max(0.0, -initial_balance)
        elif account_data.account_type == AccountType.PASSIVKONTO:
            # For Passivkonto: positive balance goes to Haben (credit side)
            soll_balance = max(0.0, -initial_balance)
            haben_balance = max(0.0, initial_balance)
        elif account_data.account_type == AccountType.AUFWANDSKONTO:
            # For Aufwandskonto: positive balance goes to Soll (debit side)
            soll_balance = max(0.0, initial_balance)
            haben_balance = max(0.0, -initial_balance)
        elif account_data.account_type == AccountType.ERTRAGSKONTO:
            # For Ertragskonto: positive balance goes to Haben (credit side)
            soll_balance = max(0.0, -initial_balance)
            haben_balance = max(0.0, initial_balance)
        else:
            # Fallback (should not occur with our 4 defined types)
            soll_balance = max(0.0, initial_balance)
            haben_balance = max(0.0, -initial_balance)
        
        account = Account(
            number=account_data.number,
            name=account_data.name,
            account_type=account_data.account_type,
            soll_balance=soll_balance,
            haben_balance=haben_balance,
            parent_account=account_data.parent_account,
            is_active=account_data.is_active
        )
        
        self._accounts.append(account)
        self.logger.debug(f"Account created successfully: {account}")
        return account
    
    def get_all_accounts(self) -> List[Account]:
        self.logger.debug("Fetching all active accounts")
        """Get all accounts"""
        return [acc for acc in self._accounts if acc.is_active]
    
    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        self.logger.debug(f"Fetching account by number: {account_number}")
        """Get account by number"""
        for account in self._accounts:
            if account.number == account_number and account.is_active:
                self.logger.debug(f"Account found: {account}")
                return account
        self.logger.warning(f"Account with number '{account_number}' not found")
        return None
    
    def debit_account(self, account_number: str, amount: float, description: str = "Debit transaction") -> Account:
        self.logger.debug(f"Debiting account '{account_number}' with amount: {amount}")
        """Debit an account (add to Soll side)"""
        account = self.get_account_by_number(account_number)
        if not account:
            self.logger.error(f"Account '{account_number}' not found")
            raise ValueError(f"Account '{account_number}' not found")
        
        self._validate_operation_amount(amount)
        self._validate_debit_operation(account)
        account.debit(amount, description)
        self.logger.debug(f"Account debited successfully: {account}")
        return account
    
    def credit_account(self, account_number: str, amount: float, description: str = "Credit transaction") -> Account:
        self.logger.debug(f"Crediting account '{account_number}' with amount: {amount}")
        """Credit an account (add to Haben side)"""
        account = self.get_account_by_number(account_number)
        if not account:
            self.logger.error(f"Account '{account_number}' not found")
            raise ValueError(f"Account '{account_number}' not found")
        
        self._validate_operation_amount(amount)
        self._validate_credit_operation(account)
        account.credit(amount, description)
        self.logger.debug(f"Account credited successfully: {account}")
        return account

    def process_transaction(self, from_account: str, to_account: str, amount: float, description: str = "") -> dict:
        """Process a transaction between two accounts following double-entry bookkeeping"""
        self.logger.debug(f"Processing transaction: {from_account} -> {to_account}, amount: {amount}")
        
        # Validate both accounts exist
        debit_account = self.get_account_by_number(from_account)
        credit_account = self.get_account_by_number(to_account)
        
        if not debit_account:
            raise ValueError(f"Debit account '{from_account}' not found")
        if not credit_account:
            raise ValueError(f"Credit account '{to_account}' not found")
        
        self._validate_operation_amount(amount)
        self._validate_debit_operation(debit_account)
        self._validate_credit_operation(credit_account)
        
        # Validate transaction account types
        transaction_warnings = self._validate_transaction_accounts(debit_account, credit_account)
        for warning in transaction_warnings:
            self.logger.warning(warning)
        
        # Create transaction description
        transaction_desc = description or f"Transfer from {from_account} to {to_account}"
        
        # Perform double-entry: Debit first account, Credit second account
        debit_account.debit(amount, transaction_desc)
        credit_account.credit(amount, transaction_desc)
        
        self.logger.info(f"Transaction completed: {from_account} -> {to_account}, amount: {amount}")
        
        return {
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "description": transaction_desc,
            "debit_account_balance": debit_account.get_balance(),
            "credit_account_balance": credit_account.get_balance(),
            "validation_warnings": transaction_warnings
        }
    
    def update_account(self, account_number: str, update_data: AccountUpdate) -> Account:
        """Update account information"""
        account = self.get_account_by_number(account_number)
        if not account:
            raise ValueError(f"Account '{account_number}' not found")
        
        if update_data.name is not None:
            account.name = update_data.name
        if update_data.account_type is not None:
            account.account_type = update_data.account_type
        if update_data.is_active is not None:
            account.is_active = update_data.is_active
        if update_data.parent_account is not None:
            account.parent_account = update_data.parent_account
        
        return account
    
    def _validate_german_account_rules(self, account_data: AccountCreate):
        """Validate German accounting rules for the 4 fundamental account types"""
        
        # SKR03/SKR04 account number validation
        account_num = int(account_data.number)
        
        if account_data.account_type == AccountType.AKTIVKONTO and not (0 <= account_num <= 2999):
            raise ValueError("Aktivkonto (Asset accounts) must be in range 0000-2999 (SKR03/SKR04)")
        elif account_data.account_type == AccountType.PASSIVKONTO and not (3000 <= account_num <= 3999):
            raise ValueError("Passivkonto (Liability/Equity accounts) must be in range 3000-3999 (SKR03/SKR04)")
        elif account_data.account_type == AccountType.AUFWANDSKONTO and not (4000 <= account_num <= 7999):
            raise ValueError("Aufwandskonto (Expense accounts) must be in range 4000-7999 (SKR03/SKR04)")
        elif account_data.account_type == AccountType.ERTRAGSKONTO and not (8000 <= account_num <= 9999):
            raise ValueError("Ertragskonto (Revenue accounts) must be in range 8000-9999 (SKR03/SKR04)")
    
    def _validate_operation_amount(self, amount: float):
        """Validate operation amount"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if round(amount, 2) != amount:
            raise ValueError("Amount cannot have more than 2 decimal places")
    
    def _validate_debit_operation(self, account: Account):
        """Validate if a debit operation is appropriate for the account type"""
        # According to German accounting principles:
        # DEBIT (Soll) increases: Aktivkonto (Assets), Aufwandskonto (Expenses)
        # DEBIT (Soll) decreases: Passivkonto (Liabilities/Equity), Ertragskonto (Revenue)
        
        if account.account_type in [AccountType.AKTIVKONTO, AccountType.AUFWANDSKONTO]:
            # These account types naturally increase with debit - this is normal
            pass
        elif account.account_type in [AccountType.PASSIVKONTO, AccountType.ERTRAGSKONTO]:
            # These account types decrease with debit - warn but allow
            self.logger.warning(f"Debiting {account.account_type.value} account {account.number} will decrease its balance")
        else:
            self.logger.warning(f"Unknown account type {account.account_type.value} for debit operation")
    
    def _validate_credit_operation(self, account: Account):
        """Validate if a credit operation is appropriate for the account type"""
        # According to German accounting principles:
        # CREDIT (Haben) increases: Passivkonto (Liabilities/Equity), Ertragskonto (Revenue)
        # CREDIT (Haben) decreases: Aktivkonto (Assets), Aufwandskonto (Expenses)
        
        if account.account_type in [AccountType.PASSIVKONTO, AccountType.ERTRAGSKONTO]:
            # These account types naturally increase with credit - this is normal
            pass
        elif account.account_type in [AccountType.AKTIVKONTO, AccountType.AUFWANDSKONTO]:
            # These account types decrease with credit - warn but allow
            self.logger.warning(f"Crediting {account.account_type.value} account {account.number} will decrease its balance")
        else:
            self.logger.warning(f"Unknown account type {account.account_type.value} for credit operation")
    
    def _validate_transaction_accounts(self, from_account: Account, to_account: Account) -> List[str]:
        """Validate transaction accounts according to German accounting principles"""
        warnings = []
        
        # Check if the transaction makes sense according to German accounting rules
        from_type = from_account.account_type
        to_type = to_account.account_type
        
        # Bestandskonten (Balance Sheet Accounts) transactions
        if from_type == AccountType.AKTIVKONTO and to_type == AccountType.AKTIVKONTO:
            warnings.append("INFO: Aktivtausch - Asset transfer between Aktivkonten")
        elif from_type == AccountType.PASSIVKONTO and to_type == AccountType.PASSIVKONTO:
            warnings.append("INFO: Passivtausch - Liability transfer between Passivkonten")
        elif from_type == AccountType.AKTIVKONTO and to_type == AccountType.PASSIVKONTO:
            warnings.append("INFO: Bilanzverlängerung - Increasing both assets and liabilities")
        elif from_type == AccountType.PASSIVKONTO and to_type == AccountType.AKTIVKONTO:
            warnings.append("INFO: Bilanzverkürzung - Decreasing both assets and liabilities")
        
        # Erfolgswirksame Geschäftsvorfälle (Transactions involving P&L accounts)
        elif from_type == AccountType.AUFWANDSKONTO and to_type == AccountType.AKTIVKONTO:
            warnings.append("INFO: Expense payment - Increasing expense, decreasing asset")
        elif from_type == AccountType.AKTIVKONTO and to_type == AccountType.ERTRAGSKONTO:
            warnings.append("INFO: Revenue receipt - Increasing asset, increasing revenue")
        elif from_type == AccountType.AUFWANDSKONTO and to_account == AccountType.PASSIVKONTO:
            warnings.append("INFO: Accrued expense - Increasing expense, increasing liability")
        elif from_type == AccountType.PASSIVKONTO and to_account == AccountType.ERTRAGSKONTO:
            warnings.append("INFO: Deferred revenue - Decreasing liability, increasing revenue")
        elif from_type == AccountType.AUFWANDSKONTO and to_account == AccountType.ERTRAGSKONTO:
            warnings.append("WARNING: Direct expense to revenue transfer (unusual)")
        elif from_type == AccountType.ERTRAGSKONTO and to_account == AccountType.AUFWANDSKONTO:
            warnings.append("WARNING: Direct revenue to expense transfer (unusual)")
        
        # Other combinations
        else:
            warnings.append(f"INFO: Transaction between {from_type.value} and {to_type.value}")
        
        return warnings
    
    # ===== Standard Accounts Methods =====
    
    def get_standard_account_info(self, account_number: str) -> dict:
        """Get standard account information by number"""
        return get_standard_account(account_number)
    
    def search_standard_accounts(self, query: str) -> List[dict]:
        """Search standard accounts by number, name, or category"""
        return search_accounts(query)
    
    def create_standard_account(self, account_number: str, initial_balance: float = 0.0) -> dict:
        """Create an account using standard German account details"""
        standard_info = get_standard_account(account_number)
        
        if not standard_info:
            return {"success": False, "error": f"Unknown standard account number: {account_number}"}
        
        # Check if account already exists
        if self.get_account_by_number(account_number):
            return {"success": False, "error": f"Account {account_number} already exists"}
        
        try:
            # Create account data using standard information
            account_data = AccountCreate(
                number=account_number,
                name=standard_info["name"],
                account_type=standard_info["type"],
                balance=initial_balance
            )
            
            account = self.create_account(account_data)
            self.logger.info(f"Created standard account: {account_number} - {standard_info['name']}")
            
            return {
                "success": True, 
                "data": account,
                "standard_info": {
                    "category": standard_info.get("category", ""),
                    "is_standard": True
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to create standard account {account_number}: {e}")
            return {"success": False, "error": str(e)}
    
    def create_starter_accounts(self, with_balances: dict = None) -> dict:
        """Create a set of recommended starter accounts for new businesses"""
        starter_numbers = get_starter_accounts()
        created_accounts = []
        errors = []
        
        balances = with_balances or {}
        
        for account_number in starter_numbers:
            initial_balance = balances.get(account_number, 0.0)
            result = self.create_standard_account(account_number, initial_balance)
            
            if result["success"]:
                created_accounts.append(result["data"])
            else:
                errors.append(f"{account_number}: {result['error']}")
        
        return {
            "success": len(errors) == 0,
            "created_accounts": created_accounts,
            "errors": errors,
            "total_created": len(created_accounts)
        }
    
    def get_account_suggestions(self, query: str, limit: int = 10) -> List[dict]:
        """Get account suggestions based on search query"""
        suggestions = self.search_standard_accounts(query)
        
        # Add indication if account already exists
        for suggestion in suggestions[:limit]:
            existing_account = self.get_account_by_number(suggestion["number"])
            suggestion["already_exists"] = existing_account is not None
            if existing_account:
                suggestion["current_balance"] = existing_account.get_balance()
        
        return suggestions[:limit]
    
    # ===== End Standard Accounts Methods =====
    
    def get_account_count(self) -> int:
        """Get total number of active accounts"""
        return len([acc for acc in self._accounts if acc.is_active])
    
    def get_account_balance(self, account_number: str) -> float:
        """Get net balance (Soll - Haben) for an account"""
        account = self.get_account_by_number(account_number)
        if not account:
            raise ValueError(f"Account '{account_number}' not found")
        return account.get_balance()
