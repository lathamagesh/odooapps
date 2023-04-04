import base64

import io

import time
from odoo import api, models, _
from datetime import datetime
# from xlsxwriter import worksheet


# import xlwt

try:
    from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
    from xlsxwriter.utility import xl_rowcol_to_cell
except ImportError:
    ReportXlsx = object

class ReportInventoryMovement(models.AbstractModel):
    _name = 'report.inventory_movement_report.inventory_movement'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        print(data)
        # code changed by jagadishmagesh1999@gmail.com
        sheet = workbook.add_worksheet('Inventory Movement Report')
        background_color = workbook.add_format({
            'align': 'left',
            'valign': 'top',
            "bg_color": "white",
            'border': 1
        })
        background_color_2 = workbook.add_format({"bg_color": "#FFFFFF" })
        algin_center = workbook.add_format({'align': 'center'})
        bold = workbook.add_format({'align': 'center', "bold": 1})

        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'left'})
        today_date = datetime.strftime(datetime.now(), "%d/%m/%Y")
        # d = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        merge_format_2 = workbook.add_format({
            'bold': 1,
            'border': 2,
            'align': 'center',
            'fg_color': 'fffbcc',
        })
        heading_1 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'fg_color': '00661a',
            'color': 'white',
        })

        heading_2 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'fg_color': 'cc0000',
            'color': 'white',
        })

        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 13)
        sheet.set_column('D:D', 13)
        sheet.set_column('E:E', 8)
        sheet.set_column('F:F', 17)
        sheet.set_column('G:G', 7)
        sheet.set_column('H:H', 17)
        sheet.set_column('I:I', 17)
        sheet.set_column('N:I', 30)
        sheet.set_column('K:I', 20)
        sheet.set_column('L:I', 20)
        sheet.set_column('M:I', 30)
        image_data = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        sheet.insert_image('A1:C1', "any_name.png", {'image_data': image_data, 'x_scale': 0.25, 'y_scale': 0.30})

        sheet.set_row(0, 30)
        heading = "Inventory Movement Report"
        sheet.merge_range('C1:G1', heading, bold)

        sheet.set_row(1, 60)
        heading_ ="From Date : " + data['date_from'] +"                                 "+ "To Date: " + data['date_to']+ "                                 "+"Report date: " + today_date + "          "+  "\n"
        heading_ += "Opening Balance : " + data['open_balance']+"                                "+ "Closing Balance : " + data['close_balance'] + "                         "+"Total Value: " + data["t_out"] +"\n\n"
        uid = self._context.get('uid')
        user = self.env['res.users'].browse(uid)
        print("current user name "+ user.name)
        heading_ += "                                                                                                                                                          "+" printed by : " + user.name
        # adm = self.env['res.users'].search([('partner_id', '=', 7)])
        # for rec in adm:
        #     if rec.partner_id.id == 7:
        #         print("name----------" + str(rec.name))
        #         heading_ += " printed by : " + rec.name

        sheet.merge_range('A2:I2', heading_, background_color)
        border = workbook.add_format({'border': 1,
                                      'align': 'center',"bg_color": "white",})
        row = 4
        col = 0
        sheet.set_row(0, 30)
        heading = data["product_name"] + " - Stock Movement & Valuation"
        sheet.set_row(3, 27)
        sheet.merge_range('A3:I3', heading, heading_1)

        # heading = data["product_name"] + " - Stock OUT"
        # sheet.merge_range('A10:I10', heading, heading_2)
        #
        # sheet.write(row, col, 'S.No', heading_1)
        # sheet.write(row, col + 1, 'Date', heading_1)
        # sheet.write(row, col + 2, 'Voucher Number', heading_1)
        # sheet.write(row, col + 3, 'Partner Name', heading_1)
        # sheet.write(row, col + 4, 'Quantity', heading_1)
        # sheet.write(row, col + 5, 'Source Location', heading_1)
        # sheet.write(row, col + 6, 'Destination', heading_1)
        # sheet.write(row, col + 7, 'Value', heading_1)
        # sheet.write(row, col + 8, 'Action', heading_1)
        #
        # sheet.write(row, col + 10, 'S.No', heading_2)
        # sheet.write(row, col + 11, 'Date', heading_2)
        # sheet.write(row, col + 12, 'Voucher Number', heading_2)
        # sheet.write(row, col + 13, 'Partner Name', heading_2)
        # sheet.write(row, col + 14, 'Quantity', heading_2)
        # sheet.write(row, col + 15, 'Source Location', heading_2)
        # sheet.write(row, col + 16, 'Destination', heading_2)
        # sheet.write(row, col + 17, 'Value', heading_2)
        # sheet.write(row, col + 18, 'Action', heading_2)
        sheet.write('A%s' % (row), 'S.No', heading_1)
        sheet.write('B%s' % (row), 'Date', heading_1)
        sheet.write('C%s' % (row), 'Voucher Number', heading_1)
        sheet.write('D%s' % (row), 'Partner Name', heading_1)
        sheet.write('E%s' % (row), 'Quantity', heading_1)
        sheet.write('H%s' % (row), 'Source Location', heading_1)
        sheet.write('I%s' % (row), 'Destination', heading_1)
        sheet.write('G%s' % (row), 'Value', heading_1)
        sheet.write('F%s' % (row), 'Action', heading_1)
        row += 1

        rev = row
        s_no = 1
        for stock in data['stock_in_values']:
            sheet.write('A%s' % (rev), s_no, border)
            sheet.write('B%s' % (rev), stock['date'], date_style)
            sheet.write('C%s' % (rev), stock['voucher_number'], border)
            if stock['location_id'] == "Inventory adjustment":
                sheet.write('C%s' % (rev), stock['inventory_ref'], border)
            # if stock['voucher_number'] == "Product Quantity Updated":
            #     sheet.write('F%s' % (rev), "Quantity Updated", border)
            sheet.write('D%s' % (rev), stock['partner_name'], border)
            sheet.write('E%s' % (rev), stock['qty'], border)
            sheet.write('H%s' % (rev), stock['location_id'], border)
            if stock['location_id'] == "Vendors":
                sheet.write('F%s' % (rev), "Purchased", border)
            if stock['location_id'] == "Production":
                sheet.write('F%s' % (rev), "Manufactured", border)
            if stock['location_id'] == "Inventory adjustment":
                sheet.write('F%s' % (rev), "Inventory addon", border)
            if stock['location_id'] == "Product Quantity Updated":
                sheet.write('F%s' % (rev), "Quantity Updated", border)
            sheet.write('I%s' % (rev), stock['location_dest_id'], border)
            # sheet.write(row, col + 5, stock['unit'], border)border
            rev += 1
            s_no +=1

        for cost in data['cost_in_values']:
            sheet.write('G%s' % (row), cost['value'], border)
            row += 1


        # for var in data['out_values']:
        #             sheet.write('G%s' % (row), var['value'], border)
        #             row +=1
        for var in data['out_values']:
                sheet.write('A%s' % (rev), s_no, border)
                sheet.write('B%s' % (rev), var['create_date'], algin_center)
                sheet.write('C%s' % (rev), var['stock_move'], border)
                if var['location_dest_id'] == "Inventory adjustment":
                    sheet.write('C%s' % (rev), var['inventory_move'], border)
                # if var['voucher_number'] == "Product Quantity Updated":
                #     sheet.write('C%s' % (rev), var['stock_move'], border)
                # if var['stock_move'] == sale:
                #     sheet.write('D%s' % (rev), stock['partner_name'])
                sheet.write('E%s' % (rev), var['quantity'], border)
                sheet.write('H%s' % (rev), var['location_id'], border)
                sheet.write('I%s' % (rev), var['location_dest_id'], border)
                if var['location_dest_id'] == "Customers":
                    sheet.write('F%s' % (rev), "Sold", border)
                if var['location_dest_id'] == "Production":
                    sheet.write('F%s' % (rev), "Manufacturing", border)
                if var['location_dest_id'] == "Inventory adjustment":
                    sheet.write('F%s' % (rev), "Inventory takeaway", border)
                if var['location_dest_id'] == "Scrap":
                    sheet.write('F%s' % (rev), "Scrap", border)
                if var['location_dest_id'] == "Product Quantity Updated":
                    sheet.write('F%s' % (rev), "Inventory takeaway", border)
                if var['location_dest_id'] == "Vendors":
                    sheet.write('F%s' % (rev), "Quantity Transfer", border)
                sheet.write('G%s' % (rev), var['value'], border)
                sheet.write('D%s' % (rev), var['partner_name'], border)
                rev += 1
                s_no += 1

        # for stock in data['stock_out_values']:
        #         sheet.write('D%s' % (row), stock['partner_name'], border)
        #         row += 1
        #         s_no += 1






        # row = 5
        # col = 7
        # for cost in data['cost_in_values']:
        #     sheet.write(row, col, cost['value'], border)
        #     row += 1
        #     col = 7
        #
        # row = 10
        # col = 0
        # s_no = 1
        # for stock in data['stock_out_values']:
        #     sheet.write(row, col, s_no, border)
        #     sheet.write(row, col + 1, stock['date'], border)
        #     sheet.write(row, col + 2, stock['voucher_number'], border)
        #     sheet.write(row, col + 3, stock['partner_name'], border)
        #     sheet.write(row, col + 4, stock['qty'], border)
        #     sheet.write(row, col + 5, stock['location_id'], border)
        #     sheet.write(row, col + 6, stock['location_dest_id'], border)
        #     if stock['location_dest_id'] == "Customers":
        #         sheet.write(row, col + 8, "Sold", border)
        #     if stock['location_dest_id'] == "Production":
        #         sheet.write(row, col + 8, "Manufacturing", border)
        #     if stock['location_dest_id'] == "Inventory adjustment":
        #         sheet.write(row, col + 8, "Inventory takeaway", border)
        #     if stock['location_dest_id'] == "Scrap":
        #         sheet.write(row, col + 8, "Scrap", border)
        #     if stock['voucher_number'] == "Product Quantity Updated":
        #         sheet.write(row, col + 8, "Inventory takeaway", border)
        #     row += 1
        #     col = 10
        #     s_no += 1
        #
        # row = 10
        # col = 7
        # for var in data['out_values']:
        #             sheet.write(row, col, var['value'], border)
        #             sheet.write(row, col+3, var['quantity'], border)
        #             row += 1
        #             col = 7


        #
        # row =5
        # col = 18
        # for var in data['unit_out_values']:
        #     sheet.write(row, col+1, var['unit'])
        #     row+=1
        #     col =14


        # for cost in data['unit_out_values']:
        #     sheet.write(row, col + 5, cost['unit'], border)
        #     row += 1
        #     col = 14

        # uid = self._context.get('uid')
        # user = self.env['res.users'].browse(uid)
        # print("current user name "+ user.name)

        # admin = self.env['mrp.production'].search([('production_location_id', '=', 15)])
        # for rev in admin:
        #     if rev.production_location_id.id == 15:
        #         print("user_name----------" + str(rev.order_prepared_by))
        #         # sheet.write(17, 1, rev.order_prepared_by)


