# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class PhuCapNhanVien(models.Model):
    _name = 'phu_cap_nhan_vien'
    _description = 'Phụ cấp của nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_phu_cap_nv'
    _order = 'ngay_ap_dung desc'

    ma_phu_cap_nv = fields.Char("Mã", required=True, copy=False, readonly=True, default='New')
    
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", 
                                    related='nhan_vien_id.phong_ban_id', store=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", 
                                  related='nhan_vien_id.chuc_vu_id', store=True)
    
    loai_phu_cap_id = fields.Many2one('loai_phu_cap', string="Loại phụ cấp", 
                                       required=True, tracking=True)
    
    muc_phu_cap = fields.Float("Mức phụ cấp", required=True, tracking=True)
    
    ngay_ap_dung = fields.Date("Ngày áp dụng", required=True, default=fields.Date.today, tracking=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc", tracking=True)
    
    trang_thai = fields.Selection([
        ('dang_ap_dung', 'Đang áp dụng'),
        ('het_hieu_luc', 'Hết hiệu lực'),
    ], string="Trạng thái", compute='_compute_trang_thai', store=True, tracking=True)
    
    ghi_chu = fields.Text("Ghi chú")
    active = fields.Boolean("Hoạt động", default=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ma_phu_cap_nv', 'New') == 'New':
            vals['ma_phu_cap_nv'] = self.env['ir.sequence'].next_by_code('phu_cap_nhan_vien') or 'New'
        return super(PhuCapNhanVien, self).create(vals)
    
    @api.depends('ngay_ap_dung', 'ngay_ket_thuc')
    def _compute_trang_thai(self):
        today = date.today()
        for record in self:
            if record.ngay_ket_thuc and today > record.ngay_ket_thuc:
                record.trang_thai = 'het_hieu_luc'
            elif record.ngay_ap_dung and today >= record.ngay_ap_dung:
                record.trang_thai = 'dang_ap_dung'
            else:
                record.trang_thai = 'het_hieu_luc'
    
    @api.constrains('ngay_ap_dung', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_ap_dung:
                if record.ngay_ket_thuc <= record.ngay_ap_dung:
                    raise ValidationError("Ngày kết thúc phải sau ngày áp dụng!")
    
    @api.constrains('muc_phu_cap')
    def _check_muc_phu_cap(self):
        for record in self:
            if record.muc_phu_cap < 0:
                raise ValidationError("Mức phụ cấp không được âm!")
    
    def action_ket_thuc(self):
        """Kết thúc phụ cấp"""
        self.write({
            'ngay_ket_thuc': date.today(),
            'active': False
        })
