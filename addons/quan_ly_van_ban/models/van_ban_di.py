from odoo import models, fields, api
from datetime import datetime

# văn bản đi: số hiệu, tên văn bản, số văn bản đi, năm, nơi đến
class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin văn bản đi'
    _rec_name = 'ten_van_ban'

    ma_van_ban_di = fields.Char("Mã văn bản đi", required=True)
    so_hieu_van_ban = fields.Char("Số hiệu văn bản", required=True)
    ten_van_ban = fields.Char("Tên văn bản", required=True)
    nam = fields.Char("Năm", compute="_compute_tinh_nam", store=True)
    so_van_ban_di = fields.Integer("Số văn bản", required=True)
    noi_nhan = fields.Char("Nơi nhận", required=True)
    ngay_di = fields.Date("Ngày đi", required=True)
    loai_van_ban_id = fields.Many2one('loai_van_ban', string="Loại văn bản", required=True)
    
    @api.depends("ngay_di")
    def _compute_tinh_nam(self): 
        for record in self:
            if record.ngay_di:
                record.nam = datetime.now().year