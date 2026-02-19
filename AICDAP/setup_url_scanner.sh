#!/bin/bash

# AICDAP URL Scanner Integration Setup Script
# This script sets up the integrated phishing URL detection feature

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if script is run from the correct directory
if [ ! -f "setup_url_scanner.sh" ]; then
    print_error "Please run this script from the AICDAP root directory"
    exit 1
fi

print_status "Setting up AICDAP URL Scanner Integration..."

# 1. Setup Backend Dependencies
print_status "Installing backend dependencies..."

cd backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

print_success "Backend dependencies installed successfully"

# 2. Verify ML Model
print_status "Checking ML model..."

if [ -f "model/phish_model.pkl" ]; then
    print_success "Phishing detection model found"
else
    print_warning "Phishing detection model not found!"
    print_status "Please ensure the model file is in backend/model/phish_model.pkl"
fi

# 3. Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p temp
mkdir -p uploads

cd ..

# 4. Setup Frontend Dependencies
print_status "Setting up frontend dependencies..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js packages..."
    npm install
else
    print_status "Updating Node.js packages..."
    npm update
fi

# Install additional dependencies if needed
print_status "Installing axios for API communication..."
npm install axios

print_success "Frontend dependencies installed successfully"

# 5. Environment Configuration
print_status "Setting up environment configuration..."

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_status "Creating .env.local file..."
    cat > .env.local << EOF
# API Configuration
REACT_APP_API_BASE_URL=http://localhost:8000

# App Configuration
REACT_APP_APP_NAME=AICDAP
REACT_APP_VERSION=1.0.0

# Feature Flags
REACT_APP_ENABLE_URL_SCANNER=true
REACT_APP_ENABLE_BULK_ANALYSIS=true
REACT_APP_ENABLE_SCAN_HISTORY=true

# UI Configuration
REACT_APP_MAX_BULK_URLS=50
REACT_APP_SCAN_TIMEOUT=30000

# Environment
NODE_ENV=development
EOF
    print_success ".env.local created"
else
    print_status ".env.local already exists"
fi

cd ..

# 6. Backend Environment Setup
print_status "Setting up backend environment..."

cd backend

if [ ! -f ".env" ]; then
    print_status "Creating backend .env file..."
    cat > .env << EOF
# FastAPI Configuration
APP_HOST=localhost
APP_PORT=8000
DEBUG=true

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Database Configuration (if using database)
# DATABASE_URL=your_database_url_here

# Email Service Configuration (if needed)
# RESEND_API_KEY=your_resend_api_key_here

# Supabase Configuration (if using)
# SUPABASE_URL=your_supabase_url_here
# SUPABASE_ANON_KEY=your_supabase_anon_key_here
EOF
    print_success "Backend .env created"
else
    print_status "Backend .env already exists"
fi

cd ..

# 7. Test the setup
print_status "Testing the setup..."

# Check Python imports
print_status "Testing Python imports..."
cd backend
source venv/bin/activate

python3 -c "
import sys
try:
    import fastapi
    import joblib
    import numpy as np
    import pandas as pd
    from utils.feature_extractor import url_features
    print('✓ All Python dependencies imported successfully')

    # Test feature extraction
    test_url = 'https://example.com'
    features = url_features(test_url)
    print(f'✓ Feature extraction working - extracted {len(features)} features')

except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'✗ Error testing setup: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    print_success "Python setup test passed"
else
    print_error "Python setup test failed"
    exit 1
fi

cd ..

# 8. Create startup scripts
print_status "Creating startup scripts..."

# Backend startup script
cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "Starting AICDAP Backend..."
cd backend
source venv/bin/activate
python main.py
EOF

chmod +x start_backend.sh

# Frontend startup script
cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "Starting AICDAP Frontend..."
cd frontend
npm start
EOF

chmod +x start_frontend.sh

# Combined startup script
cat > start_all.sh << 'EOF'
#!/bin/bash
echo "Starting AICDAP Full Stack Application..."

# Start backend in background
echo "Starting backend..."
./start_backend.sh &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
./start_frontend.sh &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Application starting up..."
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap 'echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
EOF

chmod +x start_all.sh

print_success "Startup scripts created"

# 9. Create README for the URL Scanner feature
print_status "Creating feature documentation..."

cat > URL_SCANNER_README.md << 'EOF'
# AICDAP URL Scanner Integration

This document describes the integrated URL scanner feature that provides AI-powered phishing detection.

## Features

- **Single URL Analysis**: Analyze individual URLs for phishing indicators
- **Bulk URL Analysis**: Analyze up to 50 URLs simultaneously
- **Real-time Results**: Get instant analysis results with confidence scores
- **Risk Level Classification**: URLs classified as Low, Low-Medium, Medium, or High risk
- **Whitelist Support**: Trusted domains automatically marked as safe
- **Scan History**: Track recent scans and results
- **Dashboard Integration**: URL scanner status widget in admin dashboard

## Architecture

### Backend Components
- `services/phishing_detector.py`: Core ML-based detection service
- `utils/feature_extractor.py`: URL feature extraction utilities
- `model/phish_model.pkl`: Trained machine learning model
- API endpoints at `/api/analyze-url` and `/api/analyze-urls/bulk`

### Frontend Components
- `components/URLScanner.js`: Main scanner interface
- `components/URLScannerWidget.js`: Dashboard widget
- `services/urlAnalysisService.js`: API communication service
- `pages/URLScanner.js`: Standalone scanner page

## API Endpoints

### Single URL Analysis
```
POST /api/analyze-url
Body: {"url": "https://example.com"}
```

### Bulk URL Analysis
```
POST /api/analyze-urls/bulk
Body: {"urls": ["https://example1.com", "https://example2.com"]}
```

### Scanner Statistics
```
GET /api/url-analysis/stats
```

## Usage

### Via Web Interface
1. Navigate to `/url-scanner` for public access
2. Navigate to `/admin/url-scanner` for admin interface
3. Enter URL(s) and click "Scan" or "Analyze All"

### Via API
```javascript
// Single URL
const response = await fetch('/api/analyze-url', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({url: 'https://suspicious-site.com'})
});
const result = await response.json();
```

## Configuration

### Environment Variables
- `REACT_APP_API_BASE_URL`: Backend API URL (default: http://localhost:8000)
- `REACT_APP_MAX_BULK_URLS`: Maximum URLs for bulk analysis (default: 50)
- `REACT_APP_SCAN_TIMEOUT`: Request timeout in milliseconds (default: 30000)

### Detection Thresholds
- Default confidence threshold: 0.7 (70%)
- Modifiable in `services/phishing_detector.py`

## Model Information

The phishing detection model uses the following features:
- URL length
- Number of dots and hyphens
- Path length
- Presence of @ symbol
- Punycode usage
- IP address detection
- Subdomain analysis
- Character entropy

## Troubleshooting

### Common Issues
1. **Model not found**: Ensure `model/phish_model.pkl` exists
2. **API connection failed**: Check backend is running on correct port
3. **CORS errors**: Verify FRONTEND_URL in backend .env

### Logs
- Backend logs: Check console output when running backend
- Frontend logs: Check browser developer console
- Analysis logs: Check `fp_log.csv` for borderline cases

## Security Considerations

- URLs are not stored permanently by default
- Analysis history is kept in browser memory only
- No personal data is collected during scanning
- Whitelist prevents false positives on trusted domains

## Performance

- Single URL analysis: ~100-500ms
- Bulk analysis: ~50-200ms per URL
- Model loading: ~1-2 seconds on startup
- Memory usage: ~50-100MB for model

## Future Enhancements

- Real-time threat feed integration
- Custom domain whitelisting
- Analysis result export
- Historical trending
- Advanced reporting features
EOF

print_success "Documentation created"

# 10. Final verification
print_status "Running final verification..."

# Check if all required files exist
required_files=(
    "backend/main.py"
    "backend/services/phishing_detector.py"
    "backend/utils/feature_extractor.py"
    "backend/model/phish_model.pkl"
    "frontend/src/components/URLScanner.js"
    "frontend/src/services/urlAnalysisService.js"
    "frontend/package.json"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    print_success "All required files are present"
else
    print_warning "Missing files detected:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
fi

# 11. Summary
echo ""
echo "==================== SETUP COMPLETE ===================="
print_success "AICDAP URL Scanner Integration setup completed!"
echo ""
echo "Next steps:"
echo "1. Start the backend: ./start_backend.sh"
echo "2. Start the frontend: ./start_frontend.sh"
echo "3. Or start both: ./start_all.sh"
echo ""
echo "Access points:"
echo "- Backend API: http://localhost:8000"
echo "- Frontend App: http://localhost:3000"
echo "- URL Scanner: http://localhost:3000/url-scanner"
echo "- Admin Scanner: http://localhost:3000/admin/url-scanner"
echo ""
echo "Documentation:"
echo "- Feature docs: URL_SCANNER_README.md"
echo "- API docs: http://localhost:8000/docs (when backend is running)"
echo ""
print_status "Happy scanning! 🛡️"
echo "=========================================================="
