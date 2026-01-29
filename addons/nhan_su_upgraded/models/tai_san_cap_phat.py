# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class TaiSanCapPhat(models.Model):
    _name = 'tai_san_cap_phat'
    _description = 'Tài sản cấp phát cho nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_tai_san'
    _order = 'ngay_cap_phat desc'

    # Thông tin tài sản
    ma_tai_san = fields.Char("Mã tài sản", required=True, copy=False, tracking=True)
    ten_tai_san = fields.Char("Tên tài sản", required=True, tracking=True)
    loai_tai_san_id = fields.Many2one('loai_tai_san', string="Loại tài sản", required=True, tracking=True)
    
    # Thông tin chi tiết
    nhan_hieu = fields.Char("Nhãn hiệu/Hãng")
    model = fields.Char("Model/Phiên bản")
    serial_number = fields.Char("Serial Number", tracking=True)
    ngay_mua = fields.Date("Ngày mua")
    gia_tri = fields.Float("Giá trị", tracking=True)
    
    # Thông tin cấp phát
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", related='nhan_vien_id.phong_ban_id', store=True)
    ngay_cap_phat = fields.Date("Ngày cấp phát", tracking=True)
    nguoi_cap_phat_id = fields.Many2one('res.users', string="Người cấp phát", 
                                         default=lambda self: self.env.user, tracking=True)
    
    # Thông tin thu hồi
    ngay_thu_hoi = fields.Date("Ngày thu hồi", tracking=True)
    nguoi_thu_hoi_id = fields.Many2one('res.users', string="Người thu hồi", tracking=True)
    ly_do_thu_hoi = fields.Text("Lý do thu hồi")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('kho', 'Trong kho'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('da_thu_hoi', 'Đã thu hồi'),
        ('hong_hoc', 'Hỏng hóc'),
        ('thanh_ly', 'Thanh lý'),
    ], string="Trạng thái", default='kho', required=True, tracking=True)
    
    tinh_trang = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('can_sua_chua', 'Cần sửa chữa'),
        ('hong', 'Hỏng'),
    ], string="Tình trạng", default='tot', tracking=True)
    
    # Thời gian sử dụng
    thoi_gian_su_dung = fields.Integer("Thời gian sử dụng (ngày)", 
                                        compute='_compute_thoi_gian_su_dung', store=True)
    
    # Biên bản
    bien_ban_ban_giao = fields.Binary("Biên bản bàn giao")
    bien_ban_ban_giao_name = fields.Char("Tên file bàn giao")
    bien_ban_thu_hoi = fields.Binary("Biên bản thu hồi")
    bien_ban_thu_hoi_name = fields.Char("Tên file thu hồi")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('ngay_cap_phat', 'ngay_thu_hoi', 'trang_thai')
    def _compute_thoi_gian_su_dung(self):
        for record in self:
            if record.ngay_cap_phat:
                if record.trang_thai == 'dang_su_dung':
                    # Đang sử dụng: tính từ ngày cấp phát đến hôm nay
                    delta = date.today() - record.ngay_cap_phat
                    record.thoi_gian_su_dung = delta.days
                elif record.ngay_thu_hoi:
                    # Đã thu hồi: tính từ ngày cấp phát đến ngày thu hồi
                    delta = record.ngay_thu_hoi - record.ngay_cap_phat
                    record.thoi_gian_su_dung = delta.days
                else:
                    record.thoi_gian_su_dung = 0
            else:
                record.thoi_gian_su_dung = 0
    
    @api.constrains('serial_number')
    def _check_serial_number(self):
        for record in self:
            if record.serial_number:
                duplicate = self.search([
                    ('serial_number', '=', record.serial_number),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        f"Serial Number {record.serial_number} đã tồn tại "
                        f"(Tài sản: {duplicate.ten_tai_san})!"
                    )
    
    @api.constrains('ma_tai_san')
    def _check_ma_tai_san(self):
        for record in self:
            duplicate = self.search([
                ('ma_tai_san', '=', record.ma_tai_san),
                ('id', '!=', record.id)
            ], limit=1)
            if duplicate:
                raise ValidationError(f"Mã tài sản {record.ma_tai_san} đã tồn tại!")
    
    def action_cap_phat(self):
        """Cấp phát tài sản cho nhân viên"""
        self.ensure_one()
        if self.trang_thai != 'kho':
            raise ValidationError("Chỉ có thể cấp phát tài sản đang ở trong kho!")
        
        return {
            'name': 'Cấp phát tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'tai_san_cap_phat',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'show_cap_phat': True}
        }
    
    def action_thu_hoi(self):
        """Thu hồi tài sản"""
        self.ensure_one()
        if self.trang_thai != 'dang_su_dung':
            raise ValidationError("Chỉ có thể thu hồi tài sản đang được sử dụng!")
        
        return {
            'name': 'Thu hồi tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'tai_san_cap_phat',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'show_thu_hoi': True}
        }
    
    def action_bao_hong(self):
        """Báo hỏng tài sản"""
        self.ensure_one()
        self.write({
            'trang_thai': 'hong_hoc',
            'tinh_trang': 'hong'
        })
        # Tạo activity để thông báo
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=f'Tài sản {self.ma_tai_san} bị hỏng',
            note=f'Tài sản {self.ten_tai_san} (Mã: {self.ma_tai_san}) đã bị hỏng. '
                 f'Vui lòng kiểm tra và xử lý.',
            user_id=self.env.user.id,
        )
    
    def action_thanh_ly(self):
        """Thanh lý tài sản"""
        self.ensure_one()
        self.write({'trang_thai': 'thanh_ly'})
    
    def write(self, vals):
        """Override write để tự động cập nhật trạng thái"""
        # Tự động cập nhật trạng thái khi cấp phát
        if vals.get('nhan_vien_id') and vals.get('ngay_cap_phat'):
            vals['trang_thai'] = 'dang_su_dung'
            vals['nguoi_cap_phat_id'] = self.env.user.id
        
        # Tự động cập nhật trạng thái khi thu hồi
        if vals.get('ngay_thu_hoi'):
            vals['trang_thai'] = 'da_thu_hoi'
            vals['nguoi_thu_hoi_id'] = self.env.user.id
            
        return super(TaiSanCapPhat, self).write(vals)
