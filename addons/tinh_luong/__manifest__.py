# -*- coding: utf-8 -*-
{
    'name': "Quản lý Tính lương - Chuyên nghiệp",
    'summary': """
        Hệ thống tính lương toàn diện với bảo hiểm, thuế TNCN, 
        phụ cấp và tích hợp chấm công""",
    'description': """
        Module tính lương bao gồm:
        - Bảng lương chi tiết từng nhân viên
        - Quản lý các khoản thu nhập: lương cơ bản, phụ cấp, thưởng, tăng ca
        - Quản lý các khoản khấu trừ: BHXH, BHYT, BHTN, thuế TNCN
        - Tự động tích hợp dữ liệu chấm công
        - Tính phạt đi muộn, về sớm, vắng mặt
        - Tính thuế TNCN theo bậc thuế luỹ tiến
        - Quản lý phụ cấp linh hoạt
        - Báo cáo và thống kê lương
        - Xuất bảng lương Excel/PDF
    """,
    'author': "Your Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources/Payroll',
    'version': '15.0.1.0.0',
    'depends': ['base', 'mail', 'nhan_su_upgraded', 'cham_cong'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data
        'data/sequence.xml',
        'data/loai_phu_cap_data.xml',
        'data/thue_tncn_bac_data.xml',
        
        # Views - Configuration
        'views/loai_phu_cap.xml',
        'views/thue_tncn_bac.xml',
        'views/cau_hinh_luong.xml',
        
        # Views - Main models
        'views/bang_luong.xml',
        'views/chi_tiet_luong.xml',
        'views/phu_cap_nhan_vien.xml',
        
        # Views - Reports
        'views/bao_cao_luong.xml',
        
        # Menu
        'views/menu.xml',
        
        # Reports
        'reports/report_bang_luong.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
