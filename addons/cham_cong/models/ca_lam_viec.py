# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CaLamViec(models.Model):
    _name = 'ca_lam_viec'
    _description = 'Ca làm việc'
    _rec_name = 'ten_ca'
    _order = 'gio_bat_dau'

    ma_ca = fields.Char("Mã ca", required=True)
    ten_ca = fields.Selection([
        ("Sáng", "Sáng"),
        ("Chiều", "Chiều"),
        ("Cả ngày", "Cả ngày"),
        ("Ca đêm", "Ca đêm"),
        ("Ca xoay 1", "Ca xoay 1"),
        ("Ca xoay 2", "Ca xoay 2"),
        ("Ca 12 giờ", "Ca 12 giờ"),
    ], string="Tên ca", required=True)
    
    gio_bat_dau = fields.Char("Giờ bắt đầu", required=True, help="Định dạng HH:MM (VD: 08:00)")
    gio_ket_thuc = fields.Char("Giờ kết thúc", required=True, help="Định dạng HH:MM (VD: 17:00)")
    
    so_gio_lam_viec = fields.Float("Số giờ làm việc", compute='_compute_so_gio_lam_viec', store=True)
    
    mo_ta = fields.Text("Mô tả")
    active = fields.Boolean("Hoạt động", default=True)
    
    @api.depends('gio_bat_dau', 'gio_ket_thuc')
    def _compute_so_gio_lam_viec(self):
        from datetime import datetime
        for record in self:
            if record.gio_bat_dau and record.gio_ket_thuc:
                try:
                    gio_bd = datetime.strptime(record.gio_bat_dau, '%H:%M')
                    gio_kt = datetime.strptime(record.gio_ket_thuc, '%H:%M')
                    delta = gio_kt - gio_bd
                    record.so_gio_lam_viec = delta.total_seconds() / 3600
                except:
                    record.so_gio_lam_viec = 0
            else:
                record.so_gio_lam_viec = 0
    
    @api.constrains('gio_bat_dau', 'gio_ket_thuc')
    def _check_gio(self):
        from datetime import datetime
        for record in self:
            try:
                gio_bd = datetime.strptime(record.gio_bat_dau, '%H:%M')
                gio_kt = datetime.strptime(record.gio_ket_thuc, '%H:%M')
                if gio_kt <= gio_bd:
                    raise ValidationError("Giờ kết thúc phải sau giờ bắt đầu!")
            except ValueError:
                raise ValidationError("Định dạng giờ không hợp lệ! Vui lòng nhập theo định dạng HH:MM (VD: 08:00)")
    
    _sql_constraints = [
        ('ma_ca_unique', 'unique(ma_ca)', 'Mã ca đã tồn tại!'),
    ]
