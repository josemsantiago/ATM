#!/usr/bin/env python3
"""
ATM Simulator Launcher
Provides multiple ways to run the ATM simulator with different configurations
"""

import sys
import os
import argparse
import json
from pathlib import Path

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file}' not found. Using defaults.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        return {}

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Enhanced ATM Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_atm.py                    # Run with default settings
  python run_atm.py --demo             # Run with demo data
  python run_atm.py --config custom.json  # Use custom config
  python run_atm.py --enhanced         # Run enhanced version
  python run_atm.py --reset            # Reset all data
        """
    )

    parser.add_argument(
        '--config', '-c',
        default='config.json',
        help='Configuration file to use (default: config.json)'
    )

    parser.add_argument(
        '--demo', '-d',
        action='store_true',
        help='Run with demo data pre-loaded'
    )

    parser.add_argument(
        '--enhanced', '-e',
        action='store_true',
        help='Run the enhanced version with all features'
    )

    parser.add_argument(
        '--reset', '-r',
        action='store_true',
        help='Reset all user data and start fresh'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='ATM Simulator v2.0.0'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    print("=" * 60)
    print("🏦 Enhanced ATM Simulator")
    print("=" * 60)

    if args.reset:
        print("🔄 Resetting system data...")
        # Remove data files if they exist
        data_files = ['atm_data.json', 'user_data.json', 'transactions.json']
        for file in data_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"   ✅ Removed {file}")
        print("   ✅ System reset complete!")
        print()

    if args.demo:
        print("🎯 Loading demo data...")
        os.environ['ATM_DEMO_MODE'] = 'true'

    if args.enhanced:
        print("⚡ Enhanced mode enabled")
        os.environ['ATM_ENHANCED_MODE'] = 'true'

    # Determine which ATM version to run
    if args.enhanced or os.path.exists('enhanced_atm.py'):
        try:
            print("🚀 Starting Enhanced ATM...")
            import enhanced_atm
            enhanced_atm.main() if hasattr(enhanced_atm, 'main') else None
        except ImportError:
            print("❌ Enhanced ATM not available, falling back to basic version")
            import ATMSimulator
            ATMSimulator.main() if hasattr(ATMSimulator, 'main') else None
    else:
        print("🚀 Starting Basic ATM...")
        try:
            import ATMSimulator
            # Try to run main function, or instantiate ATM class
            if hasattr(ATMSimulator, 'main'):
                ATMSimulator.main()
            else:
                # Look for ATM class or similar entry point
                atm = ATMSimulator.ATM() if hasattr(ATMSimulator, 'ATM') else None
        except ImportError as e:
            print(f"❌ Error importing ATM simulator: {e}")
            sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using the ATM Simulator!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)