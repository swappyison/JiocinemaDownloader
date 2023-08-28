#!/bin/bash

# Start jioscraper.py
python3 jioscraper.py

# Wait for the first script to finish (you can adjust the sleep time if needed)
sleep 10

# Start jiobulkdownloader.py
python3 jiobulkdownloader.py
