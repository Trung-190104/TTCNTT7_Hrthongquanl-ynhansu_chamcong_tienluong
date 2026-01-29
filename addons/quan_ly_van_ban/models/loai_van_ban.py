from odoo import models, fields, api

# văn bản đến: số hiệu, tên văn bản, số văn bản đến, nơi gửi, mức độ khẩn (hỏa tốc, thượng khẩn, khẩn)
class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Bảng chứa thông tin các loại văn bản'
    _rec_name = 'ten_loai_van_ban'

    ma_loai_van_ban = fields.Char("Mã loại văn bản", required=True)
    ten_loai_van_ban = fields.Char("Tên loại văn bản", required=True)
    
    van_ban_den_ids = fields.One2many(
        "van_ban_den", 
        inverse_name="loai_van_ban_id", 
        string="Danh sách văn bản đến"
    )
    
    van_ban_di_ids = fields.One2many(
        "van_ban_di", 
        inverse_name="loai_van_ban_id", 
        string="Danh sách văn bản đi"
    )