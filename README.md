# Portfolio Contact Form API

A FastAPI backend application that handles contact form submissions from your portfolio website and sends emails via Gmail SMTP.

## Features

- ✅ RESTful API endpoint for contact form submissions
- ✅ Email validation using Pydantic
- ✅ Gmail SMTP integration with app password authentication
- ✅ Professional HTML email formatting
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling and logging
- ✅ Health check endpoint

## Project Structure

```
Backend/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic validation models
├── email_service.py     # Email sending functionality
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── config.env          # Environment variables (git-ignored)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Prerequisites

- Python 3.10 or higher
- Gmail account with App Password enabled

## Installation

### 1. Clone or navigate to the Backend directory

```bash
cd "d:\Code\AntiGravity\Updated Portfolio\Backend"
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

The `config.env` file is already configured with your credentials. If you need to update them:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RECIPIENT_EMAIL=your-email@gmail.com
ALLOWED_ORIGINS=*
```

**Important:** Update `config.py` line 11 to load from `config.env`:

```python
load_dotenv('config.env')
```

## Gmail App Password Setup

Since you're using Gmail, you need an App Password (not your regular Gmail password):

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification (enable if not already)
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Use this generated password in your `config.env` file

## Running the Server

### Development mode (with auto-reload):

```bash
uvicorn main:app --reload --port 8000
```

### Production mode:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **URL:** `GET /`
- **Description:** API information and available endpoints
- **Response:**
  ```json
  {
    "name": "Portfolio Contact API",
    "version": "1.0.0",
    "status": "running"
  }
  ```

### 2. Health Check
- **URL:** `GET /health`
- **Description:** Check if the API is running
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "contact-api"
  }
  ```

### 3. Contact Form Submission
- **URL:** `POST /api/contact`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Inquiry about your work",
    "message": "Hello! I'm interested in discussing a project..."
  }
  ```
- **Success Response (200):**
  ```json
  {
    "success": true,
    "message": "Your message has been sent successfully! We'll get back to you soon."
  }
  ```
- **Error Response (500):**
  ```json
  {
    "detail": "Failed to send your message. Please try again later."
  }
  ```

## Testing

### Using curl:

```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"subject\":\"Test Subject\",\"message\":\"This is a test message from the contact form.\"}"
```

### Using PowerShell:

```powershell
$body = @{
    name = "Test User"
    email = "test@example.com"
    subject = "Test Subject"
    message = "This is a test message from the contact form."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/contact" -Method Post -Body $body -ContentType "application/json"
```

### Interactive API Documentation:

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Frontend Integration

Update your portfolio's contact form to send POST requests to:

```
http://localhost:8000/api/contact
```

### Example JavaScript (Fetch API):

```javascript
const formData = {
  name: "John Doe",
  email: "john@example.com",
  subject: "Project Inquiry",
  message: "Hello, I would like to..."
};

fetch('http://localhost:8000/api/contact', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(formData)
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    alert(data.message);
  }
})
.catch(error => console.error('Error:', error));
```

## Production Deployment

For production:

1. **Update CORS origins** in `config.env`:
   ```env
   ALLOWED_ORIGINS=https://your-portfolio-domain.com
   ```

2. **Use a production ASGI server** (uvicorn with multiple workers):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Consider using a process manager** like:
   - **systemd** (Linux)
   - **PM2** (cross-platform)
   - **Supervisor** (Linux)

4. **Set up a reverse proxy** (nginx, Apache) in front of uvicorn

## Troubleshooting

### "SMTP Authentication failed"
- Verify your Gmail App Password is correct
- Ensure 2-Step Verification is enabled on your Google account
- Check that you're using an App Password, not your regular password

### "Connection refused"
- Check if the server is running: `http://localhost:8000/health`
- Verify the port 8000 is not in use by another application

### CORS errors from frontend
- Ensure your frontend URL is in `ALLOWED_ORIGINS`
- Check the browser console for specific CORS error messages

## License

This project is part of your portfolio website.

---

**Author:** Arnab  
**Email:** ornab@dummy.com
