# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DanhGiaNhanVien(models.Model):
    _name = 'danh_gia_nhan_vien'
    _description = 'Đánh giá hiệu suất nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_danh_gia'
    _order = 'ngay_danh_gia desc'

    # Thông tin cơ bản
    ma_danh_gia = fields.Char("Mã đánh giá", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", related='nhan_vien_id.phong_ban_id', store=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", related='nhan_vien_id.chuc_vu_id', store=True)
    
    # Thời gian đánh giá
    ngay_danh_gia = fields.Date("Ngày đánh giá", required=True, default=fields.Date.today, tracking=True)
    ky_danh_gia = fields.Selection([
        ('thang', 'Tháng'),
        ('quy', 'Quý'),
        ('nam', 'Năm'),
    ], string="Kỳ đánh giá", required=True, default='thang', tracking=True)
    
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng")
    
    quy = fields.Selection([
        ('1', 'Quý 1'),
        ('2', 'Quý 2'),
        ('3', 'Quý 3'),
        ('4', 'Quý 4'),
    ], string="Quý")
    
    nam = fields.Char("Năm", required=True, default=lambda self: str(fields.Date.today().year))
    
    # Người đánh giá
    nguoi_danh_gia_id = fields.Many2one('res.users', string="Người đánh giá", 
                                         default=lambda self: self.env.user, required=True, tracking=True)
    
    # Các tiêu chí đánh giá (thang điểm 0-100)
    diem_kpi = fields.Float("Điểm KPI", help="Hoàn thành chỉ tiêu công việc (0-100)", tracking=True)
    diem_ky_nang = fields.Float("Điểm kỹ năng", help="Kỹ năng chuyên môn (0-100)", tracking=True)
    diem_thai_do = fields.Float("Điểm thái độ", help="Thái độ làm việc và tinh thần (0-100)", tracking=True)
    diem_dong_gop = fields.Float("Điểm đóng góp", help="Đóng góp cho tập thể (0-100)", tracking=True)
    diem_hoc_tap = fields.Float("Điểm học tập", help="Khả năng học hỏi và phát triển (0-100)", tracking=True)
    
    # Điểm tổng và xếp loại
    diem_tong = fields.Float("Điểm tổng", compute='_compute_diem_tong', store=True, tracking=True)
    xep_loai = fields.Selection([
        ('xuat_sac', 'Xuất sắc'),
        ('tot', 'Tốt'),
        ('trung_binh', 'Trung bình'),
        ('yeu', 'Yếu'),
    ], string="Xếp loại", compute='_compute_xep_loai', store=True, tracking=True)
    
    # Nhận xét
    diem_manh = fields.Text("Điểm mạnh")
    diem_yeu = fields.Text("Điểm yếu")
    ke_hoach_phat_trien = fields.Text("Kế hoạch phát triển")
    nhan_xet_chung = fields.Text("Nhận xét chung")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ], string="Trạng thái", default='nhap', required=True, tracking=True)
    
    ly_do_tu_choi = fields.Text("Lý do từ chối")
    
    @api.model
    def create(self, vals):
        if vals.get('ma_danh_gia', 'New') == 'New':
            vals['ma_danh_gia'] = self.env['ir.sequence'].next_by_code('danh_gia_nhan_vien') or 'New'
        return super(DanhGiaNhanVien, self).create(vals)
    
    @api.depends('diem_kpi', 'diem_ky_nang', 'diem_thai_do', 'diem_dong_gop', 'diem_hoc_tap')
    def _compute_diem_tong(self):
        for record in self:
            # Tính trung bình cộng các điểm
            diem_list = [
                record.diem_kpi or 0,
                record.diem_ky_nang or 0,
                record.diem_thai_do or 0,
                record.diem_dong_gop or 0,
                record.diem_hoc_tap or 0,
            ]
            record.diem_tong = sum(diem_list) / 5 if any(diem_list) else 0
    
    @api.depends('diem_tong')
    def _compute_xep_loai(self):
        for record in self:
            if record.diem_tong >= 90:
                record.xep_loai = 'xuat_sac'
            elif record.diem_tong >= 75:
                record.xep_loai = 'tot'
            elif record.diem_tong >= 50:
                record.xep_loai = 'trung_binh'
            else:
                record.xep_loai = 'yeu'
    
    @api.constrains('diem_kpi', 'diem_ky_nang', 'diem_thai_do', 'diem_dong_gop', 'diem_hoc_tap')
    def _check_diem(self):
        for record in self:
            for field_name in ['diem_kpi', 'diem_ky_nang', 'diem_thai_do', 'diem_dong_gop', 'diem_hoc_tap']:
                diem = getattr(record, field_name)
                if diem and (diem < 0 or diem > 100):
                    raise ValidationError(f"Điểm phải nằm trong khoảng 0-100!")
    
    def action_gui_duyet(self):
        """Gửi đánh giá để duyệt"""
        self.write({'trang_thai': 'cho_duyet'})
        # Có thể thêm logic gửi thông báo cho quản lý
    
    def action_duyet(self):
        """Duyệt đánh giá"""
        self.write({'trang_thai': 'da_duyet'})
    
    def action_tu_choi(self):
        """Từ chối đánh giá"""
        return {
            'name': 'Lý do từ chối',
            'type': 'ir.actions.act_window',
            'res_model': 'danh_gia_nhan_vien',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'show_tu_choi': True}
        }
    
    def action_quay_lai_nhap(self):
        """Đưa về trạng thái nháp"""
        self.write({'trang_thai': 'nhap', 'ly_do_tu_choi': False})
