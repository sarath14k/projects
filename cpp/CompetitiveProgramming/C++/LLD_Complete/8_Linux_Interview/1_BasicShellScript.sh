#!/bin/bash

# To run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/8_Linux_Interview && chmod +x 1_BasicShellScript.sh && ./1_BasicShellScript.sh

# ==========================================
# CONCEPT: Basic Shell Scripting
# 
# WHAT: Automating terminal commands using a script.
# HOW: Start the file with a "Shebang" (#!/bin/bash), define variables, use conditionals, and loops.
# WHY: Saves time for repetitive tasks like server backups, log parsing, or deployments.
# ==========================================

echo "--- 1. VARIABLES ---"
NAME="Sarath"  # Note: No spaces around '='
echo "Hello, $NAME! Welcome to your shell script."

echo -e "\n--- 2. CONDITIONALS ---"
# Check if a directory exists
TARGET_DIR="./test_dir"
if [ -d "$TARGET_DIR" ]; then
    echo "Directory exists!"
else
    echo "Directory not found. Creating it..."
    mkdir $TARGET_DIR
fi

echo -e "\n--- 3. LOOPS ---"
# Loop 3 times
for i in {1..3}; do
    echo "Iteration number: $i"
done

echo -e "\n--- 4. COMMAND SUBSTITUTION ---"
# Save the output of a command into a variable
CURRENT_TIME=$(date +"%T")
echo "The current time is: $CURRENT_TIME"

# Cleanup for the demo
rm -r $TARGET_DIR
