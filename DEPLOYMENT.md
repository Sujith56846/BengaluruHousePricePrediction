# Bangalore House Price Predictor - Deployment Guide

## 🚀 Quick Start

1. **Clone and Setup**
```bash
git clone <repository-url>
cd BangaloreHousePrediction
pip install -r requirements.txt
```

2. **Run Locally**
```bash
python app.py
# Visit: http://localhost:5000
```

## 📦 Deployment Options

### 1. 🐳 Docker Deployment (Recommended)

**Build and Run:**
```bash
# Build the image
docker build -t bangalore-house-predictor .

# Run the container
docker run -p 5000:5000 bangalore-house-predictor
```

**Using Docker Compose:**
```bash
docker-compose up -d
```

### 2. ☁️ Heroku Deployment

**Setup:**
```bash
# Install Heroku CLI
npm install -g heroku

# Login and create app
heroku login
heroku create bangalore-house-predictor

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main
```

**Procfile for Heroku:**
```
web: gunicorn app:app
```

### 3. 🌐 AWS EC2 Deployment

**Launch EC2 Instance:**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone repository
git clone <your-repo>
cd BangaloreHousePrediction

# Install requirements
pip3 install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/your/app/static;
        expires 1y;
    }
}
```

### 4. 🔥 Google Cloud Platform

**Using Cloud Run:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/bangalore-predictor
gcloud run deploy --image gcr.io/PROJECT-ID/bangalore-predictor --platform managed
```

**Using App Engine:**
Create `app.yaml`:
```yaml
runtime: python39

env_variables:
  FLASK_ENV: production

automatic_scaling:
  min_instances: 0
  max_instances: 10
```

Deploy:
```bash
gcloud app deploy
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Required Variables:**
- `FLASK_APP`: app.py
- `FLASK_ENV`: production
- `PORT`: 5000 (or your preferred port)
- `SECRET_KEY`: Generate a secure secret key

**Optional Variables:**
- `WORKERS`: Number of Gunicorn workers (default: 4)
- `LOG_LEVEL`: INFO, DEBUG, WARNING, ERROR
- `ENABLE_API_RATE_LIMITING`: True/False

### Model Files

Ensure your trained model is present:
```
├── linear_regression_model.pkl   # Production model (R² = 0.8554)
└── Cleaned_data.csv              # Location list and feature reference
```

**Note:** The application uses only Linear Regression for predictions. Lasso and Ridge regression models are available in the Jupyter notebook (`bangalore_house_price_pred.ipynb`) for analysis and comparison purposes.

## 🔒 Production Security

### 1. **Environment Setup**
```bash
# Create production environment file
echo "FLASK_ENV=production" > .env
echo "FLASK_DEBUG=False" >> .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')" >> .env
```

### 2. **Nginx SSL Configuration**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. **Rate Limiting**
The app includes built-in rate limiting. Configure in `.env`:
```
ENABLE_API_RATE_LIMITING=True
API_RATE_LIMIT=100  # requests per minute
```

## 📊 Monitoring & Logging

### Health Check Endpoint
```bash
curl http://your-domain.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "models_loaded": 1,
  "locations_available": 240,
  "model_type": "Linear Regression"
}
```

### Log Configuration
```python
# In app.py - already configured
import logging
logging.basicConfig(level=logging.INFO)
```

## 🎯 Performance Optimization

### 1. **Model Caching**
Models are loaded once at startup and cached in memory.

### 2. **Static File Serving**
Configure your web server to serve static files directly:

**Nginx:**
```nginx
location /static {
    alias /path/to/app/static;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. **Database Optimization** (Future)
For high-traffic scenarios, consider adding Redis for caching:
```bash
pip install redis flask-caching
```

## 🧪 Testing Deployment

### Local Testing
```bash
# Test API endpoints
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "total_sqft": 1200,
    "bath": 2,
    "bhk": 2,
    "location": "Electronic City"
  }'
```

### Load Testing
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test with 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://your-domain.com/
```

## 📱 Domain Setup

### 1. **DNS Configuration**
Point your domain to your server:
```
Type: A
Name: @
Value: YOUR_SERVER_IP
TTL: 3600
```

### 2. **SSL Certificate**
Using Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔄 Continuous Deployment

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.2
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /path/to/your/app
          git pull origin main
          pip install -r requirements.txt
          sudo systemctl restart your-app-service
```

## 🛠️ Troubleshooting

### Common Issues

**1. Models not loading:**
```bash
# Check model files exist
ls -la *.pkl
# Check Python path and permissions
python -c "import joblib; print('OK')"
```

**2. Port already in use:**
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill process
sudo kill -9 <PID>
```

**3. Memory issues:**
```bash
# Check memory usage
free -h
# Reduce Gunicorn workers
export WORKERS=2
```

### Logs
```bash
# View application logs
tail -f app.log

# View Gunicorn logs
tail -f /var/log/gunicorn/error.log

# View Nginx logs
tail -f /var/log/nginx/error.log
```

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify all model files are present
3. Ensure all dependencies are installed
4. Test API endpoints manually
5. Check server resources (CPU, memory, disk)

## 🚀 Next Steps

After successful deployment:

1. **Setup monitoring** (Prometheus, Grafana)
2. **Add analytics** (Google Analytics)
3. **Implement caching** (Redis)
4. **Setup alerts** (Sentry, email notifications)
5. **Add more features** (user accounts, prediction history)
6. **Scale horizontally** (load balancer, multiple instances)

Happy Deploying! 🎉