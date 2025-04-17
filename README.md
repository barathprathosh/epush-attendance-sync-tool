# epush-attendance-sync-tool
Python Scripts to poll your Epush Server for logs and sync with your ERPNext instance.

## Setup Specifications

1. Setup dependencies
    ```
    cd epush-attendance-sync-tool
      && pip install -r requirements.txt
    ```
2. Setup `local_config.py`

   Make a copy of and rename `local_config.py.template` file.

3. Run this script using `python3 erpnext_sync.py`
4. Set Up Task Scheduler
   1. Open Task Scheduler (Win + S → search for Task Scheduler).
   2. Click "Create Task" (not Basic Task).
   3. General Tab:
        * Name: ERPNext Sync
        * Select Run whether user is logged on or not
        * Check Run with highest privileges
   4. Triggers Tab → New:
        * Begin the task: On a schedule
        * Settings: Daily
        * Repeat task every: 5 minutes
        * For a duration of: 1 day
        * Click OK
   5. Actions Tab → New:
        * Action: Start a program
        * Program/script: C:\path\to\your\run_erpnext_sync.bat
   6. Apply and Save

Software Package Link - https://drive.google.com/drive/folders/1z5e5aMuYahHtnMLtDr90HL1Kz467vnfk?usp=drive_link
