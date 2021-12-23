import base64
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def print_labels(self):
        # product_uom_qty = sum(self.move_ids_without_package.mapped('product_uom_qty'))
        # product_uom_qty = self.move_ids_without_package.mapped('product_uom_qty')
        # label_height = self.move_ids_without_package.mapped('product_packaging.packaging_type_id.label_height')
        # data = {}
        self.with_context(lang=self.partner_id.lang)

        def append_pdf(input, output):
            [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

        output = PdfFileWriter()
        report_name = 'Certification Label Report'
        address = ""
        if self.partner_id.street:
            address += "{}\n".format(self.partner_id.street)
        if self.partner_id.street2:
            address += "{}\n".format(self.partner_id.street2)
        if self.partner_id.city:
            address += "{}, ".format(self.partner_id.city)
        if self.partner_id.state_id:
            address += "{}, ".format(self.partner_id.state_id.name)
        if self.partner_id.zip:
            address += "{}, ".format(self.partner_id.zip)
        if self.partner_id.country_id:
            address += "{}, ".format(self.partner_id.country_id.name)
        for line in self.move_ids_without_package:
            label_height = line.product_packaging.packaging_type_id.label_height or 100
            data = {
                'move_line': line,
                'label_height': str(label_height),
                'picking_id': self,
                'address': address
            }
            print('\n', data)
            report = self.env.ref('stock_certification_label.action_print_label')
            if label_height == 50:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label').id
            if label_height == 60:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label_60').id
            if label_height == 70:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label_70').id
            if label_height == 100:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label_100').id
            if label_height == 150:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label_150').id
            if label_height == 180:
                report.paperformat_id = self.env.ref('stock_certification_label.paperformat_stock_label_180').id
            main_content_pdf = report._render_qweb_pdf(self.ids, data=data)
            main_content_pdf_encode = base64.encodebytes(main_content_pdf[0])
            # print(main_content_pdf_encode)
            with open(os.path.expanduser('/tmp/line_{}.pdf'.format(line.id)), 'wb') as fout:
                fout.write(base64.decodebytes(main_content_pdf_encode))

            append_pdf(PdfFileReader(
                open("/tmp/line_{}.pdf".format(line.id), "rb"), strict=False), output)
            os.remove("/tmp/line_{}.pdf".format(line.id))

        output.write(open("/tmp/CombinedPages.pdf", "wb"))
        output_file = open("/tmp/CombinedPages.pdf", "rb")
        output_byte = output_file.read()
        attachment = self.env['ir.attachment'].create({
            'name': report_name,
            'store_fname': report_name + '.pdf',
            'datas': base64.encodebytes(output_byte),
            'res_model': 'stock.picking',
            'res_id': self.id,
            'type': 'binary',
            'url': 'url',
            'mimetype': 'application/pdf'})
        os.remove('/tmp/CombinedPages.pdf')

        action = {
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=ir.attachment&id=" + str(
                attachment.id) + "&filename_field=name&field=datas&download=true&name=" + attachment.name,
            'target': 'self'
        }
        return action
