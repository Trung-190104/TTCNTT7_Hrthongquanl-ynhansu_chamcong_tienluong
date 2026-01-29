# -*- coding: utf-8 -*-
{
    'name': "Quản lý Chấm công - Nâng cao",
    'summary': """
        Hệ thống chấm công toàn diện với tổng hợp công tháng, 
        quản lý ca làm việc và điểm danh thông minh""",
    'author': "Your Company",
    'category': 'Human Resources',
    'version': '15.0.1.0.0',
    'depends': ['base', 'mail', 'nhan_su_upgraded'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data
        'data/ca_lam_viec_data.xml',
        
        # Actions
        'views/actions.xml',
        
        # Views
        'views/ca_lam_viec.xml',
        'views/don_tu.xml',
        'views/bang_cham_cong.xml',
        'views/tong_hop_cong_thang.xml',
        'views/dot_dang_ky.xml',
        'views/dang_ky_ca_lam_theo_ngay.xml',
        'views/diem_danh_thu_cong.xml',
        
        # Menu
        'views/menu_cham_cong.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'cham_cong/static/src/js/face_recognition.js',
            'cham_cong/static/src/css/face_recognition.css',
        ],
    },
}
