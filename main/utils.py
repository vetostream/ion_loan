import subprocess
from django.conf import settings
from django.template.loader import render_to_string

def generate_to_pdf(template, context, pdf_name):
    rendered_html = render_to_string(template, context)

    html_file = f'{pdf_name}.html' 
    pdf_file = f'{pdf_name}.pdf'

    html_path =  f'{settings.REPORTS_PATH}/{html_file}'
    pdf_path = f'{settings.REPORTS_PATH}/{pdf_file}'

    # save html
    with open(html_path, 'w') as file:
        file.writelines(rendered_html)

    # convert html to pdf
    convert_process = subprocess.Popen(['wkhtmltopdf', html_path, pdf_path])

    convert_process.wait()

    if convert_process:
        return pdf_path

    return None
