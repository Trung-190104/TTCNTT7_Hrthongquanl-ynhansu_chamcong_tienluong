# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ThueTNCNBac(models.Model):
    _name = 'thue_tncn_bac'
    _description = 'Bậc thuế thu nhập cá nhân'
    _rec_name = 'ten_bac'
    _order = 'bac asc'

    bac = fields.Integer("Bậc", required=True)
    ten_bac = fields.Char("Tên bậc", compute='_compute_ten_bac', store=True)
    
    thu_nhap_tu = fields.Float("Thu nhập từ (triệu/tháng)", required=True)
    thu_nhap_den = fields.Float("Thu nhập đến (triệu/tháng)")
    
    thue_suat = fields.Float("Thuế suất (%)", required=True)
    
    ghi_chu = fields.Text("Ghi chú")
    active = fields.Boolean("Hoạt động", default=True)
    
    @api.depends('bac', 'thu_nhap_tu', 'thu_nhap_den', 'thue_suat')
    def _compute_ten_bac(self):
        for record in self:
            if record.thu_nhap_den and record.thu_nhap_den > 0:
                record.ten_bac = f"Bậc {record.bac}: {record.thu_nhap_tu} - {record.thu_nhap_den} triệu ({record.thue_suat}%)"
            else:
                record.ten_bac = f"Bậc {record.bac}: Trên {record.thu_nhap_tu} triệu ({record.thue_suat}%)"
    
    @api.constrains('thu_nhap_tu', 'thu_nhap_den')
    def _check_thu_nhap(self):
        for record in self:
            if record.thu_nhap_den and record.thu_nhap_den > 0:
                if record.thu_nhap_den <= record.thu_nhap_tu:
                    raise ValidationError("Thu nhập đến phải lớn hơn thu nhập từ!")
    
    @api.constrains('thue_suat')
    def _check_thue_suat(self):
        for record in self:
            if record.thue_suat < 0 or record.thue_suat > 100:
                raise ValidationError("Thuế suất phải từ 0% đến 100%!")
    
    _sql_constraints = [
        ('bac_unique', 'unique(bac)', 'Bậc thuế đã tồn tại!'),
    ]
    
    @api.model
    def tinh_thue_tncn(self, thu_nhap_tinh_thue):
        """
        Tính thuế TNCN theo bậc thuế lũy tiến
        :param thu_nhap_tinh_thue: Thu nhập tính thuế sau khi trừ các khoản giảm trừ (triệu đồng)
        :return: Số tiền thuế phải nộp (triệu đồng)
        """
        if thu_nhap_tinh_thue <= 0:
            return 0
        
        bac_thue = self.search([('active', '=', True)], order='bac asc')
        
        tong_thue = 0
        thu_nhap_con_lai = thu_nhap_tinh_thue
        
        for bac in bac_thue:
            if thu_nhap_con_lai <= 0:
                break
            
            # Xác định khoảng thu nhập chịu thuế ở bậc này
            if bac.thu_nhap_den and bac.thu_nhap_den > 0:
                # Có cận trên
                khoang_chiu_thue = bac.thu_nhap_den - bac.thu_nhap_tu
                if thu_nhap_con_lai > khoang_chiu_thue:
                    # Thu nhập còn lại nhiều hơn khoảng này
                    thue_bac_nay = khoang_chiu_thue * bac.thue_suat / 100
                    thu_nhap_con_lai -= khoang_chiu_thue
                else:
                    # Thu nhập còn lại ít hơn hoặc bằng khoảng này
                    thue_bac_nay = thu_nhap_con_lai * bac.thue_suat / 100
                    thu_nhap_con_lai = 0
            else:
                # Không có cận trên (bậc cuối cùng)
                thue_bac_nay = thu_nhap_con_lai * bac.thue_suat / 100
                thu_nhap_con_lai = 0
            
            tong_thue += thue_bac_nay
        
        return tong_thue
