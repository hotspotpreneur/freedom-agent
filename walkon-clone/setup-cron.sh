#!/bin/bash
#==============================================================================
# Liverpool News Aggregator - Cron Setup Script
#==============================================================================
# This script sets up automatic scraping every 5 minutes (300 seconds)
# Run: bash setup-cron.sh
#==============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRAPER_PATH="$SCRIPT_DIR/maximum-scraper.py"
LOG_FILE="$SCRIPT_DIR/scraper.log"
JSON_FILE="$SCRIPT_DIR/liverpool-news.json"
THEME_DIR="$SCRIPT_DIR/wp-theme"
# Path where WordPress has the theme installed (adjust if needed)
WP_THEME_PATH="/home/username/public_html/kopite.online/wp-content/themes/kopite-news"

echo "🏆 Setting up Liverpool News Aggregator cron job..."
echo "===================================================="

# Update WP_THEME_PATH with actual username
WP_THEME_PATH=$(echo $WP_THEME_PATH | sed "s|username|$USER|")

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found. Please install Python 3 first."
    exit 1
fi

# Test the scraper
echo "📋 Testing scraper..."
cd "$SCRIPT_DIR"
python3 "$SCRAPER_PATH"
if [ $? -eq 0 ]; then
    echo "✅ Scraper works!"
else
    echo "❌ Scraper failed. Check the errors above."
    exit 1
fi

# Copy JSON to local theme folder (for backup/development)
if [ -d "$THEME_DIR" ]; then
    cp "$JSON_FILE" "$THEME_DIR/liverpool-news.json"
    echo "📁 Copied JSON to local theme folder"
fi

# Copy JSON to WordPress theme folder (if it exists)
if [ -d "$WP_THEME_PATH" ]; then
    cp "$JSON_FILE" "$WP_THEME_PATH/liverpool-news.json"
    echo "📁 Copied JSON to WordPress theme folder"
fi

# Create cron entry (runs scraper then copies JSON to both locations)
CRON_JOB="*/5 * * * * cd $SCRIPT_DIR && python3 $SCRAPER_PATH >> $LOG_FILE 2>&1 && cp $JSON_FILE $THEME_DIR/ && cp $JSON_FILE $WP_THEME_PATH/ 2>/dev/null"

# Remove existing cron entries for this script
crontab -l 2>/dev/null | grep -v "maximum-scraper.py" > /tmp/current-cron

# Add new cron entry
echo "$CRON_JOB" >> /tmp/current-cron
crontab /tmp/current-cron

# Clean up
rm /tmp/current-cron

echo ""
echo "✅ Cron job installed!"
echo "📅 Runs every 5 minutes"
echo "📁 Log file: $LOG_FILE"
echo "📊 Data file: $JSON_FILE"
echo "📊 Theme reads: $THEME_DIR/liverpool-news.json"
echo ""
echo "IMPORTANT: If the WordPress copy failed, edit setup-cron.sh"
echo "and change 'username' to your cPanel username"
echo ""
echo "Commands:"
echo "  View cron:  crontab -l"
echo "  Edit cron:  crontab -e"
echo "  View log:   tail -f $LOG_FILE"
echo "  Run now:    python3 $SCRAPER_PATH"
echo ""
echo "To remove: crontab -l | grep -v maximum-scraper.py | crontab -"