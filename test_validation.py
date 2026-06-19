import pandas as pd
from validation import TransactionValidator

# Load sample data
df = pd.read_csv('sample_data.csv')
print(f'Sample data loaded: {len(df)} records')

# Validate
validator = TransactionValidator('country_rules.json')
valid_df, invalid_df, errors = validator.validate_dataset(df)

print(f'Valid records: {len(valid_df)}')
print(f'Invalid records: {len(invalid_df)}')
print(f'Total errors: {len(errors)}')
print()
print('Sample errors (first 3):')
for i, error in enumerate(errors[:3]):
    print(f'  - Row {error["row"]}: {error["error"]}')
