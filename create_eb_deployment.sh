#!/bin/bash

# AWS Elastic Beanstalk Deployment Package Creator
# Universidad de los Andes - MISW4304
# Blacklist Microservice

echo "🚀 Creating AWS Elastic Beanstalk deployment package..."

# Set variables
PACKAGE_NAME="blacklist-microservice-eb-deployment"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FINAL_PACKAGE="${PACKAGE_NAME}_${TIMESTAMP}.zip"

# Change to the api directory
cd api

# Remove any existing deployment packages
echo "🧹 Cleaning up old deployment packages..."
rm -f ../${PACKAGE_NAME}*.zip

# Create the deployment package
echo "📦 Creating deployment package: ${FINAL_PACKAGE}"

# Create zip file excluding unnecessary files
zip -r "../${FINAL_PACKAGE}" . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "*.pyo" \
    -x "*.pyd" \
    -x ".git/*" \
    -x ".gitignore" \
    -x "*.log" \
    -x "venv/*" \
    -x ".env" \
    -x "*.sqlite" \
    -x "*.db" \
    -x ".DS_Store" \
    -x "Thumbs.db"

# Go back to parent directory
cd ..

# Check if the package was created successfully
if [ -f "${FINAL_PACKAGE}" ]; then
    echo "✅ Deployment package created successfully: ${FINAL_PACKAGE}"
    echo "📊 Package size: $(du -h ${FINAL_PACKAGE} | cut -f1)"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Go to AWS Elastic Beanstalk Console"
    echo "2. Create a new application or environment"
    echo "3. Upload the file: ${FINAL_PACKAGE}"
    echo "4. Make sure to select Python platform"
    echo "5. Set WSGI path to: application:application"
    echo ""
    echo "📁 Package location: $(pwd)/${FINAL_PACKAGE}"
else
    echo "❌ Error: Failed to create deployment package"
    exit 1
fi
