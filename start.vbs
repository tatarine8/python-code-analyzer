Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

venvExists = fso.FolderExists("venv")
reqExists = fso.FileExists("requirements.txt")

show = False

If Not venvExists Then
    show = True
ElseIf reqExists Then
    Set reqFile = fso.GetFile("requirements.txt")
    Set venvDir = fso.GetFolder("venv")
    If reqFile.DateLastModified > venvDir.DateLastModified Then
        show = True
    End If
End If

If show Then
    ' 🧾 Створюємо тимчасовий файл showmsg.vbs
    Set tempMsg = fso.CreateTextFile("showmsg.vbs", True, True)
    tempMsg.WriteLine "Set objShell = CreateObject(""WScript.Shell"")"
    tempMsg.WriteLine "Set obj = CreateObject(""WScript.Shell"")"
    tempMsg.WriteLine "obj.Popup ""⏳ Готується середовище для запуску Python Code Analyzer..."" & vbCRLF & vbCRLF & ""Це може зайняти до 30 секунд..."", 5, ""Ініціалізація"", 64"
    tempMsg.WriteLine "Set fso = CreateObject(""Scripting.FileSystemObject"")"
    tempMsg.WriteLine "fso.DeleteFile WScript.ScriptFullName"
    tempMsg.Close

    ' 🚀 Запускаємо showmsg.vbs — воно самовидалиться після завершення
    shell.Run "wscript showmsg.vbs", 0, False
End If

' ▶️ Запускаємо основний .bat
shell.Run "run_app.bat", 0, False
