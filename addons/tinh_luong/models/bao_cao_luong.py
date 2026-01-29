# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools

class BaoCaoLuong(models.Model):
    _name = 'bao_cao_luong'
    _description = 'Báo cáo lương'
    _auto = False  # Không tạo bảng trong DB
    _rec_name = 'nhan_vien_id'
    _order = 'thang desc, nam desc, phong_ban_id'

    # Thông tin nhân viên
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", readonly=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", readonly=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", readonly=True)
    
    # Kỳ lương
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", readonly=True)
    nam = fields.Char("Năm", readonly=True)
    
    # Thu nhập
    luong_co_ban = fields.Float("Lương cơ bản", readonly=True)
    luong_theo_cong = fields.Float("Lương theo công", readonly=True)
    tong_phu_cap = fields.Float("Tổng phụ cấp", readonly=True)
    tong_thuong = fields.Float("Tổng thưởng", readonly=True)
    tong_tang_ca = fields.Float("Tổng tăng ca", readonly=True)
    tong_thu_nhap = fields.Float("Tổng thu nhập", readonly=True)
    
    # Khấu trừ
    bhxh = fields.Float("BHXH", readonly=True)
    bhyt = fields.Float("BHYT", readonly=True)
    bhtn = fields.Float("BHTN", readonly=True)
    tong_bao_hiem = fields.Float("Tổng BH", readonly=True)
    thue_tncn = fields.Float("Thuế TNCN", readonly=True)
    tong_phat = fields.Float("Tổng phạt", readonly=True)
    tong_khau_tru = fields.Float("Tổng khấu trừ", readonly=True)
    
    # Lương thực lĩnh
    luong_thuc_linh = fields.Float("Lương thực lĩnh", readonly=True)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_tinh', 'Đã tính'),
        ('da_duyet', 'Đã duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", readonly=True)
    
    def init(self):
        """Tạo view trong database"""
        tools.drop_view_if_exists(self.env.cr, 'bao_cao_luong')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW bao_cao_luong AS (
                SELECT
                    bl.id as id,
                    bl.nhan_vien_id,
                    bl.phong_ban_id,
                    bl.chuc_vu_id,
                    bl.thang,
                    bl.nam,
                    bl.luong_co_ban,
                    bl.luong_theo_cong,
                    bl.tong_phu_cap,
                    bl.tong_thuong,
                    bl.tong_tang_ca,
                    bl.tong_thu_nhap,
                    bl.bhxh,
                    bl.bhyt,
                    bl.bhtn,
                    bl.tong_bao_hiem,
                    bl.thue_tncn,
                    bl.tong_phat,
                    bl.tong_khau_tru,
                    bl.luong_thuc_linh,
                    bl.trang_thai
                FROM bang_luong bl
                WHERE bl.trang_thai IN ('da_tinh', 'da_duyet', 'da_thanh_toan')
            )
        """)
