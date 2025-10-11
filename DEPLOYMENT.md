# Deployment Guide for Lead Follow-up AI Agent

This guide covers deploying the Lead Follow-up AI Agent to various cloud platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended for beginners)
- **Pros**: Free tier, easy setup, automatic deployments
- **Cons**: Limited resources on free tier
- **Time**: 5-10 minutes

### Option 2: Railway
- **Pros**: Generous free tier, fast deployments
- **Cons**: Credit-based pricing
- **Time**: 5-10 minutes

### Option 3: AWS Lambda
- **Pros**: Pay-per-use, highly scalable
- **Cons**: More complex setup, cold starts
- **Time**: 15-30 minutes

## 📋 Prerequisites

Before deploying, ensure you have:

1. **GitHub Repository**: Your code pushed to GitHub
2. **OpenAI API Key**: Valid API key with credits
3. **Environment Variables**: All required config values
4. **Database Plan**: Decide on database hosting (SQLite for simple, PostgreSQL for production)

## 🌐 Render Deployment

### Step 1: Connect Repository
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository and branch

### Step 2: Configure Service
```yaml
Name: lead-followup-ai-agent
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Set Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
LOG_LEVEL=INFO
```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build and deployment (5-10 minutes)
3. Your API will be available at: `https://your-app-name.onrender.com`

## 🚂 Railway Deployment

### Step 1: Connect Repository
1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository

### Step 2: Configure Service
Railway will auto-detect Python and install dependencies.

### Step 3: Set Environment Variables
In Railway dashboard:
```bash
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
LOG_LEVEL=INFO
```

### Step 4: Deploy
1. Railway will automatically deploy
2. Your API will be available at the provided URL
3. You can set a custom domain in the settings

## ☁️ AWS Lambda Deployment

### Step 1: Prepare for Lambda
Create a `lambda_handler.py` file:

```python
import json
from mangum import Mangum
from app.main import app

# Create ASGI handler for Lambda
handler = Mangum(app, lifespan="off")

# Lambda handler function
def lambda_handler(event, context):
    return handler(event, context)
```

### Step 2: Update Requirements
Add to `requirements.txt`:
```txt
mangum==0.17.0
```

### Step 3: Create Deployment Package
```bash
# Install dependencies
pip install -r requirements.txt -t package/

# Copy your source code
cp -r src/ package/
cp -r app/ package/

# Create ZIP file
cd package && zip -r ../lambda-deployment.zip .
```

### Step 4: Deploy to Lambda
1. Go to AWS Lambda Console
2. Create new function
3. Upload the ZIP file
4. Set environment variables
5. Configure API Gateway trigger

## 🐳 Docker Deployment

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Build and Run
```bash
# Build image
docker build -t lead-followup-ai-agent .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e LLM_MODEL=gpt-4o \
  lead-followup-ai-agent
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_production_api_key

# Optional (with defaults)
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
LOG_LEVEL=INFO

# Database (for production)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Security
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Security Considerations
1. **API Key Management**: Use environment variables, never commit keys
2. **CORS Configuration**: Restrict to your domains
3. **Rate Limiting**: Implement rate limiting for production
4. **Authentication**: Add API key or JWT authentication
5. **HTTPS**: Always use HTTPS in production

### Monitoring and Logging
1. **Application Logs**: Use cloud logging services
2. **Performance Monitoring**: Set up APM tools
3. **Error Tracking**: Implement error reporting
4. **Health Checks**: Monitor `/api/v1/health` endpoint

## 📊 Database Options

### SQLite (Development/Simple)
- **Pros**: Simple, no setup, included
- **Cons**: Not suitable for production, limited concurrency
- **Use Case**: Development, testing, simple deployments

### PostgreSQL (Production)
- **Pros**: Robust, scalable, concurrent access
- **Cons**: Requires setup, additional cost
- **Use Case**: Production, high-traffic applications

### Database Migration
To switch to PostgreSQL:

1. Update `DATABASE_URL` in environment
2. Install PostgreSQL adapter: `pip install psycopg2-binary`
3. Update `src/database.py`:
```python
# Remove SQLite-specific connect_args
engine = create_engine(DATABASE_URL)
```

## 🔄 CI/CD Setup

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v1.0.0
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

## 🧪 Testing Deployment

### Health Check
```bash
curl https://your-api-url.com/api/v1/health
```

### Test Lead Analysis
```bash
curl -X POST https://your-api-url.com/api/v1/lead \
  -H "Content-Type: application/json" \
  -d '{
    "zoho_id": "TEST_001",
    "company_name": "Test Corp",
    "contact_name": "John Doe",
    "email": "john@test.com"
  }'
```

### Load Testing
Use tools like Apache Bench or Artillery:
```bash
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 -T application/json \
  -p test_payload.json \
  https://your-api-url.com/api/v1/lead
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   - Check Python path and imports
   - Ensure all `__init__.py` files exist

2. **Database Connection**
   - Verify `DATABASE_URL` format
   - Check database permissions

3. **OpenAI API Errors**
   - Verify API key is valid
   - Check API quota and billing

4. **Port Binding**
   - Use `$PORT` environment variable
   - Ensure port is available

### Debug Mode
Set `LOG_LEVEL=DEBUG` for detailed logging.

### Local Testing
Test locally before deploying:
```bash
python start_server.py
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use multiple instances behind a load balancer
- Implement session affinity if needed
- Use shared database for state

### Vertical Scaling
- Increase memory and CPU allocation
- Optimize database queries
- Use connection pooling

### Caching
- Implement Redis for caching
- Cache LLM responses for similar leads
- Use CDN for static assets

## 💰 Cost Optimization

### OpenAI API
- Use appropriate model for your needs
- Implement request caching
- Monitor usage and set limits

### Infrastructure
- Use spot instances where possible
- Implement auto-scaling
- Monitor resource usage

---

**Need help?** Check the main README.md or create an issue in the repository.



