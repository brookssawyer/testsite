# Deployment Checklist - taketheliveunder.com

Use this checklist to track your deployment progress.

## Pre-Deployment

- [ ] Code is committed and pushed to GitHub (`brookssawyer/testsite`)
- [ ] You have The Odds API key from https://the-odds-api.com
- [ ] You have Railway account (https://railway.app)
- [ ] You have Vercel account (https://vercel.com)
- [ ] You have access to your domain registrar for DNS

## Generate Secrets

- [ ] Run `python generate_secret_key.py` to get SECRET_KEY
- [ ] Save the SECRET_KEY somewhere safe (you'll need it for Railway)

## Railway Backend Deployment

- [ ] Create new Railway project
- [ ] Connect to GitHub repo `brookssawyer/testsite`
- [ ] Add environment variables:
  - [ ] `ODDS_API_KEY` = (your key from the-odds-api.com)
  - [ ] `SECRET_KEY` = (generated from script above)
  - [ ] `USE_KENPOM` = `false`
  - [ ] `SPORT_MODE` = `ncaa`
  - [ ] `ENVIRONMENT` = `production`
  - [ ] `ALLOWED_ORIGINS` = `https://taketheliveunder.com,https://www.taketheliveunder.com`
  - [ ] `LOG_LEVEL` = `INFO`
- [ ] Deployment completes successfully
- [ ] Both processes running (web + worker)
- [ ] Copy Railway URL (e.g., `https://testsite-production-xxx.up.railway.app`)
- [ ] Test health endpoint: `curl https://your-app.railway.app/health`
- [ ] Verify worker logs show "Starting NCAA Basketball Monitor..."

## Vercel Frontend Deployment

- [ ] Create new Vercel project
- [ ] Import from GitHub: `brookssawyer/testsite`
- [ ] Set Root Directory to `frontend`
- [ ] Add environment variable:
  - [ ] `NEXT_PUBLIC_API_URL` = (Railway URL from above)
- [ ] Deploy completes successfully
- [ ] Visit Vercel deployment URL
- [ ] Login page loads
- [ ] Test login with `admin` / `changeme`
- [ ] Dashboard loads (shows "Waiting for games..." or live data)
- [ ] No CORS errors in browser console

## Custom Domain Configuration

- [ ] In Vercel, go to Settings → Domains
- [ ] Add domain: `taketheliveunder.com`
- [ ] Add domain: `www.taketheliveunder.com`
- [ ] Note the DNS records Vercel provides
- [ ] Go to your domain registrar's DNS settings
- [ ] Add A record:
  - Type: `A`
  - Name: `@`
  - Value: (IP from Vercel, usually `76.76.21.21`)
- [ ] Add CNAME record:
  - Type: `CNAME`
  - Name: `www`
  - Value: `cname.vercel-dns.com`
- [ ] Wait 15-30 minutes for DNS propagation
- [ ] Check propagation: https://www.whatsmydns.net
- [ ] Visit `https://taketheliveunder.com`
- [ ] Verify SSL is active (padlock icon)

## Post-Deployment Verification

- [ ] Backend health check works: `https://your-app.railway.app/health`
- [ ] Frontend loads at `https://taketheliveunder.com`
- [ ] Login works with admin/changeme
- [ ] Change admin password immediately
- [ ] Dashboard updates every 30-40 seconds
- [ ] Railway logs show monitor polling for games
- [ ] No CORS errors in browser console
- [ ] Admin panel accessible at `/admin`
- [ ] All features working (triggered games, analytics, etc.)

## Security & Cleanup

- [ ] Admin password changed from default
- [ ] SECRET_KEY is strong and stored securely
- [ ] ODDS_API_KEY not exposed in frontend
- [ ] Railway environment variables double-checked
- [ ] No sensitive data in git repository

## Optional Enhancements

- [ ] Set up monitoring/alerts for Railway app
- [ ] Monitor API usage at the-odds-api.com
- [ ] Consider upgrading The Odds API plan if needed
- [ ] Set up email/SMS alerts for high-confidence triggers
- [ ] Add additional users via admin panel
- [ ] Adjust confidence weights based on performance

## Troubleshooting Resources

If you encounter issues, see:
- **DEPLOYMENT.md** - Full deployment guide with troubleshooting section
- **CLAUDE.md** - Developer documentation
- **Railway logs** - Check both web and worker processes
- **Vercel logs** - Check build and runtime logs
- **Browser console** - Check for CORS or API connection errors

---

**Notes:**

Railway URL (save this): ________________________________

Vercel URL (save this): ________________________________

SECRET_KEY (saved securely): ✓

Domain DNS propagated: ______ (date/time)

Deployment completed: ______ (date/time)
