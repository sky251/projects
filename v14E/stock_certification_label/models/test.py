def print_inspection_quotation(self):
    self.ensure_one()

    main_content_pdf = ''
    report_name = ''

    if 'shelf_report' in self.env.context:
        report_name = 'Shelf Quotation Report'
        main_content_pdf = self.env.ref(
            'sale_quote_inspection.action_shelf_quotation_report').render_qweb_pdf(self.ids)

        main_content_pdf_encode = base64.encodestring(main_content_pdf[0])

        # if self.company_id and self.company_id.report_cover_pdf:
        #     with open(os.path.expanduser('/tmp/report_cover_pdf.pdf'), 'wb') as fout:
        #         fout.write(base64.decodestring(
        #             self.company_id.report_cover_pdf))
        with open(os.path.expanduser('/tmp/main_content_pdf.pdf'), 'wb') as fout:
            fout.write(base64.decodestring(main_content_pdf_encode))
        if self.company_id and self.company_id.report_back_cover_pdf:
            with open(os.path.expanduser('/tmp/report_back_cover_pdf.pdf'), 'wb') as fout:
                fout.write(base64.decodestring(
                    self.company_id.report_back_cover_pdf))

        def append_pdf(input, output):
            [output.addPage(input.getPage(page_num))
             for page_num in range(input.numPages)]

        output = PdfFileWriter()
        if self.company_id and self.company_id.report_cover_pdf:
            append_pdf(PdfFileReader(
                open("/tmp/report_cover_pdf.pdf", "rb"), strict=False), output)
        append_pdf(PdfFileReader(
            open("/tmp/main_content_pdf.pdf", "rb"), strict=False), output)
        if self.company_id and self.company_id.report_back_cover_pdf:
            append_pdf(PdfFileReader(
                open("/tmp/report_back_cover_pdf.pdf", "rb"), strict=False), output)
        output.write(open("/tmp/CombinedPages.pdf", "wb"))
        output_file = open("/tmp/CombinedPages.pdf", "rb")
        output_byte = output_file.read()
        attachment = self.env['ir.attachment'].create({
            'name': report_name,
            'store_fname': report_name + '.pdf',
            'datas': base64.encodestring(output_byte),
            'res_model': 'project.task',
            'res_id': self.id,
            'type': 'binary',
            'url': 'url',
            'mimetype': 'application/pdf'})

        if self.company_id and self.company_id.report_cover_pdf:
            os.remove('/tmp/report_cover_pdf.pdf')
        os.remove('/tmp/main_content_pdf.pdf')
        if self.company_id and self.company_id.report_cover_pdf:
            os.remove('/tmp/report_back_cover_pdf.pdf')
        os.remove('/tmp/CombinedPages.pdf')
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document/%s' % str(attachment.id),
            'target': 'blank'
        }
