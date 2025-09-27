#!/usr/bin/env python3
"""
ATM Simulator Test Suite
Tests core functionality of the ATM simulator
"""

import unittest
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ATMSimulator import User, BankUser

class TestUser(unittest.TestCase):
    """Test User class functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.user = User("Test User", "1234", "password123")

    def test_user_creation(self):
        """Test user creation with valid parameters"""
        self.assertEqual(self.user.get_name(), "Test User")
        self.assertEqual(self.user.get_pin(), "1234")
        self.assertEqual(self.user.get_password(), "password123")

    def test_name_change(self):
        """Test changing user name"""
        self.user.change_name("New Name")
        self.assertEqual(self.user.get_name(), "New Name")

    def test_pin_change(self):
        """Test changing user PIN"""
        self.user.change_pin("5678")
        self.assertEqual(self.user.get_pin(), "5678")

    def test_password_change(self):
        """Test changing user password"""
        self.user.change_password("newpassword")
        self.assertEqual(self.user.get_password(), "newpassword")

class TestBankUser(unittest.TestCase):
    """Test BankUser class functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.bank_user = BankUser("Bank User", "1234", "password123")

    def test_bank_user_creation(self):
        """Test bank user creation with initial balance"""
        self.assertEqual(self.bank_user.get_name(), "Bank User")
        self.assertEqual(self.bank_user.get_balance(), 0.0)

    def test_deposit(self):
        """Test deposit functionality"""
        initial_balance = self.bank_user.get_balance()
        self.bank_user.deposit(100.0)
        self.assertEqual(self.bank_user.get_balance(), initial_balance + 100.0)

    def test_deposit_negative_amount(self):
        """Test deposit with negative amount (should be rejected)"""
        initial_balance = self.bank_user.get_balance()
        # Assuming deposit method should handle negative amounts gracefully
        self.bank_user.deposit(-50.0)
        # Balance should remain unchanged
        self.assertEqual(self.bank_user.get_balance(), initial_balance)

    def test_withdraw_sufficient_funds(self):
        """Test withdrawal with sufficient funds"""
        self.bank_user.deposit(200.0)
        initial_balance = self.bank_user.get_balance()
        self.bank_user.withdraw(50.0)
        self.assertEqual(self.bank_user.get_balance(), initial_balance - 50.0)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds"""
        initial_balance = self.bank_user.get_balance()
        self.bank_user.withdraw(1000.0)  # Amount larger than balance
        # Balance should remain unchanged if withdrawal fails
        self.assertEqual(self.bank_user.get_balance(), initial_balance)

    def test_withdraw_negative_amount(self):
        """Test withdrawal with negative amount"""
        self.bank_user.deposit(100.0)
        initial_balance = self.bank_user.get_balance()
        self.bank_user.withdraw(-25.0)
        # Balance should remain unchanged
        self.assertEqual(self.bank_user.get_balance(), initial_balance)

    def test_multiple_transactions(self):
        """Test multiple transactions"""
        # Start with deposit
        self.bank_user.deposit(500.0)
        self.assertEqual(self.bank_user.get_balance(), 500.0)

        # Withdraw some money
        self.bank_user.withdraw(150.0)
        self.assertEqual(self.bank_user.get_balance(), 350.0)

        # Deposit more
        self.bank_user.deposit(75.0)
        self.assertEqual(self.bank_user.get_balance(), 425.0)

class TestBankingOperations(unittest.TestCase):
    """Test advanced banking operations"""

    def setUp(self):
        """Set up test fixtures for banking operations"""
        self.sender = BankUser("Sender", "1111", "pass1")
        self.receiver = BankUser("Receiver", "2222", "pass2")
        self.sender.deposit(1000.0)

    def test_balance_inquiry(self):
        """Test balance inquiry functionality"""
        self.assertEqual(self.sender.get_balance(), 1000.0)
        self.assertEqual(self.receiver.get_balance(), 0.0)

    def test_user_inheritance(self):
        """Test that BankUser properly inherits from User"""
        self.assertIsInstance(self.sender, User)
        self.assertIsInstance(self.sender, BankUser)

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUser))
    suite.addTests(loader.loadTestsFromTestCase(TestBankUser))
    suite.addTests(loader.loadTestsFromTestCase(TestBankingOperations))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 Running ATM Simulator Test Suite")
    print("=" * 50)

    success = run_tests()

    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)