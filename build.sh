#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Step 1: Generate data from JSON folders
echo "Generating data..."
python3 generate_data.py

# Step 2: Build the React application
echo "Building frontend..."
cd frontend
npm run build
cd ..

echo "Build complete! Static site is available in the 'docs/' directory."
echo "You can now push to GitHub and set up GitHub Pages to point to the '/docs' folder."
