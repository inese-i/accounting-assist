"""
Account Categories for Hierarchical Bilanz Structure

This module defines the hierarchical structure of accounts according to HGB standards:
- Aktiva (Assets): Anlagevermögen, Umlaufvermögen
- Passiva (Liabilities & Equity): Eigenkapital, Fremdkapital

Each category has subcategories that group related accounts together.
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple


class AccountCategory(str, Enum):
    """Account categories for hierarchical Bilanz structure"""
    
    # AKTIVA (Assets) - Main categories
    ANLAGEVERMOEGEN = "anlagevermoegen"           # Fixed Assets
    UMLAUFVERMOEGEN = "umlaufvermoegen"           # Current Assets
    
    # AKTIVA - Anlagevermögen subcategories
    IMMATERIELLE_ANLAGEN = "immaterielle_anlagen" # Intangible Assets
    SACHANLAGEN = "sachanlagen"                   # Tangible Assets
    FINANZANLAGEN = "finanzanlagen"               # Financial Assets
    
    # AKTIVA - Umlaufvermögen subcategories
    VORRAETE = "vorraete"                         # Inventory
    FORDERUNGEN = "forderungen"                   # Receivables
    LIQUIDE_MITTEL = "liquide_mittel"             # Cash & Cash Equivalents
    
    # PASSIVA (Liabilities & Equity) - Main categories
    EIGENKAPITAL = "eigenkapital"                 # Equity
    FREMDKAPITAL = "fremdkapital"                 # Liabilities
    
    # PASSIVA - Eigenkapital subcategories
    GEZEICHNETES_KAPITAL = "gezeichnetes_kapital" # Share Capital
    KAPITALRUECKLAGEN = "kapitalruecklagen"       # Capital Reserves
    GEWINNRUECKLAGEN = "gewinnruecklagen"         # Retained Earnings
    
    # PASSIVA - Fremdkapital subcategories
    VERBINDLICHKEITEN = "verbindlichkeiten"       # Payables
    RUECKSTELLUNGEN = "rueckstellungen"           # Provisions


# Category hierarchy and display information
CATEGORY_HIERARCHY = {
    # AKTIVA - Main categories
    AccountCategory.ANLAGEVERMOEGEN: {
        "name": "Anlagevermögen",
        "parent": None,
        "children": [
            AccountCategory.IMMATERIELLE_ANLAGEN,
            AccountCategory.SACHANLAGEN,
            AccountCategory.FINANZANLAGEN
        ],
        "bilanz_section": "aktiva",
        "sort_order": 1
    },
    AccountCategory.UMLAUFVERMOEGEN: {
        "name": "Umlaufvermögen", 
        "parent": None,
        "children": [
            AccountCategory.VORRAETE,
            AccountCategory.FORDERUNGEN,
            AccountCategory.LIQUIDE_MITTEL
        ],
        "bilanz_section": "aktiva",
        "sort_order": 2
    },
    
    # AKTIVA - Anlagevermögen subcategories
    AccountCategory.IMMATERIELLE_ANLAGEN: {
        "name": "Immaterielle Anlagen",
        "parent": AccountCategory.ANLAGEVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 1
    },
    AccountCategory.SACHANLAGEN: {
        "name": "Sachanlagen",
        "parent": AccountCategory.ANLAGEVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 2
    },
    AccountCategory.FINANZANLAGEN: {
        "name": "Finanzanlagen",
        "parent": AccountCategory.ANLAGEVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 3
    },
    
    # AKTIVA - Umlaufvermögen subcategories
    AccountCategory.VORRAETE: {
        "name": "Vorräte",
        "parent": AccountCategory.UMLAUFVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 1
    },
    AccountCategory.FORDERUNGEN: {
        "name": "Forderungen",
        "parent": AccountCategory.UMLAUFVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 2
    },
    AccountCategory.LIQUIDE_MITTEL: {
        "name": "Liquide Mittel",
        "parent": AccountCategory.UMLAUFVERMOEGEN,
        "children": [],
        "bilanz_section": "aktiva",
        "sort_order": 3
    },
    
    # PASSIVA - Main categories
    AccountCategory.EIGENKAPITAL: {
        "name": "Eigenkapital",
        "parent": None,
        "children": [
            AccountCategory.GEZEICHNETES_KAPITAL,
            AccountCategory.KAPITALRUECKLAGEN,
            AccountCategory.GEWINNRUECKLAGEN
        ],
        "bilanz_section": "passiva",
        "sort_order": 1
    },
    AccountCategory.FREMDKAPITAL: {
        "name": "Fremdkapital",
        "parent": None,
        "children": [
            AccountCategory.VERBINDLICHKEITEN,
            AccountCategory.RUECKSTELLUNGEN
        ],
        "bilanz_section": "passiva",
        "sort_order": 2
    },
    
    # PASSIVA - Eigenkapital subcategories
    AccountCategory.GEZEICHNETES_KAPITAL: {
        "name": "Gezeichnetes Kapital",
        "parent": AccountCategory.EIGENKAPITAL,
        "children": [],
        "bilanz_section": "passiva",
        "sort_order": 1
    },
    AccountCategory.KAPITALRUECKLAGEN: {
        "name": "Kapitalrücklagen",
        "parent": AccountCategory.EIGENKAPITAL,
        "children": [],
        "bilanz_section": "passiva",
        "sort_order": 2
    },
    AccountCategory.GEWINNRUECKLAGEN: {
        "name": "Gewinnrücklagen",
        "parent": AccountCategory.EIGENKAPITAL,
        "children": [],
        "bilanz_section": "passiva",
        "sort_order": 3
    },
    
    # PASSIVA - Fremdkapital subcategories
    AccountCategory.VERBINDLICHKEITEN: {
        "name": "Verbindlichkeiten",
        "parent": AccountCategory.FREMDKAPITAL,
        "children": [],
        "bilanz_section": "passiva",
        "sort_order": 1
    },
    AccountCategory.RUECKSTELLUNGEN: {
        "name": "Rückstellungen",
        "parent": AccountCategory.FREMDKAPITAL,
        "children": [],
        "bilanz_section": "passiva",
        "sort_order": 2
    }
}


# Account number ranges for automatic categorization
ACCOUNT_CATEGORY_RANGES = {
    # Anlagevermögen (Fixed Assets) 0000-0999
    AccountCategory.IMMATERIELLE_ANLAGEN: ("0100", "0199"),
    AccountCategory.SACHANLAGEN: ("0200", "0499"),
    AccountCategory.FINANZANLAGEN: ("0500", "0999"),
    
    # Umlaufvermögen (Current Assets) 1000-2999
    AccountCategory.LIQUIDE_MITTEL: ("1000", "1299"),     # Cash, Bank
    AccountCategory.FORDERUNGEN: ("1400", "1599"),        # Receivables
    AccountCategory.VORRAETE: ("1600", "1999"),           # Inventory
    
    # Eigenkapital (Equity) 3000-3399
    AccountCategory.GEZEICHNETES_KAPITAL: ("3000", "3099"),
    AccountCategory.KAPITALRUECKLAGEN: ("3100", "3199"),
    AccountCategory.GEWINNRUECKLAGEN: ("3200", "3399"),
    
    # Fremdkapital (Liabilities) 3400-3999
    AccountCategory.VERBINDLICHKEITEN: ("3400", "3699"),
    AccountCategory.RUECKSTELLUNGEN: ("3700", "3999"),
}


def get_account_category(account_number: str) -> Optional[AccountCategory]:
    """
    Determine account category based on account number
    
    Args:
        account_number: 4-digit account number as string
        
    Returns:
        AccountCategory or None if no match found
    """
    for category, (start, end) in ACCOUNT_CATEGORY_RANGES.items():
        if start <= account_number <= end:
            return category
    
    # Fallback based on account type ranges
    if "0000" <= account_number <= "2999":
        # Default for assets not in specific ranges
        if "0000" <= account_number <= "0999":
            return AccountCategory.SACHANLAGEN  # Default fixed assets
        else:
            return AccountCategory.LIQUIDE_MITTEL  # Default current assets
    elif "3000" <= account_number <= "3399":
        return AccountCategory.GEZEICHNETES_KAPITAL  # Default equity
    elif "3400" <= account_number <= "3999":
        return AccountCategory.VERBINDLICHKEITEN  # Default liabilities
    
    return None


def get_category_hierarchy(category: AccountCategory) -> Dict:
    """
    Get full hierarchy information for a category
    
    Args:
        category: AccountCategory enum
        
    Returns:
        Dictionary with category information
    """
    return CATEGORY_HIERARCHY.get(category, {})


def get_main_categories(bilanz_section: Optional[str] = None) -> List[AccountCategory]:
    """
    Get all main categories (top-level)
    
    Args:
        bilanz_section: Filter by 'aktiva' or 'passiva', or None for all
        
    Returns:
        List of main category enums
    """
    categories = [
        cat for cat, info in CATEGORY_HIERARCHY.items() 
        if info.get("parent") is None
    ]
    
    if bilanz_section:
        categories = [
            cat for cat in categories 
            if CATEGORY_HIERARCHY[cat].get("bilanz_section") == bilanz_section
        ]
    
    # Sort by sort_order
    categories.sort(key=lambda cat: CATEGORY_HIERARCHY[cat].get("sort_order", 999))
    
    return categories


def get_subcategories(parent_category: AccountCategory) -> List[AccountCategory]:
    """
    Get all subcategories for a parent category
    
    Args:
        parent_category: Parent AccountCategory enum
        
    Returns:
        List of subcategory enums
    """
    parent_info = CATEGORY_HIERARCHY.get(parent_category, {})
    subcategories = parent_info.get("children", [])
    
    # Sort by sort_order
    subcategories.sort(key=lambda cat: CATEGORY_HIERARCHY[cat].get("sort_order", 999))
    
    return subcategories


def get_category_path(category: AccountCategory) -> List[AccountCategory]:
    """
    Get the full path from root to category
    
    Args:
        category: AccountCategory enum
        
    Returns:
        List of categories from root to target category
    """
    path = [category]
    current = category
    
    while True:
        parent = CATEGORY_HIERARCHY.get(current, {}).get("parent")
        if parent is None:
            break
        path.insert(0, parent)
        current = parent
    
    return path


def is_category_in_bilanz_section(category: AccountCategory, bilanz_section: str) -> bool:
    """
    Check if category belongs to a specific Bilanz section
    
    Args:
        category: AccountCategory enum
        bilanz_section: 'aktiva' or 'passiva'
        
    Returns:
        True if category belongs to the section
    """
    return CATEGORY_HIERARCHY.get(category, {}).get("bilanz_section") == bilanz_section
