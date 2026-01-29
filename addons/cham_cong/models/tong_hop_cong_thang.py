# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
import calendar
from odoo.exceptions import ValidationError

class TongHopCongThang(models.Model):
    _name = 'tong_hop_cong_thang'
    _description = 'Tổng hợp công tháng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_tong_hop'
    _order = 'thang desc, nam desc'

    ma_tong_hop = fields.Char("Mã tổng hợp", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", related='nhan_vien_id.phong_ban_id', store=True)
    
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", required=True, default=lambda self: str(datetime.now().month), tracking=True)
    
    nam = fields.Char("Năm", required=True, default=lambda self: str(datetime.now().year), tracking=True)
    
    # Thống kê chấm công
    so_ngay_di_lam = fields.Integer("Số ngày đi làm", compute='_compute_thong_ke', store=True)
    so_ngay_di_muon = fields.Integer("Số ngày đi muộn", compute='_compute_thong_ke', store=True)
    so_ngay_ve_som = fields.Integer("Số ngày về sớm", compute='_compute_thong_ke', store=True)
    so_ngay_vang_mat = fields.Integer("Số ngày vắng mặt", compute='_compute_thong_ke', store=True)
    so_ngay_vang_co_phep = fields.Integer("Số ngày nghỉ có phép", compute='_compute_thong_ke', store=True)
    
    tong_phut_di_muon = fields.Float("Tổng phút đi muộn", compute='_compute_thong_ke', store=True)
    tong_phut_ve_som = fields.Float("Tổng phút về sớm", compute='_compute_thong_ke', store=True)
    
    # Tỷ lệ
    ty_le_di_lam_dung_gio = fields.Float("Tỷ lệ đi làm đúng giờ (%)", 
                                          compute='_compute_ty_le', store=True)
    ty_le_vang_mat = fields.Float("Tỷ lệ vắng mặt (%)", compute='_compute_ty_le', store=True)
    
    # Xếp loại
    xep_loai = fields.Selection([
        ('xuat_sac', 'Xuất sắc'),
        ('tot', 'Tốt'),
        ('trung_binh', 'Trung bình'),
        ('yeu', 'Yếu'),
    ], string="Xếp loại", compute='_compute_xep_loai', store=True, tracking=True)
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('locked', 'Đã khóa'),
    ], string="Trạng thái", default='draft', required=True, tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ma_tong_hop', 'New') == 'New':
            nhan_vien = self.env['nhan_vien'].browse(vals.get('nhan_vien_id'))
            thang = vals.get('thang')
            nam = vals.get('nam')
            vals['ma_tong_hop'] = f"THC-{nhan_vien.ma_dinh_danh}-{thang}/{nam}"
        return super(TongHopCongThang, self).create(vals)
    
    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_thong_ke(self):
        for record in self:
            if not record.nhan_vien_id or not record.thang or not record.nam:
                record.so_ngay_di_lam = 0
                record.so_ngay_di_muon = 0
                record.so_ngay_ve_som = 0
                record.so_ngay_vang_mat = 0
                record.so_ngay_vang_co_phep = 0
                record.tong_phut_di_muon = 0
                record.tong_phut_ve_som = 0
                continue
            
            # Tìm tất cả bản ghi chấm công trong tháng
            thang_int = int(record.thang)
            nam_int = int(record.nam)
            ngay_dau = date(nam_int, thang_int, 1)
            ngay_cuoi = date(nam_int, thang_int, calendar.monthrange(nam_int, thang_int)[1])
            
            cham_cong_records = self.env['bang_cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', ngay_dau),
                ('ngay_cham_cong', '<=', ngay_cuoi)
            ])
            
            # Đếm theo trạng thái
            # Số ngày đi làm = TỔNG SỐ NGÀY có chấm công (không trùng lặp)
            # Bất kể đi làm đúng giờ, đi muộn, về sớm hay cả hai
            ngay_di_lam_records = cham_cong_records.filtered(
                lambda r: r.trang_thai in ['di_lam', 'di_muon', 've_som', 'di_muon_ve_som']
            )
            record.so_ngay_di_lam = len(ngay_di_lam_records)
            
            # Đếm số ngày đi muộn (bao gồm cả đi muộn và về sớm)
            record.so_ngay_di_muon = len(cham_cong_records.filtered(
                lambda r: r.trang_thai in ['di_muon', 'di_muon_ve_som']
            ))
            
            # Đếm số ngày về sớm (bao gồm cả đi muộn và về sớm)
            record.so_ngay_ve_som = len(cham_cong_records.filtered(
                lambda r: r.trang_thai in ['ve_som', 'di_muon_ve_som']
            ))
            
            record.so_ngay_vang_mat = len(cham_cong_records.filtered(
                lambda r: r.trang_thai == 'vang_mat'
            ))
            record.so_ngay_vang_co_phep = len(cham_cong_records.filtered(
                lambda r: r.trang_thai == 'vang_mat_co_phep'
            ))
            
            # Tổng phút đi muộn và về sớm
            record.tong_phut_di_muon = sum(cham_cong_records.mapped('phut_di_muon'))
            record.tong_phut_ve_som = sum(cham_cong_records.mapped('phut_ve_som'))
    
    @api.depends('so_ngay_di_lam', 'so_ngay_di_muon', 'so_ngay_vang_mat', 'thang', 'nam')
    def _compute_ty_le(self):
        for record in self:
            if not record.thang or not record.nam:
                record.ty_le_di_lam_dung_gio = 0
                record.ty_le_vang_mat = 0
                continue
                
            # Tổng số ngày làm việc trong tháng (giả sử 22 ngày)
            tong_ngay_lam_viec = 22
            
            if tong_ngay_lam_viec > 0:
                # Tỷ lệ đi làm đúng giờ
                record.ty_le_di_lam_dung_gio = (record.so_ngay_di_lam / tong_ngay_lam_viec) * 100
                # Tỷ lệ vắng mặt
                record.ty_le_vang_mat = (record.so_ngay_vang_mat / tong_ngay_lam_viec) * 100
            else:
                record.ty_le_di_lam_dung_gio = 0
                record.ty_le_vang_mat = 0
    
    @api.depends('ty_le_di_lam_dung_gio', 'ty_le_vang_mat', 'so_ngay_di_muon')
    def _compute_xep_loai(self):
        for record in self:
            # Logic xếp loại
            if record.ty_le_di_lam_dung_gio >= 95 and record.ty_le_vang_mat <= 2:
                record.xep_loai = 'xuat_sac'
            elif record.ty_le_di_lam_dung_gio >= 85 and record.ty_le_vang_mat <= 5:
                record.xep_loai = 'tot'
            elif record.ty_le_di_lam_dung_gio >= 70 and record.ty_le_vang_mat <= 10:
                record.xep_loai = 'trung_binh'
            else:
                record.xep_loai = 'yeu'
    
    @api.constrains('nhan_vien_id', 'thang', 'nam')
    def _check_unique_thang(self):
        for record in self:
            duplicate = self.search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('thang', '=', record.thang),
                ('nam', '=', record.nam),
                ('id', '!=', record.id)
            ], limit=1)
            if duplicate:
                raise ValidationError(
                    f"Đã tồn tại bản tổng hợp công tháng {record.thang}/{record.nam} "
                    f"cho nhân viên {record.nhan_vien_id.ho_va_ten}!"
                )
    
    def action_tinh_lai(self):
        """Tính lại thống kê"""
        self._compute_thong_ke()
        self._compute_ty_le()
        self._compute_xep_loai()
    
    def action_xac_nhan(self):
        """Xác nhận tổng hợp"""
        self.write({'trang_thai': 'confirmed'})
    
    def action_khoa(self):
        """Khóa tổng hợp (không cho sửa nữa)"""
        self.write({'trang_thai': 'locked'})
    
    def action_mo_khoa(self):
        """Mở khóa"""
        self.write({'trang_thai': 'draft'})
    
    @api.model
    def action_tao_tong_hop_hang_loat(self, thang, nam):
        """Tạo tổng hợp công cho tất cả nhân viên trong tháng"""
        nhan_viens = self.env['nhan_vien'].search([
            ('trang_thai_lam_viec', '=', 'dang_lam_viec')
        ])
        
        for nv in nhan_viens:
            # Kiểm tra đã tồn tại chưa
            existing = self.search([
                ('nhan_vien_id', '=', nv.id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ], limit=1)
            
            if not existing:
                self.create({
                    'nhan_vien_id': nv.id,
                    'thang': thang,
                    'nam': nam,
                })
