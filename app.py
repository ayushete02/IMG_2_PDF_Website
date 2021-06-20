import os
from os import path
from PIL import Image
from pythonfiles import i2pconverter,docx2pdfconvert
from PyPDF2 import PdfFileMerger
from docx2pdf import convert
from flask import *
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
import datetime
import threading
import random
now = datetime.datetime.now()

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS_CAM_SCANNER = {'pdf', 'txt'}
ALLOWED_EXTENSIONS_JPG2PDF = {'jpg'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


def allowed_file_cam_scanner(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_CAM_SCANNER
def allowed_file_jpg2pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_JPG2PDF

@app.route('/', methods=['GET', 'POST'])
def home():
    Clear_Directory()
    return render_template('home.html') 

@app.route('/watermark_Remover', methods=['GET', 'POST'])
def index():
    Clear_Directory()
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file_cam_scanner(file.filename):
            filename = secure_filename(file.filename)
            file.save( filename)

            input_file = PdfFileReader(open(filename, 'rb'))
            output = PdfFileWriter()
            for page_number in range(input_file.getNumPages()):
                page = input_file.getPage(page_number)
                page.mediaBox.lowerLeft = (page.mediaBox.getLowerLeft_x(), 20)
                output.addPage(page)
            output_stream = open(app.config['UPLOAD_FOLDER'] + filename, 'wb')
            output.write(output_stream)
            return redirect(url_for('uploaded_file', filename=filename))
    else:
        Clear_Directory()
        return ''' <script> alert("You have not selected any file.."); </script>
            <p style="display: flex; justify-content: center; text-align: center;">

            Go back..
                <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
            </p>'''


@app.route('/Img2Pdf',methods = ['GET', 'POST'])
def convertimg2pdf():
    Clear_Directory()
    if request.method == 'POST':
        
        global f1
        fi = request.files['img']
        f1 = fi.filename
        if f1.endswith('jpg' or 'JPG'):
            fi.save(f1)
            os.rename(f'{i2pconverter(f1)}',f'uploads/Jpg2Pdf_Converter.pdf')
            return redirect(url_for('uploaded_file', filename='Jpg2Pdf_Converter.pdf'))
        else:
            Clear_Directory()
            return ''' <script> alert("You have not selected any file.."); </script>
                <p style="display: flex; justify-content: center; text-align: center;">

                Go back..
                    <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
                </p>'''
    else:
        Clear_Directory()
        return ''' <script> alert("You have not selected any file.."); </script>
        <p style="display: flex; justify-content: center; text-align: center;">

        Go back..
            <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
        </p>'''


@app.route('/PDF_merge', methods=['GET', 'POST'])
def upload_files():
    Clear_Directory()
    if request.method == 'POST':
        mergePDF = PdfFileMerger()
        files_to_upload = request.files.getlist("file")

        if files_to_upload != '':
            try:

                rand = str(random.randint(1, 10000))
                file_name_pdf = 'PDF_Merger'+rand+'.pdf'
                for item in files_to_upload:
                    f = item
                    f.save(f.filename)
                    if f.filename.endswith('.pdf') or f.filename.endswith('.PDF'):
                        print(f.filename)
                        mergePDF.append(f.filename)
                    else:
                        Clear_Directory()
                        return ''' <script> alert("You have not selected any file.."); </script>
                                <p style="display: flex; justify-content: center; text-align: center;">

                                Go back..
                                    <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
                                </p>'''

                pdfOutput = open(file_name_pdf, 'wb')
                mergePDF.write(pdfOutput)
                pdfOutput.close()
                os.rename(f'{file_name_pdf}',f'uploads/PdfMergerConverter.pdf')
                return redirect(url_for('uploaded_file', filename='PdfMergerConverter.pdf'))
            except:
                Clear_Directory()
                return ''' <script> alert("You have not selected any file.."); </script>
                        <p style="display: flex; justify-content: center; text-align: center;">

                        Go back..
                            <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
                        </p>'''
    else:
        Clear_Directory()
        return ''' <script> alert("You have not selected any file.."); </script>
            <p style="display: flex; justify-content: center; text-align: center;">

            Go back..
            <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
        </p>'''

@app.route('/Img2Pdf_merger',methods = ['GET', 'POST'])
def convert_merge():
    Clear_Directory()
    if request.method == 'POST':
        
        mergePDF = PdfFileMerger()
        files_to_upload = request.files.getlist("file")
        try:
            
            if files_to_upload != '':
                rand = str(random.randint(1, 10000))
                file_name_pdf = 'PDF_Merger'+rand+'.pdf'
                print(file_name_pdf)
                for item in files_to_upload:
                    f = item
                    f.save(f.filename)
                    if f.filename.endswith('.jpg') or f.filename.endswith('.JPG'):
                        # f4 = i2pconverter(f.filename)
                        mergePDF.append(i2pconverter(f.filename))
                    else:
                        Clear_Directory()
                        return ''' <script> alert("You have not selected any file.."); </script>
                            <p style="display: flex; justify-content: center; text-align: center;">

                            Go back..
                                <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
                            </p>'''

                pdfOutput = open(file_name_pdf, 'wb')
                mergePDF.write(pdfOutput)
                pdfOutput.close()
                os.rename(f'{file_name_pdf}',f'uploads/Jpg2Pdf_Converter.pdf')
                return redirect(url_for('uploaded_file', filename='Jpg2Pdf_Converter.pdf'))
        except:
            Clear_Directory()
            return ''' <script> alert("You have not selected any file.."); </script>
     <p style="display: flex; justify-content: center; text-align: center;">

       Go back..
        <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
    </p>'''

            
    Clear_Directory()
    return ''' <script> alert("You have not selected any file.."); </script>
     <p style="display: flex; justify-content: center; text-align: center;">

       Go back..
        <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
    </p>'''

@app.route('/DOC2PDF',methods = ['GET', 'POST'])
def convertdoc():
    Clear_Directory()
    if request.method == 'POST':
        try:
 
            file = request.files['file']
            f1 = file.filename
            if f1.endswith('.docx'):
                file.save(f1)
                print(f1)
                os.rename(f"{f1}",f'file.docx')
                docx2pdfconvert('file.docx')
                os.rename(f'{i2pconverter(f1)}',f'uploads/Jpg2Pdf_Converter.pdf')
                return redirect(url_for('uploaded_file', filename='Jpg2Pdf_Converter.pdf'))
        except:
            Clear_Directory()
            return ''' <script> alert("You have not selected any file.."); </script>
            <p style="display: flex; justify-content: center; text-align: center;">

            Go back..
                <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
            </p>'''
    else:
        Clear_Directory()
        return ''' <script> alert("You have not selected any file.."); </script>
        <p style="display: flex; justify-content: center; text-align: center;">

        Go back..
            <a href="https://onlinejpg2pdf.herokuapp.com/"><button style="text-align: center;">Back !!</button></a>
        </p>'''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

def Clear_Directory():
    try:
        for items in os.listdir():
            if items.endswith('.pdf') or items.endswith('.jpg') or items.endswith('.docx')  or items.endswith('.png'):
                print("Remove "+items)
                os.remove(items)
        for items in os.listdir('uploads'):
            if items.endswith('.pdf') or items.endswith('.jpg') or items.endswith('.docx')  or items.endswith('.png'):
                print("Remove "+items)
                os.remove('uploads/'+items)
        for items in os.listdir('downloads'):
            if items.endswith('.pdf') or items.endswith('.jpg') or items.endswith('.docx')  or items.endswith('.png'):
                print("Remove "+items)
                os.remove('downloads/'+items)
    except:
        for items in os.listdir('uploads'):
            if items.endswith('.pdf') or items.endswith('.jpg') or items.endswith('.docx')  or items.endswith('.png'):
                print("Remove "+items)
                os.remove('uploads/'+items)
        for items in os.listdir('downloads'):
            if items.endswith('.pdf') or items.endswith('.jpg') or items.endswith('.docx')  or items.endswith('.png'):
                print("Remove "+items)
                os.remove('downloads/'+items)




if __name__ == "__main__":
    app.run(debug=True)