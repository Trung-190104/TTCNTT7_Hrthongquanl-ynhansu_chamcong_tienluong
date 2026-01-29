# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
import json
import logging

_logger = logging.getLogger(__name__)

class ChamCongController(http.Controller):
    
    @http.route('/cham_cong/webcam_recognition', type='json', auth='user', methods=['POST'])
    def webcam_face_recognition(self, image_data, loai_diem_danh='vao'):
        """
        API nhận diện khuôn mặt từ webcam
        :param image_data: Dữ liệu ảnh base64
        :param loai_diem_danh: 'vao' hoặc 'ra'
        :return: Thông tin kết quả điểm danh
        """
        try:
            # Import thư viện nhận diện (cần cài đặt: pip install face_recognition)
            try:
                import face_recognition
                import numpy as np
            except ImportError:
                return {
                    'success': False,
                    'message': 'Chưa cài đặt thư viện face_recognition. Vui lòng cài đặt: pip install face_recognition'
                }
            
            # Decode ảnh từ base64
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            
            # Chuyển đổi thành numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            import cv2
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Nhận diện khuôn mặt trong ảnh
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                return {
                    'success': False,
                    'message': 'Không phát hiện khuôn mặt trong ảnh. Vui lòng thử lại!'
                }
            
            if len(face_locations) > 1:
                return {
                    'success': False,
                    'message': 'Phát hiện nhiều hơn 1 khuôn mặt. Vui lòng đảm bảo chỉ có 1 người trong khung hình!'
                }
            
            # Trích xuất đặc trưng khuôn mặt
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                return {
                    'success': False,
                    'message': 'Không thể trích xuất đặc trưng khuôn mặt!'
                }
            
            current_face_encoding = face_encodings[0]
            
            # Tìm kiếm nhân viên phù hợp
            nhan_viens = request.env['nhan_vien'].search([
                ('anh_khuon_mat', '!=', False),
                ('trang_thai_lam_viec', '=', 'dang_lam_viec')
            ])
            
            matched_nhan_vien = None
            best_match_distance = 0.6  # Ngưỡng so sánh (thấp hơn = giống nhau hơn)
            
            for nv in nhan_viens:
                if not nv.anh_khuon_mat:
                    continue
                
                try:
                    # Decode ảnh nhân viên từ database
                    nv_image_data = base64.b64decode(nv.anh_khuon_mat)
                    nv_nparr = np.frombuffer(nv_image_data, np.uint8)
                    nv_image = cv2.imdecode(nv_nparr, cv2.IMREAD_COLOR)
                    
                    # Nhận diện khuôn mặt nhân viên
                    nv_face_encodings = face_recognition.face_encodings(nv_image)
                    
                    if not nv_face_encodings:
                        continue
                    
                    nv_face_encoding = nv_face_encodings[0]
                    
                    # So sánh khuôn mặt
                    face_distance = face_recognition.face_distance([nv_face_encoding], current_face_encoding)[0]
                    
                    if face_distance < best_match_distance:
                        best_match_distance = face_distance
                        matched_nhan_vien = nv
                
                except Exception as e:
                    _logger.error(f"Error comparing face for employee {nv.ho_va_ten}: {str(e)}")
                    continue
            
            if not matched_nhan_vien:
                return {
                    'success': False,
                    'message': 'Không tìm thấy nhân viên phù hợp. Vui lòng đăng ký ảnh khuôn mặt hoặc điểm danh thủ công!'
                }
            
            # Tạo hoặc cập nhật bản ghi chấm công
            from datetime import datetime
            ngay_hom_nay = datetime.now().date()
            
            bang_cham_cong = request.env['bang_cham_cong'].search([
                ('nhan_vien_id', '=', matched_nhan_vien.id),
                ('ngay_cham_cong', '=', ngay_hom_nay)
            ], limit=1)
            
            if not bang_cham_cong:
                bang_cham_cong = request.env['bang_cham_cong'].create({
                    'nhan_vien_id': matched_nhan_vien.id,
                    'ngay_cham_cong': ngay_hom_nay,
                })
            
            gio_hien_tai = datetime.now()
            
            if loai_diem_danh == 'vao':
                if bang_cham_cong.gio_vao:
                    return {
                        'success': False,
                        'message': f'{matched_nhan_vien.ho_va_ten} đã điểm danh vào lúc {bang_cham_cong.gio_vao.strftime("%H:%M:%S")}!'
                    }
                
                bang_cham_cong.write({
                    'gio_vao': gio_hien_tai,
                    'phuong_thuc_diem_danh_vao': 'webcam'
                })
                
                return {
                    'success': True,
                    'message': f'Điểm danh vào thành công!',
                    'nhan_vien': matched_nhan_vien.ho_va_ten,
                    'gio': gio_hien_tai.strftime('%H:%M:%S'),
                    'trang_thai': bang_cham_cong.trang_thai
                }
            
            else:  # loai_diem_danh == 'ra'
                if bang_cham_cong.gio_ra:
                    return {
                        'success': False,
                        'message': f'{matched_nhan_vien.ho_va_ten} đã điểm danh ra lúc {bang_cham_cong.gio_ra.strftime("%H:%M:%S")}!'
                    }
                
                if not bang_cham_cong.gio_vao:
                    return {
                        'success': False,
                        'message': f'{matched_nhan_vien.ho_va_ten} chưa điểm danh vào!'
                    }
                
                bang_cham_cong.write({
                    'gio_ra': gio_hien_tai,
                    'phuong_thuc_diem_danh_ra': 'webcam'
                })
                
                return {
                    'success': True,
                    'message': f'Điểm danh ra thành công!',
                    'nhan_vien': matched_nhan_vien.ho_va_ten,
                    'gio': gio_hien_tai.strftime('%H:%M:%S'),
                    'trang_thai': bang_cham_cong.trang_thai
                }
        
        except Exception as e:
            _logger.error(f"Error in webcam_face_recognition: {str(e)}")
            return {
                'success': False,
                'message': f'Lỗi hệ thống: {str(e)}'
            }
