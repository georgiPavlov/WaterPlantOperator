#!/bin/bash
echo "🌱 Water Plant Automation System Status"
echo "========================================"

# Check WaterPlantApp
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8001/admin/" 2>/dev/null | grep -q "200\|302"; then
    echo "✅ WaterPlantApp (Backend): Running on http://localhost:8001"
else
    echo "❌ WaterPlantApp (Backend): Not responding"
fi

# Check WaterVue
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000/" 2>/dev/null | grep -q "200"; then
    echo "✅ WaterVue (Frontend): Running on http://localhost:3000"
elif curl -s -o /dev/null -w "%{http_code}" "http://localhost:3001/" 2>/dev/null | grep -q "200"; then
    echo "✅ WaterVue (Frontend): Running on http://localhost:3001"
else
    echo "❌ WaterVue (Frontend): Not responding"
fi

# Check WaterPlantOperator
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/" 2>/dev/null | grep -q "200"; then
    echo "✅ WaterPlantOperator (Hardware): Running on http://localhost:8000"
else
    echo "❌ WaterPlantOperator (Hardware): Not responding"
fi

echo ""
echo "🔐 Login Credentials:"
echo "   Username: testuser"
echo "   Password: testpass123"
