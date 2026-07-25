# 🚀 AI Wiki Quiz Generator - Deployment Guide

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database (or use provided Neon database)
- Google Gemini API key
- Git

## 🏗️ Deployment Options

### Option 1: Vercel (Recommended for Frontend + Backend)

1. **Prepare the repository:**
   ```bash
   git add .
   git commit -m "Production ready deployment"
   git push origin main
   ```

2. **Deploy to Vercel:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```

3. **Configure environment variables in Vercel dashboard:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `GEMINI_API_KEY`: Your Google Gemini API key

### Option 2: Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build -d
   ```

2. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

### Option 3: Manual Server Deployment

#### Backend Deployment:

1. **Install dependencies:**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   pip install -r ../requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your production values (Database URL, Gemini API Key)
   ```

3. **Run the server:**
   ```bash
   # Run directly with Python (uses Uvicorn)
   python run.py
   ```

#### Frontend Deployment:

1. **Build for production:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Serve with nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /path/to/frontend/build;
           try_files $uri $uri/ /index.html;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔧 Environment Configuration

### Production Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Application
DEBUG=False
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
WORKERS=4
RELOAD=False

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints

- **API Health**: `GET /health`
- **API Status**: `GET /`
- **API Documentation**: `GET /docs`

### Monitoring Setup

1. **Add monitoring to your deployment:**
   ```python
   # Add to main.py
   from prometheus_client import Counter, Histogram, generate_latest
   
   REQUEST_COUNT = Counter('app_requests_total', 'Total requests')
   REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
   ```

2. **Set up alerts for:**
   - Database connection failures
   - API response time > 5s
   - Error rate > 5%

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Use HTTPS in production
- [ ] Set secure CORS origins
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database SSL
- [ ] Set up proper logging
- [ ] Configure firewall rules
- [ ] Use strong passwords
- [ ] Regular security updates

### Rate Limiting

```python
# Add to main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/quiz/generate")
@limiter.limit("10/minute")
async def generate_quiz(request: Request, ...):
    # Your existing code
```

## 📈 Performance Optimization

### Database Optimization

```sql
-- Add indexes for better performance
CREATE INDEX CONCURRENTLY idx_quiz_url ON quiz_records(url);
CREATE INDEX CONCURRENTLY idx_quiz_created_at ON quiz_records(created_at);
CREATE INDEX CONCURRENTLY idx_quiz_title ON quiz_records(title);
```

### Caching Strategy

```python
# Add Redis caching
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check connection string
   - Verify database is running
   - Check firewall settings

2. **API Key Issues**
   - Verify Gemini API key is valid
   - Check API quotas and limits
   - Ensure proper permissions

3. **CORS Errors**
   - Update allowed origins
   - Check frontend URL configuration

4. **Memory Issues**
   - Increase server memory
   - Optimize database queries
   - Implement caching

### Log Analysis

```bash
# View application logs
tail -f /var/log/ai-quiz-generator/app.log

# Check error logs
grep "ERROR" /var/log/ai-quiz-generator/app.log

# Monitor performance
grep "duration" /var/log/ai-quiz-generator/app.log
```

## 📞 Support

For deployment issues:

1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure all services are running
4. Check network connectivity
5. Review the troubleshooting section above

## 🔄 Updates & Maintenance

### Updating the Application

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Update dependencies:**
   ```bash
   pip install -r requirements-prod.txt --upgrade
   npm install --production
   ```

3. **Restart services:**
   ```bash
   # Docker
   docker-compose restart
   
   # Manual
   systemctl restart ai-quiz-generator
   ```

### Backup Strategy

1. **Database backups:**
   ```bash
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   ```

2. **Application backups:**
   ```bash
   tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/app
   ```

## 📊 Performance Metrics

Monitor these key metrics:

- **Response Time**: < 2s for quiz generation
- **Uptime**: > 99.9%
- **Error Rate**: < 1%
- **Database Connections**: < 80% of max
- **Memory Usage**: < 80% of available
- **CPU Usage**: < 70% of available

---

**Your AI Wiki Quiz Generator is now production-ready!** 🎉

