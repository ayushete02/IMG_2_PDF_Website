import img2pdf
import os
from docx2pdf import convert

def i2pconverter(file):
    pdfname = file.split('.')[0]+'converted'+'.pdf'
    with open(pdfname,'wb') as f:
        f.write(img2pdf.convert(file))
        f.close()
    # os.rename(f'{pdfname}',f'uploads/Jpg2Pdf_Converter.pdf')
    return pdfname

def docx2pdfconvert(file):
    convert(file)        
    convert(file, "output.pdf")
    convert("my_docx_folder/")
