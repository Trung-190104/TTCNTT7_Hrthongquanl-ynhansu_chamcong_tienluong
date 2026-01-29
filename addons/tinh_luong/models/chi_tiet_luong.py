# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChiTietLuong(models.Model):
    _name = 'chi_tiet_luong'
    _description = 'Chi tiết các khoản thu nhập và khấu trừ'
    _rec_name = 'ten_khoan'
    _order = 'loai, ten_khoan'

    bang_luong_id = fields.Many2one('bang_luong', string="Bảng lương", required=True, ondelete='cascade')
    
    loai = fields.Selection([
        ('phu_cap', 'Phụ cấp'),
        ('thuong', 'Thưởng'),
        ('tang_ca', 'Tăng ca'),
        ('thu_nhap_khac', 'Thu nhập khác'),
        ('phat', 'Phạt'),
        ('khau_tru_khac', 'Khấu trừ khác'),
    ], string="Loại", required=True)
    
    # Dùng cho phụ cấp
    loai_phu_cap_id = fields.Many2one('loai_phu_cap', string="Loại phụ cấp")
    
    ten_khoan = fields.Char("Tên khoản", required=True)
    so_tien = fields.Float("Số tiền", required=True)
    
    # Dùng để tính toán chi tiết
    so_luong = fields.Float("Số lượng", help="VD: số giờ tăng ca, số ngày...")
    don_vi = fields.Char("Đơn vị", help="VD: giờ, ngày, lần...")
    don_gia = fields.Float("Đơn giá")
    
    ghi_chu = fields.Text("Ghi chú")
    
    @api.model
    def create(self, vals):
        """Auto-set loai from context if not provided"""
        if 'loai' not in vals and self.env.context.get('default_loai'):
            vals['loai'] = self.env.context.get('default_loai')
        return super(ChiTietLuong, self).create(vals)
    
    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.loai in ['phu_cap', 'thuong', 'tang_ca', 'thu_nhap_khac']:
                # Các khoản thu nhập phải dương
                if record.so_tien < 0:
                    raise ValidationError("Số tiền thu nhập không được âm!")
            elif record.loai in ['phat', 'khau_tru_khac']:
                # Các khoản khấu trừ phải dương (sẽ trừ đi khi tính)
                if record.so_tien < 0:
                    raise ValidationError("Số tiền khấu trừ không được âm!")
    
    @api.onchange('so_luong', 'don_gia')
    def _onchange_tinh_so_tien(self):
        """Tự động tính số tiền = số lượng x đơn giá"""
        if self.so_luong and self.don_gia:
            self.so_tien = self.so_luong * self.don_gia
