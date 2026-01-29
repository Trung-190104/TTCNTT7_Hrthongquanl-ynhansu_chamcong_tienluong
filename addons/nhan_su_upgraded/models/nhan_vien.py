# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ho_va_ten'
    _order = 'ten asc, tuoi desc'

    # Thông tin cơ bản
    ma_dinh_danh = fields.Char("Mã định danh", required=True, tracking=True)
    ho_ten_dem = fields.Char("Họ tên đệm", required=True, tracking=True)
    ten = fields.Char("Tên", required=True, tracking=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True, tracking=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True, tracking=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)
    gioi_tinh = fields.Selection(
        [
            ("Nam", "Nam"),
            ("Nữ", "Nữ")
        ],
        string="Giới tính",
        required=True,
        tracking=True
    )
    que_quan = fields.Char("Quê quán", required=True)
    email = fields.Char("Email", required=True, tracking=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True, tracking=True)
    anh = fields.Binary("Ảnh")
    
    # Thông tin công việc
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", compute="_compute_cong_tac", store=True, tracking=True)
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", compute="_compute_cong_tac", store=True, tracking=True)
    
    # Trạng thái làm việc
    trang_thai_lam_viec = fields.Selection([
        ('dang_lam_viec', 'Đang làm việc'),
        ('nghi_viec', 'Nghỉ việc'),
        ('nghi_thai_san', 'Nghỉ thai sản'),
        ('tam_nghi', 'Tạm nghỉ'),
    ], string="Trạng thái làm việc", default='dang_lam_viec', required=True, tracking=True)
    
    ngay_vao_lam = fields.Date("Ngày vào làm", tracking=True)
    ngay_nghi_viec = fields.Date("Ngày nghỉ việc", tracking=True)
    
    # Quan hệ One2many
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
    
    # Quan hệ với các model mới
    danh_gia_ids = fields.One2many(
        "danh_gia_nhan_vien",
        inverse_name="nhan_vien_id",
        string="Lịch sử đánh giá"
    )
    hop_dong_ids = fields.One2many(
        "hop_dong_lao_dong",
        inverse_name="nhan_vien_id",
        string="Hợp đồng lao động"
    )
    tai_san_ids = fields.One2many(
        "tai_san_cap_phat",
        inverse_name="nhan_vien_id",
        string="Tài sản được cấp phát"
    )
    
    # Computed fields cho thống kê
    hop_dong_hien_tai_id = fields.Many2one(
        "hop_dong_lao_dong",
        string="Hợp đồng hiện tại",
        compute="_compute_hop_dong_hien_tai",
        store=True
    )
    diem_danh_gia_trung_binh = fields.Float(
        "Điểm đánh giá TB",
        compute="_compute_diem_danh_gia_trung_binh",
        store=True
    )
    so_tai_san_dang_giu = fields.Integer(
        "Số tài sản đang giữ",
        compute="_compute_so_tai_san_dang_giu",
        store=True
    )
    
    # Thêm ảnh khuôn mặt cho nhận diện (dùng cho chấm công)
    anh_khuon_mat = fields.Binary("Ảnh khuôn mặt (cho nhận diện)", help="Ảnh này sẽ được dùng cho hệ thống nhận diện khuôn mặt khi chấm công")
    
    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self): 
        for record in self:
            if record.ngay_sinh:
                year_now = datetime.now().year  
                record.tuoi = year_now - record.ngay_sinh.year 
    
    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_va_ten(self):
        for record in self:
            record.ho_va_ten = (record.ho_ten_dem or '') + ' ' + (record.ten or '')
            
    @api.constrains("tuoi")
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được nhỏ hơn 18")
    
    @api.depends("lich_su_cong_tac_ids", "lich_su_cong_tac_ids.trang_thai")
    def _compute_cong_tac(self):
        for record in self:
            if record.lich_su_cong_tac_ids:
                lich_su = self.env['lich_su_cong_tac'].search([
                    ('nhan_vien_id', '=', record.id),
                    ('loai_chuc_vu', '=', "Chính"),
                    ('trang_thai', '=', "Đang giữ")
                ], limit=1)
                record.chuc_vu_id = lich_su.chuc_vu_id.id if lich_su else False
                record.phong_ban_id = lich_su.phong_ban_id.id if lich_su else False
            else:
                record.chuc_vu_id = False
                record.phong_ban_id = False
    
    @api.depends("hop_dong_ids", "hop_dong_ids.trang_thai")
    def _compute_hop_dong_hien_tai(self):
        for record in self:
            hop_dong = self.env['hop_dong_lao_dong'].search([
                ('nhan_vien_id', '=', record.id),
                ('trang_thai', '=', 'dang_hieu_luc')
            ], limit=1)
            record.hop_dong_hien_tai_id = hop_dong.id if hop_dong else False
    
    @api.depends("danh_gia_ids", "danh_gia_ids.diem_tong")
    def _compute_diem_danh_gia_trung_binh(self):
        for record in self:
            if record.danh_gia_ids:
                tong_diem = sum(record.danh_gia_ids.mapped('diem_tong'))
                record.diem_danh_gia_trung_binh = tong_diem / len(record.danh_gia_ids)
            else:
                record.diem_danh_gia_trung_binh = 0.0
    
    @api.depends("tai_san_ids", "tai_san_ids.trang_thai")
    def _compute_so_tai_san_dang_giu(self):
        for record in self:
            record.so_tai_san_dang_giu = len(record.tai_san_ids.filtered(
                lambda t: t.trang_thai == 'dang_su_dung'
            ))
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if '@' not in record.email:
                    raise ValidationError("Email không hợp lệ!")
                # Kiểm tra trùng email
                duplicate = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(f"Email {record.email} đã được sử dụng bởi nhân viên {duplicate.ho_va_ten}!")
    
    @api.constrains('ma_dinh_danh')
    def _check_ma_dinh_danh(self):
        for record in self:
            if record.ma_dinh_danh:
                duplicate = self.search([
                    ('ma_dinh_danh', '=', record.ma_dinh_danh),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(f"Mã định danh {record.ma_dinh_danh} đã tồn tại!")
