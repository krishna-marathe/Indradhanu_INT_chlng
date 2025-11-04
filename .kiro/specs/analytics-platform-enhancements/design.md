# Analytics Platform Enhancements - Design Document

## Overview

This design document outlines the technical architecture and implementation approach for enhancing the Indradhanu Analytics platform with PDF report generation, MongoDB storage, React frontend migration, comprehensive error handling, and production deployment capabilities.

## Architecture

### High-Level System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Flask Backend  │    │   MongoDB       │
│                 │    │                  │    │   Database      │
│ - Upload Modal  │◄──►│ - Upload API     │◄──►│                 │
│ - Results Panel │    │ - Report API     │    │ - Upload Meta   │
│ - History Dash  │    │ - History API    │    │ - Insights      │
│ - Chart Grid    │    │ - Static Files   │    │ - Analytics     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Analytics Engine │
                       │                  │
                       │ - Data Loader    │
                       │ - Data Cleaner   │
                       │ - Visualizer     │
                       │ - Insights Gen   │
                       └──────────────────┘
```

### Technology Stack

- **Frontend**: React 18+ with TypeScript, Axios for API calls, Material-UI or Tailwind CSS
- **Backend**: Flask with Flask-CORS, Flask-PyMongo, ReportLab for PDF generation
- **Database**: MongoDB for persistent storage
- **File Storage**: Local filesystem (development) → AWS S3 (production)
- **Deployment**: Render/Railway for backend, Vercel for frontend

## Components and Interfaces

### 1. PDF Report Generation System

#### Flask Backend Components

**ReportGenerator Class**
```python
class ReportGenerator:
    def __init__(self, upload_data, charts_paths, insights):
        self.upload_data = upload_data
        self.charts_paths = charts_paths
        self.insights = insights
    
    def generate_pdf(self) -> BytesIO:
        # Create PDF with reportlab
        # Include summary statistics
        # Embed chart images
        # Add insights section
        pass
    
    def generate_csv_summary(self) -> StringIO:
        # Create CSV with key metrics
        pass
```

**API Endpoint**
```python
@app.route('/report/<filename>')
def generate_report(filename):
    # Retrieve analysis data from MongoDB
    # Generate PDF using ReportGenerator
    # Return file download response
    pass
```

#### Frontend Integration
- Add "Download Report" button to ResultsPanel component
- Implement download trigger with proper file handling
- Show progress indicator during PDF generation

### 2. MongoDB Storage System

#### Database Schema

**uploads Collection**
```javascript
{
  _id: ObjectId,
  filename: String,
  original_filename: String,
  upload_timestamp: Date,
  file_size: Number,
  file_type: String,
  processing_status: String, // 'processing', 'completed', 'failed'
  data_summary: {
    rows: Number,
    columns: Number,
    column_names: [String]
  },
  insights: [String],
  charts: [{
    type: String,
    filename: String,
    url: String,
    title: String
  }],
  error_log: String // if processing failed
}
```

#### MongoDB Integration
```python
from flask_pymongo import PyMongo
from datetime import datetime

class AnalyticsStorage:
    def __init__(self, mongo_client):
        self.db = mongo_client.db
        self.uploads = self.db.uploads
    
    def save_upload_metadata(self, upload_data):
        # Save complete analysis results
        pass
    
    def get_upload_history(self, limit=50, offset=0):
        # Retrieve paginated upload history
        pass
    
    def get_upload_by_filename(self, filename):
        # Retrieve specific upload data
        pass
```

### 3. React Frontend Migration

#### Component Structure

```
src/
├── components/
│   ├── UploadModal.tsx
│   ├── ResultsPanel.tsx
│   ├── ChartGrid.tsx
│   ├── HistoryDashboard.tsx
│   ├── ErrorBoundary.tsx
│   └── LoadingSpinner.tsx
├── hooks/
│   ├── useFileUpload.ts
│   ├── useAnalytics.ts
│   └── useHistory.ts
├── services/
│   ├── api.ts
│   └── types.ts
├── utils/
│   ├── fileValidation.ts
│   └── errorHandling.ts
└── App.tsx
```

#### Key Components Design

**UploadModal Component**
```typescript
interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: (results: AnalyticsResults) => void;
}

const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onUploadSuccess
}) => {
  // Drag & drop functionality
  // File validation
  // Upload progress
  // Error handling
};
```

**ResultsPanel Component**
```typescript
interface ResultsPanelProps {
  results: AnalyticsResults;
  onDownloadReport: (filename: string) => void;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({
  results,
  onDownloadReport
}) => {
  // Display statistics
  // Show insights
  // Render chart grid
  // Download report button
};
```

#### API Service Layer
```typescript
class AnalyticsAPI {
  private baseURL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
  
  async uploadFile(file: File): Promise<AnalyticsResults> {
    // Handle file upload with progress
  }
  
  async downloadReport(filename: string): Promise<Blob> {
    // Download PDF report
  }
  
  async getUploadHistory(): Promise<UploadHistory[]> {
    // Fetch upload history
  }
}
```

### 4. Error Handling System

#### Backend Error Handling

**Custom Exception Classes**
```python
class AnalyticsError(Exception):
    def __init__(self, message: str, error_code: str, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}

class FileValidationError(AnalyticsError):
    pass

class ProcessingTimeoutError(AnalyticsError):
    pass

class ChartGenerationError(AnalyticsError):
    pass
```

**Error Handler Middleware**
```python
@app.errorhandler(AnalyticsError)
def handle_analytics_error(error):
    return jsonify({
        'error': True,
        'message': error.message,
        'error_code': error.error_code,
        'details': error.details
    }), 400

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Log error details
    # Return generic error response
    pass
```

#### Frontend Error Handling

**Error Boundary Component**
```typescript
class ErrorBoundary extends React.Component {
  // Catch and display React errors
  // Provide fallback UI
  // Log errors for debugging
}
```

**Error Context**
```typescript
interface ErrorContextType {
  errors: AppError[];
  addError: (error: AppError) => void;
  clearErrors: () => void;
}

const ErrorContext = React.createContext<ErrorContextType>();
```

### 5. Deployment Architecture

#### Development vs Production Configuration

**Environment Configuration**
```python
# config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')
    
class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_URI = 'mongodb://localhost:27017/analytics_dev'
    
class ProductionConfig(Config):
    DEBUG = False
    MONGODB_URI = os.environ.get('MONGODB_URI')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
```

**Static File Handling**
- Development: Local filesystem storage
- Production: AWS S3 with CloudFront CDN
- Implement file upload service abstraction

#### Deployment Strategy

**Backend Deployment (Render/Railway)**
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Frontend Deployment (Vercel)**
```json
// vercel.json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "@api_url"
  }
}
```

## Data Models

### Upload Metadata Model
```typescript
interface UploadMetadata {
  id: string;
  filename: string;
  originalFilename: string;
  uploadTimestamp: Date;
  fileSize: number;
  fileType: string;
  processingStatus: 'processing' | 'completed' | 'failed';
  dataSummary: {
    rows: number;
    columns: number;
    columnNames: string[];
  };
  insights: string[];
  charts: ChartMetadata[];
  errorLog?: string;
}

interface ChartMetadata {
  type: 'line' | 'bar' | 'heatmap';
  filename: string;
  url: string;
  title: string;
}
```

### Analytics Results Model
```typescript
interface AnalyticsResults {
  message: string;
  filename: string;
  rows: number;
  columns: number;
  charts: ChartMetadata[];
  insights: string[];
  processingTime: number;
  uploadId: string;
}
```

## Error Handling Strategy

### File Validation
- Check file size limits (max 100MB)
- Validate file extensions and MIME types
- Verify file content structure
- Handle corrupted files gracefully

### Processing Errors
- Implement timeout handling for large files
- Graceful degradation when chart generation fails
- Partial results display when some processing succeeds
- Retry mechanisms for transient failures

### User Experience
- Clear error messages with actionable guidance
- Progress indicators for long-running operations
- Fallback options when features are unavailable
- Offline capability indicators

## Testing Strategy

### Backend Testing
- Unit tests for each analytics component
- Integration tests for API endpoints
- MongoDB integration tests
- PDF generation tests
- Error handling tests

### Frontend Testing
- Component unit tests with React Testing Library
- Integration tests for user workflows
- API mocking for isolated testing
- Accessibility testing
- Cross-browser compatibility testing

### End-to-End Testing
- Complete upload and analysis workflow
- Report generation and download
- History dashboard functionality
- Error scenarios and recovery

## Security Considerations

### File Upload Security
- File type validation and sanitization
- Virus scanning for uploaded files
- Size limits and rate limiting
- Secure file storage with proper permissions

### API Security
- Input validation and sanitization
- Rate limiting and DDoS protection
- CORS configuration for production
- Authentication and authorization (future enhancement)

### Data Privacy
- Secure handling of uploaded data
- Data retention policies
- User data anonymization options
- GDPR compliance considerations

## Performance Optimization

### Backend Optimization
- Async processing for large files
- Caching for frequently accessed data
- Database indexing for query performance
- Connection pooling for MongoDB

### Frontend Optimization
- Code splitting and lazy loading
- Image optimization for charts
- Caching strategies for API responses
- Progressive loading for large datasets

### Infrastructure Optimization
- CDN for static file delivery
- Database query optimization
- Horizontal scaling capabilities
- Monitoring and alerting systems