# Changelog

All notable changes to the ATM Simulator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Environment variable configuration support via .env file
- .env.example template for secure configuration management

### Security
- Added recommendation to use environment variables for security salt

## [2.0.0] - 2024-09-30

### Added
- Enhanced ATM system with professional features
- Multiple account types (Checking, Savings, Premium)
- Advanced security management with lockout protection
- Transaction history and comprehensive logging
- Data persistence using JSON file storage
- Session management with automatic timeout
- Profile management functionality
- Account management features
- Daily withdrawal limits per account type
- Overdraft protection with configurable limits
- Comprehensive test suite

### Changed
- Upgraded from basic ATM to enterprise-level simulation
- Improved authentication with PIN and password verification
- Enhanced user class with profile information

### Security
- Added password hashing with SHA-256
- Implemented failed login attempt tracking
- Added session timeout protection
- Comprehensive audit logging

## [1.0.0] - 2023

### Added
- Initial ATM simulator implementation
- Basic user authentication
- Deposit and withdrawal functionality
- Balance inquiry
- Simple BankUser and User classes
- Basic test coverage

### Features
- PIN-based authentication
- Basic banking operations
- Object-oriented design with inheritance

---

## Types of Changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes
