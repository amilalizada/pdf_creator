import pdfkit
import base64
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

async def convert_to_pdf(html_file, output_name, config_path, options=None, data=None):

    config = pdfkit.configuration(wkhtmltopdf=config_path)
    return pdfkit.from_string(html_file, output_name, options=options, configuration=config)



# def send_mail(data: dict):
#     msg = MailBody
def get_pdf():
    file = 'output32.pdf'

    return file


def get_image_file_as_base64_data():
    with open("/Users/amil/Documents/Projects/pdf_creator/images/sign.png", 'rb') as image_file:

        return base64.b64encode(image_file.read())

def get_html_string():
    return """
    <!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
  integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<style>
*{
    font-family: arial, sans-serif;
}
  table {
    font-family: arial, sans-serif;
    width: 98%;
    border: none;
    margin-left: 20px;
  }
  tbody{
    padding-left: 30px;
  }

  td,
  th {
    /* border: 1px solid #dddddd; */
    text-align: left;
    padding: 6px;
    /* padding-left: 35px; */
    text-align: right;

  }
    .th-head{
    color: #283592;
  }
  

  tr:nth-child(even) {
    background-color: #dddddd;
  }
</style>

<body>
  <div style="width: 80%; margin: auto;" class="container">
    <div style="height: 8px;
    background-color: #283592" class="horizontal-line"></div>

    <section class="invoice-section">
      <header style="padding: 0;">
        <!-- <h1 style="margin-left: 10px;
        width: 300px;
        color: #6d64e8; font-family: sans-serif; margin-top: 40px;" class="company-name">JLTECH LLC</h1> -->

        <div style="padding: 0;" class="company-info d-flex justify-content-between mt-5">
          <ul style="list-style: none;" class="address-info">
            <li style="margin-left: 10px;
            width: 300px;
            color: #6d64e8; font-family: sans-serif; height: 40px; font-size: 30px;" class="company-name p-0 m-0">JLTECH LLC</li>
            <li>AGA Business Center 12th floor</li>
            <li>Khojali Ave 55, Baku, Azerbaijan AZ 1001</li>
            <li>(051) 450-00-15</li>
          </ul>

          <ul style="list-style: none;" class="bank-info flex-end">
            <li style="color: #6d64e8;">Tax ID: 2004130131</li>
            <li style="color: #6d64e8;">IBAN: AZ76PAHA40060AZNHC0100164830</li>
            <li>Bank: «PAŞA Bank» ASC</li>
            <li>S.W.I.F.T BIC: PAHAAZ22</li>
            <li>Bank Code: 505141</li>
            <li>TAX ID: 1700767721</li>
            <li>Acc: AZ82NABZ01350100000000071944</li>
          </ul>
        </div>
      </header>

      <main style="padding-left: 35px;">
        <h1 style="color: #283592;" class="invoice-title">Invoice</h1>
        <span style="color: #e01b84;" class="invoice-date">{{data.date}}</span>

        <section class="invoice-details row">
          <div class="d-flex flex-column col-4">
            <h1 class="invoice-label">Invoice for</h1>
            <ul style="list-style: none;" class="invoice-address p-0">
              <li>{{data.company_name}}</li>
              <li>{{data.company_address}}</li>
              <li>{{data.company_location}}</li>
            </ul>
          </div>

          <div class="d-flex flex-column col-4">
            <div class="mb-5">
              <h4 class="invoice-label">Payable to</h4>
              <span class="invoice-recipient">JLTECH LLC</span>
            </div>
            <div class="invoice-project">
              <h4 class="invoice-label">Project</h4>
              <span class="invoice-project-name">{{data.project_name}}</span>
            </div>

          </div>

          <div class="d-flex flex-column col-4">

            <div class="">
              <h4 class="invoice-label">Invoice #</h4>
              <span class="invoice-number">{{data.invoice_id}}</span>
            </div>

            <div class="mt-5">
              <h4 class="invoice-label mt-5">Due date</h4>
              <span class="invoice-due-date">{{data.due_date}}</span>
            </div>
          </div>
          <div class="col-3"></div>

        </section>

        <hr class="invoice-divider" />

      </main>
      <table style="border: none;">
        <tr style="padding-left: 30px;">
          <th class="th-head" style="text-align: left;">Description</th>
          <th class="th-head">Qty</th>
          <th class="th-head">Unit price</th>
          <th class="th-head">Total price</th>

        </tr>
        {% for desc in data.desciptions %}
        <tr>
          <td style="text-align: left;" class="desc">{{desc.description}}</td>
          <td>{{desc.qty}}</td>
          <td>₼{{desc.unitprice}}</td>
          <td>₼{{desc.total_price}}</td>
        {% endfor %}

        </tr>
        
      </table>

      <hr style="height:1px;border-width:0;color:gray;background-color: #dddddd; width: 96%; margin-right: 10px; margin-top: 20px;">
    </section>

    <div style="width: 100%; margin: auto; padding-left: 35px; margin: 0px; box-sizing: border-box;" class="d-flex justify-content-between mt-4">
      <div style="width: 200px;" class="note">
        <span style="margin-left: 15px;" class="notes-label col-6">Notes:</span>
      </div>
      <div style="width: 280px;" class="totals">
        <div class="text-right">
          <div class="d-flex justify-content-between">
            <p style="color: #6d64e8;" class="summary-label">Subtotal</p>
            <span class="summary-value">₼{{data.final_amount}}</span>
          </div>

        </div>
        <div class="text-right">
          <div class="d-flex text-right justify-content-between">

            <p style="text-align: right; width: 60px; color: #6d64e8;" class="summary-label">VAT</p>
            <span class="summary-value">₼{{data.vat}}</span>
          </div>
        </div>
      </div>

      
    </div>
    <div style="height: 40px;" class="total d-flex justify-content-end">
      <span style="color: #e01b84; font-family: sans-serif; font-size: 30px;"> ₼{{data.final_amount}}</span>
    </div>


    <div style="height: 40px;" class="mt-5">
      <img class="padding-left: 25px" src="/Users/amil/Documents/Projects/pdf_creator/images/sign.png" alt="Image">
    </div>

</body>

</html>
    
    """