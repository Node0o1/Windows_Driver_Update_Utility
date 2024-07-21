# Windows_Driver_Update_Utility
####type: terminal-application

## Description
Install/Update drivers in Windows OS and runs the SystemFileChecker (sfc) tool to verify integrity of system files.

## About
> Does not download anything. Only install/updates .inf driver configuration file that are already located within the C:\\Windows\\System32\\DriverStore\\ directory.
> This does not create a restore point. It is recoended to create a system restore point that you can revert to in case of confilct.
> There is a C ++ version that I am working on with much more functionality. The c++ version currently supports creating a system restore point autonomously.
> you can find out more by visiting <a href="https://github.com/Node0o1/UpdateUtility"> **this** </a> page.

### Usage:
from within the Windows Driver_Update_utility directory, run
 ```sh
 python ./windows_driver_update_utility.py
 ```

### **Note**:
- *This application does not create a restore point.*
- *This only installs/updates drivers that are already on the local machine.*
- *This does resolve some current driver issues as is. Be sure to create a restore point if using this Python version so you can revert in case of error.*
