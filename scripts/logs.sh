#!/bin/bash

echo "📋 NILM Container Logs:"
echo "======================="

# Show logs with follow option
docker logs -f nilm-ha
