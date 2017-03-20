:: This simple line allow a local administrator to access sensitive data from a locked session on a computer
:: need psexec
psexec64.exe -s \\localhost -i %SESSIONID% taskmgr
