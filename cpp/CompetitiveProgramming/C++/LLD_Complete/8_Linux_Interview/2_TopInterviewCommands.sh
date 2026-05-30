#!/bin/bash

# ==========================================
# CONCEPT: Top Linux Interview Commands (Deep Dive)
# 
# These are the most frequently asked commands in Linux/Backend interviews.
# Note: This is an educational reference file, not meant to be executed directly.
# ==========================================

# ==========================================
# 1. 'grep' (Global Regular Expression Print)
# ==========================================
# Q1: How to find a string ignoring case?
# Ans: grep -i "error" /var/log/syslog
#
# Q2: How to count the number of matching lines?
# Ans: grep -c "Exception" server.log
#
# Q3: How to print the matched line ALONG with 3 lines after it?
# Ans: grep -A 3 "FATAL" server.log   (-A for After, -B for Before, -C for Context)
#
# Q4: How to search recursively in all files in a directory?
# Ans: grep -r "main" /home/sarath/projects
#
# Q5: How to invert the match (show lines that DO NOT contain the word)?
# Ans: grep -v "DEBUG" server.log

# ==========================================
# 2. 'find'
# ==========================================
# Q1: How to find all .cpp files modified in the last 7 days?
# Ans: find . -type f -name "*.cpp" -mtime -7
#
# Q2: How to find and delete all files larger than 100MB?
# Ans: find . -type f -size +100M -exec rm -f {} \;
#
# Q3: How to find a file by its exact name starting from the root directory?
# Ans: find / -type f -name "config.yaml"
#
# Q4: How to find all empty directories?
# Ans: find . -type d -empty
#
# Q5: How to find files owned by a specific user?
# Ans: find /var/log -user root

# ==========================================
# 3. 'awk'
# ==========================================
# Q1: How to print the 2nd column of a CSV file?
# Ans: awk -F ',' '{print $2}' data.csv
#
# Q2: How to print the last column of a file with unknown number of columns?
# Ans: awk '{print $NF}' data.txt
#
# Q3: How to filter and print rows where the 3rd column is greater than 50?
# Ans: awk '$3 > 50 {print $0}' data.txt
#
# Q4: How to find the total sum of all numbers in the 1st column?
# Ans: awk '{sum += $1} END {print sum}' numbers.txt
#
# Q5: How to print line numbers along with the line content?
# Ans: awk '{print NR, $0}' file.txt

# ==========================================
# 4. 'sed' (Stream Editor)
# ==========================================
# Q1: How to replace "foo" with "bar" globally in a file?
# Ans: sed -i 's/foo/bar/g' filename.txt
#
# Q2: How to delete the first line of a file?
# Ans: sed -i '1d' filename.txt
#
# Q3: How to delete all empty lines from a file?
# Ans: sed -i '/^$/d' filename.txt
#
# Q4: How to replace "foo" with "bar" ONLY on lines containing "test"?
# Ans: sed -i '/test/s/foo/bar/g' filename.txt
#
# Q5: How to print lines 5 to 10 from a file?
# Ans: sed -n '5,10p' filename.txt

# ==========================================
# 5. 'chmod' & 'chown'
# ==========================================
# Q1: What does chmod 755 do?
# Ans: Grants Read/Write/Execute (7) for the owner, and Read/Execute (5) for group and others.
#
# Q2: How to give execute permission to a script for everyone?
# Ans: chmod +x script.sh
#
# Q3: How to recursively change permissions of a directory and all its contents?
# Ans: chmod -R 755 /var/www/html
#
# Q4: How to change the owner of a file to user 'sarath' and group 'admin'?
# Ans: chown sarath:admin file.txt
#
# Q5: How to apply 'chown' recursively to a folder?
# Ans: chown -R sarath:admin /home/sarath/project

# ==========================================
# 6. 'lsof' & Networking
# ==========================================
# Q1: How to find which process is running on port 8080?
# Ans: lsof -i :8080
#
# Q2: How to list all open files by a specific user?
# Ans: lsof -u sarath
#
# Q3: How to find which port a specific PID (e.g., 1234) is listening on?
# Ans: lsof -p 1234 | grep LISTEN
#
# Q4: (Using netstat) How to see all active listening ports?
# Ans: netstat -tuln
#
# Q5: (Using netcat) How to check if a remote server is reachable on a specific port?
# Ans: nc -vz 192.168.1.5 80

# ==========================================
# 7. 'top' / 'ps' / 'kill'
# ==========================================
# Q1: How to find the Process ID (PID) of your java app?
# Ans: ps aux | grep java
#
# Q2: How to forcefully kill a process by its PID?
# Ans: kill -9 <PID>
#
# Q3: How to kill all processes with a specific name?
# Ans: killall nginx  (or pkill nginx)
#
# Q4: In 'top', how do you sort by Memory usage?
# Ans: Open 'top', then press 'Shift + M'. (Shift + P for CPU).
#
# Q5: How to run a process in the background and keep it running after logout?
# Ans: nohup python3 script.py &

# ==========================================
# 8. 'df', 'du', & 'tar'
# ==========================================
# Q1: How to check overall disk space left on your system?
# Ans: df -h  (-h makes it human readable: GB/MB instead of bytes).
#
# Q2: How to find the size of the current directory?
# Ans: du -sh .
#
# Q3: How to find the 5 largest files/directories in current path?
# Ans: du -sh * | sort -rh | head -n 5
#
# Q4: How to compress a folder into a tar.gz archive?
# Ans: tar -czvf archive_name.tar.gz /path/to/folder
#
# Q5: How to extract a tar.gz archive?
# Ans: tar -xzvf archive_name.tar.gz
