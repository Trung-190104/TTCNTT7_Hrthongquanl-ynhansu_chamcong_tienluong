# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class DangKyCaLamTheoNgay(models.Model):
    _name = 'dang_ky_ca_lam_theo_ngay'
    _description = "Đăng ký ca làm theo ngày"
    _rec_name = 'ma_dot_ngay'
    _order = 'dot_dang_ky_id desc, ngay_lam asc'

    ma_dot_ngay = fields.Char("Mã đợt ngày", default='/', copy=False)
    dot_dang_ky_id = fields.Many2one('dot_dang_ky', string="Đợt đăng ký", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_lam = fields.Date(string="Ngày làm", required=True)
    ca_lam = fields.Selection([
        ("", ""),
        ("Sáng", "Sáng"),
        ("Chiều", "Chiều"),
        ("Cả ngày", "Cả Ngày"),
    ], string="Ca làm", default="")

    @api.model
    def create(self, vals):
        # Tự động tạo mã nếu là /
        if vals.get('ma_dot_ngay', '/') == '/':
            dot = self.env['dot_dang_ky'].browse(vals.get('dot_dang_ky_id'))
            nv = self.env['nhan_vien'].browse(vals.get('nhan_vien_id'))
            ngay = vals.get('ngay_lam')
            if dot and nv and ngay:
                ngay_str = datetime.strptime(str(ngay), '%Y-%m-%d').strftime('%Y%m%d')
                vals['ma_dot_ngay'] = f"{dot.ma_dot}_{nv.ma_dinh_danh}_{ngay_str}"
            else:
                vals['ma_dot_ngay'] = f"DK_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return super(DangKyCaLamTheoNgay, self).create(vals)

    @api.constrains('ngay_lam', 'dot_dang_ky_id')
    def _check_ngay_lam(self):
        for record in self:
            if record.ngay_lam and record.dot_dang_ky_id:
                if record.ngay_lam < record.dot_dang_ky_id.ngay_bat_dau or record.ngay_lam > record.dot_dang_ky_id.ngay_ket_thuc:
                    raise ValidationError(f'Ngày làm phải nằm trong khoảng thời gian của đợt đăng ký (từ {record.dot_dang_ky_id.ngay_bat_dau} đến {record.dot_dang_ky_id.ngay_ket_thuc})')

    @api.constrains('nhan_vien_id', 'dot_dang_ky_id')
    def _check_nhan_vien_in_dot_dang_ky(self):
        for record in self:
            if record.nhan_vien_id not in record.dot_dang_ky_id.nhan_vien_ids:
                raise ValidationError(f'Nhân viên {record.nhan_vien_id.ho_va_ten} không thuộc đợt đăng ký này!')
    
    _sql_constraints = [
        ('unique_nhan_vien_ngay', 'unique(nhan_vien_id, ngay_lam)', 
         'Nhân viên đã đăng ký ca làm cho ngày này rồi!')
    ]
