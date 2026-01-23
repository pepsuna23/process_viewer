Set WshShell = CreateObject("WScript.Shell")
' Run the batch file hidden (0)
WshShell.Run chr(34) & "run_process_viewer.bat" & chr(34), 0
Set WshShell = Nothing
