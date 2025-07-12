"""
Standard German Chart of Accounts (Standardkontenrahmen HGB)

This module provides the standard German account naming conventions
according to HGB (Handelsgesetzbuch) accounting principles.

Future extensions can include other standards like:
- DATEV SKR03/SKR04
- International standards
- Industry-specific charts
"""

from typing import Dict, List
from enum import Enum
from .account import AccountType
from .account_categories import AccountCategory


class AccountingStandard(str, Enum):
    """Different accounting standards/frameworks"""
    HGB_STANDARD = "hgb_standard"  # German HGB Standard
    DATEV_SKR03 = "datev_skr03"    # DATEV SKR03
    DATEV_SKR04 = "datev_skr04"    # DATEV SKR04
    CUSTOM = "custom"              # Custom chart of accounts


# Standard German Chart of Accounts (Standardkontenrahmen HGB)
STANDARD_GERMAN_ACCOUNTS: Dict[str, Dict] = {
    
    # ===== AKTIVKONTEN (ASSETS) 0000-2999 =====
    
    # Anlagevermögen (Fixed Assets) 0000-0999
    "0100": {"name": "Geschäfts- oder Firmenwert", "type": AccountType.AKTIVKONTO, "category": AccountCategory.IMMATERIELLE_ANLAGEN},
    "0120": {"name": "Gewerbliche Schutzrechte und ähnliche Rechte", "type": AccountType.AKTIVKONTO, "category": AccountCategory.IMMATERIELLE_ANLAGEN},
    "0140": {"name": "Software", "type": AccountType.AKTIVKONTO, "category": AccountCategory.IMMATERIELLE_ANLAGEN},
    "0200": {"name": "Grundstücke und Bauten", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0300": {"name": "Technische Anlagen und Maschinen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0400": {"name": "Andere Anlagen, Betriebs- und Geschäftsausstattung", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0410": {"name": "Büroausstattung", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0420": {"name": "EDV-Anlagen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0500": {"name": "Anlagen im Bau", "type": AccountType.AKTIVKONTO, "category": AccountCategory.SACHANLAGEN},
    "0600": {"name": "Anteile an verbundenen Unternehmen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FINANZANLAGEN},
    "0700": {"name": "Beteiligungen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FINANZANLAGEN},
    "0800": {"name": "Wertpapiere des Anlagevermögens", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FINANZANLAGEN},
    
    # Umlaufvermögen (Current Assets) 1000-2999
    "1000": {"name": "Kasse", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "1200": {"name": "Bank", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "1210": {"name": "Postbank", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "1220": {"name": "Sparkasse", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "1230": {"name": "Fremdwährungskonten", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "1400": {"name": "Forderungen aus Lieferungen und Leistungen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1410": {"name": "Forderungen gegen verbundene Unternehmen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1420": {"name": "Zweifelhafte Forderungen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1500": {"name": "Sonstige Vermögensgegenstände", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1570": {"name": "Geleistete Anzahlungen", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1580": {"name": "Vorsteuer", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    "1600": {"name": "Roh-, Hilfs- und Betriebsstoffe", "type": AccountType.AKTIVKONTO, "category": AccountCategory.VORRAETE},
    "1700": {"name": "Unfertige Erzeugnisse", "type": AccountType.AKTIVKONTO, "category": AccountCategory.VORRAETE},
    "1800": {"name": "Fertige Erzeugnisse", "type": AccountType.AKTIVKONTO, "category": AccountCategory.VORRAETE},
    "1900": {"name": "Waren", "type": AccountType.AKTIVKONTO, "category": AccountCategory.VORRAETE},
    "2000": {"name": "Wertpapiere des Umlaufvermögens", "type": AccountType.AKTIVKONTO, "category": AccountCategory.LIQUIDE_MITTEL},
    "2100": {"name": "Aktive Rechnungsabgrenzungsposten", "type": AccountType.AKTIVKONTO, "category": AccountCategory.FORDERUNGEN},
    
    # ===== PASSIVKONTEN (LIABILITIES & EQUITY) 3000-3999 =====
    
    # Eigenkapital (Equity) 3000-3399
    "3000": {"name": "Gezeichnetes Kapital", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEZEICHNETES_KAPITAL},
    "3100": {"name": "Kapitalrücklagen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.KAPITALRUECKLAGEN},
    "3200": {"name": "Gewinnrücklagen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3210": {"name": "Gesetzliche Rücklage", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3220": {"name": "Freie Rücklagen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3300": {"name": "Gewinnvortrag", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3310": {"name": "Verlustvortrag", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3320": {"name": "Jahresüberschuss", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    "3330": {"name": "Jahresfehlbetrag", "type": AccountType.PASSIVKONTO, "category": AccountCategory.GEWINNRUECKLAGEN},
    
    # Rückstellungen (Provisions) 3400-3699
    "3400": {"name": "Rückstellungen für Pensionen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.RUECKSTELLUNGEN},
    "3410": {"name": "Steuerrückstellungen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.RUECKSTELLUNGEN},
    "3420": {"name": "Sonstige Rückstellungen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.RUECKSTELLUNGEN},
    
    # Verbindlichkeiten (Liabilities) 3700-3999
    "3700": {"name": "Verbindlichkeiten aus Lieferungen und Leistungen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3710": {"name": "Verbindlichkeiten gegen verbundene Unternehmen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3720": {"name": "Wechselverbindlichkeiten", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3750": {"name": "Erhaltene Anzahlungen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3760": {"name": "Sonstige Verbindlichkeiten", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3800": {"name": "Verbindlichkeiten gegenüber Kreditinstituten", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3850": {"name": "Darlehen", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3900": {"name": "Umsatzsteuer", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3910": {"name": "Lohnsteuer", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3920": {"name": "Sozialversicherung", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    "3950": {"name": "Passive Rechnungsabgrenzungsposten", "type": AccountType.PASSIVKONTO, "category": AccountCategory.VERBINDLICHKEITEN},
    
    # ===== AUFWANDSKONTEN (EXPENSES) 4000-7999 =====
    
    # Materialaufwand (Material Expenses) 4000-4999
    "4000": {"name": "Aufwendungen für Roh-, Hilfs- und Betriebsstoffe", "type": AccountType.AUFWANDSKONTO, "category": "Materialaufwand"},
    "4100": {"name": "Aufwendungen für bezogene Waren", "type": AccountType.AUFWANDSKONTO, "category": "Materialaufwand"},
    "4200": {"name": "Aufwendungen für bezogene Leistungen", "type": AccountType.AUFWANDSKONTO, "category": "Materialaufwand"},
    "4300": {"name": "Nachlässe auf Materialaufwand", "type": AccountType.AUFWANDSKONTO, "category": "Materialaufwand"},
    
    # Personalaufwand (Personnel Expenses) 5000-5999
    "5000": {"name": "Löhne und Gehälter", "type": AccountType.AUFWANDSKONTO, "category": "Personalaufwand"},
    "5100": {"name": "Soziale Abgaben", "type": AccountType.AUFWANDSKONTO, "category": "Personalaufwand"},
    "5200": {"name": "Aufwendungen für Altersversorgung", "type": AccountType.AUFWANDSKONTO, "category": "Personalaufwand"},
    "5300": {"name": "Sonstige Personalaufwendungen", "type": AccountType.AUFWANDSKONTO, "category": "Personalaufwand"},
    "5400": {"name": "Freiwillige soziale Aufwendungen", "type": AccountType.AUFWANDSKONTO, "category": "Personalaufwand"},
    
    # Betriebsaufwand (Operating Expenses) 6000-6999
    "6000": {"name": "Abschreibungen auf Sachanlagen", "type": AccountType.AUFWANDSKONTO, "category": "Abschreibungen"},
    "6100": {"name": "Abschreibungen auf immaterielle Vermögensgegenstände", "type": AccountType.AUFWANDSKONTO, "category": "Abschreibungen"},
    "6200": {"name": "Raumkosten", "type": AccountType.AUFWANDSKONTO, "category": "Raumkosten"},
    "6210": {"name": "Mieten", "type": AccountType.AUFWANDSKONTO, "category": "Raumkosten"},
    "6220": {"name": "Nebenkosten", "type": AccountType.AUFWANDSKONTO, "category": "Raumkosten"},
    "6230": {"name": "Heizung", "type": AccountType.AUFWANDSKONTO, "category": "Raumkosten"},
    "6240": {"name": "Strom", "type": AccountType.AUFWANDSKONTO, "category": "Raumkosten"},
    "6300": {"name": "Bürokosten", "type": AccountType.AUFWANDSKONTO, "category": "Bürokosten"},
    "6310": {"name": "Porto", "type": AccountType.AUFWANDSKONTO, "category": "Bürokosten"},
    "6320": {"name": "Telefon", "type": AccountType.AUFWANDSKONTO, "category": "Bürokosten"},
    "6330": {"name": "Büromaterial", "type": AccountType.AUFWANDSKONTO, "category": "Bürokosten"},
    "6400": {"name": "Versicherungen", "type": AccountType.AUFWANDSKONTO, "category": "Versicherungen"},
    "6410": {"name": "Betriebshaftpflicht", "type": AccountType.AUFWANDSKONTO, "category": "Versicherungen"},
    "6420": {"name": "Sachversicherungen", "type": AccountType.AUFWANDSKONTO, "category": "Versicherungen"},
    "6500": {"name": "Reisekosten", "type": AccountType.AUFWANDSKONTO, "category": "Reisekosten"},
    "6510": {"name": "Fahrtkosten", "type": AccountType.AUFWANDSKONTO, "category": "Reisekosten"},
    "6520": {"name": "Übernachtungskosten", "type": AccountType.AUFWANDSKONTO, "category": "Reisekosten"},
    "6530": {"name": "Bewirtungskosten", "type": AccountType.AUFWANDSKONTO, "category": "Reisekosten"},
    "6600": {"name": "Werbung", "type": AccountType.AUFWANDSKONTO, "category": "Werbekosten"},
    "6610": {"name": "Anzeigen", "type": AccountType.AUFWANDSKONTO, "category": "Werbekosten"},
    "6620": {"name": "Messen und Ausstellungen", "type": AccountType.AUFWANDSKONTO, "category": "Werbekosten"},
    "6700": {"name": "Rechts- und Beratungskosten", "type": AccountType.AUFWANDSKONTO, "category": "Beratungskosten"},
    "6710": {"name": "Steuerberatungskosten", "type": AccountType.AUFWANDSKONTO, "category": "Beratungskosten"},
    "6720": {"name": "Wirtschaftsprüfungskosten", "type": AccountType.AUFWANDSKONTO, "category": "Beratungskosten"},
    "6800": {"name": "Verschiedene Aufwendungen", "type": AccountType.AUFWANDSKONTO, "category": "Sonstiges"},
    "6810": {"name": "Bücher und Zeitschriften", "type": AccountType.AUFWANDSKONTO, "category": "Sonstiges"},
    "6820": {"name": "Fortbildung", "type": AccountType.AUFWANDSKONTO, "category": "Sonstiges"},
    "6900": {"name": "Instandhaltung", "type": AccountType.AUFWANDSKONTO, "category": "Instandhaltung"},
    "6910": {"name": "Reparaturen", "type": AccountType.AUFWANDSKONTO, "category": "Instandhaltung"},
    
    # Finanzaufwand (Financial Expenses) 7000-7999
    "7000": {"name": "Zinsen und ähnliche Aufwendungen", "type": AccountType.AUFWANDSKONTO, "category": "Finanzaufwand"},
    "7100": {"name": "Abschreibungen auf Finanzanlagen", "type": AccountType.AUFWANDSKONTO, "category": "Finanzaufwand"},
    "7200": {"name": "Außerordentliche Aufwendungen", "type": AccountType.AUFWANDSKONTO, "category": "Außerordentliches"},
    
    # ===== ERTRAGSKONTEN (REVENUE) 8000-9999 =====
    
    # Umsatzerlöse (Sales Revenue) 8000-8999
    "8000": {"name": "Umsatzerlöse", "type": AccountType.ERTRAGSKONTO, "category": "Umsatzerlöse"},
    "8100": {"name": "Erlösschmälerungen", "type": AccountType.ERTRAGSKONTO, "category": "Umsatzerlöse"},
    "8110": {"name": "Skonti", "type": AccountType.ERTRAGSKONTO, "category": "Umsatzerlöse"},
    "8120": {"name": "Rabatte", "type": AccountType.ERTRAGSKONTO, "category": "Umsatzerlöse"},
    "8200": {"name": "Bestandsveränderungen fertige Erzeugnisse", "type": AccountType.ERTRAGSKONTO, "category": "Bestandsveränderungen"},
    "8300": {"name": "Andere aktivierte Eigenleistungen", "type": AccountType.ERTRAGSKONTO, "category": "Eigenleistungen"},
    
    # Sonstige Erträge (Other Income) 9000-9999
    "9000": {"name": "Zinserträge", "type": AccountType.ERTRAGSKONTO, "category": "Finanzerträge"},
    "9100": {"name": "Erträge aus Beteiligungen", "type": AccountType.ERTRAGSKONTO, "category": "Finanzerträge"},
    "9200": {"name": "Sonstige betriebliche Erträge", "type": AccountType.ERTRAGSKONTO, "category": "Sonstige Erträge"},
    "9210": {"name": "Provisionserlöse", "type": AccountType.ERTRAGSKONTO, "category": "Sonstige Erträge"},
    "9220": {"name": "Mieterlöse", "type": AccountType.ERTRAGSKONTO, "category": "Sonstige Erträge"},
    "9300": {"name": "Außerordentliche Erträge", "type": AccountType.ERTRAGSKONTO, "category": "Außerordentliches"},
    "9400": {"name": "Erträge aus Auflösung von Rückstellungen", "type": AccountType.ERTRAGSKONTO, "category": "Sonstige Erträge"},
    "9900": {"name": "Periodenfremde Erträge", "type": AccountType.ERTRAGSKONTO, "category": "Sonstige Erträge"},
}


class StandardAccountsManager:
    """Manager for different accounting standards and chart of accounts"""
    
    def __init__(self, standard: AccountingStandard = AccountingStandard.HGB_STANDARD):
        self.current_standard = standard
        self._accounts = self._load_accounts_for_standard(standard)
    
    def _load_accounts_for_standard(self, standard: AccountingStandard) -> Dict[str, Dict]:
        """Load accounts for the specified standard"""
        if standard == AccountingStandard.HGB_STANDARD:
            return STANDARD_GERMAN_ACCOUNTS
        # Future: Add other standards here
        else:
            return {}
    
    def get_account(self, account_number: str) -> Dict:
        """Get standard account details by number"""
        return self._accounts.get(account_number, {})
    
    def get_accounts_by_type(self, account_type: AccountType) -> Dict[str, Dict]:
        """Get all standard accounts of a specific type"""
        return {
            number: details 
            for number, details in self._accounts.items() 
            if details.get("type") == account_type
        }
    
    def get_accounts_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all accounts in a specific category"""
        return {
            number: details 
            for number, details in self._accounts.items() 
            if details.get("category", "").lower() == category.lower()
        }
    
    def search_accounts(self, query: str) -> List[Dict]:
        """Search accounts by number, name, or category"""
        query_lower = query.lower()
        results = []
        
        for number, details in self._accounts.items():
            if (query_lower in number or 
                query_lower in details.get("name", "").lower() or 
                query_lower in details.get("category", "").lower()):
                results.append({
                    "number": number,
                    "name": details.get("name", ""),
                    "type": details.get("type"),
                    "category": details.get("category", "")
                })
        
        return sorted(results, key=lambda x: x["number"])
    
    def get_starter_accounts(self) -> List[str]:
        """Get a recommended set of starter accounts for new businesses"""
        return [
            "1000",  # Kasse
            "1200",  # Bank
            "1400",  # Forderungen aus L&L
            "1580",  # Vorsteuer
            "3000",  # Gezeichnetes Kapital
            "3700",  # Verbindlichkeiten aus L&L
            "3900",  # Umsatzsteuer
            "5000",  # Löhne und Gehälter
            "6300",  # Bürokosten
            "6500",  # Reisekosten
            "8000",  # Umsatzerlöse
        ]
    
    def get_all_categories(self) -> List[str]:
        """Get all available account categories"""
        categories = set()
        for details in self._accounts.values():
            if "category" in details:
                categories.add(details["category"])
        return sorted(list(categories))
    
    def get_accounts_in_range(self, start_number: str, end_number: str) -> Dict[str, Dict]:
        """Get accounts in a number range"""
        return {
            number: details 
            for number, details in self._accounts.items() 
            if start_number <= number <= end_number
        }


# ===== INTEGRATED CATEGORY & STANDARD ACCOUNT FUNCTIONS =====

def get_accounts_by_category(category: AccountCategory) -> Dict[str, Dict]:
    """Get all standard accounts for a specific category"""
    return {
        number: details for number, details in STANDARD_GERMAN_ACCOUNTS.items()
        if details.get("category") == category
    }

def get_category_structure_with_accounts() -> Dict:
    """Get the complete category hierarchy with their standard accounts"""
    from .account_categories import CATEGORY_HIERARCHY, get_main_categories, get_subcategories
    
    structure = {}
    
    # Build structure for both aktiva and passiva
    for section in ["aktiva", "passiva"]:
        structure[section] = {}
        main_categories = get_main_categories(section)
        
        for main_cat in main_categories:
            main_info = CATEGORY_HIERARCHY[main_cat]
            main_accounts = get_accounts_by_category(main_cat)
            
            structure[section][main_cat.value] = {
                "name": main_info["name"],
                "accounts": main_accounts,
                "subcategories": {}
            }
            
            # Add subcategories
            subcategories = get_subcategories(main_cat)
            for sub_cat in subcategories:
                sub_info = CATEGORY_HIERARCHY[sub_cat]
                sub_accounts = get_accounts_by_category(sub_cat)
                
                structure[section][main_cat.value]["subcategories"][sub_cat.value] = {
                    "name": sub_info["name"],
                    "accounts": sub_accounts
                }
    
    return structure

def get_recommended_accounts_for_category(category: AccountCategory, limit: int = 5) -> List[Dict]:
    """Get recommended accounts for a specific category"""
    category_accounts = get_accounts_by_category(category)
    
    # Define priority accounts for each category
    priority_accounts = {
        AccountCategory.LIQUIDE_MITTEL: ["1000", "1200"],  # Kasse, Bank
        AccountCategory.FORDERUNGEN: ["1400", "1440"],     # Forderungen aus L&L, Steuererstattungsansprüche
        AccountCategory.VORRAETE: ["1600", "1620"],        # Handelswaren, Rohstoffe
        AccountCategory.SACHANLAGEN: ["0200", "0300", "0410"],  # Grundstücke, Maschinen, Büroausstattung
        AccountCategory.VERBINDLICHKEITEN: ["3700", "3740"],    # Verbindlichkeiten aus L&L, Steuerverbindlichkeiten
        AccountCategory.GEZEICHNETES_KAPITAL: ["3000"],         # Gezeichnetes Kapital
        # Add more as needed
    }
    
    recommended = []
    priority_list = priority_accounts.get(category, [])
    
    # Add priority accounts first
    for account_num in priority_list:
        if account_num in category_accounts:
            account_info = category_accounts[account_num].copy()
            account_info["number"] = account_num
            account_info["is_recommended"] = True
            recommended.append(account_info)
    
    # Add other accounts up to limit
    remaining_slots = limit - len(recommended)
    if remaining_slots > 0:
        for account_num, account_info in list(category_accounts.items())[:remaining_slots]:
            if account_num not in priority_list:
                account_info_copy = account_info.copy()
                account_info_copy["number"] = account_num
                account_info_copy["is_recommended"] = False
                recommended.append(account_info_copy)
    
    return recommended

def create_account_from_standard(account_number: str, initial_balance: float = 0.0) -> Dict:
    """Create account data from standard account with automatic category assignment"""
    standard_account = get_standard_account(account_number)
    if not standard_account:
        raise ValueError(f"Standard account {account_number} not found")
    
    return {
        "number": account_number,
        "name": standard_account["name"],
        "account_type": standard_account["type"],
        "category": standard_account.get("category"),
        "balance": initial_balance,
        "is_active": True,
        "is_standard_account": True
    }

def validate_account_category_consistency(account_number: str, provided_category: AccountCategory = None) -> bool:
    """Validate if the account number is consistent with its category"""
    from .account_categories import get_account_category
    
    # Get category from account number ranges
    derived_category = get_account_category(account_number)
    
    # Get category from standard account definition
    standard_account = get_standard_account(account_number)
    standard_category = standard_account.get("category") if standard_account else None
    
    # Check consistency
    if provided_category:
        return provided_category in [derived_category, standard_category]
    
    both_exist = derived_category is not None and standard_category is not None
    return derived_category == standard_category if both_exist else True

def get_category_summary() -> Dict:
    """Get summary of all categories with account counts"""
    from .account_categories import CATEGORY_HIERARCHY
    
    summary = {}
    for category, info in CATEGORY_HIERARCHY.items():
        accounts = get_accounts_by_category(category)
        summary[category.value] = {
            "name": info["name"],
            "section": info["bilanz_section"],
            "parent": info["parent"].value if info["parent"] else None,
            "account_count": len(accounts),
            "sample_accounts": list(accounts.keys())[:3]  # First 3 as examples
        }
    
    return summary

def get_account_navigation_structure() -> Dict:
    """Get a navigation-friendly structure for frontend use"""
    structure = get_category_structure_with_accounts()
    
    # Simplify for navigation
    navigation = {"aktiva": [], "passiva": []}
    
    for section in ["aktiva", "passiva"]:
        for main_cat_key, main_cat_data in structure[section].items():
            nav_item = {
                "key": main_cat_key,
                "name": main_cat_data["name"],
                "account_count": len(main_cat_data["accounts"]),
                "subcategories": []
            }
            
            for sub_cat_key, sub_cat_data in main_cat_data["subcategories"].items():
                nav_item["subcategories"].append({
                    "key": sub_cat_key,
                    "name": sub_cat_data["name"],
                    "account_count": len(sub_cat_data["accounts"])
                })
            
            navigation[section].append(nav_item)
    
    return navigation


# Global instance for easy access
default_manager = StandardAccountsManager(AccountingStandard.HGB_STANDARD)

# Convenience functions
def get_standard_account(account_number: str) -> Dict:
    """Get standard account details by number"""
    return default_manager.get_account(account_number)

def search_accounts(query: str) -> List[Dict]:
    """Search accounts by number, name, or category"""
    return default_manager.search_accounts(query)

def get_accounts_by_type(account_type: AccountType) -> Dict[str, Dict]:
    """Get all standard accounts of a specific type"""
    return default_manager.get_accounts_by_type(account_type)

def get_starter_accounts() -> List[str]:
    """Get recommended starter accounts"""
    return default_manager.get_starter_accounts()

def get_all_categories() -> List[str]:
    """Get all available account categories"""
    return default_manager.get_all_categories()
