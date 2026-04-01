#!/bin/bash
# Quick Deploy to Render using Render API

echo "=========================================="
echo "  Deploying to Render..."
echo "=========================================="

# Check for Render API token
if [ -z "$RENDER_API_TOKEN" ]; then
    echo "Error: RENDER_API_TOKEN not set"
    echo ""
    echo "To get your Render API token:"
    echo "1. Go to https://dashboard.render.com/api-keys"
    echo "2. Click 'Create API Key'"
    echo "3. Copy the token"
    echo "4. Run: export RENDER_API_TOKEN='your-token-here'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Get the Blueprint spec
BLUEPRINT=$(cat <<'EOF'
{
  "name": "dropshipping-api",
  "region": "singapore",
  "serviceType": "web_service",
  "envVars": [
    {"key": "PYTHON_VERSION", "value": "3.11"},
    {"key": "BUILD_COMMAND", "value": "pip install -r requirements.txt"},
    {"key": "START_COMMAND", "value": "uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT"}
  ]
}
EOF
)

# Create or update the service
echo "Creating web service..."

RESPONSE=$(curl -s -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$BLUEPRINT")

# Check if service was created
if echo "$RESPONSE" | grep -q "id"; then
    SERVICE_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "Service created: $SERVICE_ID"
else
    echo "Response: $RESPONSE"
fi

echo ""
echo "=========================================="
echo "  Deployment triggered!"
echo "=========================================="
echo ""
echo "Check deployment status at:"
echo "https://dashboard.render.com"
