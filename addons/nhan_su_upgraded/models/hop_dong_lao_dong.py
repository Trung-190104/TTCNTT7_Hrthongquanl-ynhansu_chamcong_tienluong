# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp đồng lao động'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'so_hop_dong'
    _order = 'ngay_ky desc'

    # Thông tin hợp đồng
    so_hop_dong = fields.Char("Số hợp đồng", required=True, copy=False, tracking=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", related='nhan_vien_id.phong_ban_id', store=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", related='nhan_vien_id.chuc_vu_id', store=True)
    
    # Loại hợp đồng
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('co_thoi_han_1_nam', 'Có thời hạn 1 năm'),
        ('co_thoi_han_3_nam', 'Có thời hạn 3 năm'),
        ('khong_thoi_han', 'Không thời hạn'),
        ('mua_vu', 'Mùa vụ'),
        ('hoc_viec', 'Học việc'),
    ], string="Loại hợp đồng", required=True, default='thu_viec', tracking=True)
    
    # Thời gian
    ngay_ky = fields.Date("Ngày ký", required=True, default=fields.Date.today, tracking=True)
    ngay_hieu_luc = fields.Date("Ngày hiệu lực", required=True, tracking=True)
    ngay_het_han = fields.Date("Ngày hết hạn", tracking=True)
    thoi_han_hop_dong = fields.Integer("Thời hạn (tháng)", compute='_compute_thoi_han', store=True)
    
    # Cảnh báo hết hạn
    so_ngay_con_lai = fields.Integer("Số ngày còn lại", compute='_compute_so_ngay_con_lai', store=True)
    canh_bao_het_han = fields.Boolean("Cảnh báo hết hạn", compute='_compute_canh_bao_het_han', store=True)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('dang_hieu_luc', 'Đang hiệu lực'),
        ('het_han', 'Hết hạn'),
        ('da_gia_han', 'Đã gia hạn'),
        ('da_cham_dut', 'Đã chấm dứt'),
    ], string="Trạng thái", default='nhap', required=True, tracking=True, compute='_compute_trang_thai', store=True)
    
    # Thông tin lương
    muc_luong_co_ban = fields.Float("Mức lương cơ bản", tracking=True)
    phu_cap = fields.Float("Phụ cấp", tracking=True)
    tong_thu_nhap = fields.Float("Tổng thu nhập", compute='_compute_tong_thu_nhap', store=True)
    
    # Nội dung hợp đồng
    vi_tri_cong_viec = fields.Char("Vị trí công việc", tracking=True)
    dia_diem_lam_viec = fields.Char("Địa điểm làm việc")
    mo_ta_cong_viec = fields.Text("Mô tả công việc")
    che_do_lam_viec = fields.Text("Chế độ làm việc")
    
    # Gia hạn/Chấm dứt
    hop_dong_cu_id = fields.Many2one('hop_dong_lao_dong', string="Hợp đồng cũ")
    hop_dong_moi_id = fields.Many2one('hop_dong_lao_dong', string="Hợp đồng mới (gia hạn)")
    ngay_cham_dut = fields.Date("Ngày chấm dứt")
    ly_do_cham_dut = fields.Text("Lý do chấm dứt")
    
    # File đính kèm
    file_hop_dong = fields.Binary("File hợp đồng")
    file_hop_dong_name = fields.Char("Tên file")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('ngay_hieu_luc', 'ngay_het_han')
    def _compute_thoi_han(self):
        for record in self:
            if record.ngay_hieu_luc and record.ngay_het_han:
                delta = record.ngay_het_han - record.ngay_hieu_luc
                record.thoi_han_hop_dong = int(delta.days / 30)
            else:
                record.thoi_han_hop_dong = 0
    
    @api.depends('muc_luong_co_ban', 'phu_cap')
    def _compute_tong_thu_nhap(self):
        for record in self:
            record.tong_thu_nhap = (record.muc_luong_co_ban or 0) + (record.phu_cap or 0)
    
    @api.depends('ngay_het_han')
    def _compute_so_ngay_con_lai(self):
        today = date.today()
        for record in self:
            if record.ngay_het_han and record.trang_thai == 'dang_hieu_luc':
                delta = record.ngay_het_han - today
                record.so_ngay_con_lai = delta.days
            else:
                record.so_ngay_con_lai = 0
    
    @api.depends('so_ngay_con_lai')
    def _compute_canh_bao_het_han(self):
        for record in self:
            # Cảnh báo khi còn 30 ngày hoặc ít hơn
            record.canh_bao_het_han = (0 < record.so_ngay_con_lai <= 30)
    
    @api.depends('ngay_hieu_luc', 'ngay_het_han', 'ngay_cham_dut', 'hop_dong_moi_id')
    def _compute_trang_thai(self):
        today = date.today()
        for record in self:
            if record.ngay_cham_dut:
                record.trang_thai = 'da_cham_dut'
            elif record.hop_dong_moi_id:
                record.trang_thai = 'da_gia_han'
            elif record.ngay_het_han and today > record.ngay_het_han:
                record.trang_thai = 'het_han'
            elif record.ngay_hieu_luc and today >= record.ngay_hieu_luc:
                record.trang_thai = 'dang_hieu_luc'
            else:
                record.trang_thai = 'nhap'
    
    @api.constrains('ngay_hieu_luc', 'ngay_het_han')
    def _check_ngay(self):
        for record in self:
            if record.ngay_het_han and record.ngay_hieu_luc:
                if record.ngay_het_han <= record.ngay_hieu_luc:
                    raise ValidationError("Ngày hết hạn phải sau ngày hiệu lực!")
    
    @api.constrains('nhan_vien_id', 'ngay_hieu_luc', 'ngay_het_han')
    def _check_hop_dong_trung(self):
        """Kiểm tra không được có 2 hợp đồng hiệu lực cùng lúc"""
        for record in self:
            if record.trang_thai == 'dang_hieu_luc':
                hop_dong_trung = self.search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('trang_thai', '=', 'dang_hieu_luc'),
                    ('id', '!=', record.id)
                ], limit=1)
                if hop_dong_trung:
                    raise ValidationError(
                        f"Nhân viên {record.nhan_vien_id.ho_va_ten} đang có hợp đồng hiệu lực "
                        f"(Số HĐ: {hop_dong_trung.so_hop_dong})!"
                    )
    
    def action_gia_han(self):
        """Tạo hợp đồng gia hạn"""
        self.ensure_one()
        return {
            'name': 'Gia hạn hợp đồng',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_nhan_vien_id': self.nhan_vien_id.id,
                'default_hop_dong_cu_id': self.id,
                'default_loai_hop_dong': self.loai_hop_dong,
                'default_muc_luong_co_ban': self.muc_luong_co_ban,
                'default_phu_cap': self.phu_cap,
            }
        }
    
    def action_cham_dut(self):
        """Chấm dứt hợp đồng"""
        self.ensure_one()
        return {
            'name': 'Chấm dứt hợp đồng',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'show_cham_dut': True}
        }
    
    @api.model
    def _cron_canh_bao_het_han_hop_dong(self):
        """Cron job: Gửi cảnh báo hợp đồng sắp hết hạn"""
        hop_dong_sap_het_han = self.search([
            ('canh_bao_het_han', '=', True),
            ('trang_thai', '=', 'dang_hieu_luc')
        ])
        
        for hop_dong in hop_dong_sap_het_han:
            # Tạo activity nhắc nhở
            hop_dong.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=f'Hợp đồng {hop_dong.so_hop_dong} sắp hết hạn',
                note=f'Hợp đồng của nhân viên {hop_dong.nhan_vien_id.ho_va_ten} '
                     f'sẽ hết hạn vào {hop_dong.ngay_het_han}. '
                     f'Còn {hop_dong.so_ngay_con_lai} ngày. '
                     f'Vui lòng xem xét gia hạn hoặc chấm dứt hợp đồng.',
                user_id=self.env.user.id,
            )
