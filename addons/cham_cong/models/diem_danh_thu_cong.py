# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class DiemDanhThuCong(models.TransientModel):
    _name = 'diem_danh_thu_cong'
    _description = 'Điểm danh thủ công'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_cham_cong = fields.Date("Ngày chấm công", required=True, default=fields.Date.today)
    loai_diem_danh = fields.Selection([
        ('vao', 'Điểm danh vào'),
        ('ra', 'Điểm danh ra'),
    ], string="Loại điểm danh", required=True, default='vao')
    
    gio_diem_danh = fields.Datetime("Giờ điểm danh", required=True, default=fields.Datetime.now)
    ghi_chu = fields.Text("Ghi chú")
    
    def action_diem_danh(self):
        """Thực hiện điểm danh"""
        self.ensure_one()
        
        # Tìm hoặc tạo bản ghi chấm công
        bang_cham_cong = self.env['bang_cham_cong'].search([
            ('nhan_vien_id', '=', self.nhan_vien_id.id),
            ('ngay_cham_cong', '=', self.ngay_cham_cong)
        ], limit=1)
        
        if not bang_cham_cong:
            # Tạo mới bản ghi chấm công
            bang_cham_cong = self.env['bang_cham_cong'].create({
                'nhan_vien_id': self.nhan_vien_id.id,
                'ngay_cham_cong': self.ngay_cham_cong,
            })
        
        # Cập nhật giờ vào/ra
        if self.loai_diem_danh == 'vao':
            if bang_cham_cong.gio_vao:
                raise ValidationError(
                    f"Nhân viên {self.nhan_vien_id.ho_va_ten} đã điểm danh vào lúc "
                    f"{bang_cham_cong.gio_vao.strftime('%H:%M:%S')}!"
                )
            bang_cham_cong.write({
                'gio_vao': self.gio_diem_danh,
                'phuong_thuc_diem_danh_vao': 'thu_cong'
            })
            message = f"Điểm danh vào thành công lúc {self.gio_diem_danh.strftime('%H:%M:%S')}"
        else:
            if bang_cham_cong.gio_ra:
                raise ValidationError(
                    f"Nhân viên {self.nhan_vien_id.ho_va_ten} đã điểm danh ra lúc "
                    f"{bang_cham_cong.gio_ra.strftime('%H:%M:%S')}!"
                )
            if not bang_cham_cong.gio_vao:
                raise ValidationError("Nhân viên chưa điểm danh vào!")
            
            bang_cham_cong.write({
                'gio_ra': self.gio_diem_danh,
                'phuong_thuc_diem_danh_ra': 'thu_cong'
            })
            message = f"Điểm danh ra thành công lúc {self.gio_diem_danh.strftime('%H:%M:%S')}"
        
        # Thêm ghi chú vào chatter
        if self.ghi_chu:
            bang_cham_cong.message_post(body=self.ghi_chu)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công!',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }
