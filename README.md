# Accounting System (HGB)

A production-ready FastAPI backend and Streamlit frontend for HGB (Handelsgesetzbuch) accounting, following HGB standards with full Soll/Haben (debit/credit) support.

**Features:** Complete accounting app with accounts, bookings, transactions, Bilanz (balance sheet), standard account catalog, and double-entry validation.

## Quick Start

### 1. Install Dependencies
```b- Modern UI: Streamlit frontend with accounting interface and educational contentsh
pip install -r requirements.txt
```

### 2. Run the Application

**Backend (FastAPI):**
```bash
cd backend
python main.py
```

**Frontend (Streamlit UI):**
```bash
cd frontend
streamlit run streamlit_app.py
```

The API will be available at: **http://localhost:8000**  
The UI will be available at: **http://localhost:8501**

### 3. View API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Streamlit UI**: http://localhost:8501

## API Endpoints

### Basic Endpoints
- `GET /` - API status and account count
- `GET /health` - Health check

### Account Management
- `POST /api/v1/accounts` - Create a new account
- `GET /api/v1/accounts` - List all accounts
- `GET /api/v1/accounts/{account_number}` - Get specific account by number

### Account Operations
- `POST /api/v1/accounts/{account_number}/debit` - Debit an account (Soll)
- `POST /api/v1/accounts/{account_number}/credit` - Credit an account (Haben)
- `POST /api/v1/accounts/transaction` - Process double-entry transaction

### Standard Accounts
- `GET /api/v1/accounts/standard/search` - Search standard account catalog
- `GET /api/v1/accounts/standard/{account_number}` - Get standard account info
- `POST /api/v1/accounts/standard/{account_number}` - Create from standard catalog
- `POST /api/v1/accounts/standard/starter-pack` - Create essential business accounts

### Bilanz (Balance Sheet)
- `GET /api/v1/bilanz/` - Get complete Bilanz
- `GET /api/v1/bilanz/validate` - Validate Bilanz balance
- `GET /api/v1/bilanz/account/{account_number}/resolution` - Account Bilanz contribution

## Account Types (HGB Standard)

| Type | German Term | Category | Account Numbers | Normal Side |
|------|-------------|----------|----------------|-------------|
| `aktivkonto` | Aktivkonto | Bestandskonto (Balance Sheet) | 0000-2999 | SOLL (Debit) |
| `passivkonto` | Passivkonto | Bestandskonto (Balance Sheet) | 3000-3999 | HABEN (Credit) |
| `aufwandskonto` | Aufwandskonto | Erfolgskonto (P&L) | 4000-7999 | SOLL (Debit) |
| `ertragskonto` | Ertragskonto | Erfolgskonto (P&L) | 8000-9999 | HABEN (Credit) |

### Account Type Details

**Bestandskonten (Balance Sheet Accounts):**
- **Aktivkonto**: Assets (Kasse, Bank, Forderungen, Anlagevermögen)
- **Passivkonto**: Liabilities & Equity (Verbindlichkeiten, Kredite, Eigenkapital)

**Erfolgskonten (P&L Accounts):**
- **Aufwandskonto**: Expenses (Bürokosten, Gehälter, Miete, Abschreibungen)
- **Ertragskonto**: Revenue (Umsatzerlöse, Zinserträge, außerordentliche Erträge)

## Example Usage

### Create Accounts from Standard Catalog
```bash
# Create essential business accounts (starter pack)
curl -X POST "http://localhost:8000/api/v1/accounts/standard/starter-pack"

# Create individual standard account
curl -X POST "http://localhost:8000/api/v1/accounts/standard/1000?initial_balance=1000.0"
```

### Create a Custom Account
```bash
curl -X POST "http://localhost:8000/api/v1/accounts" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "1000",
    "name": "Kasse",
    "account_type": "aktivkonto",
    "balance": 1000.0
  }'
```

### Search Standard Accounts
```bash
curl "http://localhost:8000/api/v1/accounts/standard/search?query=kasse&limit=10"
```

### Process Double-Entry Transaction
```bash
curl -X POST "http://localhost:8000/api/v1/accounts/transaction" \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "1000",
    "to_account": "1200", 
    "amount": 500.0,
    "description": "Transfer cash to bank"
  }'
```

### View All Accounts
```bash
curl http://localhost:8000/api/v1/accounts
```

### Get Bilanz (Balance Sheet)
```bash
curl http://localhost:8000/api/v1/bilanz/
```

## Accounting Rules (Soll an Haben)

### Double-Entry Principle
Every transaction follows "Soll an Haben" (Debit to Credit):
- **SOLL (Debit)**: Left side of T-account
- **HABEN (Credit)**: Right side of T-account

### Account Behavior

**Aktivkonto (Assets):**
- SOLL increases balance (Zugang)
- HABEN decreases balance (Abgang)

**Passivkonto (Liabilities/Equity):**
- SOLL decreases balance (Tilgung)
- HABEN increases balance (Aufnahme)

**Aufwandskonto (Expenses):**
- SOLL increases expenses (Aufwand)
- HABEN corrections/reversals (Stornierung)

**Ertragskonto (Revenue):**
- SOLL corrections/reversals (Stornierung)
- HABEN increases revenue (Ertrag)

### Bilanzveränderungen (Balance Sheet Changes)

1. **Aktivtausch**: Asset ↔ Asset (no total change)
2. **Passivtausch**: Liability ↔ Liability (no total change)
3. **Bilanzverlängerung**: Asset ↑ + Liability ↑ (total increases)
4. **Bilanzverkürzung**: Asset ↓ + Liability ↓ (total decreases)

## Features

### 🇩🇪 Accounting Standards
- Full HGB (Handelsgesetzbuch) compliance
- Proper Soll/Haben (debit/credit) implementation
- Account numbering system (0000-9999)
- Bilanzveränderungen visualization (Aktivtausch, Passivtausch, etc.)

### 📊 Account Management
- 4 account types: Aktivkonto, Passivkonto, Aufwandskonto, Ertragskonto
- Standard account catalog with instant search
- Account creation from catalog or custom setup
- Starter pack for essential business accounts

### 🔄 Transaction Processing
- Double-entry bookkeeping ("Soll an Haben")
- Real-time transaction validation
- Transaction effects preview
- Complete transaction history with entry tracking

### 📋 Balance Sheet (Bilanz)
- Real-time Bilanz generation
- Balance validation (Aktiva = Passiva)
- Account resolution and contribution analysis
- Educational content for accounting principles

### 🖥️ User Interface
- Modern Streamlit frontend
- Instant dropdown suggestions for accounts
- Educational tooltips and guidance
- Multi-tab interface (Dashboard, Accounts, Transactions, Bilanz)

## Project Structure

```
hgb-accountant/
├── backend/
│   ├── main.py                    # Server entry point (Uvicorn runner)
│   ├── app/
│   │   ├── main.py               # FastAPI application factory
│   │   ├── api/
│   │   │   ├── __init__.py       # API router aggregation
│   │   │   └── endpoints/
│   │   │       └── accounts.py   # Account and Bilanz endpoints
│   │   ├── core/
│   │   │   └── config.py         # Application settings
│   │   ├── models/
│   │   │   ├── account.py        # Account model and account types
│   │   │   ├── bilanz.py         # Bilanz (Balance Sheet) model
│   │   │   └── standard_accounts.py # Standard account catalog
│   │   ├── schemas/
│   │   │   ├── account.py        # Pydantic schemas for validation
│   │   │   └── bilanz.py         # Bilanz response schemas
│   │   └── services/
│   │       ├── account_service.py # Business logic layer
│   │       └── bilanz_service.py  # Bilanz calculation service
│   └── tests/
│       └── test_account_service.py # Unit tests
├── frontend/
│   ├── streamlit_app.py          # Main Streamlit application
│   └── .streamlit/
│       └── config.toml           # Streamlit configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                     # This file
```

## Architecture

This project follows **production-ready FastAPI best practices** with **HGB accounting standards**:

- **HGB Compliance**: Full implementation of accounting principles (Soll/Haben, Bestandskonten/Erfolgskonten)
- **Standard Account Catalog**: Complete account numbering system with search and suggestions
- **Double-Entry Bookkeeping**: Automatic validation of "Soll an Haben" transactions
- **Bilanz Integration**: Real-time balance sheet generation and validation
- **Separation of Concerns**: Clear layers for API, business logic, and data models
- **Dependency Injection**: Services are injected into endpoints for testability
- **Pydantic v2 Validation**: Modern request/response validation with accounting rules
- **Environment Configuration**: Secure handling of secrets and settings
- **Comprehensive Testing**: Unit tests for business logic
- **API Versioning**: Structured endpoints with `/api/v1/` prefix
- **Documentation**: Auto-generated OpenAPI docs with accounting context
- **Modern UI**: Streamlit frontend with German accounting interface and educational content

## Development

### Running the Application

**Backend (FastAPI with auto-reload):**
```bash
cd backend
python main.py
```

**Frontend (Streamlit UI):**
```bash
cd frontend
streamlit run streamlit_app.py
```

### Alternative Running Methods

**With Uvicorn directly:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**With Streamlit directly:**
```bash
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

**For production (with Gunicorn):**
```bash
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Update `.env` with your settings:
```bash
PROJECT_NAME="API"
SECRET_KEY="your-secret-key-here"
```

### Testing

Run the unit tests:
```bash
cd backend
python -m pytest tests/ -v
```

### API Documentation

To test the API, visit the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The documentation includes accounting context and examples for all endpoints.