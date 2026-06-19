# Test Data Folder - README

## 📁 Sample CSV Files for Testing

This folder contains 4 sample CSV files for testing the AI Transaction Validator application.

---

## 📋 Files Included:

### 1. **valid_records.csv** (15 records - ✅ ALL VALID)
- All records are perfectly formatted
- All from India (IN)
- Various payment modes (CARD, UPI, NETBANKING, CASH)
- **Use this to:** Test successful validation
- **Expected Result:** 100% success rate

### 2. **invalid_records.csv** (15 records - ❌ ALL INVALID)
- Various validation errors:
  - Invalid phone lengths
  - Invalid dates and times
  - Invalid payment modes
  - Zero and negative amounts
  - Missing fields
- **Use this to:** Test error detection
- **Expected Result:** 0% success rate, all errors shown

### 3. **international_records.csv** (15 records - ✅ ALL VALID)
- Different countries: US, SG, UK, AU, NZ, CA
- All records are valid
- Tests multi-country phone validation
- **Use this to:** Test international support
- **Expected Result:** 100% success rate with multiple countries

### 4. **mixed_records.csv** (20 records - 🔀 MIXED)
- Contains both valid and invalid records
- Includes duplicate order IDs (ORD1011, ORD1012)
- Various phone format errors
- Invalid payment modes
- Wrong date/time formats
- **Use this to:** Test comprehensive validation
- **Expected Result:** ~75% success rate

---

## 🚀 How to Use:

**Step 1:** Start the application
```bash
# Windows: Double-click run.bat
# Or Command Line:
uvicorn main:app --reload
```

**Step 2:** Open browser
```
http://localhost:8000
```

**Step 3:** Upload any CSV file from this folder

**Step 4:** Review results
- Check statistics (Total, Valid, Invalid)
- Download validation reports
- Check error details

---

## 📊 Expected Results:

| File | Records | Valid | Invalid | Success % | Notes |
|------|---------|-------|---------|-----------|-------|
| valid_records.csv | 15 | 15 | 0 | 100% | All valid Indian transactions |
| invalid_records.csv | 15 | 0 | 15 | 0% | All various error types |
| international_records.csv | 15 | 15 | 0 | 100% | US, SG, UK, AU, NZ, CA |
| mixed_records.csv | 20 | 15 | 5 | 75% | Valid + duplicates + errors |

---

## 🧪 Testing Workflow:

**Test 1 - Happy Path:**
1. Upload `valid_records.csv`
2. Verify 15/15 records pass
3. Download valid_records.csv to confirm

**Test 2 - Error Detection:**
1. Upload `invalid_records.csv`
2. Check all 15 errors are detected
3. Review error types in validation_report.csv

**Test 3 - International:**
1. Upload `international_records.csv`
2. Verify multiple countries work correctly
3. Confirm phone validation for each country

**Test 4 - Comprehensive:**
1. Upload `mixed_records.csv`
2. Check 15 valid records separated correctly
3. Review 5 invalid records and errors
4. Verify duplicate detection (ORD1011, ORD1012)

---

## 📝 CSV Format:

All files follow this exact format:
```
order_id, customer_name, country_code, phone, date, time, 
product_id, product_name, amount, payment_mode
```

**Example valid row:**
```
ORD001, Rajesh Kumar, IN, 9876543210, 2024-01-15, 10:30:00, PROD001, Laptop, 45000.00, CARD
```

---

## 🌍 Supported Countries:

| Code | Country | Phone Length |
|------|---------|--------------|
| IN | India | 10 digits |
| US | United States | 10 digits |
| SG | Singapore | 8 digits |
| UK | United Kingdom | 10 digits |
| AU | Australia | 9 digits |
| NZ | New Zealand | 9 digits |
| CA | Canada | 10 digits |
| FR | France | 9 digits |
| DE | Germany | 11 digits |
| JP | Japan | 10 digits |
| CH | Switzerland | 9 digits |

---

## 💳 Allowed Payment Modes:

✅ CARD
✅ UPI
✅ NETBANKING
✅ CASH

---

## ✔️ Validation Rules:

1. **Phone:** Must be digits only, country-specific length
2. **Date:** Must be YYYY-MM-DD format (e.g., 2024-01-15)
3. **Time:** Must be HH:MM:SS format (e.g., 10:30:00)
4. **Amount:** Must be numeric and > 0
5. **Mandatory:** All fields are required (no empty cells)
6. **Duplicates:** Order IDs must be unique

---

## 🎯 What Each File Tests:

### valid_records.csv
- ✓ Correct phone format for India
- ✓ Valid date/time format
- ✓ All payment modes
- ✓ Positive amounts
- ✓ No duplicates

### invalid_records.csv
- ✗ Too short phone (12345)
- ✗ Invalid date (2024-13-45)
- ✗ Invalid time (25:90:00)
- ✗ Unknown payment mode (BITCOIN, GPAY, WALLET)
- ✗ Zero amount (0.00)
- ✗ Negative amount (-500.00)
- ✗ Missing fields (empty phone, date, time, amount)
- ✗ Wrong country code (XX)
- ✗ Too long phone
- ✗ Non-numeric amount (ABC.00)

### international_records.csv
- ✓ US: 5551234567 (10 digits)
- ✓ SG: 98765432 (8 digits)
- ✓ UK: 2075551234 (10 digits)
- ✓ AU: 287654321 (9 digits)
- ✓ NZ: 212345678 (9 digits)
- ✓ CA: 4165551234 (10 digits)

### mixed_records.csv
- ✓ Valid India records (ORD1001-ORD1015)
- ✗ Duplicate IDs (ORD1011, ORD1012)
- ✗ Wrong phone length (987654321 - 9 digits instead of 10)
- ✗ Invalid date format (2024/01/18 instead of 2024-01-18)
- ✗ Invalid time format (18-00-00 instead of 18:00:00)
- ✗ Invalid payment mode (WALLET)
- ✗ Negative amount (-1000.00)

---

## 💡 Tips:

1. **Start Simple:** Begin with `valid_records.csv`
2. **Test Errors:** Use `invalid_records.csv` to see error handling
3. **Test Scale:** Upload multiple files to test session management
4. **Check Downloads:** Verify CSV files can be downloaded
5. **Review Reports:** Check validation_report.csv for details

---

## 📥 Download Results:

After uploading, you can download:
- ✅ `valid_records.csv` - All valid transactions
- ❌ `invalid_records.csv` - All invalid transactions
- 📋 `validation_report.csv` - Detailed error report
- 📦 `chunks_*.zip` - Split files (if > 1000 rows)

---

Happy Testing! 🧪 🚀

