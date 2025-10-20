# AWS Elastic Beanstalk Deployment Guide
## Blacklist Microservice - Universidad de los Andes MISW4304

### 🎯 Overview
This guide will help you deploy your Flask blacklist microservice to AWS Elastic Beanstalk following the best practices from the article you shared.

### 📁 Project Structure
Your application is now properly structured for AWS EB deployment:

```
api/
├── application.py          # Main entry point (required by EB)
├── requirements.txt        # Python dependencies
├── .ebextensions/         # EB configuration
│   └── python.config      # WSGI and Python settings
└── src/                   # Your application source code
    ├── app.py
    ├── config/
    ├── models/
    ├── routes/
    └── services/
```

### 🚀 Deployment Steps

#### Step 1: Create Deployment Package
Run the deployment script to create a zip file:

```bash
./create_eb_deployment.sh
```

This will create a timestamped zip file like: `blacklist-microservice-eb-deployment_20250119_143022.zip`

#### Step 2: AWS Elastic Beanstalk Setup

1. **Go to AWS Console** → Elastic Beanstalk
2. **Create Application**:
   - Application name: `blacklist-microservice`
   - Environment name: `blacklist-microservice-prod` (or your preferred name)
   - Domain: Choose an available domain or use the default

3. **Platform Configuration**:
   - Platform: `Python`
   - Platform branch: `Python 3.9` (or latest available)
   - Platform version: Use the recommended version

4. **Application Code**:
   - Select "Upload your code"
   - Choose the zip file created in Step 1
   - Version label: `v1.0` (or your version)

5. **Configuration**:
   - WSGI path: `application:application` ⚠️ **IMPORTANT**
   - Environment variables: Add any required environment variables

#### Step 3: Environment Variables
Make sure to set these environment variables in EB:

- `DATABASE_URL`: Your PostgreSQL connection string
- `JWT_SECRET_KEY`: Your JWT secret key
- Any other environment variables your app needs

#### Step 4: Deploy
Click "Create application" and wait for the deployment to complete.

### 🔧 Key Configuration Files

#### `.ebextensions/python.config`
```yaml
option_settings:
  "aws:elasticbeanstalk:container:python":
    WSGIPath: application:application
  "aws:elasticbeanstalk:application:environment":
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  "aws:elasticbeanstalk:container:python:gunicorn":
    timeout: 120
    max_requests: 1000
    max_requests_jitter: 100
```

#### `application.py`
- Creates the Flask `application` object (required by EB)
- Includes fallback routes for health checks
- Properly configures logging

### 🧪 Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check**: `GET https://your-app.region.elasticbeanstalk.com/blacklists/ping`
   - Should return: `pong`

2. **Add to Blacklist**: `POST https://your-app.region.elasticbeanstalk.com/blacklists`
   - Requires Authorization header with JWT token
   - Body: `{"email": "test@example.com"}`

3. **Check Blacklist**: `GET https://your-app.region.elasticbeanstalk.com/blacklists/test@example.com`
   - Requires Authorization header with JWT token

### 🐛 Troubleshooting

#### Common Issues:

1. **"Unable to import module 'application'"**
   - ✅ **Fixed**: We created `application.py` in the root directory

2. **"WSGI path not found"**
   - ✅ **Fixed**: We created `.ebextensions/python.config` with correct WSGI path

3. **Database Connection Issues**
   - Check your `DATABASE_URL` environment variable
   - Ensure your RDS instance allows connections from EB security group

4. **Import Errors**
   - ✅ **Fixed**: We added proper Python path configuration in `application.py`

#### Viewing Logs:
1. Go to your EB environment
2. Click "Logs" → "Request Logs" → "Last 100 Lines"
3. Click "Download" to see detailed logs

### 💰 Cost Management
**Important**: Remember to delete your EB environment when you're done testing to avoid charges!

### 🔄 Updates and Redeployment
To update your application:
1. Make your code changes
2. Run `./create_eb_deployment.sh` to create a new zip
3. Go to EB → Upload and Deploy → Choose the new zip file

### 📋 Checklist Before Deployment
- [x] `application.py` created in root directory
- [x] `.ebextensions/python.config` created with correct WSGI path
- [x] `requirements.txt` includes all dependencies
- [x] Application tested locally
- [x] Deployment script created
- [ ] Environment variables configured in EB
- [ ] Database connection tested
- [ ] Security groups configured (if using RDS)

### 🎉 Success!
Your Flask application is now ready for AWS Elastic Beanstalk deployment! The setup follows all the best practices from the article you shared, including:

- ✅ Proper file naming (`application.py`)
- ✅ Correct Flask object naming (`application`)
- ✅ WSGI configuration
- ✅ Requirements.txt with all dependencies
- ✅ EB extensions for configuration

Happy deploying! 🚀
