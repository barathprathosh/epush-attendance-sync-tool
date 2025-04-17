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

# ePushServer Windows Installation Guide

This guide will help you set up the **ePushServer** on a Windows system using the provided installer package.

---

## 📦 Download Installer Package

➡️ Download the full installer package from this Google Drive link:

**[Download Link Here – [Google Drive](https://drive.google.com/drive/folders/1z5e5aMuYahHtnMLtDr90HL1Kz467vnfk?usp=drive_link)]**

---

## 🛠️ Installation Steps

### 1. Install Java (JDK)

- Download and install the latest **Java JDK** (Java Development Kit) from:
  https://www.oracle.com/java/technologies/javase-jdk11-downloads.html  
- Add JAVA to your system environment variables:
  - Go to **Control Panel → System → Advanced system settings**
  - Click **Environment Variables**
  - Under **System Variables**, create a new variable:
    - Variable name: `JAVA_HOME`
    - Variable value: `C:\Program Files\Java\jdk-<version>`
  - Add `%JAVA_HOME%\bin` to the `Path` variable

---

### 2. Install Apache Tomcat 9

- Download **Tomcat 9** from:
  https://tomcat.apache.org/download-90.cgi
- Install to:  
  `C:\Program Files\Tomcat`

---

### 3. Install MariaDB

- Download and install **MariaDB** from:
  https://mariadb.org/download/
- During setup, **set the root password** and remember it.
- Optionally install HeidiSQL or use command line to manage databases.

---

## 🧩 Configure ePushServer

### 4. Copy Application Files

- From the downloaded installer package, extract the `epushserver` folder.
- Inside it, locate the `iclock` folder.
- Copy the `iclock` folder and paste it into:  
  `C:\Program Files\Tomcat\webapps\`

So the path should be:  
`C:\Program Files\Tomcat\webapps\iclock`

---

### 5. Import Database

- Open your MariaDB client (or use command line).
- Create a new database named: `epushserver`
- Import the provided `.sql` file from the package into this database.

#### Using Command Line:

```bash
mysql -u root -p
```

### 6. Configure Database Credentials
After loading the SQL file, open the following file in a text editor:

```bash
C:\Program Files\Tomcat\webapps\iclock\WEB-INF\databaseconfig.properties
```

Update or add the following lines:

```bash
DB_USERNAME_MYSQL=root
DB_PASSWORD_MYSQL=root
```

Save the file.

✅ Done!
Start Tomcat Server (startup.bat in bin folder)
```bash
Visit: http://localhost:8080/iclock in your browser
```
ePushServer should now be running 🎉

💡 Notes
Make sure port `8080` is not blocked by another app.

Ensure iclock folder has the correct permissions under webapps/.

### 7. Set Up Task Scheduler
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
