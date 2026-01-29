# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
import calendar
from odoo.exceptions import ValidationError

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ma_bang_luong'
    _order = 'thang desc, nam desc, ngay_tao desc'

    # Thông tin cơ bản
    ma_bang_luong = fields.Char("Mã bảng lương", required=True, copy=False, readonly=True, default='New')
    
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", 
                                    related='nhan_vien_id.phong_ban_id', store=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ", 
                                  related='nhan_vien_id.chuc_vu_id', store=True)
    
    # Kỳ lương
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", required=True, default=lambda self: str(datetime.now().month), tracking=True)
    
    nam = fields.Char("Năm", required=True, default=lambda self: str(datetime.now().year), tracking=True)
    
    ngay_tao = fields.Date("Ngày tạo", default=fields.Date.today, tracking=True)
    
    # Lương cơ bản từ hợp đồng
    hop_dong_id = fields.Many2one('hop_dong_lao_dong', string="Hợp đồng", 
                                   compute='_compute_hop_dong', store=True)
    luong_co_ban = fields.Float("Lương cơ bản", compute='_compute_luong_co_ban', store=True, tracking=True)
    
    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_hop_dong(self):
        for record in self:
            if record.nhan_vien_id:
                # Tìm hợp đồng đang hiệu lực
                hop_dong = self.env['hop_dong_lao_dong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('trang_thai', '=', 'dang_hieu_luc')
                ], limit=1)
                record.hop_dong_id = hop_dong.id if hop_dong else False
            else:
                record.hop_dong_id = False
    
    @api.depends('hop_dong_id')
    def _compute_luong_co_ban(self):
        for record in self:
            if record.hop_dong_id:
                record.luong_co_ban = record.hop_dong_id.muc_luong_co_ban or 0
            else:
                record.luong_co_ban = 0
    
    @api.onchange('nhan_vien_id')
    def _onchange_nhan_vien(self):
        """Tự động load phụ cấp của nhân viên"""
        if self.nhan_vien_id:
            # Tự động trigger compute cho hop_dong và luong_co_ban
            self._compute_hop_dong()
            self._compute_luong_co_ban()
            
            # Load phụ cấp của nhân viên (nếu đã có)
            phu_caps = self.env['phu_cap_nhan_vien'].search([
                ('nhan_vien_id', '=', self.nhan_vien_id.id),
                ('trang_thai', '=', 'dang_ap_dung')
            ])
            
            # Tạo danh sách chi tiết phụ cấp
            chi_tiet_phu_cap = []
            for pc in phu_caps:
                chi_tiet_phu_cap.append((0, 0, {
                    'loai': 'phu_cap',
                    'loai_phu_cap_id': pc.loai_phu_cap_id.id,
                    'ten_khoan': pc.loai_phu_cap_id.ten_phu_cap,
                    'so_tien': pc.muc_phu_cap,
                }))
            
            if chi_tiet_phu_cap:
                self.chi_tiet_phu_cap_ids = chi_tiet_phu_cap
    
    @api.onchange('nhan_vien_id', 'thang', 'nam')
    def _onchange_load_phu_cap(self):
        """Auto-load phụ cấp khi chọn nhân viên (chỉ khi tạo mới)"""
        if self.nhan_vien_id and self.thang and self.nam and not self.id:
            # Tìm phụ cấp của nhân viên
            phu_caps = self.env['phu_cap_nhan_vien'].search([
                ('nhan_vien_id', '=', self.nhan_vien_id.id),
                ('trang_thai', '=', 'dang_ap_dung'),
                '|',
                ('ngay_ket_thuc', '=', False),
                ('ngay_ket_thuc', '>=', fields.Date.today())
            ])
            
            # Thêm phụ cấp mới (không xóa cũ vì có thể user đã sửa)
            phu_cap_lines = []
            for pc in phu_caps:
                phu_cap_lines.append((0, 0, {
                    'loai': 'phu_cap',
                    'loai_phu_cap_id': pc.loai_phu_cap_id.id,
                    'ten_khoan': pc.loai_phu_cap_id.ten_phu_cap,
                    'so_tien': pc.muc_phu_cap,
                    'ghi_chu': f'Phụ cấp {pc.loai_phu_cap_id.ten_phu_cap}'
                }))
            
            if phu_cap_lines:
                self.chi_tiet_phu_cap_ids = phu_cap_lines
    
    # Dữ liệu chấm công
    tong_hop_cong_id = fields.Many2one('tong_hop_cong_thang', string="Tổng hợp công",
                                        compute='_compute_tong_hop_cong', store=True)
    so_ngay_lam_viec = fields.Integer("Số ngày làm việc", compute='_compute_cham_cong', store=True)
    so_ngay_nghi_co_phep = fields.Integer("Số ngày nghỉ có phép", compute='_compute_cham_cong', store=True)
    so_ngay_vang_khong_phep = fields.Integer("Số ngày vắng không phép", compute='_compute_cham_cong', store=True)
    
    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_tong_hop_cong(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                tong_hop = self.env['tong_hop_cong_thang'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('thang', '=', record.thang),
                    ('nam', '=', record.nam)
                ], limit=1)
                record.tong_hop_cong_id = tong_hop.id if tong_hop else False
            else:
                record.tong_hop_cong_id = False
    
    @api.depends('tong_hop_cong_id')
    def _compute_cham_cong(self):
        for record in self:
            if record.tong_hop_cong_id:
                tong_hop = record.tong_hop_cong_id
                record.so_ngay_lam_viec = tong_hop.so_ngay_di_lam
                record.so_ngay_nghi_co_phep = tong_hop.so_ngay_vang_co_phep
                record.so_ngay_vang_khong_phep = tong_hop.so_ngay_vang_mat
            else:
                record.so_ngay_lam_viec = 0
                record.so_ngay_nghi_co_phep = 0
                record.so_ngay_vang_khong_phep = 0
    
    # Số công chuẩn
    so_ngay_cong_chuan = fields.Integer("Số ngày công chuẩn", default=22)
    
    # Lương thực tế theo công
    luong_theo_cong = fields.Float("Lương theo công", compute='_compute_luong_theo_cong', store=True)
    
    @api.depends('luong_co_ban', 'so_ngay_lam_viec', 'so_ngay_cong_chuan')
    def _compute_luong_theo_cong(self):
        for record in self:
            if record.so_ngay_cong_chuan > 0:
                record.luong_theo_cong = (record.luong_co_ban / record.so_ngay_cong_chuan) * record.so_ngay_lam_viec
            else:
                record.luong_theo_cong = 0
    
    # Phụ cấp
    chi_tiet_phu_cap_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id', 
                                            string="Chi tiết phụ cấp",
                                            domain=[('loai', '=', 'phu_cap')])
    tong_phu_cap = fields.Float("Tổng phụ cấp", compute='_compute_tong_phu_cap', store=True)
    
    @api.depends('chi_tiet_phu_cap_ids', 'chi_tiet_phu_cap_ids.so_tien')
    def _compute_tong_phu_cap(self):
        for record in self:
            record.tong_phu_cap = sum(record.chi_tiet_phu_cap_ids.mapped('so_tien'))
    
    # Thưởng
    chi_tiet_thuong_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id',
                                           string="Chi tiết thưởng",
                                           domain=[('loai', '=', 'thuong')])
    tong_thuong = fields.Float("Tổng thưởng", compute='_compute_tong_thuong', store=True)
    
    @api.depends('chi_tiet_thuong_ids', 'chi_tiet_thuong_ids.so_tien')
    def _compute_tong_thuong(self):
        for record in self:
            record.tong_thuong = sum(record.chi_tiet_thuong_ids.mapped('so_tien'))
    
    # Tăng ca
    chi_tiet_tang_ca_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id',
                                            string="Chi tiết tăng ca",
                                            domain=[('loai', '=', 'tang_ca')])
    tong_tang_ca = fields.Float("Tổng tăng ca", compute='_compute_tong_tang_ca', store=True)
    
    @api.depends('chi_tiet_tang_ca_ids', 'chi_tiet_tang_ca_ids.so_tien')
    def _compute_tong_tang_ca(self):
        for record in self:
            record.tong_tang_ca = sum(record.chi_tiet_tang_ca_ids.mapped('so_tien'))
    
    # Thu nhập khác
    chi_tiet_thu_nhap_khac_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id',
                                                   string="Thu nhập khác",
                                                   domain=[('loai', '=', 'thu_nhap_khac')])
    tong_thu_nhap_khac = fields.Float("Thu nhập khác", compute='_compute_tong_thu_nhap_khac', store=True)
    
    @api.depends('chi_tiet_thu_nhap_khac_ids', 'chi_tiet_thu_nhap_khac_ids.so_tien')
    def _compute_tong_thu_nhap_khac(self):
        for record in self:
            record.tong_thu_nhap_khac = sum(record.chi_tiet_thu_nhap_khac_ids.mapped('so_tien'))
    
    # Tổng thu nhập
    tong_thu_nhap = fields.Float("Tổng thu nhập", compute='_compute_tong_thu_nhap', store=True, tracking=True)
    
    @api.depends('luong_theo_cong', 'tong_phu_cap', 'tong_thuong', 'tong_tang_ca', 'tong_thu_nhap_khac')
    def _compute_tong_thu_nhap(self):
        for record in self:
            record.tong_thu_nhap = (record.luong_theo_cong + record.tong_phu_cap + 
                                   record.tong_thuong + record.tong_tang_ca + record.tong_thu_nhap_khac)
    
    # ========== CÁC KHOẢN KHẤU TRỪ ==========
    
    # Bảo hiểm xã hội
    luong_dong_bao_hiem = fields.Float("Lương đóng bảo hiểm", compute='_compute_luong_dong_bao_hiem', store=True)
    
    @api.depends('luong_co_ban', 'chi_tiet_phu_cap_ids')
    def _compute_luong_dong_bao_hiem(self):
        cau_hinh = self.env['cau_hinh_luong'].get_cau_hinh()
        for record in self:
            # Lương đóng BH = lương cơ bản + các phụ cấp tính BH
            phu_cap_tinh_bh = sum(record.chi_tiet_phu_cap_ids.filtered(
                lambda x: x.loai_phu_cap_id.tinh_bao_hiem
            ).mapped('so_tien'))
            
            luong_dong_bh = record.luong_co_ban + phu_cap_tinh_bh
            
            # Giới hạn mức đóng tối đa
            if luong_dong_bh > cau_hinh.luong_dong_bh_toi_da:
                luong_dong_bh = cau_hinh.luong_dong_bh_toi_da
            
            record.luong_dong_bao_hiem = luong_dong_bh
    
    bhxh = fields.Float("BHXH (8%)", compute='_compute_bao_hiem', store=True)
    bhyt = fields.Float("BHYT (1.5%)", compute='_compute_bao_hiem', store=True)
    bhtn = fields.Float("BHTN (1%)", compute='_compute_bao_hiem', store=True)
    tong_bao_hiem = fields.Float("Tổng bảo hiểm", compute='_compute_bao_hiem', store=True)
    
    @api.depends('luong_dong_bao_hiem')
    def _compute_bao_hiem(self):
        cau_hinh = self.env['cau_hinh_luong'].get_cau_hinh()
        for record in self:
            record.bhxh = record.luong_dong_bao_hiem * cau_hinh.ty_le_bhxh_nhan_vien / 100
            record.bhyt = record.luong_dong_bao_hiem * cau_hinh.ty_le_bhyt_nhan_vien / 100
            record.bhtn = record.luong_dong_bao_hiem * cau_hinh.ty_le_bhtn_nhan_vien / 100
            record.tong_bao_hiem = record.bhxh + record.bhyt + record.bhtn
    
    # Thuế TNCN
    so_nguoi_phu_thuoc = fields.Integer("Số người phụ thuộc", default=0)
    
    thu_nhap_chiu_thue = fields.Float("Thu nhập chịu thuế", compute='_compute_thue_tncn', store=True)
    giam_tru_gia_canh = fields.Float("Giảm trừ gia cảnh", compute='_compute_thue_tncn', store=True)
    thu_nhap_tinh_thue = fields.Float("Thu nhập tính thuế", compute='_compute_thue_tncn', store=True)
    thue_tncn = fields.Float("Thuế TNCN", compute='_compute_thue_tncn', store=True, tracking=True)
    
    @api.depends('tong_thu_nhap', 'tong_bao_hiem', 'so_nguoi_phu_thuoc', 'chi_tiet_phu_cap_ids')
    def _compute_thue_tncn(self):
        cau_hinh = self.env['cau_hinh_luong'].get_cau_hinh()
        for record in self:
            # Thu nhập chịu thuế = Tổng thu nhập - các khoản không chịu thuế
            phu_cap_khong_chiu_thue = sum(record.chi_tiet_phu_cap_ids.filtered(
                lambda x: not x.loai_phu_cap_id.tinh_thue
            ).mapped('so_tien'))
            
            record.thu_nhap_chiu_thue = record.tong_thu_nhap - phu_cap_khong_chiu_thue
            
            # Giảm trừ gia cảnh
            record.giam_tru_gia_canh = (cau_hinh.giam_tru_ban_than + 
                                        cau_hinh.giam_tru_nguoi_phu_thuoc * record.so_nguoi_phu_thuoc)
            
            # Thu nhập tính thuế
            record.thu_nhap_tinh_thue = (record.thu_nhap_chiu_thue - record.tong_bao_hiem - 
                                         record.giam_tru_gia_canh)
            
            if record.thu_nhap_tinh_thue <= 0:
                record.thue_tncn = 0
            else:
                # Chuyển sang triệu để tính thuế
                thu_nhap_trieu = record.thu_nhap_tinh_thue / 1000000
                record.thue_tncn = self.env['thue_tncn_bac'].tinh_thue_tncn(thu_nhap_trieu) * 1000000
    
    # Phạt chấm công
    chi_tiet_phat_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id',
                                         string="Chi tiết phạt",
                                         domain=[('loai', '=', 'phat')])
    tong_phat = fields.Float("Tổng phạt", compute='_compute_tong_phat', store=True)
    
    @api.depends('chi_tiet_phat_ids', 'chi_tiet_phat_ids.so_tien')
    def _compute_tong_phat(self):
        for record in self:
            record.tong_phat = sum(record.chi_tiet_phat_ids.mapped('so_tien'))
    
    # Khấu trừ khác
    chi_tiet_khau_tru_khac_ids = fields.One2many('chi_tiet_luong', 'bang_luong_id',
                                                   string="Khấu trừ khác",
                                                   domain=[('loai', '=', 'khau_tru_khac')])
    tong_khau_tru_khac = fields.Float("Khấu trừ khác", compute='_compute_tong_khau_tru_khac', store=True)
    
    @api.depends('chi_tiet_khau_tru_khac_ids', 'chi_tiet_khau_tru_khac_ids.so_tien')
    def _compute_tong_khau_tru_khac(self):
        for record in self:
            record.tong_khau_tru_khac = sum(record.chi_tiet_khau_tru_khac_ids.mapped('so_tien'))
    
    # Tổng khấu trừ
    tong_khau_tru = fields.Float("Tổng khấu trừ", compute='_compute_tong_khau_tru', store=True, tracking=True)
    
    @api.depends('tong_bao_hiem', 'thue_tncn', 'tong_phat', 'tong_khau_tru_khac')
    def _compute_tong_khau_tru(self):
        for record in self:
            record.tong_khau_tru = (record.tong_bao_hiem + record.thue_tncn + 
                                   record.tong_phat + record.tong_khau_tru_khac)
    
    # ========== LƯƠNG THỰC LĨNH ==========
    
    luong_thuc_linh = fields.Float("Lương thực lĩnh", compute='_compute_luong_thuc_linh', 
                                    store=True, tracking=True)
    
    @api.depends('tong_thu_nhap', 'tong_khau_tru')
    def _compute_luong_thuc_linh(self):
        cau_hinh = self.env['cau_hinh_luong'].get_cau_hinh()
        for record in self:
            luong = record.tong_thu_nhap - record.tong_khau_tru
            
            # Làm tròn nếu được cấu hình
            if cau_hinh.lam_tron_luong and cau_hinh.buoc_lam_tron > 0:
                luong = round(luong / cau_hinh.buoc_lam_tron) * cau_hinh.buoc_lam_tron
            
            record.luong_thuc_linh = max(0, luong)
    
    # ========== TRẠNG THÁI VÀ GHI CHÚ ==========
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_tinh', 'Đã tính'),
        ('da_duyet', 'Đã duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='nhap', required=True, tracking=True)
    
    ngay_thanh_toan = fields.Date("Ngày thanh toán", tracking=True)
    nguoi_thanh_toan_id = fields.Many2one('res.users', string="Người thanh toán", tracking=True)
    
    ghi_chu = fields.Text("Ghi chú")
    
    # ========== CONSTRAINTS ==========
    
    @api.constrains('nhan_vien_id', 'thang', 'nam')
    def _check_unique_bang_luong(self):
        for record in self:
            duplicate = self.search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('thang', '=', record.thang),
                ('nam', '=', record.nam),
                ('id', '!=', record.id)
            ], limit=1)
            if duplicate:
                raise ValidationError(
                    f"Đã tồn tại bảng lương tháng {record.thang}/{record.nam} "
                    f"cho nhân viên {record.nhan_vien_id.ho_va_ten}!"
                )
    
    # ========== METHODS ==========
    
    @api.model
    def create(self, vals):
        if vals.get('ma_bang_luong', 'New') == 'New':
            vals['ma_bang_luong'] = self.env['ir.sequence'].next_by_code('bang_luong') or 'New'
        return super(BangLuong, self).create(vals)
    
    def action_tinh_luong(self):
        """Tự động tính lương"""
        self.ensure_one()
        
        if self.trang_thai != 'nhap':
            raise ValidationError("Chỉ có thể tính lại lương ở trạng thái nháp!")
        
        # Xóa các chi tiết cũ
        self.chi_tiet_phu_cap_ids.unlink()
        self.chi_tiet_phat_ids.unlink()
        
        # Tạo chi tiết phụ cấp
        self._tao_chi_tiet_phu_cap()
        
        # Tạo chi tiết phạt từ chấm công
        self._tao_chi_tiet_phat()
        
        # Cập nhật trạng thái
        self.write({'trang_thai': 'da_tinh'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def _tao_chi_tiet_phu_cap(self):
        """Tạo chi tiết phụ cấp từ phụ cấp nhân viên"""
        self.ensure_one()
        
        # Tìm các phụ cấp đang áp dụng
        phu_caps = self.env['phu_cap_nhan_vien'].search([
            ('nhan_vien_id', '=', self.nhan_vien_id.id),
            ('trang_thai', '=', 'dang_ap_dung'),
            ('active', '=', True)
        ])
        
        for phu_cap in phu_caps:
            self.env['chi_tiet_luong'].create({
                'bang_luong_id': self.id,
                'loai': 'phu_cap',
                'loai_phu_cap_id': phu_cap.loai_phu_cap_id.id,
                'ten_khoan': phu_cap.loai_phu_cap_id.ten_phu_cap,
                'so_tien': phu_cap.muc_phu_cap,
                'ghi_chu': f'Phụ cấp {phu_cap.loai_phu_cap_id.ten_phu_cap}'
            })
    
    def _tao_chi_tiet_phat(self):
        """Tạo chi tiết phạt từ chấm công"""
        self.ensure_one()
        
        if not self.tong_hop_cong_id:
            return
        
        cau_hinh = self.env['cau_hinh_luong'].get_cau_hinh()
        tong_hop = self.tong_hop_cong_id
        
        # Phạt đi muộn
        if tong_hop.tong_phut_di_muon > 0:
            phat_di_muon = tong_hop.tong_phut_di_muon * cau_hinh.muc_phat_di_muon
            self.env['chi_tiet_luong'].create({
                'bang_luong_id': self.id,
                'loai': 'phat',
                'ten_khoan': 'Phạt đi muộn',
                'so_tien': phat_di_muon,
                'so_luong': tong_hop.tong_phut_di_muon,
                'don_vi': 'phút',
                'ghi_chu': f'Phạt {tong_hop.tong_phut_di_muon} phút đi muộn x {cau_hinh.muc_phat_di_muon:,.0f}đ'
            })
        
        # Phạt về sớm
        if tong_hop.tong_phut_ve_som > 0:
            phat_ve_som = tong_hop.tong_phut_ve_som * cau_hinh.muc_phat_ve_som
            self.env['chi_tiet_luong'].create({
                'bang_luong_id': self.id,
                'loai': 'phat',
                'ten_khoan': 'Phạt về sớm',
                'so_tien': phat_ve_som,
                'so_luong': tong_hop.tong_phut_ve_som,
                'don_vi': 'phút',
                'ghi_chu': f'Phạt {tong_hop.tong_phut_ve_som} phút về sớm x {cau_hinh.muc_phat_ve_som:,.0f}đ'
            })
        
        # Phạt vắng không phép
        if self.so_ngay_vang_khong_phep > 0:
            phat_vang = self.so_ngay_vang_khong_phep * cau_hinh.muc_phat_vang_khong_phep
            self.env['chi_tiet_luong'].create({
                'bang_luong_id': self.id,
                'loai': 'phat',
                'ten_khoan': 'Phạt vắng không phép',
                'so_tien': phat_vang,
                'so_luong': self.so_ngay_vang_khong_phep,
                'don_vi': 'ngày',
                'ghi_chu': f'Phạt {self.so_ngay_vang_khong_phep} ngày vắng x {cau_hinh.muc_phat_vang_khong_phep:,.0f}đ'
            })
    
    def action_duyet(self):
        """Duyệt bảng lương"""
        self.write({'trang_thai': 'da_duyet'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def action_thanh_toan(self):
        """Thanh toán lương"""
        self.write({
            'trang_thai': 'da_thanh_toan',
            'ngay_thanh_toan': date.today(),
            'nguoi_thanh_toan_id': self.env.user.id
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def action_quay_lai_nhap(self):
        """Quay lại trạng thái nháp"""
        if self.trang_thai == 'da_thanh_toan':
            raise ValidationError("Không thể quay lại nháp sau khi đã thanh toán!")
        
        self.write({'trang_thai': 'nhap'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    @api.model
    def action_tao_bang_luong_hang_loat(self, thang, nam):
        """Tạo bảng lương hàng loạt cho tất cả nhân viên"""
        nhan_viens = self.env['nhan_vien'].search([
            ('trang_thai_lam_viec', '=', 'dang_lam_viec')
        ])
        
        bang_luong_tao_moi = self.env['bang_luong']
        
        for nv in nhan_viens:
            # Kiểm tra đã tồn tại chưa
            existing = self.search([
                ('nhan_vien_id', '=', nv.id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ], limit=1)
            
            if not existing:
                bang_luong = self.create({
                    'nhan_vien_id': nv.id,
                    'thang': thang,
                    'nam': nam,
                })
                bang_luong_tao_moi |= bang_luong
        
        # Tự động tính lương cho tất cả
        for bang_luong in bang_luong_tao_moi:
            try:
                bang_luong.action_tinh_luong()
            except Exception as e:
                # Log lỗi nhưng không dừng quá trình
                bang_luong.message_post(body=f"Lỗi khi tính lương: {str(e)}")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Hoàn thành!',
                'message': f'Đã tạo {len(bang_luong_tao_moi)} bảng lương',
                'type': 'success',
                'sticky': False,
            }
        }


    _sql_constraints = [
        ('unique_nhan_vien_thang_nam', 
         'unique(nhan_vien_id, thang, nam)', 
         'Đã tồn tại bảng lương tháng này cho nhân viên này!')
    ]
