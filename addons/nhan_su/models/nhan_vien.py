from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'ten asc, tuoi desc'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)
    gioi_tinh = fields.Selection(
        [
            ("Nam", "Nam"),
            ("Nữ", "Nữ")
        ],
        string="Giới tính",
        required=True,
    )
    que_quan = fields.Char("Quê quán", required=True)
    email = fields.Char("Email", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    anh = fields.Binary("Ảnh")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", compute="_compute_cong_tac", store=True)
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", compute="_compute_cong_tac", store=True)
    
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name="nhan_vien_id", 
        string="Danh sách lịch sử công tác"
    )
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap",
        inverse_name="nhan_vien_id",
        string="Danh sách chứng chỉ bằng cấp"
    )
    
    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self): 
        for record in self:
            if record.ngay_sinh:  # Kiểm tra nếu trường ngay_sinh tồn tại
                year_now = datetime.now().year  
                record.tuoi = year_now - record.ngay_sinh.year 
    
    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_va_ten(self):
        for record in self:
            record.ho_va_ten = (record.ho_ten_dem or '') + ' ' + (record.ten or '')
            
    @api.constrains("tuoi")
    def _check_tuoi(self):
        for record in self: # self là tập hợp tất cả bản ghi, record là bản ghi hiện tại
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được nhỏ hơn 18")
    
    @api.depends("lich_su_cong_tac_ids")
    def _compute_cong_tac(self):
        for record in self:
            if record.lich_su_cong_tac_ids:
                lich_su = self.env['lich_su_cong_tac'].search([
                    ('nhan_vien_id', '=', record.id),
                    ('loai_chuc_vu', '=', "Chính"),
                    ('trang_thai', '=', "Đang giữ")  # Kiểm tra giá trị chính xác trong DB
                ], limit=1)
                record.chuc_vu_id = lich_su.chuc_vu_id.id if lich_su else False
                record.phong_ban_id = lich_su.phong_ban_id.id if lich_su else False
