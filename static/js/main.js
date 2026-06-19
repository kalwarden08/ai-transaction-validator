/**
 * Main JavaScript for AI Transaction Validator
 */

let currentSessionId = null;
let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileSelected = document.getElementById('fileSelected');
const uploadBtn = document.getElementById('uploadBtn');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressPercent = document.getElementById('progressPercent');
const resultsSection = document.getElementById('resultsSection');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');

/**
 * Setup event listeners
 */
document.addEventListener('DOMContentLoaded', function () {
    setupDragAndDrop();
    setupFileInput();
    setupUploadButton();
});

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
}

/**
 * Setup file input change handler
 */
function setupFileInput() {
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

/**
 * Handle file selection
 */
function handleFileSelection(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Only CSV files are allowed.');
        return;
    }

    selectedFile = file;
    const fileSizeKB = (file.size / 1024).toFixed(2);

    document.getElementById('selectedFilename').textContent = file.name;
    document.getElementById('fileSize').textContent = `Size: ${fileSizeKB} KB`;
    fileSelected.style.display = 'block';
    uploadBtn.disabled = false;
}

/**
 * Setup upload button handler
 */
function setupUploadButton() {
    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            showError('Please select a file first.');
            return;
        }

        await uploadFile();
    });
}

/**
 * Upload and process file
 */
async function uploadFile() {
    try {
        hideError();
        progressSection.style.display = 'block';
        uploadBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', selectedFile);

        // Simulate progress
        simulateProgress();

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        currentSessionId = data.session_id;
        displayResults(data);

    } catch (error) {
        showError(error.message);
        progressSection.style.display = 'none';
        uploadBtn.disabled = false;
    }
}

/**
 * Simulate progress bar animation
 */
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;
        
        progressBar.style.width = progress + '%';
        progressPercent.textContent = Math.round(progress) + '%';

        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 200);
}

/**
 * Display validation results
 */
function displayResults(data) {
    // Hide upload section and progress
    uploadArea.parentElement.style.display = 'none';
    progressSection.style.display = 'none';
    progressBar.style.width = '100%';
    progressPercent.textContent = '100%';

    // Show results section
    resultsSection.style.display = 'block';

    // Update statistics
    const stats = data.statistics;
    document.getElementById('totalRecords').textContent = stats.total_records;
    document.getElementById('validRecords').textContent = stats.valid_records;
    document.getElementById('invalidRecords').textContent = stats.invalid_records;
    document.getElementById('successRate').textContent = stats.success_rate + '%';

    // Display download buttons
    displayDownloadButtons(data.files);

    // Display validation errors
    displayValidationErrors(data.validation_summary);

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

/**
 * Display download buttons
 */
function displayDownloadButtons(files) {
    const container = document.getElementById('downloadButtons');
    container.innerHTML = '';

    if (files.valid_csv) {
        container.innerHTML += `
            <div class="col-md-6 col-lg-3">
                <a href="/download/${currentSessionId}/${files.valid_csv}" 
                   class="btn btn-success w-100 download-btn" download>
                    <i class="bi bi-download"></i> Valid Records
                </a>
            </div>
        `;
    }

    if (files.invalid_csv) {
        container.innerHTML += `
            <div class="col-md-6 col-lg-3">
                <a href="/download/${currentSessionId}/${files.invalid_csv}" 
                   class="btn btn-danger w-100 download-btn" download>
                    <i class="bi bi-download"></i> Invalid Records
                </a>
            </div>
        `;
    }

    if (files.validation_report) {
        container.innerHTML += `
            <div class="col-md-6 col-lg-3">
                <a href="/download/${currentSessionId}/${files.validation_report}" 
                   class="btn btn-warning w-100 download-btn" download>
                    <i class="bi bi-download"></i> Validation Report
                </a>
            </div>
        `;
    }

    if (files.chunks && files.chunks.length > 0) {
        container.innerHTML += `
            <div class="col-md-6 col-lg-3">
                <a href="/download-zip/${currentSessionId}" 
                   class="btn btn-info w-100 download-btn" download>
                    <i class="bi bi-download"></i> Download ZIP
                </a>
            </div>
        `;
    }
}

/**
 * Display validation errors
 */
function displayValidationErrors(summary) {
    const errorTable = document.getElementById('errorTable');
    const errorTableBody = document.getElementById('errorTableBody');
    const noErrors = document.getElementById('noErrors');

    if (!summary.errors || summary.errors.length === 0) {
        errorTable.style.display = 'none';
        noErrors.style.display = 'block';
        return;
    }

    errorTable.style.display = 'table';
    noErrors.style.display = 'none';

    errorTableBody.innerHTML = '';
    summary.errors.forEach(error => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><small>#${error.row}</small></td>
            <td><small>${error.order_id}</small></td>
            <td><small class="text-danger">${escapeHtml(error.error)}</small></td>
        `;
        errorTableBody.appendChild(row);
    });
}

/**
 * Reset form for new upload
 */
function resetForm() {
    selectedFile = null;
    currentSessionId = null;
    fileInput.value = '';
    fileSelected.style.display = 'none';
    uploadBtn.disabled = true;
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    uploadArea.parentElement.style.display = 'block';
    progressBar.style.width = '0%';
    progressPercent.textContent = '0%';
    hideError();
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorAlert.style.display = 'none';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
