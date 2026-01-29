/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useRef } from "@odoo/owl";

class FaceRecognitionWidget extends Component {
    setup() {
        this.state = useState({
            isStreaming: false,
            message: '',
            messageType: '',
        });
        this.videoRef = useRef("videoElement");
        this.canvasRef = useRef("canvasElement");
        this.stream = null;
    }

    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 } 
            });
            this.videoRef.el.srcObject = this.stream;
            this.state.isStreaming = true;
            this.state.message = 'Camera đã sẵn sàng. Hãy nhìn vào camera và nhấn "Điểm danh".';
            this.state.messageType = 'info';
        } catch (err) {
            console.error("Error accessing camera:", err);
            this.state.message = 'Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập.';
            this.state.messageType = 'danger';
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.videoRef.el.srcObject = null;
            this.state.isStreaming = false;
            this.state.message = '';
        }
    }

    async captureAndRecognize(loaiDiemDanh) {
        if (!this.state.isStreaming) {
            this.state.message = 'Vui lòng bật camera trước!';
            this.state.messageType = 'warning';
            return;
        }

        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        const context = canvas.getContext('2d');

        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to base64
        const imageData = canvas.toDataURL('image/jpeg', 0.8);

        this.state.message = 'Đang xử lý nhận diện...';
        this.state.messageType = 'info';

        try {
            const result = await this.env.services.rpc({
                route: '/cham_cong/webcam_recognition',
                params: {
                    image_data: imageData,
                    loai_diem_danh: loaiDiemDanh,
                },
            });

            if (result.success) {
                this.state.message = `${result.message} - Nhân viên: ${result.nhan_vien} - Giờ: ${result.gio}`;
                this.state.messageType = 'success';
                this.stopCamera();
            } else {
                this.state.message = result.message;
                this.state.messageType = 'danger';
            }
        } catch (error) {
            console.error("Error during recognition:", error);
            this.state.message = 'Lỗi kết nối server. Vui lòng thử lại.';
            this.state.messageType = 'danger';
        }
    }

    diemDanhVao() {
        this.captureAndRecognize('vao');
    }

    diemDanhRa() {
        this.captureAndRecognize('ra');
    }

    willUnmount() {
        this.stopCamera();
    }
}

FaceRecognitionWidget.template = "cham_cong.FaceRecognitionWidget";

registry.category("actions").add("face_recognition_widget", FaceRecognitionWidget);
