#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting Midas Docker Deployment${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
  echo -e "${YELLOW}⚠️  .env file not found. Creating from example...${NC}"
  if [ -f .env.example ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file from example. Please edit it with your configuration.${NC}"
    echo -e "${YELLOW}⚠️  Deployment paused. Edit the .env file and run this script again.${NC}"
    exit 1
  else
    echo -e "${RED}❌ .env.example not found. Please create a .env file manually.${NC}"
    exit 1
  fi
fi

# Build and start using docker-compose
echo -e "${YELLOW}🔨 Building and starting containers with docker-compose...${NC}"
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check if the deployment was successful
if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ Midas deployed successfully!${NC}"
  echo -e "${YELLOW}🌐 Your application is running at: http://localhost:3000${NC}"
  echo -e "${YELLOW}📊 To view logs: docker-compose logs -f${NC}"
  echo -e "${YELLOW}🛑 To stop: docker-compose down${NC}"
else
  echo -e "${RED}❌ Deployment failed. Check the logs for more information.${NC}"
  exit 1
fi 