# Backend Deployment Guide

This guide covers deploying the DMS Dashboard backend to various platforms.

## Quick Start: Railway (Recommended)

Railway is the easiest platform for deploying FastAPI applications.

### Step 1: Prepare Backend Repository

1. Initialize git in the backend folder (if using separate repo):
   ```bash
   cd backend
   git init
   git add .
   git commit -m "Initial backend commit"
   ```

2. Create a new GitHub repository for the backend (optional, can use monorepo)

3. Push to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/dms-backend.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will auto-detect Python

### Step 3: Configure Railway

1. **Root Directory**: Set to `backend` (if using monorepo)
2. **Start Command**: Railway will auto-detect from `Procfile`
   - Or manually set: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables

In Railway project settings → Variables, add:

```bash
# AWS Configuration (REQUIRED)
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-s3-bucket-name

# Security (REQUIRED)
SECRET_KEY=your-secure-random-secret-key-here

# OpenAI (Optional - for chat functionality)
OPENAI_API_KEY=your-openai-api-key

# CORS (REQUIRED - add your Vercel frontend URL)
ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com

# Database (Optional - Railway provides PostgreSQL)
# If using Railway's PostgreSQL, Railway will auto-set DATABASE_URL
# Otherwise, use SQLite (not recommended for production):
# DATABASE_URL=sqlite:///./dms_database.db

# Environment
ENVIRONMENT=production
```

### Step 5: Deploy

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run the start command
- Provide a public URL (e.g., `https://your-app.railway.app`)

### Step 6: Test Backend

```bash
curl https://your-app.railway.app/health
# Should return: {"status":"healthy"}
```

---

## Alternative: Render

### Step 1: Create Web Service

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### Step 2: Configure Service

- **Name**: `dms-backend` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend` (if monorepo)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

Same as Railway (see above)

### Step 4: Deploy

Render will build and deploy automatically. URL format: `https://your-app.onrender.com`

**Note**: Free tier on Render spins down after inactivity. Consider upgrading for production.

---

## Database Options

### Option 1: Railway PostgreSQL (Recommended)

1. In Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically sets `DATABASE_URL` environment variable
4. Update `backend/app/database.py` to use PostgreSQL (already compatible)

### Option 2: Render PostgreSQL

1. In Render dashboard, create "PostgreSQL" database
2. Copy the "Internal Database URL"
3. Add as `DATABASE_URL` environment variable

### Option 3: SQLite (Not Recommended for Production)

- Works for development/testing
- Not suitable for production (file system limitations)
- Use only if no database service available

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key for Textract | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_S3_BUCKET` | S3 bucket name | `dms-documents` |
| `SECRET_KEY` | Application secret (generate random string) | `your-secret-key-here` |
| `ALLOWED_ORIGINS` | Comma-separated frontend URLs | `https://app.vercel.app` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | For chat functionality | (empty) |
| `DATABASE_URL` | Database connection string | `sqlite:///./dms_database.db` |
| `ENVIRONMENT` | Environment name | `development` |
| `UPLOAD_DIR` | Upload directory | `./uploads` |
| `MAX_FILE_SIZE` | Max file size in bytes | `10485760` (10MB) |

---

## Updating CORS for Production

After deploying frontend, update backend `ALLOWED_ORIGINS`:

```bash
# In Railway/Render environment variables:
ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
```

Or in `.env` file (if using file-based config):
```
ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## Testing Deployment

### 1. Health Check

```bash
curl https://your-backend-url.com/health
# Expected: {"status":"healthy"}
```

### 2. API Root

```bash
curl https://your-backend-url.com/
# Expected: {"message":"DMS Dashboard API","version":"1.0.0"}
```

### 3. Test CORS

Open browser console on your frontend and check for CORS errors when making API calls.

---

## Troubleshooting

### Backend won't start

- Check Railway/Render logs
- Verify all required environment variables are set
- Check `requirements.txt` is correct
- Ensure `Procfile` or start command is correct

### CORS errors

- Verify `ALLOWED_ORIGINS` includes your frontend URL
- Check for trailing slashes (should match exactly)
- Restart backend after updating CORS

### Database errors

- Verify `DATABASE_URL` is set correctly
- For PostgreSQL, check connection string format
- Ensure database is accessible from deployment platform

### AWS Textract errors

- Verify AWS credentials are correct
- Check S3 bucket exists and is accessible
- Verify IAM permissions for Textract and S3

---

## Production Checklist

- [ ] All environment variables set
- [ ] CORS configured with frontend URL
- [ ] Database configured (PostgreSQL recommended)
- [ ] AWS credentials configured
- [ ] Health check endpoint working
- [ ] Frontend can connect to backend
- [ ] File uploads working
- [ ] PDF processing working
- [ ] Alerts generating correctly

---

## Next Steps

1. Deploy backend and get URL
2. Update frontend `NEXT_PUBLIC_API_BASE_URL` in Vercel
3. Test end-to-end functionality
4. Set up monitoring (optional)
5. Configure custom domain (optional)

