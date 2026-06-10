#!/bin/bash
# Run Lead Scraper - North West UK Plumbers
# Usage: ./run-scraper.sh

cd /home/openclaw/.openclaw/workspace

echo "Starting lead scrape $(date)"
python3 scripts/batch-scraper.py
echo "Completed $(date)"