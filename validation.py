"""
Transaction validation engine with configurable rules.
"""
import re
import json
from datetime import datetime
from typing import List, Dict, Tuple
import pandas as pd


class TransactionValidator:
    """Validates transaction records against configurable rules."""

    def __init__(self, country_rules_path: str = "country_rules.json"):
        """
        Initialize validator with country-specific phone rules.
        
        Args:
            country_rules_path: Path to JSON file with phone validation rules
        """
        self.errors = []
        self.valid_records = []
        self.invalid_records = []
        self.country_rules = self._load_country_rules(country_rules_path)
        self.seen_order_ids = set()
        self.duplicate_order_ids = set()

    def _load_country_rules(self, path: str) -> Dict[str, int]:
        """Load country-specific phone number length rules."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found. Using default rules.")
            return {
                "IN": 10, "SG": 8, "US": 10, "UK": 10,
                "AU": 9, "NZ": 9, "CA": 10, "FR": 9, "DE": 11, "JP": 10, "CH": 9
            }

    def validate_dataset(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, List[Dict]]:
        """
        Validate entire dataset and separate valid/invalid records.
        
        Args:
            df: DataFrame containing transaction data
            
        Returns:
            Tuple of (valid_df, invalid_df, validation_errors)
        """
        self.valid_records = []
        self.invalid_records = []
        self.errors = []
        self.seen_order_ids = set()
        self.duplicate_order_ids = set()

        # First pass: detect duplicates
        for idx, row in df.iterrows():
            if pd.notna(row.get('order_id')):
                order_id = str(row['order_id']).strip()
                if order_id in self.seen_order_ids:
                    self.duplicate_order_ids.add(order_id)
                self.seen_order_ids.add(order_id)

        # Second pass: validate each record
        for idx, row in df.iterrows():
            errors = self._validate_record(row, idx)
            
            if errors:
                self.invalid_records.append(row.to_dict())
                for error in errors:
                    self.errors.append({
                        'row': idx + 2,  # +2 because row 1 is header
                        'order_id': row.get('order_id', ''),
                        'error': error
                    })
            else:
                self.valid_records.append(row.to_dict())

        # Convert to DataFrames
        valid_df = pd.DataFrame(self.valid_records) if self.valid_records else pd.DataFrame()
        invalid_df = pd.DataFrame(self.invalid_records) if self.invalid_records else pd.DataFrame()

        return valid_df, invalid_df, self.errors

    def _validate_record(self, row: pd.Series, row_index: int) -> List[str]:
        """
        Validate a single record.
        
        Args:
            row: Series representing a record
            row_index: Index of the row
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Required fields check
        required_fields = ['order_id', 'customer_name', 'country_code', 'phone',
                          'date', 'time', 'product_id', 'product_name', 'amount', 'payment_mode']
        
        for field in required_fields:
            if field not in row or pd.isna(row[field]) or str(row[field]).strip() == '':
                errors.append(f"Missing mandatory field: {field}")

        if errors:
            return errors

        # Phone validation
        phone_error = self._validate_phone(row['country_code'], row['phone'])
        if phone_error:
            errors.append(phone_error)

        # Date validation
        date_error = self._validate_date(row['date'])
        if date_error:
            errors.append(date_error)

        # Time validation
        time_error = self._validate_time(row['time'])
        if time_error:
            errors.append(time_error)

        # Payment validation
        payment_error = self._validate_payment_mode(row['payment_mode'])
        if payment_error:
            errors.append(payment_error)

        # Amount validation
        amount_error = self._validate_amount(row['amount'])
        if amount_error:
            errors.append(amount_error)

        # Duplicate order_id check
        order_id = str(row['order_id']).strip()
        if order_id in self.duplicate_order_ids:
            errors.append(f"Duplicate order_id: {order_id}")

        return errors

    def _validate_phone(self, country_code: str, phone: str) -> str:
        """Validate phone number for given country."""
        country_code = str(country_code).strip().upper()
        phone = str(phone).strip()

        # Check if country code exists
        if country_code not in self.country_rules:
            return f"Unknown country code: {country_code}"

        # Check if phone contains only digits
        if not phone.isdigit():
            return f"Phone must contain only digits: {phone}"

        # Check phone length
        expected_length = self.country_rules[country_code]
        if len(phone) != expected_length:
            return f"Phone length mismatch for {country_code}. Expected {expected_length}, got {len(phone)}"

        return ""

    def _validate_date(self, date: str) -> str:
        """Validate date format YYYY-MM-DD."""
        date = str(date).strip()
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return ""
        except ValueError:
            return f"Invalid date format (expected YYYY-MM-DD): {date}"

    def _validate_time(self, time: str) -> str:
        """Validate time format HH:MM:SS."""
        time = str(time).strip()
        try:
            datetime.strptime(time, '%H:%M:%S')
            return ""
        except ValueError:
            return f"Invalid time format (expected HH:MM:SS): {time}"

    def _validate_payment_mode(self, payment_mode: str) -> str:
        """Validate payment mode."""
        allowed_modes = {'UPI', 'CARD', 'NETBANKING', 'CASH'}
        payment_mode = str(payment_mode).strip().upper()
        
        if payment_mode not in allowed_modes:
            return f"Invalid payment mode: {payment_mode}. Allowed: {', '.join(allowed_modes)}"
        return ""

    def _validate_amount(self, amount: str) -> str:
        """Validate amount."""
        try:
            amount_float = float(str(amount).strip())
            if amount_float <= 0:
                return f"Amount must be greater than zero: {amount}"
            return ""
        except ValueError:
            return f"Amount must be numeric: {amount}"

    def generate_validation_report(self) -> pd.DataFrame:
        """Generate validation report."""
        if not self.errors:
            return pd.DataFrame(columns=['Row', 'Order ID', 'Error'])

        report_data = []
        for error in self.errors:
            report_data.append({
                'Row': error['row'],
                'Order ID': error['order_id'],
                'Error': error['error']
            })

        return pd.DataFrame(report_data)
