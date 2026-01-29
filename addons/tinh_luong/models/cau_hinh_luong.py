# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CauHinhLuong(models.Model):
    _name = 'cau_hinh_luong'
    _description = 'Cấu hình tính lương'
    _rec_name = 'ten_cau_hinh'

    ten_cau_hinh = fields.Char("Tên cấu hình", default="Cấu hình tính lương", required=True)
    
    # Lương tối thiểu vùng
    luong_toi_thieu_vung_1 = fields.Float("Lương tối thiểu vùng 1", default=4680000)
    luong_toi_thieu_vung_2 = fields.Float("Lương tối thiểu vùng 2", default=4160000)
    luong_toi_thieu_vung_3 = fields.Float("Lương tối thiểu vùng 3", default=3640000)
    luong_toi_thieu_vung_4 = fields.Float("Lương tối thiểu vùng 4", default=3250000)
    
    # Bảo hiểm xã hội
    ty_le_bhxh_cong_ty = fields.Float("Tỷ lệ BHXH công ty đóng (%)", default=17.5)
    ty_le_bhxh_nhan_vien = fields.Float("Tỷ lệ BHXH nhân viên đóng (%)", default=8)
    
    # Bảo hiểm y tế
    ty_le_bhyt_cong_ty = fields.Float("Tỷ lệ BHYT công ty đóng (%)", default=3)
    ty_le_bhyt_nhan_vien = fields.Float("Tỷ lệ BHYT nhân viên đóng (%)", default=1.5)
    
    # Bảo hiểm thất nghiệp
    ty_le_bhtn_cong_ty = fields.Float("Tỷ lệ BHTN công ty đóng (%)", default=1)
    ty_le_bhtn_nhan_vien = fields.Float("Tỷ lệ BHTN nhân viên đóng (%)", default=1)
    
    # Mức lương đóng bảo hiểm
    luong_dong_bh_toi_da = fields.Float("Mức lương đóng BH tối đa", default=46800000,
                                         help="Mức lương tối đa làm căn cứ đóng BHXH (20 lần lương tối thiểu vùng 1)")
    
    # Giảm trừ gia cảnh
    giam_tru_ban_than = fields.Float("Giảm trừ bản thân", default=11000000,
                                      help="Mức giảm trừ cho bản thân (11 triệu/tháng)")
    giam_tru_nguoi_phu_thuoc = fields.Float("Giảm trừ người phụ thuộc", default=4400000,
                                             help="Mức giảm trừ cho mỗi người phụ thuộc (4.4 triệu/tháng)")
    
    # Phạt chấm công
    muc_phat_di_muon = fields.Float("Mức phạt đi muộn (VNĐ/phút)", default=5000)
    muc_phat_ve_som = fields.Float("Mức phạt về sớm (VNĐ/phút)", default=5000)
    muc_phat_vang_khong_phep = fields.Float("Mức phạt vắng không phép (VNĐ/ngày)", default=500000)
    
    # Tăng ca
    he_so_tang_ca_ngay_thuong = fields.Float("Hệ số tăng ca ngày thường", default=1.5)
    he_so_tang_ca_ngay_nghi = fields.Float("Hệ số tăng ca ngày nghỉ", default=2.0)
    he_so_tang_ca_ngay_le = fields.Float("Hệ số tăng ca ngày lễ", default=3.0)
    
    # Số ngày công chuẩn
    so_ngay_cong_chuan = fields.Integer("Số ngày công chuẩn", default=22,
                                         help="Số ngày công tiêu chuẩn trong tháng")
    
    # Làm tròn lương
    lam_tron_luong = fields.Boolean("Làm tròn lương", default=True)
    buoc_lam_tron = fields.Integer("Bước làm tròn", default=1000,
                                    help="Làm tròn đến bội số của giá trị này (VD: 1000 = làm tròn đến nghìn)")
    
    active = fields.Boolean("Hoạt động", default=True)
    
    @api.constrains('ty_le_bhxh_cong_ty', 'ty_le_bhxh_nhan_vien', 'ty_le_bhyt_cong_ty', 
                    'ty_le_bhyt_nhan_vien', 'ty_le_bhtn_cong_ty', 'ty_le_bhtn_nhan_vien')
    def _check_ty_le_bao_hiem(self):
        for record in self:
            if (record.ty_le_bhxh_cong_ty < 0 or record.ty_le_bhxh_nhan_vien < 0 or
                record.ty_le_bhyt_cong_ty < 0 or record.ty_le_bhyt_nhan_vien < 0 or
                record.ty_le_bhtn_cong_ty < 0 or record.ty_le_bhtn_nhan_vien < 0):
                raise ValidationError("Tỷ lệ bảo hiểm không được âm!")
            
            if (record.ty_le_bhxh_cong_ty > 100 or record.ty_le_bhxh_nhan_vien > 100 or
                record.ty_le_bhyt_cong_ty > 100 or record.ty_le_bhyt_nhan_vien > 100 or
                record.ty_le_bhtn_cong_ty > 100 or record.ty_le_bhtn_nhan_vien > 100):
                raise ValidationError("Tỷ lệ bảo hiểm không được vượt quá 100%!")
    
    @api.model
    def get_cau_hinh(self):
        """Lấy cấu hình đang hoạt động"""
        cau_hinh = self.search([('active', '=', True)], limit=1)
        if not cau_hinh:
            # Tạo cấu hình mặc định nếu chưa có
            cau_hinh = self.create({
                'ten_cau_hinh': 'Cấu hình mặc định'
            })
        return cau_hinh
