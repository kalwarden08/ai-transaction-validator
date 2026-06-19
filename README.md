<<<<<<< HEAD
# AI Transaction Validator

A production-ready web application for validating transaction data with comprehensive validation rules and configurable settings.

## Features

- **File Upload**: Drag-and-drop or click to upload CSV files
- **Comprehensive Validation**:
  - Phone number validation based on country-specific rules
  - Date format validation (YYYY-MM-DD)
  - Time format validation (HH:MM:SS)
  - Payment mode validation (UPI, CARD, NETBANKING, CASH)
  - Amount validation (numeric, greater than zero)
  - Mandatory field validation
  - Duplicate order ID detection
- **Data Processing**:
  - Automatic separation of valid and invalid records
  - Configurable CSV chunking (default: 1000 rows per chunk)
  - Generation of validation reports
- **Modern Dashboard**:
  - Real-time statistics (total, valid, invalid records)
  - Success rate percentage
  - Interactive validation error summary
  - Responsive Bootstrap 5 design
- **File Download**:
  - Download valid records CSV
  - Download invalid records CSV
  - Download validation report
  - Download chunked files as ZIP

## Project Structure

```
AI_Transaction_Validator/
├── main.py                      # FastAPI application
├── validation.py                # Validation engine
├── splitter.py                  # CSV splitting utility
├── country_rules.json           # Phone validation rules
├── requirements.txt             # Python dependencies
├── sample_data.csv              # Sample CSV file
├── README.md                    # Documentation
├── uploads/                     # Uploaded files (auto-created)
├── outputs/                     # Processed files (auto-created)
├── templates/
│   └── index.html              # Main HTML template
└── static/
    ├── css/
    │   └── style.css           # Stylesheet
    └── js/
        └── main.js             # Frontend JavaScript
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**

2. **Navigate to project directory**:
   ```bash
   cd AI_Transaction_Validator
   ```

3. **Create virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the server

```bash
uvicorn main:app --reload
```

The application will be available at: **http://localhost:8000**

### Production deployment

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Configuration

### Customizing Phone Validation Rules

Edit `country_rules.json` to add or modify country phone number lengths:

```json
{
  "IN": 10,
  "US": 10,
  "UK": 10,
  "YOUR_COUNTRY": 8
}
```

### Customizing Chunk Size

Edit `main.py` and modify the `CHUNK_SIZE` constant:

```python
CHUNK_SIZE = 1000  # Default: 1000 rows per chunk
```

## CSV File Format

Your CSV file must contain the following columns:

| Column Name | Format | Example | Notes |
|-------------|--------|---------|-------|
| order_id | String | ORD001 | Unique identifier |
| customer_name | String | John Doe | Customer full name |
| country_code | String | IN | ISO 3166-1 alpha-2 code |
| phone | String | 9876543210 | Must match country length |
| date | YYYY-MM-DD | 2024-01-15 | ISO format |
| time | HH:MM:SS | 10:30:00 | 24-hour format |
| product_id | String | PROD001 | Product identifier |
| product_name | String | Laptop | Product name |
| amount | Float | 45000.00 | Must be > 0 |
| payment_mode | String | CARD | UPI, CARD, NETBANKING, or CASH |

## Validation Rules

### Phone Numbers

Phone numbers are validated based on country-specific rules defined in `country_rules.json`. The phone must:
- Contain only digits
- Match the expected length for the country

### Date Format

- Must follow YYYY-MM-DD format
- Example: 2024-01-15

### Time Format

- Must follow HH:MM:SS format (24-hour)
- Example: 14:30:00

### Payment Modes

Allowed values:
- UPI
- CARD
- NETBANKING
- CASH

### Amount

- Must be numeric (integer or decimal)
- Must be greater than 0

### Mandatory Fields

All fields are mandatory. Empty or missing values will cause validation to fail.

### Duplicates

Records with duplicate order_id values are flagged as invalid.

## Output Files

After processing, the following files are generated:

### valid_records.csv
Contains all records that passed validation.

### invalid_records.csv
Contains all records that failed validation.

### validation_report.csv
Detailed report of validation errors with row numbers and descriptions.

### Chunk Files (if applicable)
If valid records exceed the chunk size threshold:
- chunk_1.csv
- chunk_2.csv
- chunk_3.csv
- ... (as needed)

Files can be downloaded as a ZIP archive.

## API Endpoints

### GET /
Renders the main dashboard.

**Response**: HTML page

### POST /upload
Upload and process CSV file.

**Request**: Multipart form with file upload
**Response**: JSON with validation results

```json
{
  "status": "success",
  "session_id": "20240115_103000",
  "statistics": {
    "total_records": 100,
    "valid_records": 95,
    "invalid_records": 5,
    "success_rate": 95.0
  },
  "files": {
    "valid_csv": "valid_records.csv",
    "invalid_csv": "invalid_records.csv",
    "validation_report": "validation_report.csv",
    "chunks": ["chunk_1.csv"],
    "will_split": false
  },
  "validation_summary": {
    "total_errors": 5,
    "errors": [...]
  }
}
```

### GET /download/{session_id}/{filename}
Download a processed file.

### GET /download-zip/{session_id}
Download all chunk files as ZIP.

### GET /health
Health check endpoint.

## Error Handling

The application provides clear error messages for:
- Invalid file formats (non-CSV files)
- Empty files
- Missing required columns
- CSV parsing errors
- Invalid phone formats
- Invalid date/time formats
- Invalid payment modes
- Non-numeric or negative amounts
- Duplicate order IDs
- Missing mandatory fields

## Using Sample Data

A sample CSV file (`sample_data.csv`) is included with:
- Valid records demonstrating proper format
- Invalid records showing various validation errors

To test:
1. Upload `sample_data.csv` through the web interface
2. Review validation results
3. Download processed files

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, specify a different port:
```bash
uvicorn main:app --port 8001
```

### Module Not Found Error
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### CORS Issues
For cross-origin requests, FastAPI CORS middleware can be added to main.py.

## Performance

- Handles CSV files up to 50MB
- Processes thousands of records efficiently
- Automatic chunking for large valid datasets
- In-memory processing with Pandas optimization

## Security

- File validation and size limits
- Filename sanitization to prevent directory traversal
- HTML escaping to prevent XSS attacks
- Secure file storage in `outputs` and `uploads` directories

## Code Quality

- Modular architecture with separate validation and splitting modules
- Type hints for better code clarity
- Comprehensive error handling
- Clean separation of concerns
- Well-documented functions with docstrings

## Dependencies

- **FastAPI** (0.104.1): Modern web framework
- **Uvicorn** (0.24.0): ASGI server
- **Pandas** (2.1.3): Data processing
- **python-multipart** (0.0.6): File upload handling
- **aiofiles** (23.2.1): Async file operations

## Future Enhancements

Potential improvements:
- Database integration for transaction history
- User authentication and multi-tenant support
- Custom validation rule creation via UI
- Real-time progress updates via WebSocket
- Export to different formats (Excel, JSON)
- Scheduled validation jobs
- Transaction analytics dashboard

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check:
1. Sample data format in `sample_data.csv`
2. Country codes in `country_rules.json`
3. Application logs in console output
4. Browser developer console for frontend errors

---

**Version**: 1.0.0
**Last Updated**: 2024
=======
# ai-transaction-validator
AI Transaction Validator is a FastAPI-based web application for validating and processing transaction datasets. It performs country-specific phone validation, date/time and payment checks, detects data quality issues, generates cleaned CSV outputs, and automatically splits large files for efficient processing.
>>>>>>> c44c21dd5901ef1c421c0813432c1c66d9724e2c
