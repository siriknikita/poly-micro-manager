#!/usr/bin/env bash

COMMIT_MESSAGE=$1

# Update poly-micro-backend
cd poly-micro-backend
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit, skipping"
else
    git add .
    git commit -m "$COMMIT_MESSAGE"
fi
cd ..

# Update poly-micro-frontend
cd poly-micro-frontend
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit, skipping"
else
    git add .
    git commit -m "$COMMIT_MESSAGE"
fi
cd ..

# Update poly-micro-manager-app
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit, skipping"
else
    git submodule update --remote
    git add .
    git commit -m "$COMMIT_MESSAGE"
fi
cd ..

echo "All repositories have been updated successfully."