# Windows_Driver_Update_Utility
Update all drivers in Windows OS.
> Does not download anything. Only install/updates .inf driver configuration file that are already located within the C:\\Windows\\System32\\DriverStore\\ directory.
> This does not create a restore point. It is recoended to create a system restore point that you can revert to in case of confilct.
> There is a C ++ version that I am working on with much more functionality. The c++ version currently supports creating a sstem restore point autonomously.
> you can find out more by visiting <a href="https://github.com/Node0o1/UpdateUtility"> **this** </a> page.
* initial commit, will likely add some ascii and clean up files soon.
* does not create a restore point.
* only installs/updates drivers that are already on the local machine.
