# Account Categories & Standard Accounts Integration

## Overview

The HGB Accountant system now provides a **unified approach** combining hierarchical account categories with the standard German chart of accounts. This integration offers the best of both worlds:

- **Structured Organization**: HGB-compliant Bilanz hierarchy (Anlagevermögen, Umlaufvermögen, etc.)
- **Standard Compliance**: Complete German chart of accounts (SKR03/SKR04 compatible)
- **Intelligent Automation**: Automatic category assignment and recommendations
- **Easy Navigation**: Category-based browsing and account discovery

## Key Features

### 1. Hierarchical Category System
```
📊 AKTIVA (Assets)
├── 🏗️ Anlagevermögen (Fixed Assets)
│   ├── Immaterielle Anlagen (Intangible Assets)
│   ├── Sachanlagen (Tangible Assets)
│   └── Finanzanlagen (Financial Assets)
└── 💰 Umlaufvermögen (Current Assets)
    ├── Vorräte (Inventory)
    ├── Forderungen (Receivables)
    └── Liquide Mittel (Cash & Cash Equivalents)

💼 PASSIVA (Liabilities & Equity)
├── 📈 Eigenkapital (Equity)
│   ├── Gezeichnetes Kapital (Share Capital)
│   ├── Kapitalrücklagen (Capital Reserves)
│   └── Gewinnrücklagen (Retained Earnings)
└── 🏦 Fremdkapital (Liabilities)
    ├── Verbindlichkeiten (Payables)
    └── Rückstellungen (Provisions)
```

### 2. Standard Account Integration
- **500+ predefined accounts** following German HGB standards
- **Automatic category assignment** based on account number ranges
- **Consistent naming** according to German accounting principles
- **Type validation** (Aktiv, Passiv, Aufwand, Ertrag)

### 3. Intelligent Recommendations
```python
# Example: Get recommended accounts for cash management
recommended = get_recommended_accounts_for_category(
    AccountCategory.LIQUIDE_MITTEL, 
    limit=5
)
# Returns: Kasse (1000), Bank (1200), etc. with priority flags
```

### 4. Powerful Search & Navigation
- **Category-based browsing**: Find accounts by business function
- **Text search**: Search by account name, number, or description
- **Hierarchical navigation**: Navigate from category to specific accounts
- **Starter account suggestions**: Essential accounts for new businesses

## API Endpoints

### Category Management
```http
GET /accounts/categories
GET /accounts/categories/structure
GET /accounts/categories/{category}/accounts
GET /accounts/categories/{category}/recommended
```

### Standard Account Operations
```http
GET /accounts/standard/{account_number}
GET /accounts/standard/search?query={term}
GET /accounts/standard/starter
POST /accounts/standard/{account_number}/create
```

### Integration Endpoints
```http
GET /accounts/categories  # Category summary with account counts
POST /accounts/standard/{number}/create  # Create from standard template
```

## Usage Examples

### 1. Browse Categories and Accounts
```python
# Get all categories for Aktiva section
categories = get_main_categories("aktiva")

# Get accounts in Liquide Mittel category
accounts = get_accounts_by_category(AccountCategory.LIQUIDE_MITTEL)
# Returns: 1000 (Kasse), 1200 (Bank), 1210 (Postbank), etc.
```

### 2. Smart Account Setup
```python
# Get recommendations for cash accounts
recommended = get_recommended_accounts_for_category(
    AccountCategory.LIQUIDE_MITTEL
)
# Prioritizes: Kasse (1000), Bank (1200)

# Create account from standard template
account_data = create_account_from_standard("1000", initial_balance=5000.0)
# Automatically assigns: category, type, name from standard
```

### 3. Search and Discovery
```python
# Search for bank-related accounts
results = search_accounts("Bank")
# Returns: 1200 (Bank), 1210 (Postbank), 3800 (Verbindlichkeiten Kreditinstitute)

# Get starter accounts for new business
starters = get_starter_accounts()
# Returns essential accounts: 1000, 1200, 1400, 3000, 3700, 3900, etc.
```

### 4. Complete Structure Building
```python
# Get complete Bilanz structure with accounts
structure = get_category_structure_with_accounts()
# Returns hierarchical structure ready for frontend display
```

## Benefits

### For Developers
- **Unified API**: Single interface for categories and accounts
- **Type Safety**: Strong typing with enums and schemas
- **Consistent Structure**: Predictable data formats
- **Easy Integration**: Ready-made endpoints for frontend

### For Users
- **Intuitive Navigation**: Browse by business function
- **Quick Setup**: Smart recommendations for account creation
- **Standards Compliance**: HGB-compliant from the start
- **Efficient Search**: Find accounts by purpose, not just number

### For Businesses
- **Faster Onboarding**: Starter account templates
- **Correct Classification**: Automatic category assignment
- **Professional Structure**: HGB-compliant Bilanz organization
- **Scalable Growth**: Comprehensive account catalog

## Technical Implementation

### Account Category Enum
```python
class AccountCategory(str, Enum):
    # AKTIVA - Main categories
    ANLAGEVERMOEGEN = "anlagevermoegen"
    UMLAUFVERMOEGEN = "umlaufvermoegen"
    
    # AKTIVA - Subcategories
    IMMATERIELLE_ANLAGEN = "immaterielle_anlagen"
    SACHANLAGEN = "sachanlagen"
    LIQUIDE_MITTEL = "liquide_mittel"
    # ... etc
```

### Automatic Category Assignment
```python
ACCOUNT_CATEGORY_RANGES = {
    AccountCategory.LIQUIDE_MITTEL: ("1000", "1299"),
    AccountCategory.FORDERUNGEN: ("1400", "1599"),
    AccountCategory.VERBINDLICHKEITEN: ("3400", "3699"),
    # ... etc
}
```

### Standard Account Catalog
```python
STANDARD_GERMAN_ACCOUNTS = {
    "1000": {
        "name": "Kasse",
        "type": AccountType.AKTIVKONTO,
        "category": AccountCategory.LIQUIDE_MITTEL
    },
    # ... 500+ more accounts
}
```

## Integration with Bilanz Service

The category system seamlessly integrates with the Bilanz service to provide:

1. **Structured Balance Sheet Output**: Accounts grouped by categories
2. **Hierarchical Totals**: Subtotals by subcategory and main category
3. **Professional Formatting**: HGB-compliant Bilanz presentation
4. **Drill-down Capability**: From totals to individual accounts

## Future Extensions

- **P&L Categories**: Extend categories to cover profit & loss accounts
- **DATEV Integration**: Support for SKR03/SKR04 specific mappings
- **Multi-Standard Support**: Switch between different chart standards
- **Custom Categories**: User-defined category extensions
- **Localization**: Support for other accounting standards (IFRS, etc.)

## Conclusion

The integration of account categories with standard accounts creates a powerful, user-friendly system that:

✅ **Simplifies Account Management**: Browse by business function, not just numbers  
✅ **Ensures Compliance**: HGB-standard categories and accounts  
✅ **Accelerates Setup**: Smart recommendations and templates  
✅ **Enables Professional Reporting**: Structured Bilanz output  
✅ **Provides Scalability**: Comprehensive catalog for growth  

This unified approach makes the HGB Accountant system both powerful for experts and accessible for beginners, while maintaining full compliance with German accounting standards.
