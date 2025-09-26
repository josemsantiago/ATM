"""
Enhanced ATM Simulator - Professional Banking System
Author: José Santiago Echevarria
Date: 2023-2024

This enhanced version includes:
- Advanced security features
- Transaction history
- Multiple account types
- Data persistence
- Comprehensive logging
- Error handling
- Professional architecture
"""

import json
import hashlib
import logging
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('atm_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class AccountType(Enum):
    """Account type enumeration"""
    CHECKING = "checking"
    SAVINGS = "savings"
    PREMIUM = "premium"


class TransactionType(Enum):
    """Transaction type enumeration"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    BALANCE_INQUIRY = "balance_inquiry"
    PIN_CHANGE = "pin_change"


@dataclass
class Transaction:
    """Transaction data class"""
    transaction_id: str
    user_id: str
    transaction_type: TransactionType
    amount: float
    balance_after: float
    timestamp: datetime.datetime
    description: str
    to_user: Optional[str] = None


class SecurityManager:
    """Enhanced security management"""

    def __init__(self):
        self.failed_attempts = {}
        self.max_attempts = 3
        self.lockout_duration = 300  # 5 minutes

    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "atm_security_salt_2023"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed

    def check_lockout(self, user_id: str) -> bool:
        """Check if user is locked out"""
        if user_id in self.failed_attempts:
            attempts, last_attempt = self.failed_attempts[user_id]
            if attempts >= self.max_attempts:
                time_since = datetime.datetime.now() - last_attempt
                if time_since.seconds < self.lockout_duration:
                    return True
                else:
                    # Reset after lockout period
                    del self.failed_attempts[user_id]
        return False

    def record_failed_attempt(self, user_id: str):
        """Record failed login attempt"""
        now = datetime.datetime.now()
        if user_id in self.failed_attempts:
            attempts, _ = self.failed_attempts[user_id]
            self.failed_attempts[user_id] = (attempts + 1, now)
        else:
            self.failed_attempts[user_id] = (1, now)

    def clear_failed_attempts(self, user_id: str):
        """Clear failed attempts after successful login"""
        if user_id in self.failed_attempts:
            del self.failed_attempts[user_id]


class Account:
    """Enhanced account class with multiple types"""

    def __init__(self, account_id: str, account_type: AccountType, balance: float = 0.0):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance
        self.overdraft_limit = self._get_overdraft_limit()
        self.daily_withdrawal_limit = self._get_daily_limit()
        self.daily_withdrawn = 0.0
        self.last_reset_date = datetime.date.today()

    def _get_overdraft_limit(self) -> float:
        """Get overdraft limit based on account type"""
        limits = {
            AccountType.CHECKING: 100.0,
            AccountType.SAVINGS: 0.0,
            AccountType.PREMIUM: 500.0
        }
        return limits.get(self.account_type, 0.0)

    def _get_daily_limit(self) -> float:
        """Get daily withdrawal limit based on account type"""
        limits = {
            AccountType.CHECKING: 500.0,
            AccountType.SAVINGS: 300.0,
            AccountType.PREMIUM: 1000.0
        }
        return limits.get(self.account_type, 500.0)

    def reset_daily_limit_if_needed(self):
        """Reset daily withdrawal limit if new day"""
        today = datetime.date.today()
        if today > self.last_reset_date:
            self.daily_withdrawn = 0.0
            self.last_reset_date = today

    def can_withdraw(self, amount: float) -> tuple[bool, str]:
        """Check if withdrawal is possible"""
        self.reset_daily_limit_if_needed()

        if amount <= 0:
            return False, "Invalid amount"

        if self.daily_withdrawn + amount > self.daily_withdrawal_limit:
            return False, f"Daily withdrawal limit of ${self.daily_withdrawal_limit:.2f} exceeded"

        available_balance = self.balance + self.overdraft_limit
        if amount > available_balance:
            return False, "Insufficient funds"

        return True, "OK"

    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account"""
        can_withdraw, message = self.can_withdraw(amount)
        if can_withdraw:
            self.balance -= amount
            self.daily_withdrawn += amount
            return True
        return False

    def deposit(self, amount: float) -> bool:
        """Deposit money to account"""
        if amount > 0:
            self.balance += amount
            return True
        return False


class EnhancedUser:
    """Enhanced user class with security and account management"""

    def __init__(self, user_id: str, name: str, pin: str, password: str):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.password_hash = SecurityManager().hash_password(password)
        self.accounts: Dict[AccountType, Account] = {}
        self.created_date = datetime.datetime.now()
        self.last_login = None
        self.email = ""
        self.phone = ""

    def add_account(self, account_type: AccountType, initial_balance: float = 0.0):
        """Add new account to user"""
        account_id = f"{self.user_id}_{account_type.value}"
        self.accounts[account_type] = Account(account_id, account_type, initial_balance)

    def get_account(self, account_type: AccountType) -> Optional[Account]:
        """Get specific account"""
        return self.accounts.get(account_type)

    def get_total_balance(self) -> float:
        """Get total balance across all accounts"""
        return sum(account.balance for account in self.accounts.values())

    def update_profile(self, **kwargs):
        """Update user profile information"""
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'phone' in kwargs:
            self.phone = kwargs['phone']


class DatabaseManager:
    """Simple file-based database manager"""

    def __init__(self, data_file: str = "atm_data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        """Load data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                return {"users": {}, "transactions": []}
        return {"users": {}, "transactions": []}

    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def save_user(self, user: EnhancedUser):
        """Save user to database"""
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "pin": user.pin,
            "password_hash": user.password_hash,
            "email": user.email,
            "phone": user.phone,
            "created_date": user.created_date.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "accounts": {}
        }

        for account_type, account in user.accounts.items():
            user_data["accounts"][account_type.value] = {
                "account_id": account.account_id,
                "balance": account.balance,
                "daily_withdrawn": account.daily_withdrawn,
                "last_reset_date": account.last_reset_date.isoformat()
            }

        self.data["users"][user.user_id] = user_data
        self.save_data()

    def load_user(self, user_id: str) -> Optional[EnhancedUser]:
        """Load user from database"""
        if user_id in self.data["users"]:
            user_data = self.data["users"][user_id]
            user = EnhancedUser(
                user_data["user_id"],
                user_data["name"],
                user_data["pin"],
                ""  # Password will be set from hash
            )
            user.password_hash = user_data["password_hash"]
            user.email = user_data.get("email", "")
            user.phone = user_data.get("phone", "")

            if user_data.get("created_date"):
                user.created_date = datetime.datetime.fromisoformat(user_data["created_date"])

            if user_data.get("last_login"):
                user.last_login = datetime.datetime.fromisoformat(user_data["last_login"])

            # Load accounts
            for account_type_str, account_data in user_data.get("accounts", {}).items():
                account_type = AccountType(account_type_str)
                account = Account(
                    account_data["account_id"],
                    account_type,
                    account_data["balance"]
                )
                account.daily_withdrawn = account_data.get("daily_withdrawn", 0.0)
                if account_data.get("last_reset_date"):
                    account.last_reset_date = datetime.date.fromisoformat(account_data["last_reset_date"])

                user.accounts[account_type] = account

            return user
        return None

    def save_transaction(self, transaction: Transaction):
        """Save transaction to database"""
        transaction_data = {
            "transaction_id": transaction.transaction_id,
            "user_id": transaction.user_id,
            "transaction_type": transaction.transaction_type.value,
            "amount": transaction.amount,
            "balance_after": transaction.balance_after,
            "timestamp": transaction.timestamp.isoformat(),
            "description": transaction.description,
            "to_user": transaction.to_user
        }

        self.data["transactions"].append(transaction_data)
        self.save_data()

    def get_user_transactions(self, user_id: str, limit: int = 10) -> List[Transaction]:
        """Get user transaction history"""
        user_transactions = [
            Transaction(
                t["transaction_id"],
                t["user_id"],
                TransactionType(t["transaction_type"]),
                t["amount"],
                t["balance_after"],
                datetime.datetime.fromisoformat(t["timestamp"]),
                t["description"],
                t.get("to_user")
            )
            for t in self.data["transactions"]
            if t["user_id"] == user_id
        ]

        return sorted(user_transactions, key=lambda x: x.timestamp, reverse=True)[:limit]


class ATMSession:
    """ATM session management"""

    def __init__(self, user: EnhancedUser, db_manager: DatabaseManager):
        self.user = user
        self.db_manager = db_manager
        self.session_start = datetime.datetime.now()
        self.active = True
        self.session_timeout = 300  # 5 minutes

    def is_session_valid(self) -> bool:
        """Check if session is still valid"""
        if not self.active:
            return False

        elapsed = datetime.datetime.now() - self.session_start
        if elapsed.seconds > self.session_timeout:
            self.active = False
            return False

        return True

    def extend_session(self):
        """Extend session timeout"""
        self.session_start = datetime.datetime.now()

    def create_transaction(self, transaction_type: TransactionType, amount: float,
                         description: str, to_user: str = None) -> Transaction:
        """Create and save transaction"""
        transaction_id = f"{self.user.user_id}_{datetime.datetime.now().timestamp()}"

        # Get current balance from primary account
        primary_account = self.user.get_account(AccountType.CHECKING)
        balance_after = primary_account.balance if primary_account else 0.0

        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=self.user.user_id,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after,
            timestamp=datetime.datetime.now(),
            description=description,
            to_user=to_user
        )

        self.db_manager.save_transaction(transaction)
        logger.info(f"Transaction created: {transaction_id} for user {self.user.user_id}")
        return transaction


class EnhancedATMSystem:
    """Enhanced ATM System with professional features"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.security_manager = SecurityManager()
        self.sessions: Dict[str, ATMSession] = {}
        self.system_start_time = datetime.datetime.now()
        logger.info("ATM System initialized")

    def register_user(self, name: str, pin: str, password: str, email: str = "", phone: str = "") -> Optional[EnhancedUser]:
        """Register new user"""
        try:
            # Generate unique user ID
            user_id = f"USER_{len(self.db_manager.data['users']) + 1:04d}"

            # Validate input
            if len(pin) != 4 or not pin.isdigit():
                raise ValueError("PIN must be 4 digits")

            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters")

            # Create user
            user = EnhancedUser(user_id, name, pin, password)
            user.email = email
            user.phone = phone

            # Add default checking account
            user.add_account(AccountType.CHECKING, 0.0)

            # Save to database
            self.db_manager.save_user(user)

            logger.info(f"New user registered: {user_id}")
            return user

        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return None

    def authenticate_user(self, user_id: str, pin: str, password: str) -> Optional[ATMSession]:
        """Authenticate user and create session"""
        try:
            # Check lockout
            if self.security_manager.check_lockout(user_id):
                logger.warning(f"User {user_id} is locked out")
                return None

            # Load user
            user = self.db_manager.load_user(user_id)
            if not user:
                logger.warning(f"User not found: {user_id}")
                return None

            # Verify credentials
            if user.pin != pin or not self.security_manager.verify_password(password, user.password_hash):
                self.security_manager.record_failed_attempt(user_id)
                logger.warning(f"Authentication failed for user: {user_id}")
                return None

            # Clear failed attempts and update last login
            self.security_manager.clear_failed_attempts(user_id)
            user.last_login = datetime.datetime.now()
            self.db_manager.save_user(user)

            # Create session
            session = ATMSession(user, self.db_manager)
            self.sessions[user_id] = session

            logger.info(f"User authenticated successfully: {user_id}")
            return session

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        total_users = len(self.db_manager.data["users"])
        total_transactions = len(self.db_manager.data["transactions"])
        active_sessions = len([s for s in self.sessions.values() if s.is_session_valid()])

        return {
            "total_users": total_users,
            "total_transactions": total_transactions,
            "active_sessions": active_sessions,
            "system_uptime": str(datetime.datetime.now() - self.system_start_time),
            "system_status": "Online"
        }


def main():
    """Main ATM application"""
    print("🏦 Enhanced ATM System - Professional Banking Simulation")
    print("=" * 60)

    atm = EnhancedATMSystem()

    while True:
        print("\n🏠 Main Menu")
        print("1. Register New User")
        print("2. Login")
        print("3. System Statistics")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            # User registration
            print("\n📝 User Registration")
            name = input("Enter your full name: ").strip()
            pin = input("Create a 4-digit PIN: ").strip()
            password = input("Create a password (min 6 characters): ").strip()
            email = input("Enter email (optional): ").strip()
            phone = input("Enter phone (optional): ").strip()

            user = atm.register_user(name, pin, password, email, phone)
            if user:
                print(f"✅ Registration successful! Your user ID is: {user.user_id}")
                print("Please remember your User ID, PIN, and password for future logins.")
            else:
                print("❌ Registration failed. Please check your input and try again.")

        elif choice == "2":
            # User login
            print("\n🔐 User Login")
            user_id = input("Enter your User ID: ").strip()
            pin = input("Enter your PIN: ").strip()
            password = input("Enter your password: ").strip()

            session = atm.authenticate_user(user_id, pin, password)
            if session:
                print(f"✅ Welcome back, {session.user.name}!")
                user_menu(session)
            else:
                print("❌ Authentication failed. Please check your credentials.")

        elif choice == "3":
            # System statistics
            stats = atm.get_system_stats()
            print("\n📊 System Statistics")
            print(f"Total Users: {stats['total_users']}")
            print(f"Total Transactions: {stats['total_transactions']}")
            print(f"Active Sessions: {stats['active_sessions']}")
            print(f"System Uptime: {stats['system_uptime']}")
            print(f"Status: {stats['system_status']}")

        elif choice == "4":
            print("👋 Thank you for using the Enhanced ATM System!")
            break

        else:
            print("❌ Invalid option. Please try again.")


def user_menu(session: ATMSession):
    """User menu after login"""
    while session.is_session_valid():
        print(f"\n💳 User Menu - {session.user.name}")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Account Management")
        print("7. Update Profile")
        print("8. Logout")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            check_balance(session)
        elif choice == "2":
            deposit_money(session)
        elif choice == "3":
            withdraw_money(session)
        elif choice == "4":
            transfer_money(session)
        elif choice == "5":
            transaction_history(session)
        elif choice == "6":
            account_management(session)
        elif choice == "7":
            update_profile(session)
        elif choice == "8":
            print("🚪 Logging out...")
            session.active = False
            break
        else:
            print("❌ Invalid option. Please try again.")

        session.extend_session()

    if not session.is_session_valid():
        print("⏰ Session expired. Please log in again.")


def check_balance(session: ATMSession):
    """Check account balance"""
    print("\n💰 Account Balances")

    total_balance = 0.0
    for account_type, account in session.user.accounts.items():
        print(f"{account_type.value.title()}: ${account.balance:.2f}")
        total_balance += account.balance

    print(f"Total Balance: ${total_balance:.2f}")

    # Create transaction record
    session.create_transaction(
        TransactionType.BALANCE_INQUIRY,
        0.0,
        "Balance inquiry"
    )


def deposit_money(session: ATMSession):
    """Deposit money to account"""
    print("\n💵 Deposit Money")

    try:
        amount = float(input("Enter amount to deposit: $"))

        if amount <= 0:
            print("❌ Invalid amount. Amount must be positive.")
            return

        # Select account
        account_type = select_account(session.user)
        if not account_type:
            return

        account = session.user.get_account(account_type)
        if account.deposit(amount):
            session.db_manager.save_user(session.user)

            print(f"✅ Successfully deposited ${amount:.2f}")
            print(f"New balance: ${account.balance:.2f}")

            # Create transaction record
            session.create_transaction(
                TransactionType.DEPOSIT,
                amount,
                f"Deposit to {account_type.value} account"
            )
        else:
            print("❌ Deposit failed.")

    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")


def withdraw_money(session: ATMSession):
    """Withdraw money from account"""
    print("\n💸 Withdraw Money")

    try:
        amount = float(input("Enter amount to withdraw: $"))

        # Select account
        account_type = select_account(session.user)
        if not account_type:
            return

        account = session.user.get_account(account_type)
        can_withdraw, message = account.can_withdraw(amount)

        if not can_withdraw:
            print(f"❌ Withdrawal failed: {message}")
            return

        if account.withdraw(amount):
            session.db_manager.save_user(session.user)

            print(f"✅ Successfully withdrew ${amount:.2f}")
            print(f"New balance: ${account.balance:.2f}")

            # Create transaction record
            session.create_transaction(
                TransactionType.WITHDRAWAL,
                amount,
                f"Withdrawal from {account_type.value} account"
            )
        else:
            print("❌ Withdrawal failed.")

    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")


def transfer_money(session: ATMSession):
    """Transfer money to another user"""
    print("\n💸 Transfer Money")

    try:
        to_user_id = input("Enter recipient's User ID: ").strip()
        amount = float(input("Enter amount to transfer: $"))

        # Load recipient
        recipient = session.db_manager.load_user(to_user_id)
        if not recipient:
            print("❌ Recipient not found.")
            return

        # Select source account
        account_type = select_account(session.user)
        if not account_type:
            return

        account = session.user.get_account(account_type)
        can_withdraw, message = account.can_withdraw(amount)

        if not can_withdraw:
            print(f"❌ Transfer failed: {message}")
            return

        # Confirm transfer
        print(f"Transfer ${amount:.2f} to {recipient.name}?")
        confirm = input("Enter 'YES' to confirm: ").strip().upper()

        if confirm != "YES":
            print("❌ Transfer cancelled.")
            return

        # Process transfer
        if account.withdraw(amount):
            # Add to recipient's primary account
            recipient_account = recipient.get_account(AccountType.CHECKING)
            if not recipient_account:
                recipient.add_account(AccountType.CHECKING, 0.0)
                recipient_account = recipient.get_account(AccountType.CHECKING)

            recipient_account.deposit(amount)

            # Save both users
            session.db_manager.save_user(session.user)
            session.db_manager.save_user(recipient)

            print(f"✅ Successfully transferred ${amount:.2f} to {recipient.name}")
            print(f"New balance: ${account.balance:.2f}")

            # Create transaction records
            session.create_transaction(
                TransactionType.TRANSFER,
                amount,
                f"Transfer to {recipient.name}",
                to_user_id
            )
        else:
            print("❌ Transfer failed.")

    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")


def transaction_history(session: ATMSession):
    """Show transaction history"""
    print("\n📋 Transaction History")

    transactions = session.db_manager.get_user_transactions(session.user.user_id, 10)

    if not transactions:
        print("No transactions found.")
        return

    print(f"{'Date':<20} {'Type':<15} {'Amount':<12} {'Description'}")
    print("-" * 70)

    for transaction in transactions:
        date_str = transaction.timestamp.strftime("%Y-%m-%d %H:%M")
        amount_str = f"${transaction.amount:.2f}"
        print(f"{date_str:<20} {transaction.transaction_type.value:<15} {amount_str:<12} {transaction.description}")


def select_account(user: EnhancedUser) -> Optional[AccountType]:
    """Select account type"""
    if len(user.accounts) == 1:
        return list(user.accounts.keys())[0]

    print("\nSelect account:")
    account_types = list(user.accounts.keys())
    for i, account_type in enumerate(account_types, 1):
        account = user.accounts[account_type]
        print(f"{i}. {account_type.value.title()} (${account.balance:.2f})")

    try:
        choice = int(input("Enter account number: ")) - 1
        if 0 <= choice < len(account_types):
            return account_types[choice]
        else:
            print("❌ Invalid selection.")
            return None
    except ValueError:
        print("❌ Invalid selection.")
        return None


def account_management(session: ATMSession):
    """Account management menu"""
    print("\n🏦 Account Management")
    print("1. Add New Account")
    print("2. View Account Details")
    print("3. Back to Main Menu")

    choice = input("Select an option: ").strip()

    if choice == "1":
        print("\nSelect account type to add:")
        print("1. Savings Account")
        print("2. Premium Account")

        acc_choice = input("Enter choice: ").strip()

        if acc_choice == "1" and AccountType.SAVINGS not in session.user.accounts:
            session.user.add_account(AccountType.SAVINGS, 0.0)
            session.db_manager.save_user(session.user)
            print("✅ Savings account added successfully!")
        elif acc_choice == "2" and AccountType.PREMIUM not in session.user.accounts:
            session.user.add_account(AccountType.PREMIUM, 0.0)
            session.db_manager.save_user(session.user)
            print("✅ Premium account added successfully!")
        else:
            print("❌ Account already exists or invalid selection.")

    elif choice == "2":
        print("\n📋 Account Details")
        for account_type, account in session.user.accounts.items():
            print(f"\n{account_type.value.title()} Account:")
            print(f"  Account ID: {account.account_id}")
            print(f"  Balance: ${account.balance:.2f}")
            print(f"  Daily Limit: ${account.daily_withdrawal_limit:.2f}")
            print(f"  Daily Withdrawn: ${account.daily_withdrawn:.2f}")
            print(f"  Overdraft Limit: ${account.overdraft_limit:.2f}")


def update_profile(session: ATMSession):
    """Update user profile"""
    print("\n👤 Update Profile")
    print(f"Current Name: {session.user.name}")
    print(f"Current Email: {session.user.email}")
    print(f"Current Phone: {session.user.phone}")

    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Email")
    print("3. Phone")
    print("4. PIN")
    print("5. Password")
    print("6. Back to Main Menu")

    choice = input("Select an option: ").strip()

    if choice == "1":
        new_name = input("Enter new name: ").strip()
        if new_name:
            session.user.name = new_name
            session.db_manager.save_user(session.user)
            print("✅ Name updated successfully!")

    elif choice == "2":
        new_email = input("Enter new email: ").strip()
        session.user.email = new_email
        session.db_manager.save_user(session.user)
        print("✅ Email updated successfully!")

    elif choice == "3":
        new_phone = input("Enter new phone: ").strip()
        session.user.phone = new_phone
        session.db_manager.save_user(session.user)
        print("✅ Phone updated successfully!")

    elif choice == "4":
        current_pin = input("Enter current PIN: ").strip()
        if current_pin == session.user.pin:
            new_pin = input("Enter new 4-digit PIN: ").strip()
            if len(new_pin) == 4 and new_pin.isdigit():
                session.user.pin = new_pin
                session.db_manager.save_user(session.user)
                print("✅ PIN updated successfully!")

                # Create transaction record
                session.create_transaction(
                    TransactionType.PIN_CHANGE,
                    0.0,
                    "PIN changed"
                )
            else:
                print("❌ PIN must be 4 digits.")
        else:
            print("❌ Current PIN is incorrect.")

    elif choice == "5":
        current_password = input("Enter current password: ").strip()
        if session.security_manager.verify_password(current_password, session.user.password_hash):
            new_password = input("Enter new password (min 6 characters): ").strip()
            if len(new_password) >= 6:
                session.user.password_hash = session.security_manager.hash_password(new_password)
                session.db_manager.save_user(session.user)
                print("✅ Password updated successfully!")
            else:
                print("❌ Password must be at least 6 characters.")
        else:
            print("❌ Current password is incorrect.")


if __name__ == "__main__":
    main()