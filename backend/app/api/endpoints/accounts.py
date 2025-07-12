from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Optional

from app.schemas.account import (
    AccountCreate, 
    AccountResponse, 
    AccountUpdate, 
    AccountOperation, 
    OperationResponse,
    AccountEntryResponse,
    StandardAccountResponse,
    CategoryAccountsResponse,
    CategoryRecommendationsResponse,
    SearchResultResponse,
    StarterAccountsResponse,
    StarterAccountResponse
)
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.account_service import AccountService
from app.models.account_categories import AccountCategory
from app.models.standard_accounts import (
    get_standard_account,
    get_accounts_by_category,
    get_category_structure_with_accounts,
    get_recommended_accounts_for_category,
    create_account_from_standard,
    get_category_summary,
    search_accounts as search_standard_accounts,
    get_starter_accounts
)

router = APIRouter()

# Global instance for in-memory storage persistence
_account_service_instance = None

# Dependency injection
def get_account_service() -> AccountService:
    global _account_service_instance
    if _account_service_instance is None:
        _account_service_instance = AccountService()
    return _account_service_instance

@router.post("/", response_model=AccountResponse, summary="Create Account")
def create_account(
    account_data: AccountCreate,
    service: AccountService = Depends(get_account_service)
):
    """
    Create a new German accounting account following HGB standards.
    
    **German Account Number Rules (SKR03/SKR04):**
    - **0000-2999**: Assets (Aktiva)
    - **3000-3999**: Liabilities & Equity (Passiva & Eigenkapital)
    - **4000-7999**: Expenses (Aufwand)
    - **8000-9999**: Revenue (Ertrag)
    """
    try:
        account = service.create_account(account_data)
        return AccountResponse(
            number=account.number,
            name=account.name,
            account_type=account.account_type,
            soll_balance=account.soll_balance,
            haben_balance=account.haben_balance,
            balance=account.get_balance(),
            parent_account=account.parent_account,
            category=account.category,
            category_name=account.get_category_name(),
            is_active=account.is_active,
            created_at=account.created_at,
            soll_entries=[],
            haben_entries=[]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AccountResponse], summary="List All Accounts")
def get_accounts(service: AccountService = Depends(get_account_service)):
    """Get all active accounts in the system"""
    accounts = service.get_all_accounts()
    return [
        AccountResponse(
            number=acc.number,
            name=acc.name,
            account_type=acc.account_type,
            soll_balance=acc.soll_balance,
            haben_balance=acc.haben_balance,
            balance=acc.get_balance(),
            parent_account=acc.parent_account,
            category=acc.category,
            category_name=acc.get_category_name(),
            is_active=acc.is_active,
            created_at=acc.created_at,
            soll_entries=[
                AccountEntryResponse(amount=entry.amount, description=entry.description, date=entry.date)
                for entry in acc.soll_entries
            ],
            haben_entries=[
                AccountEntryResponse(amount=entry.amount, description=entry.description, date=entry.date)
                for entry in acc.haben_entries
            ]
        )
        for acc in accounts
    ]

@router.get("/{account_number}", response_model=AccountResponse, summary="Get Account")
def get_account(
    account_number: str,
    service: AccountService = Depends(get_account_service)
):
    """Get specific account by number"""
    account = service.get_account_by_number(account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return AccountResponse(
        number=account.number,
        name=account.name,
        account_type=account.account_type,
        soll_balance=account.soll_balance,
        haben_balance=account.haben_balance,
        balance=account.get_balance(),
        parent_account=account.parent_account,
        category=account.category,
        category_name=account.get_category_name(),
        is_active=account.is_active,
        created_at=account.created_at,
        soll_entries=[
            AccountEntryResponse(amount=entry.amount, description=entry.description, date=entry.date)
            for entry in account.soll_entries
        ],
        haben_entries=[
            AccountEntryResponse(amount=entry.amount, description=entry.description, date=entry.date)
            for entry in account.haben_entries
        ]
    )

@router.get("/{account_number}/balance", response_model=float, summary="Get Account Balance")
def get_account_balance(
    account_number: str,
    service: AccountService = Depends(get_account_service)
):
    """Get net balance (Soll - Haben) for an account"""
    account = service.get_account_by_number(account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.get_balance()

@router.post("/{account_number}/debit", response_model=OperationResponse, summary="Debit Account")
def debit_account(
    account_number: str,
    operation: AccountOperation,
    service: AccountService = Depends(get_account_service)
):
    """Debit an account (add to Soll side)"""
    try:
        account = service.debit_account(account_number, operation.amount, operation.description or "Debit transaction")
        return OperationResponse(
            account=account.number,
            account_name=account.name,
            operation="debit",
            amount=operation.amount,
            new_balance=account.get_balance(),
            account_type=account.account_type
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{account_number}/credit", response_model=OperationResponse, summary="Credit Account")
def credit_account(
    account_number: str,
    operation: AccountOperation,
    service: AccountService = Depends(get_account_service)
):
    """Credit an account (add to Haben side)"""
    try:
        account = service.credit_account(account_number, operation.amount, operation.description or "Credit transaction")
        return OperationResponse(
            account=account.number,
            account_name=account.name,
            operation="credit",
            amount=operation.amount,
            new_balance=account.get_balance(),
            account_type=account.account_type
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transaction", response_model=TransactionResponse, summary="Process Transaction")
def process_transaction(
    transaction_data: TransactionCreate,
    service: AccountService = Depends(get_account_service)
):
    """
    Process a transaction between two accounts using double-entry bookkeeping.
    
    **German Accounting Rules:**
    - The first account (from_account) will be debited (Soll)
    - The second account (to_account) will be credited (Haben)
    - **Debit increases**: Assets (Aktiva), Expenses (Aufwand)
    - **Credit increases**: Liabilities (Passiva), Equity (Eigenkapital), Revenue (Ertrag)
    
    **Example**: Transfer €100 from Bank to Cash
    - Bank account (Aktivkonto) will be credited -€100 (decrease)
    - Cash account (Aktivkonto) will be debited +€100 (increase)
    """
    try:
        result = service.process_transaction(
            from_account=transaction_data.from_account,
            to_account=transaction_data.to_account,
            amount=transaction_data.amount,
            description=transaction_data.description or f"Transfer from {transaction_data.from_account} to {transaction_data.to_account}"
        )
        return TransactionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== STANDARD ACCOUNTS ENDPOINTS =====

@router.get("/standard/search", summary="Search Standard Accounts")
def search_standard_accounts(
    query: str,
    limit: int = 10,
    service: AccountService = Depends(get_account_service)
):
    """
    Search standard German accounts by number, name, or category.
    
    **Parameters:**
    - **query**: Search term (account number, name, or category)
    - **limit**: Maximum number of results to return
    
    **Examples:**
    - Search by number: `1000` → Returns Kasse
    - Search by name: `bank` → Returns Bank accounts
    - Search by category: `liquide` → Returns cash and bank accounts
    """
    suggestions = service.get_account_suggestions(query, limit)
    return {
        "query": query,
        "results": suggestions,
        "total_found": len(suggestions)
    }

@router.get("/standard/{account_number}", summary="Get Standard Account Info")
def get_standard_account_info(
    account_number: str,
    service: AccountService = Depends(get_account_service)
):
    """
    Get detailed information about a standard German account.
    
    **Returns:**
    - Account name, type, and category
    - Whether the account already exists in your system
    - Current balance if it exists
    """
    standard_info = service.get_standard_account_info(account_number)
    
    if not standard_info:
        raise HTTPException(status_code=404, detail=f"Standard account {account_number} not found")
    
    # Check if account already exists
    existing_account = service.get_account_by_number(account_number)
    
    result = {
        "number": account_number,
        "name": standard_info["name"],
        "type": standard_info["type"],
        "category": standard_info.get("category", ""),
        "already_exists": existing_account is not None
    }
    
    if existing_account:
        result["current_balance"] = existing_account.get_balance()
        result["soll_balance"] = existing_account.soll_balance
        result["haben_balance"] = existing_account.haben_balance
    
    return result

@router.post("/standard/{account_number}", response_model=AccountResponse, summary="Create Standard Account")
def create_standard_account(
    account_number: str,
    initial_balance: float = 0.0,
    service: AccountService = Depends(get_account_service)
):
    """
    Create an account using standard German account details.
    
    **Parameters:**
    - **account_number**: 4-digit German account number (e.g., 1000 for Kasse)
    - **initial_balance**: Starting balance for the account
    
    **Example**: Create account 1000 (Kasse) with €500 initial balance
    """
    result = service.create_standard_account(account_number, initial_balance)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    account = result["data"]
    return AccountResponse(
        number=account.number,
        name=account.name,
        account_type=account.account_type,
        soll_balance=account.soll_balance,
        haben_balance=account.haben_balance,
        balance=account.get_balance(),
        parent_account=account.parent_account,
        is_active=account.is_active,
        created_at=account.created_at,
        soll_entries=[
            AccountEntryResponse(
                amount=entry.amount,
                description=entry.description,
                date=entry.date
            ) for entry in account.soll_entries
        ],
        haben_entries=[
            AccountEntryResponse(
                amount=entry.amount,
                description=entry.description,
                date=entry.date
            ) for entry in account.haben_entries
        ]
    )

@router.post("/standard/starter-pack", summary="Create Starter Account Pack")
def create_starter_accounts(
    service: AccountService = Depends(get_account_service)
):
    """
    Create a recommended set of starter accounts for new businesses.
    
    **Includes:**
    - 1000: Kasse (Cash)
    - 1200: Bank (Bank Account)
    - 1400: Forderungen aus L&L (Accounts Receivable)
    - 1580: Vorsteuer (Input VAT)
    - 3000: Gezeichnetes Kapital (Share Capital)
    - 3700: Verbindlichkeiten aus L&L (Accounts Payable)
    - 3900: Umsatzsteuer (Output VAT)
    - 5000: Löhne und Gehälter (Wages & Salaries)
    - 6300: Bürokosten (Office Expenses)
    - 6500: Reisekosten (Travel Expenses)
    - 8000: Umsatzerlöse (Sales Revenue)
    """
    result = service.create_starter_accounts()
    
    if not result["success"]:
        return {
            "success": False,
            "message": "Some accounts could not be created",
            "errors": result["errors"],
            "created_accounts": len(result["created_accounts"]),
            "total_attempted": len(result["errors"]) + len(result["created_accounts"])
        }
    
    return {
        "success": True,
        "message": f"Successfully created {len(result['created_accounts'])} starter accounts",
        "created_accounts": [
            AccountResponse(
                number=acc.number,
                name=acc.name,
                account_type=acc.account_type,
                soll_balance=acc.soll_balance,
                haben_balance=acc.haben_balance,
                balance=acc.get_balance(),
                parent_account=acc.parent_account,
                category=acc.category,
                category_name=acc.get_category_name(),
                is_active=acc.is_active,
                created_at=acc.created_at,
                soll_entries=[],
                haben_entries=[]
            ) for acc in result["created_accounts"]
        ]
    }


# ===== CATEGORY & STANDARD ACCOUNT INTEGRATION ENDPOINTS =====

@router.get("/categories", summary="Get Category Overview")
def get_categories():
    """Get overview of all account categories with summary information"""
    return get_category_summary()

@router.get("/categories/structure", summary="Get Category Structure with Accounts")
def get_category_structure():
    """Get complete category hierarchy with associated standard accounts"""
    return get_category_structure_with_accounts()

@router.get("/categories/{category}/accounts", response_model=CategoryAccountsResponse, summary="Get Accounts by Category")
def get_accounts_by_category_endpoint(category: str):
    """Get all standard accounts for a specific category"""
    try:
        # Convert string to AccountCategory enum
        account_category = AccountCategory(category)
        accounts = get_accounts_by_category(account_category)
        
        # Format response
        formatted_accounts = []
        for number, details in accounts.items():
            formatted_accounts.append(StandardAccountResponse(
                number=number,
                name=details["name"],
                type=details["type"],
                category=details["category"]
            ))
        
        return CategoryAccountsResponse(
            category=category,
            category_name=account_category.value.replace("_", " ").title(),
            accounts=formatted_accounts,
            total_accounts=len(formatted_accounts)
        )
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

@router.get("/categories/{category}/recommended", response_model=CategoryRecommendationsResponse, summary="Get Recommended Accounts for Category")
def get_recommended_accounts_endpoint(category: str, limit: int = 5):
    """Get recommended accounts for a specific category"""
    try:
        account_category = AccountCategory(category)
        recommended = get_recommended_accounts_for_category(account_category, limit)
        
        return CategoryRecommendationsResponse(
            category=category,
            category_name=account_category.value.replace("_", " ").title(),
            recommended_accounts=recommended,
            total_recommended=len(recommended)
        )
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

@router.get("/standard/{account_number}", response_model=StandardAccountResponse, summary="Get Standard Account Details")
def get_standard_account_endpoint(account_number: str):
    """Get details of a standard account by number"""
    account = get_standard_account(account_number)
    if not account:
        raise HTTPException(status_code=404, detail=f"Standard account {account_number} not found")
    
    return StandardAccountResponse(
        number=account_number,
        name=account["name"],
        type=account["type"],
        category=account.get("category")
    )

@router.post("/standard/{account_number}/create", response_model=AccountResponse, summary="Create Account from Standard")
def create_account_from_standard_endpoint(
    account_number: str, 
    initial_balance: float = 0.0,
    service: AccountService = Depends(get_account_service)
):
    """Create a new account based on a standard account template"""
    try:
        # Get standard account details
        standard_account = get_standard_account(account_number)
        if not standard_account:
            raise HTTPException(status_code=404, detail=f"Standard account {account_number} not found")
        
        # Create account data from standard
        account_data = create_account_from_standard(account_number, initial_balance)
        
        # Use the existing create_account method
        from app.schemas.account import AccountCreate
        create_request = AccountCreate(
            number=account_data["number"],
            name=account_data["name"],
            account_type=account_data["account_type"],
            parent_account=account_data.get("parent_account"),
            initial_balance=initial_balance
        )
        
        account = service.create_account(create_request)
        return AccountResponse(
            number=account.number,
            name=account.name,
            account_type=account.account_type,
            soll_balance=account.soll_balance,
            haben_balance=account.haben_balance,
            balance=account.get_balance(),
            parent_account=account.parent_account,
            category=account.category,
            category_name=account.get_category_name(),
            is_active=account.is_active,
            created_at=account.created_at,
            soll_entries=[],
            haben_entries=[]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/standard/search", response_model=SearchResultResponse, summary="Search Standard Accounts")
def search_standard_accounts_endpoint(query: str):
    """Search standard accounts by number, name, or category"""
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters long")
    
    results = search_standard_accounts(query.strip())
    
    return SearchResultResponse(
        query=query,
        results=results,
        total_results=len(results)
    )

@router.get("/standard/starter", response_model=StarterAccountsResponse, summary="Get Starter Account Recommendations")
def get_starter_accounts_endpoint():
    """Get recommended starter accounts for new businesses"""
    starter_numbers = get_starter_accounts()
    starter_accounts = []
    
    for number in starter_numbers:
        account = get_standard_account(number)
        if account:
            starter_accounts.append(StarterAccountResponse(
                number=number,
                name=account["name"],
                type=account["type"],
                category=account.get("category"),
                description=f"Essential account for {account['name'].lower()}"
            ))
    
    return StarterAccountsResponse(
        starter_accounts=starter_accounts,
        total_accounts=len(starter_accounts),
        description="Recommended accounts for new business setup"
    )
