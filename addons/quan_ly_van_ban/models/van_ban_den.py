from odoo import models, fields, api
from datetime import datetime

# văn bản đến: số hiệu, tên văn bản, số văn bản đến, nơi gửi, mức độ khẩn (hỏa tốc, thượng khẩn, khẩn)
class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa thông tin văn bản đến'
    _rec_name = 'ten_van_ban'

    ma_van_ban_den = fields.Char("Mã văn bản đến", required=True)
    so_hieu_van_ban = fields.Char("Số hiệu văn bản", required=True)
    ten_van_ban = fields.Char("Tên văn bản", required=True)
    nam = fields.Char("Năm", compute="_compute_tinh_nam", store=True)
    so_van_ban_den = fields.Integer("Số văn bản", required=True)
    noi_gui = fields.Char("Nơi gửi", required=True)
    muc_do_khan = fields.Selection(
        [
            ("Hỏa tốc", "Hỏa tốc"),
            ("Thượng khẩn", "Thượng khẩn"),
            ("Khẩn", "Khẩn")
        ],
        string="Mức độ khẩn",
        required=True
    )
    ngay_den = fields.Date("Ngày đến", required=True)
    loai_van_ban_id = fields.Many2one('loai_van_ban', string="Loại văn bản", required=True)
    
    @api.depends("ngay_den")
    def _compute_tinh_nam(self): 
        for record in self:
            if record.ngay_den:
                record.nam = datetime.now().year