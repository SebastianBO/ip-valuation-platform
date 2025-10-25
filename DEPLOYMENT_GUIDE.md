# 🚀 Deployment Guide

Your IP Valuation Platform can be deployed publicly in several ways. Here are the best options:

---

## ✅ Option 1: Streamlit Community Cloud (RECOMMENDED - FREE!)

**Best for:** Streamlit apps (like this one)
**Cost:** FREE
**Time:** 5 minutes
**URL:** Custom subdomain (e.g., `ip-valuation.streamlit.app`)

### Step 1: Create GitHub Repository

```bash
# Navigate to your project
cd /Users/sebastianbenzianolsson/Developer/ipsegmentation

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - IP Valuation Platform"

# Create GitHub repo (via gh CLI or web)
gh repo create ip-valuation-platform --public --source=. --remote=origin --push
```

Or manually:
1. Go to https://github.com/new
2. Create new repository: `ip-valuation-platform`
3. Follow the instructions to push

```bash
git remote add origin https://github.com/YOUR_USERNAME/ip-valuation-platform.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io

2. **Sign in** with GitHub

3. **Click "New app"**

4. **Fill in:**
   - Repository: `YOUR_USERNAME/ip-valuation-platform`
   - Branch: `main`
   - Main file path: `app.py`

5. **Click "Deploy"**

6. **Wait 2-3 minutes** for deployment

7. **Your app will be live at:**
   ```
   https://YOUR_USERNAME-ip-valuation-platform.streamlit.app
   ```

### Step 3: Add API Key (Secret)

1. In Streamlit Cloud dashboard, click **"⚙️ Settings"**

2. Go to **"Secrets"**

3. Add:
   ```toml
   FINANCIAL_DATASETS_API_KEY = "0a799aee-ff2b-40a2-903c-f8737226d148"
   ```

4. Click **"Save"**

5. App will automatically restart with the secret

### Step 4: Update App to Use Secrets

Modify `app.py`:

```python
import streamlit as st

# Try to get API key from secrets, fallback to input
try:
    default_api_key = st.secrets.get("FINANCIAL_DATASETS_API_KEY", "")
except:
    default_api_key = ""

api_key = st.text_input(
    "Financial Datasets API Key",
    value=default_api_key,
    type="password",
    help="Get your API key from financialdatasets.ai"
)
```

**Done! Your app is now live and public!** 🎉

---

## Option 2: Railway (Alternative - Also Great!)

**Best for:** Python apps with databases
**Cost:** $5/month (free trial available)
**Time:** 10 minutes
**URL:** Custom domain supported

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Deploy

```bash
# Login
railway login

# Initialize project
railway init

# Add environment variable
railway variables set FINANCIAL_DATASETS_API_KEY=0a799aee-ff2b-40a2-903c-f8737226d148

# Deploy
railway up
```

### Step 3: Configure

Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0",
    "healthcheckPath": "/_stcore/health"
  }
}
```

**Your app will be live at:** `https://your-app.railway.app`

---

## Option 3: Render (Another Good Option)

**Best for:** Static sites, web services
**Cost:** FREE tier available
**Time:** 10 minutes

### Step 1: Create `render.yaml`

```yaml
services:
  - type: web
    name: ip-valuation-platform
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
    envVars:
      - key: FINANCIAL_DATASETS_API_KEY
        value: 0a799aee-ff2b-40a2-903c-f8737226d148
```

### Step 2: Deploy

1. Go to https://render.com
2. Connect GitHub repository
3. Select "Web Service"
4. Choose your repo
5. Click "Create Web Service"

**Your app will be live at:** `https://your-app.onrender.com`

---

## 🚫 Why Not Vercel?

Vercel is designed for:
- ✅ Next.js applications
- ✅ Static sites
- ✅ Serverless functions (short-lived)

Streamlit needs:
- ❌ Persistent Python server (long-running)
- ❌ WebSocket connections
- ❌ Stateful sessions

**Vercel's serverless architecture can't maintain persistent WebSocket connections that Streamlit requires.**

### Workaround (Not Recommended)

If you MUST use Vercel, you'd need to:

1. **Convert to Next.js** - Rebuild entire UI in React
2. **Use Vercel Functions** - API routes for calculations
3. **Separate backend** - Deploy Streamlit separately, Vercel as frontend

This defeats the purpose. **Use Streamlit Cloud instead!**

---

## 🎯 Recommended: Streamlit Cloud

Here's why Streamlit Cloud is the best choice:

### ✅ Pros
- **FREE** for public apps
- **Perfect** for Streamlit (duh!)
- **Auto-deploy** on git push
- **Secrets management** built-in
- **Custom subdomain** included
- **SSL certificate** automatic
- **No configuration** needed
- **Community support**

### ❌ Cons
- Must be public (or pay for private)
- Limited resources on free tier
- Streamlit subdomain (can't use custom domain on free tier)

### Comparison

| Feature | Streamlit Cloud | Railway | Render | Vercel |
|---------|----------------|---------|--------|--------|
| **Cost** | FREE | $5/mo | FREE tier | Not suitable |
| **Setup Time** | 5 min | 10 min | 10 min | Days (rebuild) |
| **Custom Domain** | No (free) | Yes | Yes | N/A |
| **Auto Deploy** | Yes | Yes | Yes | N/A |
| **Best For** | Streamlit | Python apps | All apps | Next.js |

---

## 🚀 Quick Start: Deploy in 5 Minutes

### The Fastest Way:

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy IP Valuation Platform"
git push

# 2. Go to https://share.streamlit.io

# 3. Click "New app", select your repo

# 4. Add API key to secrets

# 5. Done! ✨
```

**Your app is now public and accessible worldwide!**

Share the URL with:
- Investors
- Team members
- Clients
- Anyone interested in IP valuation

---

## 📊 Performance Tips for Public Deployment

### 1. Add Caching

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_segment_data(ticker):
    return engine.prepare_segment_financials(ticker)
```

### 2. Optimize API Calls

```python
# Don't call API multiple times for same data
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = fetch_data(ticker)
```

### 3. Add Loading States

```python
with st.spinner("Analyzing company..."):
    # Long-running operations
    results = analyze_company(ticker)
```

### 4. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=10):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator
```

---

## 🔒 Security Best Practices

### 1. Never Commit Secrets

```bash
# Add to .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Use Streamlit Secrets

```python
# In production
api_key = st.secrets["FINANCIAL_DATASETS_API_KEY"]

# In development (fallback)
api_key = st.text_input("API Key", type="password")
```

### 3. Validate Input

```python
def validate_ticker(ticker):
    if not ticker or len(ticker) > 5:
        st.error("Invalid ticker symbol")
        return False
    return True
```

### 4. Handle Errors Gracefully

```python
try:
    result = analyze_company(ticker)
except Exception as e:
    st.error(f"Analysis failed: {str(e)}")
    st.info("Please try a different ticker")
```

---

## 📈 Monitoring Your Deployed App

### Streamlit Cloud Dashboard

Shows:
- **Uptime** - Is app running?
- **Resource usage** - CPU, memory
- **Logs** - Error messages
- **Visitors** - Traffic stats (paid tier)

### Add Analytics

```python
# Add Google Analytics
import streamlit.components.v1 as components

components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
""", height=0)
```

---

## 🎉 You're Ready to Deploy!

Choose your deployment method:

1. **Easiest:** Streamlit Cloud (5 minutes)
2. **More control:** Railway ($5/month)
3. **Alternative:** Render (free tier)

Follow the steps above and your IP Valuation Platform will be live!

---

## Need Help?

- **Streamlit Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs

**Questions? Issues? Let me know!** 🚀
