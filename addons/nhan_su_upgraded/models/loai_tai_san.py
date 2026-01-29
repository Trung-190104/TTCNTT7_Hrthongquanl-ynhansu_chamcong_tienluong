# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LoaiTaiSan(models.Model):
    _name = 'loai_tai_san'
    _description = 'Loại tài sản'
    _rec_name = 'ten_loai'
    _order = 'ten_loai'

    ma_loai = fields.Char("Mã loại", required=True)
    ten_loai = fields.Char("Tên loại", required=True)
    mo_ta = fields.Text("Mô tả")
    
    # Thống kê
    tai_san_ids = fields.One2many('tai_san_cap_phat', 'loai_tai_san_id', string="Danh sách tài sản")
    so_luong_tai_san = fields.Integer("Số lượng tài sản", compute='_compute_so_luong', store=True)
    
    @api.depends('tai_san_ids')
    def _compute_so_luong(self):
        for record in self:
            record.so_luong_tai_san = len(record.tai_san_ids)
    
    _sql_constraints = [
        ('ma_loai_unique', 'unique(ma_loai)', 'Mã loại tài sản đã tồn tại!'),
    ]
