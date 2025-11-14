# Deployment Guide - Take The Live Under

This guide will walk you through deploying the NCAA Basketball Betting Monitor to production.

**Target Setup:**
- Backend: Railway (FastAPI + Monitor Worker)
- Frontend: Vercel (Next.js)
- Domain: taketheliveunder.com

---

## Prerequisites

1. GitHub repository: `github.com/brookssawyer/testsite`
2. The Odds API key from https://the-odds-api.com
3. Railway account (https://railway.app)
4. Vercel account (https://vercel.com)
5. Domain registrar access for DNS configuration

---

## Part 1: Backend Deployment (Railway)

### Step 1: Create Railway Project

1. Go to https://railway.app and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `brookssawyer/testsite`
5. Railway will automatically detect the Procfile

### Step 2: Configure Environment Variables

In the Railway dashboard, go to your project settings and add these environment variables:

```bash
# Required API Key
ODDS_API_KEY=<your-odds-api-key-from-the-odds-api.com>

# Security - Generate a strong random string
SECRET_KEY=<generate-with-command-below>

# Data Source Configuration
USE_KENPOM=false

# Sport Mode
SPORT_MODE=ncaa

# Environment
ENVIRONMENT=production

# CORS - Include your domain
ALLOWED_ORIGINS=https://taketheliveunder.com,https://www.taketheliveunder.com

# Logging
LOG_LEVEL=INFO
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use this online: https://randomkeygen.com/

### Step 3: Verify Deployment

1. Railway will automatically deploy your app
2. Both processes should be running:
   - **web**: FastAPI server (handles API requests)
   - **worker**: Monitor script (polls for games every 30-40 seconds)

3. Check the deployment logs:
   - Look for "Uvicorn running on..." (web process)
   - Look for "Starting NCAA Basketball Monitor..." (worker process)

4. Get your Railway URL:
   - Go to Settings → Domains
   - Copy the Railway-provided URL (e.g., `https://testsite-production.up.railway.app`)
   - OR add a custom domain if you prefer

### Step 4: Test the Backend

```bash
# Health check
curl https://your-app.railway.app/health

# Expected response:
# {"status":"healthy","environment":"production"}
```

### Step 5: Verify Monitor is Running

Check the Railway logs for the worker process. You should see:
- "Starting NCAA Basketball Monitor..."
- "Fetching live games..."
- Poll updates every 30-40 seconds

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Project

1. Go to https://vercel.com and sign in
2. Click "Add New Project"
3. Import `brookssawyer/testsite` from GitHub
4. **IMPORTANT**: Set Root Directory to `frontend`
   - Click "Edit" next to Root Directory
   - Enter: `frontend`

### Step 2: Configure Environment Variables

In the Vercel project settings, add:

```bash
NEXT_PUBLIC_API_URL=https://your-app-name.railway.app
```

**Replace `your-app-name.railway.app` with your actual Railway URL from Part 1, Step 3.**

### Step 3: Deploy

1. Click "Deploy"
2. Vercel will build and deploy your Next.js app
3. Wait for deployment to complete (usually 2-3 minutes)

### Step 4: Test the Frontend

1. Click the deployment URL from Vercel (e.g., `https://testsite.vercel.app`)
2. You should see the login page
3. Try logging in with default credentials:
   - Username: `admin`
   - Password: `changeme`
4. **IMPORTANT**: Change the admin password immediately after first login!

---

## Part 3: Custom Domain Configuration

### Step 1: Add Domain to Vercel

1. In your Vercel project, go to Settings → Domains
2. Add `taketheliveunder.com`
3. Add `www.taketheliveunder.com` (will redirect to main domain)
4. Vercel will provide DNS records to configure

### Step 2: Configure DNS at Your Registrar

You'll need to add these DNS records (Vercel will show you the exact values):

**For root domain (taketheliveunder.com):**
- Type: `A`
- Name: `@`
- Value: `76.76.21.21` (Vercel's IP)

**For www subdomain:**
- Type: `CNAME`
- Name: `www`
- Value: `cname.vercel-dns.com`

**Exact values will be shown in Vercel dashboard.**

### Step 3: Wait for DNS Propagation

- DNS changes can take 5 minutes to 48 hours
- Usually completes within 15-30 minutes
- Check status at: https://www.whatsmydns.net

### Step 4: SSL Certificate

- Vercel automatically provisions SSL certificates
- Once DNS propagates, SSL will be active
- Your site will be accessible via `https://taketheliveunder.com`

---

## Part 4: Post-Deployment Verification

### Checklist

- [ ] Backend health check responds: `curl https://your-app.railway.app/health`
- [ ] Railway logs show both web and worker processes running
- [ ] Monitor worker is polling for games (check logs)
- [ ] Frontend loads at Vercel URL
- [ ] Login works with admin/changeme
- [ ] Custom domain resolves to Vercel
- [ ] SSL certificate is active (https works)
- [ ] Frontend can connect to backend (check browser console for errors)
- [ ] Dashboard shows "Waiting for games..." or live game data
- [ ] No CORS errors in browser console

### Test API Connection

Open browser console on your frontend and run:
```javascript
fetch('https://your-app.railway.app/health')
  .then(r => r.json())
  .then(console.log)
```

Should return: `{status: "healthy", environment: "production"}`

---

## Part 5: Security & Maintenance

### Change Default Password

1. Log in with admin/changeme
2. Go to Admin Panel
3. Change password immediately

### Monitor Application Logs

**Railway:**
- Dashboard → Deployments → View Logs
- Monitor both web and worker processes
- Look for errors or API rate limit warnings

**Vercel:**
- Dashboard → Deployments → Functions
- Check for build errors or runtime issues

### API Rate Limits

The Odds API has rate limits based on your plan:
- Free tier: Limited requests per month
- Monitor usage at: https://the-odds-api.com/account

If you run out of requests, the monitor will log errors but won't crash.

### Costs

**Railway:**
- $5/month for 500 hours execution time
- This covers both processes running 24/7

**Vercel:**
- Free tier includes:
  - 100 GB bandwidth
  - Unlimited websites
  - Automatic SSL

**The Odds API:**
- Check your plan at the-odds-api.com
- Free tier may have limited requests

### Data Storage

All data is stored in CSV files:
- `data/ncaa_live_log.csv` - All polls
- `data/ncaa_results.csv` - Game results
- `data/users.json` - User accounts

Railway automatically persists these files in the deployment.

---

## Troubleshooting

### Frontend can't connect to backend

1. Check CORS configuration in Railway:
   - Verify `ALLOWED_ORIGINS` includes your domain
   - Format: `https://taketheliveunder.com,https://www.taketheliveunder.com`

2. Check Vercel environment variable:
   - `NEXT_PUBLIC_API_URL` must match Railway URL exactly
   - Must include `https://`

3. Redeploy frontend after changing env vars:
   - Vercel → Deployments → Redeploy

### Monitor not polling

1. Check Railway logs for worker process
2. Verify `ODDS_API_KEY` is set correctly
3. Check API quota at the-odds-api.com
4. Look for errors in logs

### Domain not resolving

1. Wait longer (DNS propagation can take time)
2. Check DNS records are correct in registrar
3. Use https://www.whatsmydns.net to check propagation
4. Verify you added both A and CNAME records

### SSL certificate not working

1. Wait for DNS to fully propagate first
2. Vercel will auto-provision SSL once DNS is ready
3. Check Vercel dashboard for SSL status
4. May take 15-30 minutes after DNS propagates

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `ODDS_API_KEY` | Yes | `abc123...` | From the-odds-api.com |
| `SECRET_KEY` | Yes | `random-string-32-chars` | For JWT tokens |
| `USE_KENPOM` | No | `false` | Use KenPom (paid) or ESPN (free) |
| `SPORT_MODE` | No | `ncaa` | `ncaa` or `nba` for testing |
| `ENVIRONMENT` | No | `production` | Environment mode |
| `ALLOWED_ORIGINS` | Yes | `https://taketheliveunder.com` | CORS domains (comma-separated) |
| `LOG_LEVEL` | No | `INFO` | Logging level |

### Frontend (Vercel)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | `https://yourapp.railway.app` | Backend URL |

---

## Next Steps After Deployment

1. **Change admin password** - First priority!
2. **Monitor the first few games** - Verify confidence scoring works
3. **Adjust confidence weights** if needed (Admin Panel)
4. **Set up monitoring** - Check logs daily initially
5. **Track performance** - Use the analytics dashboard
6. **Consider alerts** - Add email/SMS notifications (see CLAUDE.md for ideas)

---

## Support & Documentation

- **Main documentation**: See `CLAUDE.md`
- **API documentation**: Visit `https://your-app.railway.app/docs` (FastAPI auto-docs)
- **Railway docs**: https://docs.railway.app
- **Vercel docs**: https://vercel.com/docs
- **The Odds API docs**: https://the-odds-api.com/liveapi/guides/v4/

---

## Quick Reference Commands

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Test backend health
curl https://your-app.railway.app/health

# Test frontend API connection (browser console)
fetch('https://your-app.railway.app/health').then(r => r.json()).then(console.log)

# Check DNS propagation
# Visit: https://www.whatsmydns.net

# Force Vercel redeploy (after env var changes)
# Vercel Dashboard → Deployments → Three dots → Redeploy
```

---

**Deployment Complete!** Your betting tracker should now be live at `https://taketheliveunder.com`

Remember to monitor logs and performance for the first few days to ensure everything is working correctly.
