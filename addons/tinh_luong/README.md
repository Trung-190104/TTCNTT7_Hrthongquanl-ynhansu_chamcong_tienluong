# MODULE TÍNH LƯƠNG - ODOO 15

## TỔNG QUAN
Module tính lương chuyên nghiệp, tích hợp với hệ thống nhân sự và chấm công, hỗ trợ:
- Tính lương tự động theo chấm công
- Quản lý phụ cấp linh hoạt
- Tính bảo hiểm xã hội, y tế, thất nghiệp
- Tính thuế TNCN theo bậc thuế lũy tiến
- Phạt chấm công (đi muộn, về sớm, vắng không phép)
- Báo cáo và thống kê lương

## CÀI ĐẶT

### 1. Yêu cầu
- Odoo 15
- Module `nhan_su_upgraded` (Quản lý nhân sự)
- Module `cham_cong` (Chấm công)

### 2. Cài đặt module
```bash
# Copy module vào thư mục addons
cp -r tinh_luong /path/to/odoo/addons/

# Restart Odoo
sudo systemctl restart odoo

# Vào Odoo > Apps > Update Apps List
# Tìm "Quản lý Tính lương - Chuyên nghiệp" và Install
```

### 3. Cấu hình ban đầu

#### Bước 1: Cấu hình tính lương
`Tính lương > Cấu hình > Cấu hình tính lương`

Cài đặt:
- **Lương tối thiểu vùng**: 4,680,000đ (vùng 1), 4,160,000đ (vùng 2)...
- **Bảo hiểm**: BHXH (17.5% + 8%), BHYT (3% + 1.5%), BHTN (1% + 1%)
- **Giảm trừ gia cảnh**: 11,000,000đ/người, 4,400,000đ/người phụ thuộc
- **Phạt chấm công**: Đi muộn 5,000đ/phút, vắng không phép 500,000đ/ngày
- **Số ngày công chuẩn**: 22 ngày/tháng

#### Bước 2: Bậc thuế TNCN
`Tính lương > Cấu hình > Bậc thuế TNCN`

Mặc định đã có 7 bậc thuế (5%, 10%, 15%, 20%, 25%, 30%, 35%)

#### Bước 3: Danh mục phụ cấp
`Tính lương > Phụ cấp > Danh mục phụ cấp`

Đã có sẵn:
- Phụ cấp ăn trưa: 30,000đ/ngày
- Phụ cấp xăng xe: 500,000đ/tháng
- Phụ cấp điện thoại: 200,000đ/tháng
- Phụ cấp chức vụ: 1,000,000đ/tháng
- ...

Bạn có thể thêm phụ cấp mới tùy theo nhu cầu.

## SỬ DỤNG

### 1. Thiết lập phụ cấp cho nhân viên
`Tính lương > Phụ cấp > Phụ cấp nhân viên > Tạo mới`

- Chọn nhân viên
- Chọn loại phụ cấp
- Nhập mức phụ cấp
- Chọn ngày áp dụng

Ví dụ:
- Nguyễn Văn A - Phụ cấp ăn trưa - 30,000đ - Áp dụng từ 01/01/2024
- Nguyễn Văn A - Phụ cấp xăng xe - 500,000đ - Áp dụng từ 01/01/2024

### 2. Tạo bảng lương

#### Tạo từng bảng lương
`Tính lương > Bảng lương > Tạo mới`

1. Chọn nhân viên
2. Chọn tháng/năm
3. Click **"Tính lương"**
   - Hệ thống tự động:
     - Lấy lương cơ bản từ hợp đồng
     - Lấy dữ liệu chấm công từ tổng hợp công
     - Tính phụ cấp đang áp dụng
     - Tính phạt chấm công
     - Tính bảo hiểm
     - Tính thuế TNCN
4. Kiểm tra và điều chỉnh (nếu cần)
5. Click **"Duyệt"**
6. Click **"Thanh toán"** khi trả lương

#### Tạo hàng loạt
`Tính lương > Bảng lương > Action > Tạo bảng lương hàng loạt`

- Nhập tháng/năm
- Hệ thống tự động tạo và tính lương cho TẤT CẢ nhân viên đang làm việc

### 3. Chi tiết bảng lương

Bảng lương bao gồm các tab:

**Tab "Thông tin lương":**
- Lương cơ bản
- Số ngày công
- Lương theo công
- Tổng thu nhập

**Tab "Chi tiết thu nhập":**
- Phụ cấp (được load tự động)
- Thưởng (nhập thủ công nếu có)
- Tăng ca (nhập thủ công)
- Thu nhập khác

**Tab "Khấu trừ":**
- Bảo hiểm (tự động tính)
- Thuế TNCN (tự động tính)
- Phạt (tự động từ chấm công)
- Khấu trừ khác (nhập thủ công nếu có)

**Tab "Thanh toán":**
- **Lương thực lĩnh** = Tổng thu nhập - Tổng khấu trừ
- Thông tin thanh toán

### 4. Báo cáo

#### Báo cáo Pivot
`Tính lương > Báo cáo > Báo cáo lương`

- Xem tổng hợp lương theo phòng ban, tháng, năm
- Phân tích xu hướng

#### Xuất phiếu lương PDF
Trong bảng lương > Click **Print > Phiếu lương**

Phiếu lương bao gồm:
- Thông tin nhân viên
- Chi tiết thu nhập
- Chi tiết khấu trừ
- Lương thực lĩnh
- Chữ ký xác nhận

## QUY TRÌNH TÍNH LƯƠNG HÀNG THÁNG

### Ngày 25-28 mỗi tháng:

1. **Kết thúc chấm công tháng**
   - `Chấm công > Tổng hợp công tháng > Tạo tổng hợp`
   - Kiểm tra và xác nhận dữ liệu

2. **Tạo bảng lương hàng loạt**
   - `Tính lương > Bảng lương > Action > Tạo hàng loạt`
   - Chọn tháng vừa kết thúc
   - Hệ thống tự động tính lương

3. **Kiểm tra và điều chỉnh**
   - Kiểm tra từng bảng lương
   - Thêm thưởng, tăng ca nếu có
   - Thêm khấu trừ đặc biệt nếu có

4. **Duyệt bảng lương**
   - Chọn tất cả bảng lương
   - Action > Duyệt

5. **Thanh toán**
   - Ngày 30/31: Chọn tất cả > Thanh toán
   - In phiếu lương phát cho nhân viên

## LƯU Ý QUAN TRỌNG

### Về bảo hiểm:
- Lương đóng BH = Lương cơ bản + Phụ cấp tính BH
- Tối đa 46,800,000đ (20 lần lương tối thiểu vùng 1)

### Về thuế TNCN:
- Thu nhập chịu thuế = Tổng thu nhập - Phụ cấp không chịu thuế
- Thu nhập tính thuế = Thu nhập chịu thuế - Bảo hiểm - Giảm trừ gia cảnh
- Tính theo bậc thuế luỹ tiến

### Về phạt:
- Tự động tính từ tổng hợp công
- Đi muộn: 5,000đ/phút (mặc định)
- Về sớm: 5,000đ/phút
- Vắng không phép: 500,000đ/ngày

### Về làm tròn:
- Mặc định làm tròn đến nghìn
- Có thể tắt trong cấu hình

## HỖ TRỢ

Nếu gặp vấn đề, hãy kiểm tra:
1. Module `nhan_su_upgraded` và `cham_cong` đã cài đặt chưa?
2. Nhân viên đã có hợp đồng lao động chưa?
3. Đã tạo tổng hợp công tháng chưa?
4. Cấu hình tính lương đã đúng chưa?

## PHÁT TRIỂN THÊM

Module có thể mở rộng:
- Tích hợp với ngân hàng (chuyển lương tự động)
- Tính lương theo KPI
- Thưởng theo doanh thu
- Hoa hồng bán hàng
- Tính lương nghỉ phép, nghỉ ốm
- ...

---

**Phiên bản:** 15.0.1.0.0  
**Tác giả:** Your Company  
**Giấy phép:** LGPL-3
