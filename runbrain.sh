#!/bin/bash
# Navigate to your project directory
#cd /Users/borisveis/source_no_icloud/financeML
#To ensure the AH action is fully captured (AH trading ends at 8:00 PM ET), set your cron job for 5:15 PM PT.
#
#Run crontab -e.
#
#Add this line:
#
#Bash
#15 17 * * 1-5 /Users/borisveis/source_no_icloud/financeML/run_brain.sh >> /Us
# Activate your pyenv virtual environment
source venv/bin/activate

echo "--- Starting Daily Brain Processing: $(date) ---"

# 1. Run the Prediction (Triggers the JIT Retraining and Logs to CSV)
python ML_Stock_Movement.py

# 2. Run the Reflector (Grades yesterday's pending predictions)
python agent/Reflector.py

echo "--- Processing Complete ---"