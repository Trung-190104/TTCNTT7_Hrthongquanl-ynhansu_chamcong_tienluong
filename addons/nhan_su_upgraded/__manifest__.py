# -*- coding: utf-8 -*-
{
    'name': "Quản lý Nhân sự - Nâng cao",
    'summary': """
        Hệ thống quản lý nhân sự toàn diện với đánh giá hiệu suất, 
        quản lý hợp đồng và tài sản cấp phát""",
    'description': """
        Module quản lý nhân sự bao gồm:
        - Quản lý thông tin nhân viên, phòng ban, chức vụ
        - Lịch sử công tác
        - Chứng chỉ bằng cấp
        - Đánh giá hiệu suất nhân viên
        - Quản lý hợp đồng lao động
        - Quản lý tài sản cấp phát
    """,
    'author': "Your Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '15.0.1.0.0',
    'depends': ['base', 'mail'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data
        'data/sequence.xml',
        'data/cron_jobs.xml',
        
        # Actions
        'views/actions.xml',
        
        # Views - Core models
        'views/nhan_vien.xml',
        'views/phong_ban.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/chung_chi_bang_cap.xml',
        'views/danh_sach_chung_chi_bang_cap.xml',
        
        # Views - New models
        'views/danh_gia_nhan_vien.xml',
        'views/hop_dong_lao_dong.xml',
        'views/tai_san_cap_phat.xml',
        'views/loai_tai_san.xml',
        
        # Menu (phải load sau cùng)
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
