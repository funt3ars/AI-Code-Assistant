#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check Python version
check_python_version() {
    local version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ $major -lt 3 ] || ([ $major -eq 3 ] && [ $minor -lt 8 ]); then
        echo -e "${RED}Python version $version is not supported. Please install Python 3.8 or higher.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Python version $version is supported.${NC}"
}

# Function to verify package installation
verify_package() {
    local package=$1
    if ! pip show $package &> /dev/null; then
        echo -e "${RED}Package $package is not installed correctly.${NC}"
        return 1
    fi
    echo -e "${GREEN}Package $package verified.${NC}"
    return 0
}

# Function to verify tools
verify_tools() {
    echo -e "${YELLOW}Verifying tools...${NC}"
    
    # Verify web scraping tool
    if [ ! -f "tools/web_scraper.py" ]; then
        echo -e "${RED}Web scraping tool not found.${NC}"
        return 1
    fi
    
    # Verify search engine tool
    if [ ! -f "tools/search_engine.py" ]; then
        echo -e "${RED}Search engine tool not found.${NC}"
        return 1
    fi
    
    # Verify LLM tool
    if [ ! -f "tools/llm_api.py" ]; then
        echo -e "${RED}LLM tool not found.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}All tools verified.${NC}"
    return 0
}

# Function to cleanup
cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    if [ -d "devin-venv" ]; then
        rm -rf devin-venv
        echo -e "${GREEN}Virtual environment removed.${NC}"
    fi
}

# Function to install dependencies with progress
install_dependencies() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    
    # Upgrade pip first
    python -m pip install --upgrade pip
    
    # Install wheel and setuptools first
    pip install --upgrade wheel setuptools

    # Install dependencies with optimizations
    pip install --no-cache-dir --only-binary :all: --prefer-binary -r devin-requirements.txt

    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install some dependencies. Please check the error messages above.${NC}"
        return 1
    fi
    
    return 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cleanup)
            cleanup
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}Setting up Devin-like AI Assistant integration...${NC}"

# Check if Python is installed and version is correct
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is required but not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

check_python_version

# Activate virtual environment (create if it doesn't exist)
if [ ! -d "devin-venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv devin-venv
fi

# Activate the virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source devin-venv/bin/activate

# Install dependencies with better error handling
install_dependencies || exit 1

# Verify key package installations
echo -e "${YELLOW}Verifying package installations...${NC}"
verify_package playwright || exit 1
verify_package duckduckgo-search || exit 1
verify_package openai || exit 1
verify_package anthropic || exit 1

# Install Playwright
echo -e "${YELLOW}Installing Playwright's Chromium browser...${NC}"
python -m playwright install chromium

# Verify tools
verify_tools || exit 1

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To activate the Devin environment:${NC}"
echo -e "    source devin-venv/bin/activate"
echo -e "${YELLOW}To use with Cursor IDE:${NC}"
echo -e "    1. Make sure .cursorrules is in your project root"
echo -e "    2. Restart Cursor to load the new rules"
echo -e "    3. Use the AI assistant with enhanced capabilities"
echo -e "${YELLOW}To cleanup the environment:${NC}"
echo -e "    ./setup-devin.sh --cleanup"
echo -e "${YELLOW}Note: This integration now uses CursorAI's built-in capabilities instead of external APIs${NC}" 