from odoo import models, fields, api
from datetime import datetime
class ChungChiBangCap(models.Model):
    _name = 'danh_sach_chung_chi_bang_cap'
    _description = 'Bảng chứa thông tin danh sách chứng chỉ, bằng cấp'
    _rec_name = "nhan_vien_id"
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    chung_chi_id = fields.Many2one("chung_chi_bang_cap", string="Tên chứng chỉ", required=True)
    loai_chung_chi = fields.Selection(
        [
            ("Bằng đại học", "Bằng đại học"),
            ("Chứng chỉ Tiếng Anh", "Chứng chỉ Tiếng Anh"),
            ("Chứng chỉ tin học văn phòng", "Chứng chỉ tin học văn phòng"),
        ],
        string="Loại chứng chỉ", required=True
    )
    ngay_cap = fields.Date("Ngày cấp", required=True)
    noi_cap = fields.Char("Nơi cấp")