# Deployment Guide for PRAISA

## Docker Deployment

### Quick Start with Docker

**1. Build the Docker image**:
```bash
docker build -t praisa:latest .
```

**2. Run the container**:
```bash
docker run -d -p 8000:8000 --name praisa-api praisa:latest
```

**3. Check health**:
```bash
curl http://localhost:8000/health
```

---

### Using Docker Compose

**1. Start all services**:
```bash
docker-compose up -d
```

**2. View logs**:
```bash
docker-compose logs -f api
```

**3. Stop services**:
```bash
docker-compose down
```

---

## Production Deployment

### Prerequisites
- Docker and Docker Compose installed
- PostgreSQL database (for production)
- Redis cache (optional)
- Domain name and SSL certificate

### Environment Configuration

**1. Copy environment template**:
```bash
cp .env.example .env
```

**2. Update `.env` for production**:
```env
ENV=production
DATABASE_URL=postgresql://user:password@postgres:5432/praisa_production
API_HOST=0.0.0.0
API_PORT=8000
```

**3. Enable PostgreSQL in docker-compose.yml**:
Uncomment the `postgres` service section.

---

### Deployment Steps

**1. Build and start services**:
```bash
docker-compose up -d --build
```

**2. Initialize database** (first time only):
```bash
docker-compose exec api python scripts/setup_database.py
```

**3. Verify deployment**:
```bash
curl https://your-domain.com/health
```

---

## Cloud Deployment

### AWS (Elastic Beanstalk)

**1. Install EB CLI**:
```bash
pip install awsebcli
```

**2. Initialize EB**:
```bash
eb init -p docker praisa-api
```

**3. Create environment**:
```bash
eb create praisa-production
```

**4. Deploy**:
```bash
eb deploy
```

---

### Google Cloud Platform (Cloud Run)

**1. Build and push image**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/praisa
```

**2. Deploy to Cloud Run**:
```bash
gcloud run deploy praisa \
  --image gcr.io/PROJECT_ID/praisa \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### Azure (Container Instances)

**1. Create resource group**:
```bash
az group create --name praisa-rg --location eastus
```

**2. Create container registry**:
```bash
az acr create --resource-group praisa-rg --name praisaregistry --sku Basic
```

**3. Build and push**:
```bash
az acr build --registry praisaregistry --image praisa:latest .
```

**4. Deploy container**:
```bash
az container create \
  --resource-group praisa-rg \
  --name praisa-api \
  --image praisaregistry.azurecr.io/praisa:latest \
  --dns-name-label praisa-api \
  --ports 8000
```

---

## Monitoring and Maintenance

### Health Checks

**Endpoint**: `GET /health`

**Expected Response**:
```json
{
  "status": "healthy",
  "database": {"status": "connected", "file_exists": true},
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2026-01-04T12:30:00"
}
```

### Logs

**View Docker logs**:
```bash
docker-compose logs -f api
```

**View specific service logs**:
```bash
docker logs praisa-api
```

### Database Backup

**Backup SQLite** (development):
```bash
cp praisa_demo.db praisa_demo_backup_$(date +%Y%m%d).db
```

**Backup PostgreSQL** (production):
```bash
docker-compose exec postgres pg_dump -U praisa praisa_production > backup.sql
```

---

## Scaling

### Horizontal Scaling

**1. Update docker-compose.yml**:
```yaml
api:
  deploy:
    replicas: 3
```

**2. Add load balancer** (nginx):
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs api

# Rebuild image
docker-compose build --no-cache api
```

### Database connection errors
```bash
# Verify database is running
docker-compose ps

# Check database logs
docker-compose logs postgres
```

### Health check failing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Check API logs
docker-compose logs api
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Enable authentication
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates

---

## Rollback Procedure

**1. Stop current deployment**:
```bash
docker-compose down
```

**2. Restore previous version**:
```bash
git checkout <previous-commit>
docker-compose up -d --build
```

**3. Restore database backup**:
```bash
cp praisa_demo_backup.db praisa_demo.db
```

---

## Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:8000/health`
3. Review documentation: `docs/`
