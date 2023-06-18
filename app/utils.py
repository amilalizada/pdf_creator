import pdfkit  

# def convert_to_pdf(html_file, pdf_name, object):

#     html_template ="""
    
#     <!DOCTYPE html>
#         <html>

#         <head>
#         <meta charset="UTF-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#         </head>
#         <style>
#         .container {
#             padding: 80px;
#             width: 50%;
#             margin: auto;
#             font-family: sans-serif;
#         }

#         .horizontal-line {
#             height: 8px;
#             width: 100%;

#             --tw-bg-opacity: 1;
#             background-color: rgb(30 58 138 / var(--tw-bg-opacity));

#         }

#         ul {
#             list-style: none;
#         }

#         .invoice-section {
#             padding-left: 3.5rem;
#             padding-top: 1rem;
#             padding-bottom: 1rem;
#             padding-right: 0.5rem
#         }

#         .company-name {
#             font-size: 1.5rem
#             /* 24px */
#             ;
#             line-height: 2rem
#             /* 32px */
#             ;
#             --tw-text-opacity: 1;
#             color: rgb(167 139 250 / var(--tw-text-opacity));
#         }

#         .company-info {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             font-size: 0.75rem
#             /* 12px */
#             ;
#             line-height: 1rem
#             /* 16px */
#             ;
#         }

#         .addres-info {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#             display: grid;
#             gap: 0.125rem
#         }

#         .bank-info {
#             --tw-text-opacity: 1;
#             color: rgb(156 163 175 / var(--tw-text-opacity));
#             display: grid;
#             gap: 0.125rem
#         }

#         .invoice-title {
#             --tw-text-opacity: 1;
#             color: rgb(30 58 138 / var(--tw-text-opacity));
#             font-size: 2.25rem
#             /* 36px */
#             ;
#             line-height: 2.5rem;
#             font-weight: 700
#         }

#         .invoice-date {
#             --tw-text-opacity: 1;
#             color: rgb(236 72 153 / var(--tw-text-opacity));
#             font-size: 0.875rem
#             /* 14px */
#             ;
#             line-height: 1.25rem;
#             font-weight: 700;

#         }

#         .invoice-details {
#             font-size: 0.75rem
#             /* 12px */
#             ;
#             line-height: 1rem
#             /* 16px */
#             ;
#             display: grid;
#             grid-template-columns: repeat(3, minmax(0, 1fr));
#             gap: 0.75rem
#             /* 12px */
#             ;
#             /* place-items: center; */
#             align-items: flex-start;
#             width: 80%;
#             margin-top: 1.25rem --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#         }

#         .invoice-label {
#             font-size: 0.875rem
#             /* 14px */
#             ;
#             line-height: 1.25rem
#             /* 20px */
#             ;
#             font-weight: 700;

#         }

#         .invoice-address {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#             display: grid;
#             gap: 4px;
#             padding-left: 0;
#         }

#         .invoice-recipient {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));

#         }

#         .invoice-number {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#         }

#         /* --tw-text-opacity: 1;
#         color: rgb(107 114 128 / var(--tw-text-opacity)); */
#         .invoice-project {
#             grid-column-start: 2
#         }



#         .invoice-project-name {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#         }

#         .invoice-due-date {
#             --tw-text-opacity: 1;
#             color: rgb(107 114 128 / var(--tw-text-opacity));
#         }




#         .invoice-items {
#             display: grid;
#             grid-template-columns: repeat(5, minmax(0, 1fr));

#         }

#         .item-description {
#             grid-column: span 2 / span 2;

#         }

#         .item-title {
#             font-size: 0.875rem
#             /* 14px */
#             ;
#             line-height: 1.25rem
#             /* 20px */
#             ;
#             --tw-text-opacity: 1;
#             color: rgb(30 58 138 / var(--tw-text-opacity));
#             font-weight: 700;
#             margin-bottom: 0.5rem
#             /* 8px */
#             ;

#         }

#         .text-right {
#             text-align: right;
#             font-size: 0.875rem
#             /* 14px */
#             ;
#             line-height: 1.25rem
#             /* 20px */
#             ;
#             font-weight: 700;
#             --tw-text-opacity: 1;
#             color: rgb(30 58 138 / var(--tw-text-opacity));
#             margin-bottom: 0.5rem
#             /* 8px */
#             ;


#         }

#         .item-list {
#             font-weight: 600;
#             font-size: 0.75rem
#             /* 12px */
#             ;
#             line-height: 1rem
#             /* 16px */
#             ;
#             display: grid;
#             gap: 0.5rem
#             /* 8px */
#             ;
#             padding-left: 0;

#         }

#         .text-right>.item-list {
#             color: rgb(107 114 128 / var(--tw-text-opacity));

#         }




#         .invoice-divider {
#             margin-top: 1.5rem
#             /* 24px */
#             ;
#             margin-bottom: 1.5rem
#             /* 24px */
#             ;
#         }

#         .invoice-footer {
#             display: flex;
#             align-items: start;
#             justify-content: space-between;

#         }

#         .notes-label {
#             font-size: 0.75rem
#             /* 12px */
#             ;
#             line-height: 1rem
#             /* 16px */
#             ;
#             --tw-text-opacity: 1;
#             color: rgb(156 163 175 / var(--tw-text-opacity));
#         }

#         .invoice-summary {
#             display: grid;
#             grid-template-columns: repeat(2, minmax(0, 1fr));
#             text-align: right;
#             column-gap: 2.5rem
#             /* 40px */
#             ;
#             font-size: 0.75rem
#             /* 12px */
#             ;
#             line-height: 1rem
#             /* 16px */
#             ;
#             gap: 0.5rem
#             /* 8px */
#             ;
#             place-content: start;
#             place-items: start;
#             content: start;
#             /* place-items: start; */

#         }


#         .summary-label {
#             --tw-text-opacity: 1;
#             color: rgb(30 58 138 / var(--tw-text-opacity));
#             font-weight: 600;
#             margin: 0;
#             padding: 0;

#         }

#         .summary-value {
#             font-weight: 700;

#         }

#         .total-amount {
#             grid-column: span 2 / span 2;
#             font-size: 1.875rem
#             /* 30px */
#             ;
#             line-height: 2.25rem
#             /* 36px */
#             ;

#             --tw-text-opacity: 1;
#             color: rgb(236 72 153 / var(--tw-text-opacity));
#             font-weight: 600;

#         }
#         </style>
#         <body>
#         <div class="container">
#             <div class="horizontal-line"></div>

#             <section class="invoice-section">
#             <header>
#                 <h1 style="color: red;" class="company-name">JLTECH LLC</h1>

#                 <div class="company-info">
#                 <ul class="address-info" style="padding: 0;">
#                     <li>AGA Business Center 12th floor</li>
#                     <li>Khojali Ave 55, Baku, Azerbaijan AZ 1001</li>
#                     <li>(051) 450-00-15</li>
#                 </ul>

#                 <ul class="bank-info">
#                     <li>Bank: «PAŞA Bank» ASC</li>
#                     <li>S.W.I.F.T BIC: PAHAAZ22</li>
#                     <li>Bank Code: 505141</li>
#                     <li>TAX ID: 1700767721</li>
#                     <li>Acc: AZ82NABZ01350100000000071944</li>
#                 </ul>
#                 </div>
#             </header>

#             <main>
#                 <h1 class="invoice-title">Invoice</h1>
#                 <span class="invoice-date">11/06/2023</span>

#                 <article class="invoice-details">
#                 <div>
#                     <h1 class="invoice-label">Invoice for</h1>
#                     <ul class="invoice-address">
#                     <li>MICROTECH MMC</li>
#                     <li>Khagani Rustamov 6</li>
#                     <li>Baku, Azerbaijan</li>
#                     </ul>
#                 </div>

#                 <div>
#                     <h4 class="invoice-label">Payable to</h4>
#                     <span class="invoice-recipient">JLTECH LLC</span>
#                 </div>

#                 <div>
#                     <h4 class="invoice-label">Invoice #</h4>
#                     <span class="invoice-number">31</span>
#                 </div>

#                 <div class="invoice-project">
#                     <h4 class="invoice-label">Project</h4>
#                     <span class="invoice-project-name">Service</span>
#                 </div>

#                 <div>
#                     <h4 class="invoice-label">Due date</h4>
#                     <span class="invoice-due-date">11/06/2023</span>
#                 </div>
#                 </article>

#                 <hr class="invoice-divider" />

#                 <div class="invoice-items">
#                 <div class="item-description">
#                     <h1 class="item-title">Description</h1>
#                     <ul class="item-list">
#                     <li>Tableau - Creator License (1 illik)</li>
#                     <li>Tableau - Explorer License (1 illik)</li>
#                     </ul>
#                 </div>

#                 <div class="text-right">
#                     <h1 class="item-title">Qty</h1>
#                     <ul class="item-list">
#                     <li>3</li>
#                     <li>15</li>
#                     </ul>
#                 </div>

#                 <div class="text-right">
#                     <h1 class="item-title">Unit price</h1>
#                     <ul class="item-list">
#                     <li>₼1,586.66</li>
#                     <li>₼793.32</li>
#                     </ul>
#                 </div>

#                 <div class="text-right">
#                     <h1 class="item-title">Total price</h1>
#                     <ul class="item-list">
#                     <li>₼40,000.34</li>
#                     <li>₼40,000.34</li>
#                     <li>$0.00</li>
#                     <li>$0.00</li>
#                     </ul>
#                 </div>
#                 </div>
#             </main>

#             <hr class="invoice-divider" />

#             <footer class="invoice-footer">
#                 <span class="notes-label">Notes:</span>

#                 <div class="invoice-summary">
#                 <p class="summary-label">Subtotal</p>
#                 <span class="summary-value">₼40,000.87</span>

#                 <p class="summary-label">VAT</p>
#                 <span class="summary-value">₼2,998.44</span>

#                 <p class="summary-label total-amount">₼19,658.58</p>
#                 </div>
#             </footer>
#             </section>
#         </div>

#         </body>

#         </html>
#     """
    
#     pdfkit.from_file(html_file, pdf_name)

def convert_to_pdf(html_file, output_name, options):
    pdfkit.from_file(html_file, output_name, options=options)



