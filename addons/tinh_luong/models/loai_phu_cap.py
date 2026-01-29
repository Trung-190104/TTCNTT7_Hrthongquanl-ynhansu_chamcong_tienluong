# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LoaiPhuCap(models.Model):
    _name = 'loai_phu_cap'
    _description = 'Loại phụ cấp'
    _rec_name = 'ten_phu_cap'
    _order = 'ten_phu_cap'

    ma_phu_cap = fields.Char("Mã phụ cấp", required=True)
    ten_phu_cap = fields.Char("Tên phụ cấp", required=True)
    
    loai = fields.Selection([
        ('co_dinh', 'Cố định'),
        ('theo_ngay', 'Theo ngày công'),
        ('theo_gio', 'Theo giờ làm'),
        ('theo_hieu_suat', 'Theo hiệu suất'),
    ], string="Loại tính", default='co_dinh', required=True)
    
    muc_phu_cap_mac_dinh = fields.Float("Mức phụ cấp mặc định")
    
    tinh_bao_hiem = fields.Boolean("Tính vào lương đóng bảo hiểm", default=False,
                                    help="Phụ cấp này có được tính vào lương đóng BHXH không")
    tinh_thue = fields.Boolean("Tính vào thu nhập chịu thuế", default=True,
                                help="Phụ cấp này có chịu thuế TNCN không")
    
    mo_ta = fields.Text("Mô tả")
    active = fields.Boolean("Hoạt động", default=True)
    
    # Thống kê
    so_nhan_vien = fields.Integer("Số nhân viên được hưởng", compute='_compute_so_nhan_vien')
    
    @api.depends('ma_phu_cap')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = self.env['phu_cap_nhan_vien'].search_count([
                ('loai_phu_cap_id', '=', record.id),
                ('active', '=', True)
            ])
    
    _sql_constraints = [
        ('ma_phu_cap_unique', 'unique(ma_phu_cap)', 'Mã phụ cấp đã tồn tại!'),
    ]
