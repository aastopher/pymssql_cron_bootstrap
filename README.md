# MSSQL Report Process Automation

**NOTE:** Make sure that any network drives are mounted before running the script</br>

# **Setting up the Automation Service**

## **Installing Cron Service**
* Open WSL hit Windows+R to open the run window and enter the following `C:\Windows\System32\wsl.exe`
* Inside of the WSL terminal run the following commands.
* `sudo apt update`
* `sudo apt install cron`
* `sudo apt upgrade`

## **Change path and ad cd in cron_script.sh - __ONLY__ if running from new shell instead of running from project folder**
* `source PATH_TO_PROJECT/env/bin/activate`
* `cd PATH_TO_PROJECT`

## **Lines added to the /etc/sudoers.d file with `sudo visudo`**
* Run `sudo visudo` and append the following lines
* `%sudo ALL=NOPASSWD: /usr/sbin/service cron start`
* `%sudo ALL=NOPASSWD: PATH_TO_PROJECT/python3 main.py` - **make sure to change the path**
* `%sudo ALL=NOPASSWD: PATH_TO_PROJECT/cron_script.sh` - **make sure to change the path**

## **Add a job to the root crontab**
* `sudo crontab -l` to list root crontab content, make sure there are no job lines in the file.
* `sudo crontab -e` to edit root jobs
* edit the folling line to include proper paths for your configuration
* `30 12 * * 1 cd PATH_TO_PROJECT && ./cron_script.sh >> PATH_TO_PROJECT/logs/cron.log 2>&1` - runs every Monday at 12:30pm - **make sure to change the path**
* After writing out the file you should see `crontab: installing new crontab`

## **Running the project manually after install**
* Navigate to the project folder then run your choice of the following commands
* `sudo ./cron_script.sh` - will run with virtual env
* `sudo python3 main.py` - will run from current shell env. MUST HAVE DEPENDENCIES! check [Details.md](./Details.md)

## **cron commands**
* `sudo service cron status`
* `sudo service cron start`
* `sudo service cron stop`
* `sudo crontab -e` - to edit root jobs
* `sudo crontab -l` - to list root crontab contents

## To change connection configuration please use [Connection.md](./Connection.md)
