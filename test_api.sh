#!/bin/bash
# Test MongoDB connection via API

echo "Testing MongoDB connection..."
echo "1. Testing home page:"
curl -s http://localhost:8000/ | head -5

echo -e "\n\n2. Testing MongoDB connection endpoint:"
curl -s http://localhost:8000/api/test-connection/ | python -m json.tool

echo -e "\n\n3. Testing users endpoint:"
curl -s http://localhost:8000/api/users/ | python -m json.tool

echo -e "\n\n4. Testing analytics endpoint:"
curl -s http://localhost:8000/api/analytics/ | python -m json.tool