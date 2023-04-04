from . import wizards
from . import reports

from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError

def pre_init_check(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    rpt_id =  env['ir.module.module'].search([('name', '=', 'report_xlsx')])
    if rpt_id:
        if not rpt_id.state == 'installed':
            raise UserError('This module depends on "Base report xlsx".Please install it from your Apps')
    else:
        raise UserError('This module depends on "Base report xlsx". Use this link to download the module https://apps.odoo.com/apps/modules/14.0/report_xlsx/')