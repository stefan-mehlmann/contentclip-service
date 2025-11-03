Option Explicit

Sub UploadCSVsToContentClip()
    Dim http As Object
    Dim boundary As String
    Dim file1Path As String, file2Path As String
    Dim url As String
    Dim body() As Byte
    Dim vBody As Variant
    Dim savePath As String

    ' === KONFIGURATION ===
    url = "https://cc-svc.mehlmann.com/upload/csv"
    file1Path = "C:\Users\angie\Downloads\20250925_Contentklammer_Titeldaten.csv"
    file2Path = "C:\Users\angie\Downloads\20250925_O2P.csv"
    savePath = "C:\Users\angie\Downloads\Response.csv"

    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")

    boundary = "Boundary" & Replace(Format(Timer * 1000, "0"), ",", "")

    body = BuildMultipartBodyBinary(file1Path, file2Path, boundary)
    vBody = body

    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "multipart/form-data; boundary=" & boundary
    http.send vBody

    If http.Status = 200 Then
        SaveTextToCSV http.responseText, savePath
        MsgBox "OK: Response gespeichert in " & savePath
    Else
        MsgBox "Fehler: " & http.Status & " - " & http.statusText, vbCritical
    End If
End Sub


Function BuildMultipartBodyBinary(file1Path As String, file2Path As String, boundary As String) As Byte()
    Dim stream As Object, header As String, footer As String
    Dim fileBytes1() As Byte, fileBytes2() As Byte, body() As Byte

    fileBytes1 = ReadBinaryFile(file1Path)
    fileBytes2 = ReadBinaryFile(file2Path)

    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open

    ' Datei 1
    header = "--" & boundary & vbCrLf & _
              "Content-Disposition: form-data; name=""file1""; filename=""" & Dir(file1Path) & """" & vbCrLf & _
              "Content-Type: application/octet-stream" & vbCrLf & vbCrLf
    stream.Write StringToBytesASCII(header)
    stream.Write fileBytes1
    stream.Write StringToBytesASCII(vbCrLf)

    ' Datei 2
    header = "--" & boundary & vbCrLf & _
              "Content-Disposition: form-data; name=""file2""; filename=""" & Dir(file2Path) & """" & vbCrLf & _
              "Content-Type: application/octet-stream" & vbCrLf & vbCrLf
    stream.Write StringToBytesASCII(header)
    stream.Write fileBytes2
    stream.Write StringToBytesASCII(vbCrLf)

    ' Abschluss
    footer = "--" & boundary & "--" & vbCrLf
    stream.Write StringToBytesASCII(footer)

    stream.Position = 0
    body = stream.Read
    stream.Close

    BuildMultipartBodyBinary = body
End Function


Function ReadBinaryFile(path As String) As Byte()
    Dim stream As Object
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.LoadFromFile path
    ReadBinaryFile = stream.Read
    stream.Close
End Function


Function StringToBytesASCII(text As String) As Byte()
    Dim bytes() As Byte
    bytes = StrConv(text, vbFromUnicode)
    StringToBytesASCII = bytes
End Function

Sub SaveTextToCSV(textData As String, savePath As String)
    Dim fnum As Integer
    fnum = FreeFile
    Open savePath For Output As #fnum
    Print #fnum, textData
    Close #fnum
End Sub
