# Railway Deployment Guide for YapYard

## Prerequisites
- Railway account (https://railway.app)
- GitHub repository with your YapYard code
- Groq API key for testing

## Step-by-Step Deployment

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Docker configuration for Railway deployment"
git push origin main
```

### 2. Deploy on Railway

#### Option A: Railway Dashboard (Recommended)
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your YapYard repository
5. Railway will automatically detect the Dockerfile and deploy

#### Option B: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Add your GitHub repo
railway add

# Deploy
railway up
```

### 3. Configure Environment Variables
In Railway dashboard, go to your project settings and add these environment variables:

**Required:**
- `DEFAULT_USERNAME`: Your chosen username for login
- `DEFAULT_PASSWORD`: Your chosen password for login

**Optional (already set in Dockerfile):**
- `STREAMLIT_SERVER_PORT`: 8501
- `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0
- `STREAMLIT_SERVER_HEADLESS`: true

### 4. Verify Deployment
- Railway will provide you with a public URL
- Visit the URL and test with your login credentials
- Users can then log in with their Groq API keys

## Important Notes

### Port Configuration
Railway automatically assigns a PORT environment variable. The app is configured to use this dynamic port.

### Storage
The app uses DuckDB+Parquet for ChromaDB to avoid SQLite compatibility issues in containerized environments.

### API Keys
- Users provide their own Groq API keys through the login interface
- API keys are stored in session state, not in environment variables or databases
- Each user session is independent

### Scaling
Railway automatically handles scaling based on usage. The free tier includes:
- 500 hours of runtime per month
- 1GB of memory
- Shared CPU

### Troubleshooting

#### Build Issues
- Check Railway build logs for dependency conflicts
- Ensure all required packages are in `requirements.txt`
- Verify Python version compatibility

#### Runtime Issues
- Check application logs in Railway dashboard
- Verify environment variables are set correctly
- Test locally with Docker first: `docker build -t yapyard . && docker run -p 8501:8501 yapyard`

#### Memory Issues
- If you encounter memory issues, consider upgrading your Railway plan
- Monitor memory usage in Railway dashboard

## Security Considerations
- Never commit actual `.env` files with real credentials
- Use Railway's environment variable system for sensitive data
- Regularly update dependencies for security patches

## Custom Domain (Optional)
You can add a custom domain in Railway dashboard under Settings > Domains.

## Support
For Railway-specific issues, check:
- Railway documentation: https://docs.railway.app
- Railway Discord community
- Railway status page: https://status.railway.app