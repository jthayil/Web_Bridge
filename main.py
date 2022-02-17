import configparser
import os
from datetime import datetime

from jinja2 import Template
from xhtml2pdf import pisa

path_cwd = os.getcwd()
config = configparser.ConfigParser()

wgh_report_syntax = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Weighbridge</title>
    <style>
    .textcenter {
        text-align: center;
    }
    @page {
      size: A4 portrait;
      margin: 2cm;
    }
    </style>
</head>
<body>
<div class="row">
    <div class="textcenter">{{ cpy }}</div>
    <div class="textcenter">{{ addr }}</div>
    <div class="col-12">
        <hr>
    </div>
    <table style="width:100%">
    <tr>
    <td><b>Date Time</b> : {{ rd }}</td>
    <td><b>Weight</b>: {{ wgh }}</td>
    </tr>
    </table>
</div>
</body>
</html>
"""


def html_to_pdf(rendered_html=None, pdf_filepath=None):
    if rendered_html is None:
        raise ValueError('Insufficent Arguements')
    else:
        if pdf_filepath is None:
            pdf_filepath = str(datetime.now().strftime("%m%S%f")) + '.pdf'
        this_pdf = open(pdf_filepath, "w+b")
        pisa_status = pisa.CreatePDF(rendered_html, dest=this_pdf)
        this_pdf.close()
        if pisa_status.err:
            return pisa_status.err
        return pdf_filepath


def get_wgh_report(company=None, address=None, wgh=None):
    if None in (company, address, wgh):
        raise ValueError('Insufficient Arguments')
    else:
        get_template = Template(wgh_report_syntax)
        return get_template.render(
            cpy=company,
            addr=address,
            rd=datetime.now(),
            wgh=wgh
        )


def main():
    config.read('ftspl.ini')
    try:
        company = config['DEFAULT']['company']
        address = config['DEFAULT']['address']
        wgh = config['DEFAULT']['wgh']
        return html_to_pdf(get_wgh_report(company, address, wgh), 'report.pdf')
    except KeyError:
        raise KeyError('Config Read Failed')


if __name__ == "__main__":
    main()
