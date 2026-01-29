from odoo import models, fields, api
from datetime import date

class LichSuCongTac(models.Model):
    _name = "lich_su_cong_tac"
    _description = "Bảng chứa thông tin lịch sử công tác"
    _rec_name = "nhan_vien_id"
    
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", required=True)
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", required=True)
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"),
            ("Kiêm nhiệm", "Kiêm nhiệm"),
        ],
        string="Loại chức vụ", default="Chính", 
        required=True
    )
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)

    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    trang_thai = fields.Selection(
        [
            ("Đang giữ", "Đang giữ"),
            ("Đã kết thúc", "Đã kết thúc"),
        ],
        string="Trạng thái",
        compute="_compute_trang_thai",
        store=True
    )

    @api.depends("ngay_ket_thuc")
    def _compute_trang_thai(self):
        today = date.today()
        for record in self:
            if not record.ngay_ket_thuc or record.ngay_ket_thuc >= today:
                record.trang_thai = "Đang giữ"
            else:
                record.trang_thai = "Đã kết thúc"
