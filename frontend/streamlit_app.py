import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configure the page
st.set_page_config(
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

class AccountingAPI:
    """Client for the FastAPI backend"""
    
    def __init__(self, base_url: str):
        import logging
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    
    def health_check(self) -> Dict:
        """Check if API is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return {"status": "healthy" if response.status_code == 200 else "unhealthy", "data": response.json()}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_accounts(self) -> List[Dict]:
        """Get all accounts"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/accounts")
            response.raise_for_status()
            self.logger.debug(f"Get accounts response: {response.json()}")
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching accounts: {e}")
            st.error(f"Error fetching accounts: {e}")
            return []
    
    def create_account(self, account_data: Dict) -> Dict:
        """Create a new account"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/accounts",
                json=account_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            self.logger.debug(f"Create account response: {response.json()}")
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTPError during account creation: {e}")
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            self.logger.error(f"Unexpected error during account creation: {e}")
            return {"success": False, "error": str(e)}
    
    def get_account(self, account_number: str) -> Optional[Dict]:
        """Get specific account by number"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/accounts/{account_number}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching account {account_number}: {e}")
            return None
    
    def debit_account(self, account_number: str, amount: float, description: str = "") -> Dict:
        """Debit an account"""
        try:
            data = {"amount": amount}
            if description:
                data["description"] = description
            
            response = requests.post(
                f"{self.base_url}/api/v1/accounts/{account_number}/debit",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def credit_account(self, account_number: str, amount: float, description: str = "") -> Dict:
        """Credit an account"""
        try:
            data = {"amount": amount}
            if description:
                data["description"] = description
            
            response = requests.post(
                f"{self.base_url}/api/v1/accounts/{account_number}/credit",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_bilanz(self, period_end: str = None) -> Dict:
        """Get complete Bilanz (Balance Sheet)"""
        try:
            params = {}
            if period_end:
                params["period_end"] = period_end
            
            response = requests.get(f"{self.base_url}/api/v1/bilanz/", params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            self.logger.error(f"Error fetching Bilanz: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_bilanz(self, period_end: str = None) -> Dict:
        """Validate Bilanz balance"""
        try:
            params = {}
            if period_end:
                params["period_end"] = period_end
            
            response = requests.get(f"{self.base_url}/api/v1/bilanz/validate", params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            self.logger.error(f"Error validating Bilanz: {e}")
            return {"success": False, "error": str(e)}
    
    def get_account_resolution(self, account_number: str) -> Dict:
        """Get how an account contributes to Bilanz"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/bilanz/account/{account_number}/resolution")
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            self.logger.error(f"Error getting account resolution: {e}")
            return {"success": False, "error": str(e)}
    
    def process_transaction(self, from_account: str, to_account: str, amount: float, description: str = "") -> Dict:
        """Process a transaction between two accounts"""
        try:
            transaction_data = {
                "from_account": from_account,
                "to_account": to_account,
                "amount": amount,
                "description": description
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/accounts/transaction",
                json=transaction_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ===== Standard Accounts Methods =====
    
    def search_standard_accounts(self, query: str, limit: int = 10) -> Dict:
        """Search standard German accounts"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/accounts/standard/search",
                params={"query": query, "limit": limit}
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            self.logger.error(f"Error searching standard accounts: {e}")
            return {"success": False, "error": str(e)}
    
    def get_standard_account_info(self, account_number: str) -> Dict:
        """Get standard account information"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/accounts/standard/{account_number}")
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            self.logger.error(f"Error fetching standard account info: {e}")
            return {"success": False, "error": str(e)}
    
    def create_standard_account(self, account_number: str, initial_balance: float = 0.0) -> Dict:
        """Create a standard account"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/accounts/standard/{account_number}",
                params={"initial_balance": initial_balance}
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_starter_accounts(self) -> Dict:
        """Create starter account pack"""
        try:
            response = requests.post(f"{self.base_url}/api/v1/accounts/standard/starter-pack")
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"success": False, "error": error_detail}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ===== End Standard Accounts Methods =====
# Initialize API client
api = AccountingAPI(API_BASE_URL)

def show_api_status():
    """Display API connection status"""
    status = api.health_check()
    if status["status"] == "healthy":
        st.success("✅ Connected to API")
    elif status["status"] == "unhealthy":
        st.warning("⚠️ API is running but returned an error")
    else:
        st.error(f"❌ Cannot connect to API: {status.get('error', 'Unknown error')}")
        st.info("Make sure the FastAPI backend is running on http://localhost:8000")

def format_currency(amount: float) -> str:
    """Format amount as Euro currency"""
    return f"€{amount:,.2f}"

def account_type_info():
    """Display account type information"""

    
    account_types = {
        "Aktivkonto (Bestandskonto)": {
            "numbers": "0000-2999",
            "examples": "Kasse, Bank, Forderungen, Vorräte, Anlagevermögen",
            "debit": "Increases balance (Zugang)",
            "credit": "Decreases balance (Abgang)",
            "color": "#28a745",
            "nature": "Bestandskonto - appears in Bilanz (Balance Sheet)"
        },
        "Passivkonto (Bestandskonto)": {
            "numbers": "3000-3999",
            "examples": "Verbindlichkeiten, Kredite, Eigenkapital, Rückstellungen",
            "debit": "Decreases balance (Tilgung)",
            "credit": "Increases balance (Aufnahme)",
            "color": "#dc3545",
            "nature": "Bestandskonto - appears in Bilanz (Balance Sheet)"
        },
        "Aufwandskonto (Erfolgskonto)": {
            "numbers": "4000-7999",
            "examples": "Bürokosten, Reisekosten, Gehälter, Miete, Abschreibungen",
            "debit": "Increases expenses (Aufwand)",
            "credit": "Corrections/Reversals (Stornierung)",
            "color": "#fd7e14",
            "nature": "Erfolgskonto - affects Gewinn/Verlust (P&L)"
        },
        "Ertragskonto (Erfolgskonto)": {
            "numbers": "8000-9999",
            "examples": "Umsatzerlöse, Zinserträge, außerordentliche Erträge",
            "debit": "Corrections/Reversals (Stornierung)",
            "credit": "Increases revenue (Ertrag)",
            "color": "#20c997",
            "nature": "Erfolgskonto - affects Gewinn/Verlust (P&L)"
        }
    }
    
    for account_type, info in account_types.items():
        with st.expander(f"{account_type} ({info['numbers']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Examples:** {info['examples']}")
                st.write(f"**Debit (Soll):** {info['debit']}")
            with col2:
                st.write(f"**Credit (Haben):** {info['credit']}")
                st.info(f"**Nature:** {info['nature']}")

def show_account_details(account: Dict):
    """Display detailed information for an account, including Soll/Haben balances"""
    st.write(f"Account: {account['number']} - {account['name']}")
    st.write(f"**Type:** {account['account_type']}")
    st.write(f"**Soll Balance:** {format_currency(account['soll_balance'])}")
    st.write(f"**Haben Balance:** {format_currency(account['haben_balance'])}")
    st.write(f"**Net Balance:** {format_currency(account['soll_balance'] - account['haben_balance'])}")

# Main UI

def main():
    """Main Streamlit application"""

    # Sidebar for navigation
    with st.sidebar:
        st.write("**Navigation**")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Dashboard", "➕ Create Account", "💰 Transactions", "📊 Account Types", "📋 Bilanz", "🔧 API Status"]
        )
        
        st.markdown("---")
        st.markdown("### Quick Actions")
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "➕ Create Account":
        show_create_account()
    elif page == "💰 Transactions":
        show_transactions()
    elif page == "📊 Account Types":
        account_type_info()
    elif page == "📋 Bilanz":
        show_bilanz()
    elif page == "🔧 API Status":
        show_api_status_page()

def show_dashboard():
    """Display the main dashboard"""

    
    # Check API status
    show_api_status()
    
    # Get accounts
    accounts = api.get_accounts()
    
    if not accounts:
        st.info("No accounts found. Create your first account using the 'Create Account' page.")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(accounts)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Accounts", len(accounts))
    
    with col2:
        total_balance = sum(acc.get("balance", 0) for acc in accounts)
        st.metric("Total Balance", format_currency(total_balance))
    
    with col3:
        bestandskonten = [acc for acc in accounts if acc.get("account_type") in ["aktivkonto", "passivkonto"]]
        st.metric("Bestandskonten", len(bestandskonten))
    
    with col4:
        erfolgskonten = [acc for acc in accounts if acc.get("account_type") in ["aufwandskonto", "ertragskonto"]]
        st.metric("Erfolgskonten", len(erfolgskonten))
    
    # Accounts table
    st.write("**💼 All Accounts**")
    
    # Format the dataframe for display
    display_df = df.copy()
    if "balance" in display_df.columns:
        display_df["balance"] = display_df["balance"].apply(format_currency)
    if "created_at" in display_df.columns:
        display_df["created_at"] = pd.to_datetime(display_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "number": "Account #",
            "name": "Account Name",
            "account_type": "Type",
            "balance": "Balance",
            "is_active": "Active",
            "created_at": "Created"
        }
    )
    
    # Account type distribution
    if len(accounts) > 0:
        st.write("**📊 Account Distribution**")
        type_counts = df["account_type"].value_counts()
        st.bar_chart(type_counts)
    
    # Detailed account information
    st.write("**📋 Detailed Account Information**")
    for account in accounts:
        show_account_details(account)

def show_create_account():
    """Display the create account form"""

    # Add tabs for different creation methods
    tab1, tab2, tab3 = st.tabs(["🏗️ Custom Account", "📋 Standard Accounts", "🚀 Quick Start"])
    
    with tab1:
        st.write("**Create a custom account with your own details**")
        
        with st.form("create_account_form"):
            col1, col2 = st.columns(2)

            with col1:
                account_number = st.text_input(
                    "Account Number",
                    help="4-digit German account number (e.g., 1000)",
                    placeholder="1000"
                )

                account_name = st.text_input(
                    "Account Name",
                    help="Descriptive name for the account",
                    placeholder="Kasse"
                )

                account_type = st.selectbox(
                    "Account Type",
                    options=["aktivkonto", "passivkonto", "aufwandskonto", "ertragskonto"],
                    format_func=lambda x: {
                        "aktivkonto": "Aktivkonto (Bestandskonto - Assets)",
                        "passivkonto": "Passivkonto (Bestandskonto - Liabilities/Equity)",
                        "aufwandskonto": "Aufwandskonto (Erfolgskonto - Expenses)",
                        "ertragskonto": "Ertragskonto (Erfolgskonto - Revenue)"
                    }[x]
                )

            with col2:
                initial_balance = st.number_input(
                    "Initial Balance (€)",
                    min_value=0.0,
                    value=0.0,
                    step=0.01,
                    help="Starting balance for the account"
                )

                parent_account = st.text_input(
                    "Parent Account (Optional)",
                    help="Parent account number if this is a sub-account",
                    placeholder="e.g., 1000"
                )

                is_active = st.checkbox("Active Account", value=True)

            submitted = st.form_submit_button("Create Account", type="primary")

            if submitted:
                # Validate input
                if not account_number or not account_name:
                    st.error("Account number and name are required!")
                    return

                if not account_number.isdigit() or len(account_number) != 4:
                    st.error("Account number must be exactly 4 digits!")
                    return

                # Prepare account data
                account_data = {
                    "number": account_number,
                    "name": account_name,
                    "account_type": account_type,
                    "balance": initial_balance,
                    "is_active": is_active
                }

                if parent_account:
                    account_data["parent_account"] = parent_account

                # Create account
                result = api.create_account(account_data)

                if result["success"]:
                    st.success(f"✅ Account {account_number} '{account_name}' created successfully!")
                    st.json(result["data"])
                else:
                    st.error(f"❌ Failed to create account: {result['error']}")
    
    with tab2:
        st.write("**🇩🇪 Search and create from standard German accounts**")
        
        # Search for standard accounts with dropdown suggestions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "🔍 Search Standard Accounts",
                placeholder="Start typing: 1000, kasse, bank, büro...",
                help="Search by account number (1000), name (Kasse), or category (liquide mittel)",
                key="search_input"
            )
        
        with col2:
            if st.button("🔍 Search", key="search_button"):
                # Trigger search when button is clicked
                pass
        
        # Show quick suggestions dropdown when user starts typing
        if search_query and len(search_query) >= 1:
            # Get suggestions for dropdown
            suggestion_result = api.search_standard_accounts(search_query, limit=8)
            
            if suggestion_result["success"] and suggestion_result["data"]["results"]:
                suggestions = suggestion_result["data"]["results"]
                
                # Create dropdown options
                dropdown_options = ["Select an account..."] + [
                    f"{acc['number']} - {acc['name']} ({acc['category']})" 
                    for acc in suggestions
                ]
                
                selected_suggestion = st.selectbox(
                    "📋 Quick Select:",
                    options=dropdown_options,
                    key="suggestion_dropdown"
                )
                
                # If user selects from dropdown, auto-fill search
                if selected_suggestion != "Select an account...":
                    selected_number = selected_suggestion.split(" - ")[0]
                    st.info(f"💡 Selected: {selected_suggestion}")
                    
                    # Show create button for selected account
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        initial_balance = st.number_input(
                            f"Initial Balance for {selected_number} (€)",
                            min_value=0.0,
                            value=0.0,
                            step=0.01,
                            key=f"quick_balance_{selected_number}"
                        )
                    with col2:
                        if st.button(f"✅ Create {selected_number}", key=f"quick_create_{selected_number}"):
                            create_result = api.create_standard_account(selected_number, initial_balance)
                            if create_result["success"]:
                                st.success(f"✅ Created {selected_number}")
                                st.info("💡 Use 'Refresh Data' to see the new account")
                            else:
                                st.error(f"❌ {create_result['error']}")
                
                st.markdown("---")
        
        # Full search results (when user wants to see detailed matches)
        if search_query and len(search_query) >= 2:
            search_result = api.search_standard_accounts(search_query, limit=15)
            
            if search_result["success"]:
                results = search_result["data"]["results"]
                
                if results:
                    st.write(f"**📋 Found {len(results)} matching accounts:**")
                    
                    for account in results:
                        with st.expander(f"🏦 {account['number']} - {account['name']} ({account['type']})"):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            
                            with col1:
                                st.write(f"**Number:** {account['number']}")
                                st.write(f"**Name:** {account['name']}")
                                st.write(f"**Type:** {account['type']}")
                            
                            with col2:
                                st.write(f"**Category:** {account.get('category', 'N/A')}")
                                if account.get('already_exists'):
                                    st.warning("⚠️ Already exists in your system")
                                    if 'current_balance' in account:
                                        st.write(f"**Current Balance:** {format_currency(account['current_balance'])}")
                                else:
                                    st.success("✅ Available to create")
                            
                            with col3:
                                if not account.get('already_exists'):
                                    initial_balance_key = f"balance_{account['number']}"
                                    balance = st.number_input(
                                        "Initial Balance (€)",
                                        min_value=0.0,
                                        value=0.0,
                                        step=0.01,
                                        key=initial_balance_key
                                    )
                                    
                                    if st.button(f"Create {account['number']}", key=f"create_{account['number']}"):
                                        create_result = api.create_standard_account(account['number'], balance)
                                        
                                        if create_result["success"]:
                                            st.success(f"✅ Created account {account['number']} - {account['name']}")
                                            st.info("💡 Use the 'Refresh Data' button in the sidebar to see the new account")
                                        else:
                                            st.error(f"❌ Failed to create: {create_result['error']}")
                else:
                    st.info("No matching accounts found. Try a different search term.")
            else:
                st.error(f"Search failed: {search_result['error']}")
        elif search_query and len(search_query) == 1:
            st.info("💡 Keep typing - suggestions appear above, detailed results show with 2+ characters")
        
        # Quick access to common accounts
        st.markdown("---")
        st.write("**🎯 Quick Access - Common Accounts**")
        
        common_accounts = [
            ("1000", "Kasse (Cash)"),
            ("1200", "Bank (Bank Account)"),
            ("1400", "Forderungen aus L&L (Accounts Receivable)"),
            ("3000", "Gezeichnetes Kapital (Share Capital)"),
            ("3700", "Verbindlichkeiten aus L&L (Accounts Payable)"),
            ("8000", "Umsatzerlöse (Sales Revenue)")
        ]
        
        cols = st.columns(2)
        for i, (number, name) in enumerate(common_accounts):
            with cols[i % 2]:
                if st.button(f"📋 Create {number} - {name.split('(')[0].strip()}", key=f"quick_{number}"):
                    create_result = api.create_standard_account(number, 0.0)
                    
                    if create_result["success"]:
                        st.success(f"✅ Created {number} - {name}")
                        st.info("💡 Use 'Refresh Data' to see the new account")
                    else:
                        st.error(f"❌ {create_result['error']}")
    
    with tab3:
        st.write("**🚀 Quick Start - Create Essential Business Accounts**")
        st.write("This will create a complete set of accounts needed for basic German bookkeeping.")
        
        st.info("""
        **Starter Pack includes:**
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
        """)
        
        if st.button("🚀 Create All Starter Accounts", type="primary"):
            with st.spinner("Creating starter accounts..."):
                result = api.create_starter_accounts()
                
                if result["success"]:
                    data = result["data"]
                    st.success(f"✅ {data['message']}")
                    
                    if data.get("created_accounts"):
                        st.write("**Created Accounts:**")
                        for acc in data["created_accounts"]:
                            st.write(f"- {acc['number']}: {acc['name']} ({acc['type']})")
                    
                    st.info("💡 Use 'Refresh Data' to see all new accounts")
                else:
                    data = result["data"]
                    st.warning(f"⚠️ {data.get('message', 'Some accounts could not be created')}")
                    
                    if data.get("errors"):
                        st.write("**Errors:**")
                        for error in data["errors"]:
                            st.error(f"- {error}")
                    
                    if data.get("created_accounts"):
                        st.write(f"**Successfully created {data.get('created_accounts', 0)} accounts**")

def show_transactions():
    """Display the transactions page"""

    
    # Get accounts for selection
    accounts = api.get_accounts()
    
    if not accounts:
        st.warning("No accounts available. Create an account first.")
        return
    
    # Create tabs for different transaction types
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Transfer Between Accounts", "💵 Single Account Operations", "📊 Transaction History", "📚 Bilanzveränderungen"])
    
    with tab1:
        st.write("**🔄 Double-Entry Transaction (Transfer)**")
        st.write("Process transactions between two accounts following German double-entry bookkeeping principles.")
        
        # Create simple account number list with names for display
        account_numbers = [acc['number'] for acc in accounts]
        account_dict = {acc['number']: acc for acc in accounts}
        
        # Account selection OUTSIDE the form
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**From Account (Will be debited - SOLL)**")
            from_account = st.selectbox(
                "Source Account", 
                account_numbers,
                format_func=lambda x: f"{x} - {account_dict[x]['name']} ({account_dict[x]['account_type']})",
                key="from_account_select"
            )
            
            # Show account details
            from_acc_details = account_dict[from_account]
            st.info(f"Current Balance: {format_currency(from_acc_details['balance'])}")
        
        with col2:
            st.markdown("**To Account (Will be credited - HABEN)**")
            to_account = st.selectbox(
                "Target Account", 
                account_numbers,
                format_func=lambda x: f"{x} - {account_dict[x]['name']} ({account_dict[x]['account_type']})",
                key="to_account_select"
            )
            
            # Show account details
            to_acc_details = account_dict[to_account]
            st.info(f"Current Balance: {format_currency(to_acc_details['balance'])}")
        
        # Account type validation and guidance
        from_acc_type = from_acc_details['account_type']
        to_acc_type = to_acc_details['account_type']
        
        # Provide guidance based on German accounting principles
        st.write("**📚 Transaction Guidance & Bilanzveränderungen**")
        
        # Determine the type of balance sheet change
        bilanz_change_type = ""
        bilanz_effect = ""
        
        if from_acc_type == 'aktivkonto' and to_acc_type == 'aktivkonto':
            bilanz_change_type = "🔄 **Aktivtausch** (Asset Exchange)"
            bilanz_effect = "**Bilanz Effect**: No change in balance sheet total - assets are exchanged"
            st.info("💰 **Asset Transfer**: Moving value between asset accounts (e.g., Bank to Cash)")
        elif from_acc_type == 'passivkonto' and to_acc_type == 'passivkonto':
            bilanz_change_type = "🔄 **Passivtausch** (Liability Exchange)"
            bilanz_effect = "**Bilanz Effect**: No change in balance sheet total - liabilities are exchanged"
            st.info("💳 **Liability Transfer**: Transferring between liability accounts")
        elif (from_acc_type == 'aktivkonto' and to_acc_type == 'passivkonto'):
            bilanz_change_type = "📈 **Bilanzverlängerung** (Balance Sheet Extension)"
            bilanz_effect = "**Bilanz Effect**: Increases balance sheet total - both assets and liabilities increase"
            st.info("🏦 **Taking Loan/Borrowing**: Receiving money increases asset and liability (e.g., Bank to Loan Payable)")
        elif (from_acc_type == 'passivkonto' and to_acc_type == 'aktivkonto'):
            bilanz_change_type = "📉 **Bilanzverkürzung** (Balance Sheet Contraction)"
            bilanz_effect = "**Bilanz Effect**: Decreases balance sheet total - both assets and liabilities decrease"
            st.info("💳 **Loan Payment**: Using assets to pay off liabilities (e.g., Loan Payable to Bank)")
        elif from_acc_type in ['aufwandskonto', 'ertragskonto'] or to_acc_type in ['aufwandskonto', 'ertragskonto']:
            bilanz_change_type = "� **Erfolgswirksame Buchung** (P&L Transaction)"
            bilanz_effect = "**Effect**: Involves Erfolgskonten - affects Gewinn/Verlust (Profit/Loss)"
            if from_acc_type == 'aufwandskonto' and to_acc_type == 'aktivkonto':
                st.info("💼 **Expense Payment**: Paying expenses reduces assets and increases costs")
            elif from_acc_type == 'aktivkonto' and to_acc_type == 'ertragskonto':
                st.info("💰 **Revenue Receipt**: Receiving revenue increases assets and income")
            elif from_acc_type == 'aufwandskonto' and to_acc_type == 'passivkonto':
                st.info("� **Accrued Expense**: Recording unpaid expenses increases costs and liabilities")
            elif from_acc_type == 'passivkonto' and to_acc_type == 'ertragskonto':
                st.info("💸 **Deferred Revenue**: Recording advance payments increases liabilities and revenue")
            else:
                st.info("� **Business Transaction**: Transaction involving profit/loss accounts")
        else:
            bilanz_change_type = "⚠️ **Review Transaction**"
            bilanz_effect = "**Effect**: Please verify this transaction type"
            st.warning("⚠️ **Review Transaction**: Please verify this transaction type is correct")
        
        # Display the balance sheet change type
        st.markdown(f"**{bilanz_change_type}**")
        st.caption(bilanz_effect)
        
        # Show specific account effects according to "Soll an Haben" principle
        st.markdown("**Transaction Effects (Soll an Haben):**")
        
        col_effect1, col_effect2 = st.columns(2)
        with col_effect1:
            st.markdown(f"**SOLL (Debit Side):**")
            st.markdown(f"Account: **{from_account}** ({from_acc_details['name']})")
            if from_acc_type == 'aktivkonto':
                st.write(f"📈 **Effect**: Asset balance will **increase**")
                st.write(f"⚖️ **T-Account**: +Amount on SOLL side")
            elif from_acc_type == 'passivkonto':
                st.write(f"📉 **Effect**: Liability balance will **decrease**")
                st.write(f"⚖️ **T-Account**: +Amount on SOLL side")
            elif from_acc_type == 'aufwandskonto':
                st.write(f"📊 **Effect**: Expense (Aufwand) will **increase**")
                st.write(f"⚖️ **T-Account**: +Amount on SOLL side")
            elif from_acc_type == 'ertragskonto':
                st.write(f"� **Effect**: Revenue correction/reversal")
                st.write(f"⚖️ **T-Account**: +Amount on SOLL side")
            else:
                st.write(f"�📊 **Effect**: Will be debited (+SOLL)")
        
        with col_effect2:
            st.markdown(f"**HABEN (Credit Side):**")
            st.markdown(f"Account: **{to_account}** ({to_acc_details['name']})")
            if to_acc_type == 'aktivkonto':
                st.write(f"📉 **Effect**: Asset balance will **decrease**")
                st.write(f"⚖️ **T-Account**: +Amount on HABEN side")
            elif to_acc_type == 'passivkonto':
                st.write(f"📈 **Effect**: Liability balance will **increase**")
                st.write(f"⚖️ **T-Account**: +Amount on HABEN side")
            elif to_acc_type == 'aufwandskonto':
                st.write(f"🔄 **Effect**: Expense correction/reversal")
                st.write(f"⚖️ **T-Account**: +Amount on HABEN side")
            elif to_acc_type == 'ertragskonto':
                st.write(f"📈 **Effect**: Revenue (Ertrag) will **increase**")
                st.write(f"⚖️ **T-Account**: +Amount on HABEN side")
            else:
                st.write(f"📊 **Effect**: Will be credited (+HABEN)")
        
        # Validation outside form
        accounts_are_same = from_account == to_account
        
        if accounts_are_same:
            st.error("❌ Source and target accounts cannot be the same!")
        else:
            st.success("✅ Ready to process transaction")
        
        # Transaction details (outside form for real-time preview)
        amount = st.number_input("Amount (€)", min_value=0.01, step=0.01, key="trans_amount")
        description = st.text_input("Description", placeholder="e.g., Office supplies purchase", key="trans_desc")
        
        # Transaction preview (shows immediately when amount is entered)
        if not accounts_are_same and amount > 0:
            st.markdown("**Transaction Preview (Buchungssatz):**")
            st.code(f"SOLL: {from_account} ({from_acc_details['name']}) = €{amount:.2f}")
            st.code(f"HABEN: {to_account} ({to_acc_details['name']}) = €{amount:.2f}")
            st.info(f"📝 **Buchungssatz**: {from_account} ({from_acc_details['name']}) an {to_account} ({to_acc_details['name']}) €{amount:.2f}")
        
        # Transaction form with just the submit button
        with st.form("transaction_form"):
            submitted = st.form_submit_button("💸 Process Transaction", type="primary", disabled=accounts_are_same or amount <= 0)
            
            if submitted and not accounts_are_same:
                result = api.process_transaction(from_account, to_account, amount, description)
                if result["success"]:
                    data = result["data"]
                    st.success(f"✅ Transaction processed successfully!")
                    
                    # Show validation warnings if any
                    if "validation_warnings" in data and data["validation_warnings"]:
                        st.write("**📋 Transaction Validation**")
                        for warning in data["validation_warnings"]:
                            if warning.startswith("INFO:"):
                                st.info(warning)
                            elif warning.startswith("WARNING:"):
                                st.warning(warning)
                            else:
                                st.write(warning)
                    
                    st.json({
                        "from_account": data["from_account"],
                        "to_account": data["to_account"],
                        "amount": f"€{data['amount']:.2f}",
                        "description": data["description"],
                        "new_balances": {
                            "debit_account": f"€{data['debit_account_balance']:.2f}",
                            "credit_account": f"€{data['credit_account_balance']:.2f}"
                        }
                    })
                    st.info("💡 Use 'Refresh Data' to see updated balances")
                else:
                    st.error(f"❌ Transaction failed: {result['error']}")
    
    with tab2:
        st.write("**💵 Single Account Operations**")
        st.write("Perform individual debit or credit operations on a single account.")
        
        # Account selection
        account_options = {f"{acc['number']} - {acc['name']}": acc['number'] for acc in accounts}
        selected_account_display = st.selectbox("Select Account", list(account_options.keys()))
        selected_account = account_options[selected_account_display]
        
        # Get account details
        account_details = api.get_account(selected_account)
        
        if account_details:
            # Display account info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Account Number", account_details["number"])
            with col2:
                st.metric("Account Name", account_details["name"])
            with col3:
                st.metric("Current Balance", format_currency(account_details["balance"]))
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Debit Transaction** (Add to Soll)")
                with st.form("debit_form"):
                    debit_amount = st.number_input("Debit Amount (€)", min_value=0.01, step=0.01, key="debit")
                    debit_description = st.text_input("Description", placeholder="Optional description", key="debit_desc")
                    debit_submitted = st.form_submit_button("💵 Debit Account", type="primary")
                    
                    if debit_submitted:
                        result = api.debit_account(selected_account, debit_amount, debit_description)
                        if result["success"]:
                            st.success(f"✅ Debited {format_currency(debit_amount)} from account {selected_account}")
                            st.info("💡 Use 'Refresh Data' to see updated balance")
                        else:
                            st.error(f"❌ Debit failed: {result['error']}")
            
            with col2:
                st.markdown("**Credit Transaction** (Add to Haben)")
                with st.form("credit_form"):
                    credit_amount = st.number_input("Credit Amount (€)", min_value=0.01, step=0.01, key="credit")
                    credit_description = st.text_input("Description", placeholder="Optional description", key="credit_desc")
                    credit_submitted = st.form_submit_button("💳 Credit Account", type="primary")
                    
                    if credit_submitted:
                        result = api.credit_account(selected_account, credit_amount, credit_description)
                        if result["success"]:
                            st.success(f"✅ Credited {format_currency(credit_amount)} to account {selected_account}")
                            st.info("💡 Use 'Refresh Data' to see updated balance")
                        else:
                            st.error(f"❌ Credit failed: {result['error']}")
    
    with tab3:
        st.write("**📊 Transaction History**")
        st.write("View all account entries and transaction history.")
        
        # Account selection for history
        account_options = {f"{acc['number']} - {acc['name']}": acc['number'] for acc in accounts}
        selected_account_display = st.selectbox("Select Account for History", list(account_options.keys()), key="history_account")
        selected_account = account_options[selected_account_display]
        
        # Get account details
        account_details = api.get_account(selected_account)
        
        if account_details:
            st.write(f"**Account: {account_details['name']} ({account_details['number']})**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Soll Balance", format_currency(account_details['soll_balance']))
            with col2:
                st.metric("Haben Balance", format_currency(account_details['haben_balance']))
            with col3:
                st.metric("Net Balance", format_currency(account_details['balance']))
            
            st.markdown("---")
            
            # Display entries in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Soll Entries (Debit)")
                if account_details['soll_entries']:
                    soll_df = pd.DataFrame(account_details['soll_entries'])
                    soll_df['amount'] = soll_df['amount'].apply(format_currency)
                    soll_df['date'] = pd.to_datetime(soll_df['date']).dt.strftime("%Y-%m-%d %H:%M")
                    st.dataframe(soll_df, use_container_width=True)
                else:
                    st.info("No Soll entries found.")
            
            with col2:
                st.markdown("### 📉 Haben Entries (Credit)")
                if account_details['haben_entries']:
                    haben_df = pd.DataFrame(account_details['haben_entries'])
                    haben_df['amount'] = haben_df['amount'].apply(format_currency)
                    haben_df['date'] = pd.to_datetime(haben_df['date']).dt.strftime("%Y-%m-%d %H:%M")
                    st.dataframe(haben_df, use_container_width=True)
                else:
                    st.info("No Haben entries found.")

    with tab4:
        st.write("**📚 Typen von Bilanzveränderungen (Types of Balance Sheet Changes)**")
        st.write("In German accounting, every business transaction affects the balance sheet in one of four ways:")
        
        # Create a visual representation of the four types
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔄 Ohne Veränderung der Bilanzsumme")
            st.markdown("**(No Change in Balance Sheet Total)**")
            
            with st.expander("🔄 Aktivtausch (Asset Exchange)"):
                st.write("**Definition**: Exchange between two asset accounts")
                st.write("**Effect**: Balance sheet total remains unchanged")
                st.write("**Example**: Transfer money from Bank to Cash")
                st.code("Bank (Aktivkonto) an Kasse (Aktivkonto)")
                st.write("- Soll: Kasse +€1,000")
                st.write("- Haben: Bank -€1,000")
                st.info("💡 Both accounts are on the same side (Aktiva), so total Aktiva stays the same")
            
            with st.expander("🔄 Passivtausch (Liability Exchange)"):
                st.write("**Definition**: Exchange between two liability accounts")
                st.write("**Effect**: Balance sheet total remains unchanged")
                st.write("**Example**: Convert short-term loan to long-term loan")
                st.code("Kurzfristige Verbindlichkeiten an Langfristige Verbindlichkeiten")
                st.write("- Soll: Short-term debt -€5,000")
                st.write("- Haben: Long-term debt +€5,000")
                st.info("💡 Both accounts are on the same side (Passiva), so total Passiva stays the same")
        
        with col2:
            st.markdown("### 📊 Mit Veränderung der Bilanzsumme")
            st.markdown("**(With Change in Balance Sheet Total)**")
            
            with st.expander("📈 Bilanzverlängerung (Balance Sheet Extension)"):
                st.write("**Definition**: Increase in both Aktiva and Passiva")
                st.write("**Effect**: Balance sheet total increases")
                st.write("**Example**: Taking out a loan")
                st.code("Bank (Aktivkonto) an Darlehen (Passivkonto)")
                st.write("- Soll: Bank +€10,000 (Aktiva increases)")
                st.write("- Haben: Loan +€10,000 (Passiva increases)")
                st.success("📈 Both sides of the balance sheet grow by the same amount")
            
            with st.expander("📉 Bilanzverkürzung (Balance Sheet Contraction)"):
                st.write("**Definition**: Decrease in both Aktiva and Passiva")
                st.write("**Effect**: Balance sheet total decreases")
                st.write("**Example**: Paying off a loan")
                st.code("Darlehen (Passivkonto) an Bank (Aktivkonto)")
                st.write("- Soll: Loan -€5,000 (Passiva decreases)")
                st.write("- Haben: Bank -€5,000 (Aktiva decreases)")
                st.success("📉 Both sides of the balance sheet shrink by the same amount")
        
        st.markdown("---")
        st.markdown("### 🎯 Key Principles")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Aktivtausch", "Aktiva ↔ Aktiva", delta="0", delta_color="off")
            st.caption("Same side exchange")
        
        with col2:
            st.metric("Passivtausch", "Passiva ↔ Passiva", delta="0", delta_color="off")
            st.caption("Same side exchange")
        
        with col3:
            st.metric("Bilanzverlängerung", "A↑ + P↑", delta="+", delta_color="normal")
            st.caption("Both sides grow")
        
        with col4:
            st.metric("Bilanzverkürzung", "A↓ + P↓", delta="-", delta_color="inverse")
            st.caption("Both sides shrink")
        
        st.info("💡 **Remember**: In German double-entry bookkeeping, the balance sheet equation must always balance: **Aktiva = Passiva + Eigenkapital**")
        
        st.markdown("---")
        st.markdown("### 📊 Erfolgskonten (Success Accounts)")
        st.write("**Erfolgswirksame Geschäftsvorfälle** involve Erfolgskonten and affect the company's profit/loss:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📈 Aufwandskonto (Expense Account)"):
                st.write("**Nature**: Erfolgskonto (Success Account)")
                st.write("**Effect**: Increases expenses, decreases profit")
                st.write("**Normal Side**: SOLL (Debit)")
                st.write("**Examples**: Miete, Gehälter, Bürokosten")
                st.code("T-Account Structure:\nSOLL | HABEN\n Aufwendungen | Stornierungen")
                st.info("💡 Aufwendungen reduce the company's equity through profit/loss")
        
        with col2:
            with st.expander("📈 Ertragskonto (Revenue Account)"):
                st.write("**Nature**: Erfolgskonto (Success Account)")
                st.write("**Effect**: Increases revenue, increases profit")
                st.write("**Normal Side**: HABEN (Credit)")
                st.write("**Examples**: Umsatzerlöse, Zinserträge")
                st.code("T-Account Structure:\nSOLL | HABEN\n Stornierungen | Erträge")
                st.info("💡 Erträge increase the company's equity through profit/loss")
        
        st.markdown("#### 🔄 Erfolgskonten vs. Bestandskonten")
        
        comparison_col1, comparison_col2 = st.columns(2)
        
        with comparison_col1:
            st.markdown("**🏦 Bestandskonten (Balance Sheet Accounts)**")
            st.write("• Aktivkonto & Passivkonto")
            st.write("• Appear directly in Bilanz")
            st.write("• Have opening/closing balances")
            st.write("• Represent assets, liabilities, equity")
            
        with comparison_col2:
            st.markdown("**📊 Erfolgskonten (P&L Accounts)**")
            st.write("• Aufwandskonto & Ertragskonto")
            st.write("• Affect equity through P&L")
            st.write("• Closed at year-end to equity")
            st.write("• Represent income statement items")

def show_api_status_page():
    """Display detailed API status page"""

    
    # API Health Check
    st.write("**🏥 Health Check**")
    status = api.health_check()
    
    if status["status"] == "healthy":
        st.success("✅ API is healthy and responding")
        if "data" in status:
            st.json(status["data"])
    else:
        st.error(f"❌ API Status: {status['status']}")
        if "error" in status:
            st.error(f"Error: {status['error']}")
    
    # Configuration
    st.write("**⚙️ Configuration**")
    st.code(f"API Base URL: {API_BASE_URL}")
    
    # API Endpoints
    st.write("**🔗 Available Endpoints**")
    endpoints = [
        ("GET", "/", "API root and status"),
        ("GET", "/health", "Health check"),
        ("GET", "/api/v1/accounts", "List all accounts"),
        ("POST", "/api/v1/accounts", "Create new account"),
        ("GET", "/api/v1/accounts/{number}", "Get specific account"),
        ("POST", "/api/v1/accounts/{number}/debit", "Debit account"),
        ("POST", "/api/v1/accounts/{number}/credit", "Credit account"),
        ("POST", "/api/v1/accounts/transaction", "Process double-entry transaction"),
        ("GET", "/api/v1/bilanz/", "Get complete Bilanz (Balance Sheet)"),
        ("GET", "/api/v1/bilanz/validate", "Validate Bilanz balance"),
        ("GET", "/api/v1/bilanz/account/{number}/resolution", "Get account Bilanz resolution"),
    ]
    
    for method, endpoint, description in endpoints:
        st.code(f"{method} {API_BASE_URL}{endpoint}")
        st.caption(description)
        st.markdown("")

def show_bilanz():
    """Display the Bilanz (Balance Sheet) page"""

    
    # Check API status
    show_api_status()
    
    # Date input for period end
    col1, col2 = st.columns(2)
    with col1:
        period_end = st.date_input(
            "Period End Date",
            value=None,
            help="Leave empty for current date"
        )
    
    with col2:
        if st.button("🔄 Refresh Bilanz"):
            st.info("💡 Use the main 'Refresh Data' button in the sidebar instead")
    
    # Convert date to string if provided
    period_end_str = period_end.isoformat() if period_end else None
    
    # Get Bilanz validation first
    validation_result = api.validate_bilanz(period_end_str)
    
    if validation_result["success"]:
        validation_data = validation_result["data"]
        
        # Display validation status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Aktiva Total", format_currency(validation_data["aktiva_total"]))
        
        with col2:
            st.metric("Passiva Total", format_currency(validation_data["passiva_total"]))
        
        with col3:
            balance_diff = validation_data["difference"]
            st.metric("Difference", format_currency(balance_diff))
        
        with col4:
            if validation_data["is_balanced"]:
                st.success("✅ Balanced")
            else:
                st.error("❌ Not Balanced")
    
    # Get full Bilanz
    bilanz_result = api.get_bilanz(period_end_str)
    
    if not bilanz_result["success"]:
        st.error(f"Failed to fetch Bilanz: {bilanz_result['error']}")
        return
    
    bilanz_data = bilanz_result["data"]
    
    # Display Bilanz in two columns
    st.write("**🏛️ Balance Sheet Structure**")
    
    col1, col2 = st.columns(2)
    
    # Aktiva (Assets) side
    with col1:
        st.markdown("### 📈 AKTIVA (Assets)")
        
        aktiva_positions = bilanz_data["aktiva"]["positions"]
        for category, accounts in aktiva_positions.items():
            st.markdown(f"**{category}**")
            
            category_total = 0.0
            for account in accounts:
                balance = account["balance"]
                category_total += balance
                st.write(f"  • {account['account_name']} ({account['account_number']}): {format_currency(balance)}")
            
            st.write(f"  **{category} Total: {format_currency(category_total)}**")
            st.markdown("---")
        
        # Total Aktiva
        st.markdown(f"### **TOTAL AKTIVA: {format_currency(bilanz_data['aktiva']['total'])}**")
    
    # Passiva (Liabilities + Equity) side
    with col2:
        st.markdown("### 📉 PASSIVA (Liabilities + Equity)")
        
        passiva_positions = bilanz_data["passiva"]["positions"]
        for category, accounts in passiva_positions.items():
            st.markdown(f"**{category}**")
            
            category_total = 0.0
            for account in accounts:
                balance = account["balance"]
                category_total += balance
                st.write(f"  • {account['account_name']} ({account['account_number']}): {format_currency(balance)}")
            
            st.write(f"  **{category} Total: {format_currency(category_total)}**")
            st.markdown("---")
        
        # Total Passiva
        st.markdown(f"### **TOTAL PASSIVA: {format_currency(bilanz_data['passiva']['total'])}**")
    
    # Account Resolution Section
    st.write("**🔍 Account Resolution**")
    st.write("See how individual accounts contribute to the Bilanz:")
    
    # Get all accounts for selection
    accounts = api.get_accounts()
    if accounts:
        account_options = {f"{acc['number']} - {acc['name']}": acc['number'] for acc in accounts}
        selected_account_display = st.selectbox("Select Account for Resolution", [""] + list(account_options.keys()))
        
        if selected_account_display:
            selected_account_number = account_options[selected_account_display]
            resolution_result = api.get_account_resolution(selected_account_number)
            
            if resolution_result["success"]:
                resolution_data = resolution_result["data"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Account:** {resolution_data['account_name']} ({resolution_data['account_number']})")
                    st.write(f"**Type:** {resolution_data['account_type']}")
                    st.write(f"**Soll Balance:** {format_currency(resolution_data['soll_balance'])}")
                    st.write(f"**Haben Balance:** {format_currency(resolution_data['haben_balance'])}")
                
                with col2:
                    st.write(f"**Net Balance:** {format_currency(resolution_data['net_balance'])}")
                    st.write(f"**Bilanz Side:** {resolution_data['bilanz_side'].title()}")
                    st.write(f"**Bilanz Category:** {resolution_data['bilanz_category']}")
                    st.write(f"**Contributes:** {format_currency(resolution_data['contributes_amount'])}")
            else:
                st.error(f"Failed to get account resolution: {resolution_result['error']}")
    
    # Display raw Bilanz data (optional)
    with st.expander("📊 Raw Bilanz Data"):
        st.json(bilanz_data)

if __name__ == "__main__":
    main()
