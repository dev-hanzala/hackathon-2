# Phase III Deployment Guide

Complete guide for deploying the Todo Application to production.

## Overview

This guide covers deploying:
- **Backend**: FastAPI on serverless platform (Railway/Render/Fly.io)
- **Frontend**: Next.js on Vercel
- **Database**: Neon PostgreSQL (serverless)

## Prerequisites

- Git repository with Phase II complete
- Domain name (optional, can use platform subdomains)
- Credit card for platform signups (free tiers available)

---

## Part 1: Database Setup (Neon)

### 1.1 Create Neon Account

```bash
# Visit https://neon.tech
# Sign up with GitHub account (recommended)
```

### 1.2 Create Production Database

1. Click **"New Project"**
2. Configure:
   - **Name**: `todo-app-production`
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 17 (latest)
   - **Compute Size**: 0.25 vCPU (free tier)

3. Copy connection string:
   ```
   postgresql://user:pass@host.neon.tech/database?sslmode=require
   ```

### 1.3 Initialize Database

```bash
# Set production DATABASE_URL locally (for migrations only)
export DATABASE_URL="postgresql+psycopg://..."

# Run migrations
cd backend
uv run alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
```

**Expected tables:** `user`, `task`, `session`

---

## Part 2: Backend Deployment

### Option A: Railway (Recommended)

**Why Railway:**
- Easy setup with GitHub integration
- Automatic deploys on git push
- Free tier: 500 hours/month
- Built-in environment variables
- Auto-SSL certificates

#### 2.1 Create Railway Account

```bash
# Visit https://railway.app
# Sign up with GitHub
```

#### 2.2 Deploy Backend

1. **New Project** → **Deploy from GitHub Repo**
2. Select `backend/` directory
3. Railway auto-detects Python project

#### 2.3 Configure Environment Variables

In Railway dashboard, add:

```bash
# Database
DATABASE_URL=postgresql+psycopg://... # From Neon

# Auth Secret (generate new!)
BETTER_AUTH_SECRET=<generate-32-char-secret>

# Server Config
DEBUG=false
ENVIRONMENT=production

# CORS (add your frontend domain after deploying frontend)
ALLOWED_ORIGINS=["https://your-app.vercel.app"]

# Error Tracking (Sentry)
SENTRY_DSN=https://...@sentry.io/...
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

**Generate AUTH_SECRET:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2.4 Deploy

Railway auto-deploys on commit:
```bash
git push origin main
# Railway detects push and deploys
```

**Deployment URL:** `https://your-backend.up.railway.app`

#### 2.5 Verify Deployment

```bash
# Health check
curl https://your-backend.up.railway.app/health

# API docs
open https://your-backend.up.railway.app/api/v1/docs
```

---

### Option B: Render

1. Visit https://render.com
2. **New Web Service** → Connect GitHub
3. Select backend directory
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add same variables as Railway

---

### Option C: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Initialize app
cd backend
fly launch

# Set environment variables
fly secrets set DATABASE_URL="..." BETTER_AUTH_SECRET="..."

# Deploy
fly deploy
```

---

## Part 3: Frontend Deployment (Vercel)

### 3.1 Create Vercel Account

```bash
# Visit https://vercel.com
# Sign up with GitHub
```

### 3.2 Deploy Frontend

1. **New Project** → **Import Git Repository**
2. Select `frontend/` directory as root
3. Vercel auto-detects Next.js

### 3.3 Configure Environment Variables

In Vercel dashboard → **Settings** → **Environment Variables**:

```bash
# Backend API URL (from Railway/Render)
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app

# API Version
NEXT_PUBLIC_API_VERSION=v1

# Environment
NEXT_PUBLIC_ENVIRONMENT=production

# Debug
NEXT_PUBLIC_DEBUG=false
```

### 3.4 Deploy

Vercel auto-deploys on push:
```bash
git push origin main
# Vercel builds and deploys
```

**Deployment URL:** `https://your-app.vercel.app`

### 3.5 Update Backend CORS

After frontend deploys, update backend `ALLOWED_ORIGINS`:

**Railway Dashboard:**
```bash
ALLOWED_ORIGINS=["https://your-app.vercel.app"]
```

Redeploy backend for changes to take effect.

---

## Part 4: Custom Domain (Optional)

### 4.1 Backend Domain

**Railway:**
1. Dashboard → **Settings** → **Domains**
2. Add custom domain: `api.yourdomain.com`
3. Add DNS records (Railway provides):
   ```
   CNAME api yourdomain.com → your-backend.up.railway.app
   ```

**Vercel (alternative):**
- Can also deploy backend on Vercel if preferred

### 4.2 Frontend Domain

**Vercel:**
1. Dashboard → **Settings** → **Domains**
2. Add domain: `yourdomain.com`
3. Add DNS records:
   ```
   A @ 76.76.21.21
   CNAME www cname.vercel-dns.com
   ```

### 4.3 Update Environment Variables

After adding custom domains:

**Backend:**
```bash
ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

**Frontend:**
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## Part 5: Monitoring & Observability

### 5.1 Setup Sentry (Error Tracking)

```bash
# Visit https://sentry.io
# Create account and new project

# Get DSN
# Project Settings → Client Keys (DSN)
```

**Add to backend env:**
```bash
SENTRY_DSN=https://abc123@o123.ingest.sentry.io/456
```

### 5.2 Setup Logging

**Railway/Render:**
- Built-in logs in dashboard
- Search, filter, download logs

**Advanced:** Consider log aggregation:
- Datadog
- LogDNA
- Papertrail

### 5.3 Uptime Monitoring

**Free options:**
- **UptimeRobot**: https://uptimerobot.com
- **Pingdom**: https://pingdom.com
- **StatusCake**: https://statuscake.com

**Setup:**
1. Add health check endpoint: `https://api.yourdomain.com/health`
2. Set check interval: 5 minutes
3. Configure alerts (email/SMS)

---

## Part 6: CI/CD Pipeline

### 6.1 GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install uv
          uv sync
      - name: Run tests
        run: |
          cd backend
          uv run pytest tests/
      - name: Type check
        run: |
          cd backend
          uv run mypy src/
      - name: Lint
        run: |
          cd backend
          uv run ruff check src/

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install -g pnpm
          pnpm install
      - name: Type check
        run: |
          cd frontend
          pnpm type-check
      - name: Build
        run: |
          cd frontend
          pnpm build

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy notification
        run: echo "Tests passed! Railway/Vercel auto-deploys"
```

### 6.2 Auto-Deploy Flow

1. Push to `main` branch
2. GitHub Actions runs tests
3. If tests pass, Railway/Vercel auto-deploy
4. Monitor deployment in platform dashboards
5. Verify health checks

---

## Part 7: Database Backups

### 7.1 Automated Backups (Neon)

**Neon provides:**
- Automatic backups every 24 hours
- 7-day retention (free tier)
- 30-day retention (paid plans)
- Point-in-time recovery

### 7.2 Manual Backups

```bash
# Scheduled backup (cron)
0 2 * * * cd /app/backend && ./scripts/backup-database.sh >> /var/log/backup.log 2>&1

# Upload to S3
aws s3 cp backups/ s3://my-bucket/backups/ --recursive
```

### 7.3 Backup Verification

```bash
# Test restore in staging environment
DATABASE_URL=$STAGING_DATABASE_URL ./scripts/restore-database.sh backups/latest.sql.gz
```

---

## Part 8: Security Hardening

### 8.1 Environment Variables

✅ **Do:**
- Use platform secret management (Railway Secrets, Vercel Env Vars)
- Generate unique secrets for production
- Rotate secrets every 90 days
- Never commit secrets to git

❌ **Don't:**
- Use development secrets in production
- Share secrets in chat/email
- Store secrets in plaintext files

### 8.2 CORS Configuration

```bash
# Backend - Only allow production frontend
ALLOWED_ORIGINS=["https://yourdomain.com"]

# Never use wildcard in production
ALLOWED_ORIGINS=["*"]  # ❌ INSECURE
```

### 8.3 HTTPS/SSL

- ✅ Railway/Vercel provide automatic SSL
- ✅ Force HTTPS redirects (enabled by default)
- ✅ HSTS headers (Vercel auto-includes)

### 8.4 Rate Limiting

Add rate limiting middleware (Phase IV):
```python
# backend/src/middleware/rate_limit.py
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/tasks")
@limiter.limit("100/minute")
async def list_tasks():
    ...
```

---

## Part 9: Performance Optimization

### 9.1 Database Connection Pooling

Already configured in `backend/src/db/database.py`:
```python
engine = create_engine(
    settings.database_url,
    pool_size=5,          # Max connections
    max_overflow=10,      # Extra connections when busy
    pool_pre_ping=True,   # Verify connection health
)
```

### 9.2 Frontend Caching

Vercel automatic:
- Static assets: Cached forever
- API routes: Custom cache headers
- Build cache: Speeds up deployments

### 9.3 Database Query Optimization

- ✅ Composite indexes already in place
- ✅ Query only needed fields
- Monitor slow queries in Neon dashboard

---

## Part 10: Troubleshooting

### Issue: 502 Bad Gateway (Backend)

**Cause:** Backend not responding

**Fix:**
```bash
# Check logs in Railway dashboard
# Verify DATABASE_URL is correct
# Ensure migrations ran: alembic upgrade head
```

### Issue: CORS Error (Frontend)

**Cause:** Backend ALLOWED_ORIGINS not set

**Fix:**
```bash
# Railway → Environment Variables
ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]
```

### Issue: Build Fails

**Backend:**
```bash
# Check Python version (3.11+)
# Verify pyproject.toml dependencies
# Check build logs in Railway
```

**Frontend:**
```bash
# Check Node version (18+)
# Verify package.json
# Check Vercel build logs
```

### Issue: Database Connection Timeout

**Cause:** Neon database sleeping (free tier)

**Fix:**
- First connection takes 5-10 seconds
- Upgrade to paid plan for always-on
- Or accept cold start delay

---

## Part 11: Cost Estimates

### Free Tier (Recommended for MVP)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Neon** | Free | 0.25 vCPU, 3 projects, 10 branches |
| **Railway** | $5 credit/month | ~500 hours runtime |
| **Vercel** | Free | 100 GB bandwidth, unlimited deploys |
| **Sentry** | Free | 5,000 errors/month |
| **GitHub** | Free | Unlimited public repos, 2000 min CI |

**Total: $0 - $5/month** (can run entirely free with Railway credit)

### Paid Tier (Production Scale)

| Service | Cost | Features |
|---------|------|----------|
| **Neon** | $19/month | 2 vCPU, always-on, 30-day backups |
| **Railway** | $20/month | Fixed pricing, more resources |
| **Vercel** | $20/month | Pro plan, team features |
| **Sentry** | $26/month | 50,000 errors, performance |

**Total: ~$85/month** for production-grade infrastructure

---

## Part 12: Launch Checklist

### Pre-Launch

- [ ] All tests passing (`pytest` + frontend tests)
- [ ] Environment variables configured (production values)
- [ ] Database migrations applied
- [ ] CORS configured with production domains
- [ ] Sentry error tracking configured
- [ ] Backup strategy in place
- [ ] Health checks passing
- [ ] SSL/HTTPS enabled
- [ ] Custom domain configured (optional)
- [ ] Monitoring/alerts setup

### Post-Launch

- [ ] Verify user registration works
- [ ] Test task creation/update/delete
- [ ] Monitor error rates in Sentry
- [ ] Check performance (< 2s page loads)
- [ ] Review logs for errors
- [ ] Test on mobile devices
- [ ] Share with beta users
- [ ] Monitor uptime (UptimeRobot)

---

## Part 13: Scaling Considerations

### When to Scale

**Scale backend when:**
- Response times > 2 seconds consistently
- CPU usage > 80% for extended periods
- Memory usage approaching limits

**Scale database when:**
- Query times > 500ms
- Connection pool exhausted
- Storage > 1 GB (Neon free tier limit)

### Scaling Options

**Backend:**
- Railway: Upgrade compute size ($5 → $20/month)
- Add caching layer (Redis)
- Horizontal scaling (multiple instances)

**Database:**
- Neon: Upgrade to always-on ($19/month)
- Add read replicas
- Optimize queries further

**Frontend:**
- Vercel auto-scales (no action needed)
- Add CDN for static assets (Cloudflare)
- Implement service worker for offline support

---

## Support & Resources

### Documentation
- **Backend**: `../backend/README.md`
- **Frontend**: `../frontend/README.md`
- **Database**: `../backend/docs/database-performance.md`
- **Backups**: `../backend/docs/backup-restore.md`

### Platform Docs
- Railway: https://docs.railway.app
- Vercel: https://vercel.com/docs
- Neon: https://neon.tech/docs

### Community
- GitHub Issues
- Discord (if available)
- Email support (if available)

---

**Deployment Complete!** 🎉

Your Todo application is now live in production.

**Next Steps:**
- Share with users
- Monitor performance
- Iterate based on feedback
- Plan Phase IV features
