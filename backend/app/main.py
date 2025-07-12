from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router

def create_app() -> FastAPI:
    """Create FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="""
        ## German API
        
        This API provides endpoints for managing German accounting accounts according to HGB (Handelsgesetzbuch) standards.
        
        ### Account Types
        - **Asset** (Aktiva): Accounts 0000-2999 (Cash, Bank, Inventory, etc.)
        - **Liability** (Passiva): Accounts 3000-3999 (Debts, Payables, etc.)
        - **Equity** (Eigenkapital): Accounts 3000-3999 (Capital, Retained Earnings, etc.)
        - **Expense** (Aufwand): Accounts 4000-7999 (Office costs, Travel, etc.)
        - **Revenue** (Ertrag): Accounts 8000-9999 (Sales, Interest income, etc.)
        
        ### German Accounting Rules
        - **Debit increases**: Assets and Expenses
        - **Credit increases**: Liabilities, Equity, and Revenue
        - **Double-entry**: Every transaction affects at least two accounts
        
        🔄 **Auto-reload is working!** Changes to code will restart the server automatically.
        """,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": f"{settings.PROJECT_NAME} is running",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
