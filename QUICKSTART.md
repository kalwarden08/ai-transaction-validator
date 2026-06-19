# AI Transaction Validator - Getting Started Guide

## 🚀 Quick Start (Windows)

1. **Double-click `run.bat`** file in the project directory
   - This will automatically install dependencies and start the server

2. Open your browser and go to: **http://localhost:8000**

3. Use the web interface to upload CSV files

## 🚀 Quick Start (macOS/Linux)

1. **Make the script executable**:
   ```bash
   chmod +x run.sh
   ```

2. **Run the script**:
   ```bash
   ./run.sh
   ```

3. Open your browser and go to: **http://localhost:8000**

## 📋 Manual Setup (Alternative)

### Windows Command Prompt

```batch
cd C:\Users\Acer\OneDrive\Desktop\AI_Transaction_Validator
pip install -r requirements.txt
uvicorn main:app --reload
```

### macOS/Linux Terminal

```bash
cd ~/path/to/AI_Transaction_Validator
pip3 install -r requirements.txt
uvicorn main:app --reload
```

## 📝 Testing with Sample Data

1. Start the application (see Quick Start above)
2. Click on the upload area or drag the **sample_data.csv** file
3. Click "Validate & Process"
4. Review the results:
   - 12 valid records
   - 8 invalid records
   - Detailed error report

## 🔧 Configuration Options

### Change Port Number

To run on a different port (e.g., 8001):

```bash
uvicorn main:app --reload --port 8001
```

Then access at: **http://localhost:8001**

### Change Chunk Size

Edit `main.py` and modify:

```python
CHUNK_SIZE = 1000  # Change this value
```

### Add/Modify Country Phone Rules

Edit `country_rules.json`:

```json
{
  "IN": 10,
  "US": 10,
  "YOUR_COUNTRY": 8
}
```

## 📊 Web Interface Features

### Upload Section
- **Drag & Drop**: Drag CSV files directly onto the upload area
- **Click to Browse**: Click the upload area to select files
- Shows file name and size before upload

### Processing
- **Real-time Progress**: Visual progress bar during processing
- **Error Handling**: Clear error messages for upload issues

### Results Dashboard
- **Statistics Cards**:
  - Total Records
  - Valid Records
  - Invalid Records
  - Success Rate %

- **Download Options**:
  - Valid Records CSV
  - Invalid Records CSV
  - Validation Report
  - Chunked Files (ZIP)

- **Error Table**:
  - Shows first 100 validation errors
  - Row number, Order ID, and error description

## 📁 File Outputs

After processing, files are saved in `outputs/{timestamp}/`:

- `valid_records.csv` - All valid records
- `invalid_records.csv` - All invalid records
- `validation_report.csv` - Detailed error report
- `chunk_1.csv`, `chunk_2.csv`, etc. - Split valid records
- `chunks_{timestamp}.zip` - All chunks in ZIP format

## ✅ Sample Data Description

The provided `sample_data.csv` contains:

- **Valid Records**: Properly formatted transactions from different countries
- **Invalid Records**: Examples of:
  - Incorrect phone length
  - Invalid date format
  - Invalid time format
  - Wrong payment mode
  - Zero/negative amounts
  - Duplicate order IDs

## 🐛 Troubleshooting

### Port Already in Use
```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found Error
```bash
pip install --upgrade -r requirements.txt
```

### File Not Found Error
Make sure you run the command from the project directory:
```bash
cd /path/to/AI_Transaction_Validator
```

### Browser Doesn't Show the App
- Check that the server is running (you should see "Uvicorn running on...")
- Verify you're using the correct URL: http://localhost:8000
- Try a different browser
- Check firewall settings

## 🌐 Accessing from Other Machines

To access the application from other computers on your network:

1. Find your computer's IP address:
   - **Windows**: Run `ipconfig` in Command Prompt, look for IPv4 Address
   - **macOS/Linux**: Run `ifconfig` in Terminal

2. Start the server with:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Access from another machine:
   ```
   http://<your-ip-address>:8000
   ```

## 📚 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload File (PowerShell)
```powershell
$file = "C:\path\to\file.csv"
Invoke-WebRequest -Uri "http://localhost:8000/upload" `
  -Method POST `
  -Form @{file=([io.FileInfo]$file)}
```

### Download File
```bash
curl http://localhost:8000/download/{session_id}/{filename} -o downloaded.csv
```

## 🎯 Next Steps

1. **Test the application** with the provided sample data
2. **Prepare your CSV** file with the required columns
3. **Customize validation rules** in `country_rules.json` if needed
4. **Upload and process** your transaction data
5. **Download and review** the results

## 📞 Support

For issues:
1. Check the README.md for detailed documentation
2. Review error messages in the web interface
3. Check browser console (F12) for JavaScript errors
4. Verify CSV format matches the requirements

---

**Happy Validating! 🎉**
