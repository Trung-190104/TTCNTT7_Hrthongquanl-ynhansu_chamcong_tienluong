from odoo import models, fields, api

class ChungChiBangCap(models.Model):
    _name = 'chung_chi_bang_cap'
    _description = 'Bảng chứa thông tin chứng chỉ bằng cấp'
    _rec_name = 'ten_chung_chi'
    
    ma_chung_chi = fields.Char("Mã chứng chỉ", required=True)
    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    