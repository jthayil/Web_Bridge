import os
from datetime import datetime
from xhtml2pdf import pisa
from random import randint
from jinja2 import Environment, FileSystemLoader

path_cwd = os.getcwd()
path_pdfoutput = os.path.join(path_cwd, 'pdfoutput')

if not os.path.exists(path_pdfoutput):
    os.makedirs(path_pdfoutput)


def html_to_pdf(source_html=None, output_filename=None):
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    result_file.close()
    return pisa_status.err

def html_report(name=None):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('report.html')
    return template.render(company='Aarti Pvt Ltd', date_time=datetime.now(), wgh=randint(20000, 40000))


def main():
    context = {
        'company': 'Aarti Pvt Ltd',
        'date_time': datetime.now(),
        'wgh': randint(20000, 40000)
    }
    html_to_pdf(html_report(), 'pdfoutput/report.pdf')


if __name__ == "__main__":
    main()
