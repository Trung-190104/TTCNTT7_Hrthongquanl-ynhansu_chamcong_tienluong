<h1 align="center">HỆ THỐNG QUẢN LÝ NHÂN SỰ, CHẤM CÔNG VÀ TÍNH LƯƠNG</h1>

<div align="center">
<p align="center">
  <img src="https://raw.githubusercontent.com/anhminhvdvn/CanhBaoDotNhap/main/images/logoDaiNam.png" width="150"> 
</p>

<br>
 
[![Fit DNU](https://img.shields.io/badge/Fit%20DNU-green?style=for-the-badge)](https://fitdnu.net/)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

</br>
</div>

[![Made with Odoo](https://img.shields.io/badge/Made%20with-Odoo%2015-714B67?style=for-the-badge&logo=odoo)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

<h2 align="center">Giải pháp quản lý nhân sự toàn diện trên nền tảng Odoo 15</h2>

<p align="left">
  Hệ thống quản lý nhân sự tích hợp 3 modules chính: Quản lý Nhân sự, Chấm công và Tính lương. Được xây dựng trên nền tảng Odoo 15, hệ thống cung cấp giải pháp toàn diện cho việc quản lý thông tin nhân viên, theo dõi chấm công tự động và tính lương chính xác theo quy định của Việt Nam.
</p>

---

## 🌟 Giới thiệu

Đây là **Bài tập lớn cuối kỳ** môn **Hệ thống thông tin quản lý** - phát triển từ đề tài của khóa trước và được cải tiến toàn diện.

### 📚 Thông tin học phần
- **Nhóm:** Nhóm 11
- **Lớp:** CNTT 16-05
- **Trường:** Đại học Đại Nam
- **Học kỳ:** II, Năm học 2024-2025

### 👥 Thành viên nhóm

| STT | Họ và Tên | Vai trò | Công việc chính |
|-----|-----------|---------|-----------------|
| 1 | **Chu Văn Huy** | **Trưởng nhóm** | Thiết kế kiến trúc hệ thống, phát triển module Nhân sự, quản lý dự án, tích hợp modules, viết tài liệu kỹ thuật |
| 2 | Phạm Ngọc Minh | Thành viên | Phát triển module Chấm công, thiết kế database, xử lý logic tính toán công, kiểm thử module chấm công |
| 3 | Nguyễn Thành Trung | Thành viên | Phát triển module Tính lương, xử lý tính thuế TNCN, bảo hiểm, tạo báo cáo, kiểm thử tích hợp |

### 🎓 Nguồn tham khảo
Dự án được phát triển dựa trên đề tài của **CNTT 15-01** (khóa trước):
- Hoàng Thị Kim Ngân
- Nguyễn Ngọc Ánh  
- Đinh Tuấn Anh

**Cải tiến so với phiên bản gốc:**
- ✅ Tích hợp đầy đủ 3 modules (Nhân sự - Chấm công - Tính lương)
- ✅ Tự động tính lương theo công thức Việt Nam
- ✅ Tính thuế TNCN theo 7 bậc thuế suất
- ✅ Tính bảo hiểm (BHXH, BHYT, BHTN) tự động
- ✅ Báo cáo trực quan với Pivot & Graph
- ✅ Workflow hoàn chỉnh từ nhân sự → chấm công → tính lương
- ✅ Giao diện người dùng thân thiện, 100% tiếng Việt
- ✅ Xử lý ràng buộc dữ liệu chặt chẽ

---

## 🎯 Tính năng chính

### 📋 Module 1: Quản lý Nhân sự (nhan_su_upgraded)

#### Quản lý thông tin nhân viên
- **📝 Hồ sơ nhân viên đầy đủ:**
  - Thông tin cá nhân: Họ tên, ngày sinh, CCCD, địa chỉ, điện thoại, email
  - Thông tin công việc: Mã nhân viên, phòng ban, chức vụ, ngày vào làm
  - Trạng thái làm việc: Đang làm việc, Nghỉ việc, Tạm nghỉ
  
- **📁 Quản lý phòng ban:**
  - Tạo, sửa, xóa phòng ban
  - Phân quyền trưởng phòng
  - Theo dõi số lượng nhân viên theo phòng
  
- **🏢 Quản lý chức vụ:**
  - Định nghĩa các chức vụ: Nhân viên, Trưởng phòng, Giám đốc
  - Phân cấp chức vụ
  
- **📄 Quản lý hợp đồng lao động:**
  - Hợp đồng thử việc, chính thức, thời vụ
  - Lương cơ bản theo hợp đồng
  - Ngày hiệu lực, ngày hết hạn
  - Trạng thái: Đang hiệu lực, Hết hạn

- **⭐ Đánh giá nhân viên:**
  - Xếp loại: Xuất sắc, Tốt, Trung bình, Yếu
  - Ghi chú đánh giá
  - Lịch sử đánh giá

- **🎒 Quản lý tài sản:**
  - Cấp phát tài sản cho nhân viên
  - Theo dõi tình trạng: Đang sử dụng, Đã trả lại, Hỏng

### ⏰ Module 2: Chấm công (cham_cong)

#### Đăng ký ca làm
- **📅 Đợt đăng ký ca làm:**
  - Tạo đợt đăng ký theo tháng
  - Thêm danh sách nhân viên vào đợt
  - Hạn đăng ký
  
- **🕐 Đăng ký theo ngày:**
  - Nhân viên đăng ký ca: Sáng, Chiều, Cả ngày
  - Mã đợt tự động generate (tránh trùng lặp)
  - Constraint: Mỗi nhân viên chỉ đăng ký 1 ca/ngày

- **⚙️ Cấu hình ca làm việc:**
  - Tên ca: Ca Sáng, Ca Chiều, Ca Tối
  - Giờ bắt đầu, giờ kết thúc
  - Giờ check-in, check-out

#### Quản lý chấm công
- **✅ Bảng chấm công hàng ngày:**
  - Tự động tính trạng thái: Đi làm, Đi muộn, Về sớm, Vắng mặt
  - Tính phút đi muộn, phút về sớm
  - Liên kết với đơn từ (nghỉ phép)
  
- **📊 Tổng hợp công tháng:**
  - Tổng hợp tự động từ bảng chấm công
  - Button "Tính lại" để refresh dữ liệu
  - Thống kê:
    - Số ngày đi làm
    - Số ngày đi muộn, về sớm
    - Tổng phút đi muộn, về sớm
    - Số ngày vắng mặt, nghỉ có phép
  - Tỷ lệ: % đi làm đúng giờ, % vắng mặt
  - Xếp loại tự động: Xuất sắc, Tốt, Trung bình, Yếu

- **📝 Quản lý đơn từ:**
  - Loại đơn: Nghỉ phép, Tăng ca, Đi công tác
  - Trạng thái duyệt: Chờ duyệt, Đã duyệt, Từ chối
  - Ngày bắt đầu, ngày kết thúc
  - Lý do

### 💰 Module 3: Tính lương (tinh_luong)

#### Cấu hình tính lương
- **⚙️ Cấu hình chung:**
  - Tỷ lệ BHXH: 8%
  - Tỷ lệ BHYT: 1.5%
  - Tỷ lệ BHTN: 1%
  - Mức giảm trừ gia cảnh: 11,000,000 VNĐ
  - Mức giảm trừ người phụ thuộc: 4,400,000 VNĐ
  
- **📊 Bậc thuế TNCN (7 bậc):**
  - Bậc 1: 0 - 5 triệu: 5%
  - Bậc 2: >5 - 10 triệu: 10%
  - Bậc 3: >10 - 18 triệu: 15%
  - Bậc 4: >18 - 32 triệu: 20%
  - Bậc 5: >32 - 52 triệu: 25%
  - Bậc 6: >52 - 80 triệu: 30%
  - Bậc 7: >80 triệu: 35%

#### Quản lý phụ cấp
- **💵 Loại phụ cấp:**
  - Phụ cấp ăn trưa, xăng xe, điện thoại, nhà ở...
  - Mức phụ cấp cố định
  
- **👤 Phụ cấp nhân viên:**
  - Gán phụ cấp cho từng nhân viên
  - Ngày áp dụng, ngày kết thúc
  - Trạng thái: Đang áp dụng, Đã kết thúc

#### Tính lương
- **💼 Bảng lương:**
  - **Tự động load khi chọn nhân viên:**
    - Lương cơ bản (từ hợp đồng)
    - Số ngày làm việc (từ tổng hợp công)
    - Phụ cấp đang áp dụng
  
  - **Thu nhập:**
    - Lương theo công = Lương cơ bản × (Số ngày làm / 22)
    - Tổng phụ cấp
    - Thưởng (nhập thủ công)
    - Tăng ca (nhập thủ công với số giờ × đơn giá)
    - Thu nhập khác
  
  - **Khấu trừ:**
    - BHXH = Lương cơ bản × 8%
    - BHYT = Lương cơ bản × 1.5%
    - BHTN = Lương cơ bản × 1%
    - Thuế TNCN (tính theo 7 bậc thuế suất)
    - Phạt (tự động từ chấm công hoặc nhập thủ công)
    - Khấu trừ khác
  
  - **Lương thực lĩnh:**
    ```
    Lương thực lĩnh = Tổng thu nhập - Tổng khấu trừ
    ```
  
  - **Button "Tính lương":** Tự động tính toán tất cả
  - **Trạng thái:** Nháp → Đã tính → Đã duyệt → Đã thanh toán

- **📋 Chi tiết lương:**
  - Tab "Chi tiết thu nhập": Phụ cấp, Thưởng, Tăng ca, Thu nhập khác
  - Tab "Khấu trừ": Bảo hiểm, Thuế, Phạt, Khấu trừ khác
  - Tab "Thanh toán": Thông tin chuyển khoản, ghi chú

#### Báo cáo
- **📊 Báo cáo lương:**
  - View: Tree, Pivot, Graph
  - Lọc theo: Phòng ban, Tháng, Năm, Trạng thái
  - Tổng hợp: Tổng lương theo phòng ban, theo tháng
  - Biểu đồ trực quan

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

<p align="center">
  <img src="images/sodo.png" alt="System Architecture" width="100%"/>
</p>


### Quan hệ giữa các modules:

```python
# Module Nhân sự → Chấm công
hop_dong_lao_dong.nhan_vien_id → bang_cham_cong.nhan_vien_id

# Module Chấm công → Tính lương
tong_hop_cong_thang → bang_luong.tong_hop_cong_id

# Module Nhân sự → Tính lương
hop_dong_lao_dong.muc_luong_co_ban → bang_luong.luong_co_ban
phu_cap_nhan_vien → bang_luong.chi_tiet_phu_cap_ids
```

---

## 📂 Cấu trúc dự án

```
📦 he-thong-quan-ly-nhan-su
├── 📂 nhan_su_upgraded/              # Module Quản lý Nhân sự
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── nhan_vien.py             # Model Nhân viên
│   │   ├── phong_ban.py             # Model Phòng ban
│   │   ├── chuc_vu.py               # Model Chức vụ
│   │   ├── hop_dong_lao_dong.py     # Model Hợp đồng
│   │   ├── danh_gia_nhan_vien.py    # Model Đánh giá
│   │   └── tai_san.py               # Model Tài sản
│   ├── 📂 views/
│   │   ├── nhan_vien.xml
│   │   ├── phong_ban.xml
│   │   ├── chuc_vu.xml
│   │   ├── hop_dong_lao_dong.xml
│   │   ├── menu.xml
│   │   └── ...
│   ├── 📂 security/
│   │   ├── ir.model.access.csv      # Phân quyền
│   │   └── security.xml
│   ├── 📂 data/
│   │   ├── phong_ban_data.xml       # Dữ liệu mẫu
│   │   └── chuc_vu_data.xml
│   ├── __init__.py
│   └── __manifest__.py
│
├── 📂 cham_cong/                      # Module Chấm công
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── dot_dang_ky.py           # Model Đợt đăng ký
│   │   ├── dang_ky_ca_lam_theo_ngay.py
│   │   ├── bang_cham_cong.py        # Model Bảng chấm công
│   │   ├── tong_hop_cong_thang.py   # Model Tổng hợp công
│   │   ├── ca_lam_viec.py           # Model Ca làm việc
│   │   └── don_tu.py                # Model Đơn từ
│   ├── 📂 views/
│   │   ├── dot_dang_ky.xml
│   │   ├── bang_cham_cong.xml
│   │   ├── tong_hop_cong_thang.xml
│   │   ├── menu.xml
│   │   └── ...
│   ├── 📂 security/
│   │   └── ir.model.access.csv
│   ├── 📂 data/
│   │   └── ca_lam_viec_data.xml     # Dữ liệu ca làm việc
│   ├── __init__.py
│   └── __manifest__.py
│
├── 📂 tinh_luong/                     # Module Tính lương
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── bang_luong.py            # Model Bảng lương
│   │   ├── chi_tiet_luong.py        # Model Chi tiết lương
│   │   ├── loai_phu_cap.py          # Model Loại phụ cấp
│   │   ├── phu_cap_nhan_vien.py     # Model Phụ cấp nhân viên
│   │   ├── bac_thue_tncn.py         # Model Bậc thuế
│   │   ├── cau_hinh_luong.py        # Model Cấu hình
│   │   └── bao_cao_luong.py         # Model Báo cáo
│   ├── 📂 views/
│   │   ├── bang_luong.xml
│   │   ├── loai_phu_cap.xml
│   │   ├── phu_cap_nhan_vien.xml
│   │   ├── bac_thue_tncn.xml
│   │   ├── bao_cao_luong.xml
│   │   ├── menu.xml
│   │   └── ...
│   ├── 📂 security/
│   │   └── ir.model.access.csv
│   ├── 📂 data/
│   │   ├── loai_phu_cap_data.xml    # Dữ liệu phụ cấp
│   │   ├── bac_thue_data.xml        # Dữ liệu bậc thuế
│   │   └── cau_hinh_luong_data.xml  # Cấu hình mặc định
│   ├── __init__.py
│   └── __manifest__.py
│
├── 📄 README.md                       # File này
├── 📄 LICENSE
└── 📄 .gitignore
```

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

<div align="center">

### 🖥️ Nền tảng

[![Odoo](https://img.shields.io/badge/Odoo-15.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)

### 📚 Framework & Libraries

[![XML](https://img.shields.io/badge/XML-Views-orange?style=for-the-badge&logo=xml)](https://www.w3.org/XML/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Web-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![QWeb](https://img.shields.io/badge/QWeb-Template-blue?style=for-the-badge)](https://www.odoo.com/documentation/15.0/developer/reference/frontend/qweb.html)
[![ORM](https://img.shields.io/badge/ORM-Odoo-success?style=for-the-badge)](https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html)

### 🎨 Frontend

[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.x-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![jQuery](https://img.shields.io/badge/jQuery-3.x-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com)

</div>

---

## 🛠️ Yêu cầu hệ thống

### 💻 Phần cứng tối thiểu
- **CPU:** Intel Core i3 hoặc tương đương (khuyến nghị i5 trở lên)
- **RAM:** 4GB (khuyến nghị 8GB trở lên)
- **Ổ cứng:** 10GB dung lượng trống
- **Màn hình:** Độ phân giải tối thiểu 1366x768

### 🐧 Hệ điều hành
- **Ubuntu:** 20.04 LTS / 22.04 LTS (khuyến nghị)
- **Windows:** 10/11 với WSL2
- **macOS:** 10.15 Catalina trở lên
- **Linux:** Bất kỳ distribution nào hỗ trợ Python 3.8+

### 📦 Phần mềm cần cài đặt

#### 1. Python 3.8+
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.8 python3.8-venv python3-pip

# Kiểm tra version
python3 --version
```

#### 2. PostgreSQL 13+
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# Tạo database
sudo -u postgres createdb odoo_hrms
```

#### 3. Odoo 15
```bash
# Clone Odoo 15
git clone https://github.com/odoo/odoo.git --branch 15.0 --depth 1

# Cài đặt dependencies
pip3 install -r odoo/requirements.txt
```

#### 4. Các thư viện Python cần thiết
```bash
pip3 install --upgrade pip
pip3 install wheel
pip3 install python-dateutil
pip3 install lxml
pip3 install reportlab
pip3 install xlsxwriter
```

---

## 🚀 Hướng dẫn cài đặt và chạy

### Bước 1️⃣: Chuẩn bị môi trường

```bash
# Clone repository (hoặc giải nén file đã tải)
cd ~
mkdir odoo-fitdnu
cd odoo-fitdnu

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### Bước 2️⃣: Cài đặt Odoo 15

```bash
# Clone Odoo (nếu chưa có)
git clone https://github.com/odoo/odoo.git --branch 15.0 --depth 1

# Cài đặt dependencies
pip install -r odoo/requirements.txt
```

### Bước 3️⃣: Cấu hình PostgreSQL

```bash
# Tạo user PostgreSQL
sudo -u postgres createuser -s $USER

# Tạo database
createdb odoo_hrms

# Hoặc sử dụng psql
psql -U postgres
CREATE DATABASE odoo_hrms;
CREATE USER odoo WITH PASSWORD 'odoo';
GRANT ALL PRIVILEGES ON DATABASE odoo_hrms TO odoo;
\q
```

### Bước 4️⃣: Cài đặt modules

```bash
# Giải nén file HE_THONG_FIX_BANG_LUONG_FINAL.tar.gz
tar -xzf HE_THONG_FIX_BANG_LUONG_FINAL.tar.gz

# Copy modules vào addons
mkdir -p addons
cp -r full_system/* addons/

# Hoặc tạo symbolic link
ln -s ~/full_system/nhan_su_upgraded addons/
ln -s ~/full_system/cham_cong addons/
ln -s ~/full_system/tinh_luong addons/
```

### Bước 5️⃣: Tạo file cấu hình Odoo

```bash
# Tạo file odoo.conf
cat > odoo.conf << EOF
[options]
; Database settings
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_hrms

; Addons path
addons_path = odoo/addons,addons

; Server settings
http_port = 8069
admin_passwd = admin

; Log
logfile = odoo.log
log_level = info
EOF
```

### Bước 6️⃣: Khởi động Odoo

```bash
# Khởi động lần đầu (cài đặt database)
python3 odoo/odoo-bin -c odoo.conf -d odoo_hrms --without-demo=all --stop-after-init

# Khởi động bình thường
python3 odoo/odoo-bin -c odoo.conf

# Hoặc với dev mode (auto-reload)
python3 odoo/odoo-bin -c odoo.conf --dev=all
```

### Bước 7️⃣: Truy cập hệ thống

1. Mở trình duyệt và truy cập: `http://localhost:8069`
2. Đăng nhập với:
   - **Email:** admin
   - **Password:** admin
3. Chọn database: `odoo_hrms`

### Bước 8️⃣: Cài đặt modules

1. Vào **Apps** (Ứng dụng)
2. Click **Update Apps List** (Cập nhật danh sách ứng dụng)
3. Tìm và cài đặt theo thứ tự:
   - **Quản lý Nhân sự** (nhan_su_upgraded)
   - **Chấm công** (cham_cong)
   - **Tính lương** (tinh_luong)

📌 **Lưu ý:** Phải cài đặt đúng thứ tự vì các module có dependency với nhau!

---

## 📖 Hướng dẫn sử dụng

### 🎬 WORKFLOW HOÀN CHỈNH

#### GIAI ĐOẠN 1: THIẾT LẬP HỆ THỐNG (1 lần)

##### 1.1. Tạo dữ liệu cơ bản

```
Menu: Nhân sự
```

**Bước 1: Tạo Phòng ban**
```
Nhân sự > Cấu hình > Phòng ban > Tạo mới

- Tên phòng ban: Phòng Kinh doanh
- Mô tả: Phòng kinh doanh và bán hàng
- Lưu
```

**Bước 2: Tạo Chức vụ**
```
Nhân sự > Cấu hình > Chức vụ > Tạo mới

- Tên chức vụ: Nhân viên
- Mô tả: Nhân viên bình thường
- Lưu

(Lặp lại cho: Trưởng phòng, Giám đốc...)
```

**Bước 3: Cấu hình Ca làm việc**
```
Menu: Chấm công

Chấm công > Cấu hình > Ca làm việc > Tạo mới

Ca Sáng:
- Tên ca: Ca Sáng
- Giờ bắt đầu: 08:00
- Giờ kết thúc: 12:00
- Giờ check-in: 08:00
- Giờ check-out: 12:00
- Lưu

Ca Chiều:
- Tên ca: Ca Chiều
- Giờ bắt đầu: 13:00
- Giờ kết thúc: 17:00
- Giờ check-in: 13:00
- Giờ check-out: 17:00
- Lưu
```

**Bước 4: Cấu hình Loại phụ cấp**
```
Menu: Tính lương

Tính lương > Phụ cấp > Loại phụ cấp > Tạo mới

- Tên phụ cấp: Phụ cấp ăn trưa
- Mức phụ cấp mặc định: 1,000,000
- Mô tả: Phụ cấp ăn trưa hàng tháng
- Lưu

(Lặp lại cho: Phụ cấp xăng xe, điện thoại...)
```

##### 1.2. Kiểm tra Bậc thuế TNCN

```
Tính lương > Cấu hình > Bậc thuế TNCN

✅ Hệ thống đã có sẵn 7 bậc thuế theo quy định Việt Nam
```

#### GIAI ĐOẠN 2: QUẢN LÝ NHÂN VIÊN

##### 2.1. Tạo nhân viên mới

```
Nhân sự > Nhân viên > Tạo mới

Tab "Thông tin cá nhân":
- Họ và tên: Nguyễn Văn A
- Mã nhân viên: NV001 (tự động nếu bỏ trống)
- Ngày sinh: 01/01/1990
- Giới tính: Nam
- CCCD: 001234567890
- Điện thoại: 0912345678
- Email: nva@company.com

Tab "Thông tin công việc":
- Phòng ban: Phòng Kinh doanh
- Chức vụ: Nhân viên
- Ngày vào làm: 01/01/2024
- Trạng thái: Đang làm việc

Lưu
```

##### 2.2. Tạo hợp đồng lao động

```
Nhân sự > Hợp đồng > Tạo mới

- Nhân viên: Nguyễn Văn A
- Loại hợp đồng: Chính thức
- Mức lương cơ bản: 15,000,000 VNĐ
- Ngày hiệu lực: 01/01/2024
- Trạng thái: Đang hiệu lực
- Ghi chú: Hợp đồng chính thức 2 năm

Lưu

✅ Lương cơ bản này sẽ được dùng để tính lương
```

##### 2.3. Tạo phụ cấp cho nhân viên (TÙY CHỌN)

```
Tính lương > Phụ cấp > Phụ cấp nhân viên > Tạo mới

- Nhân viên: Nguyễn Văn A
- Loại phụ cấp: Phụ cấp ăn trưa
- Mức phụ cấp: 1,000,000 VNĐ
- Ngày áp dụng: 01/01/2024
- Trạng thái: Đang áp dụng

Lưu

✅ Phụ cấp này sẽ tự động được thêm vào bảng lương
```

#### GIAI ĐOẠN 3: CHẤM CÔNG

##### 3.1. Tạo đợt đăng ký ca làm

```
Chấm công > Đợt đăng ký > Tạo mới

- Mã đợt: DOT_01_2026 (có thể điền hoặc để trống)
- Tháng đăng ký: 1
- Năm đăng ký: 2026
- Ngày bắt đầu: 01/01/2026
- Ngày kết thúc: 31/01/2026
- Hạn đăng ký: 25/12/2025

Tab "Nhân viên đăng ký": Thêm nhân viên
- Click "Add a line"
- Chọn: Nguyễn Văn A
- Chọn thêm các nhân viên khác

Lưu
```

##### 3.2. Đăng ký ca làm cho nhân viên

```
Chấm công > Đăng ký theo ngày > Tạo mới

- Đợt đăng ký: DOT_01_2026
- Nhân viên: Nguyễn Văn A
- Ngày làm: 01/01/2026
- Ca làm: Cả ngày

Lưu

✅ Mã đợt ngày tự động: DOT_01_2026_NV001_20260101

Lặp lại cho các ngày khác trong tháng...
```

##### 3.3. Chấm công hàng ngày

```
Chấm công > Bảng chấm công > Tạo mới

Ngày 01/01/2026:
- Nhân viên: Nguyễn Văn A
- Ngày chấm công: 01/01/2026
- Ca làm việc: Ca Sáng
- Giờ vào: 08:00
- Giờ ra: 12:00
- Lưu

✅ Trạng thái tự động: Đi làm
✅ Phút đi muộn: 0
✅ Phút về sớm: 0

Ngày 02/01/2026:
- Nhân viên: Nguyễn Văn A
- Ngày chấm công: 02/01/2026
- Ca làm việc: Ca Sáng
- Giờ vào: 08:15 (đi muộn)
- Giờ ra: 12:00
- Lưu

✅ Trạng thái tự động: Đi muộn
✅ Phút đi muộn: 15
✅ Phút về sớm: 0

...Tiếp tục chấm công cho các ngày khác
```

##### 3.4. Tổng hợp công cuối tháng

```
Chấm công > Tổng hợp công tháng > Tạo mới

- Nhân viên: Nguyễn Văn A
- Tháng: 1
- Năm: 2026
- Lưu

✅ Hệ thống TỰ ĐỘNG tính:
- Số ngày đi làm: 20
- Số ngày đi muộn: 3
- Tổng phút đi muộn: 45
- Số ngày vắng mặt: 2
- Tỷ lệ đi làm đúng giờ: 90.91%
- Xếp loại: Tốt

Nếu số liệu = 0:
→ Click button "TÍNH LẠI"

✅ Dữ liệu này sẽ được dùng để tính lương
```

#### GIAI ĐOẠN 4: TÍNH LƯƠNG

##### 4.1. Tạo bảng lương

```
Tính lương > Bảng lương > Tạo mới

- Nhân viên: Nguyễn Văn A
- Tháng: 1
- Năm: 2026

✅ SAU KHI CHỌN NHÂN VIÊN, TỰ ĐỘNG HIỂN THỊ:

Thông tin lương:
- Lương cơ bản: 15,000,000 VNĐ (từ hợp đồng)
- Số ngày công chuẩn: 22
- Số ngày làm việc: 20 (từ tổng hợp công)
- Số ngày nghỉ có phép: 0
- Số ngày vắng không phép: 2

Chi tiết thu nhập:
- Tổng hợp công: THC-NV001-1/2026 (có link)
- Tab "Phụ cấp": 
  * Phụ cấp ăn trưa: 1,000,000 VNĐ (tự động)

Lưu
```

##### 4.2. Thêm thưởng (NẾU CÓ)

```
Tab "Chi tiết thu nhập" > Section "Thưởng" > Add a line

- Tên khoản: Thưởng doanh số
- Số tiền: 2,000,000 VNĐ
- Ghi chú: Đạt 120% target
- Lưu dòng

✅ Loại tự động = 'thuong'
```

##### 4.3. Thêm tăng ca (NẾU CÓ)

```
Tab "Chi tiết thu nhập" > Section "Tăng ca" > Add a line

- Tên khoản: Tăng ca ngày thường
- Số lượng: 10 (giờ)
- Đơn vị: giờ
- Đơn giá: 100,000 VNĐ
- Lưu dòng

✅ Số tiền tự động = 10 × 100,000 = 1,000,000 VNĐ
```

##### 4.4. Thêm phạt (NẾU CÓ)

```
Tab "Khấu trừ" > Section "Phạt" > Add a line

- Tên khoản: Phạt đi muộn
- Số tiền: 100,000 VNĐ
- Ghi chú: 3 lần đi muộn, mỗi lần 33,333đ
- Lưu dòng
```

##### 4.5. Tính lương

```
Click button "TÍNH LƯƠNG"

✅ Hệ thống TỰ ĐỘNG tính:

LƯƠNG THEO CÔNG:
= 15,000,000 × (20/22) = 13,636,364 VNĐ

TỔNG THU NHẬP:
= Lương theo công + Phụ cấp + Thưởng + Tăng ca
= 13,636,364 + 1,000,000 + 2,000,000 + 1,000,000
= 17,636,364 VNĐ

BẢO HIỂM:
- BHXH: 15,000,000 × 8% = 1,200,000 VNĐ
- BHYT: 15,000,000 × 1.5% = 225,000 VNĐ
- BHTN: 15,000,000 × 1% = 150,000 VNĐ
- Tổng: 1,575,000 VNĐ

THUẾ TNCN:
Thu nhập tính thuế = 17,636,364 - 1,575,000 - 11,000,000 = 5,061,364 VNĐ
- Bậc 1 (0-5tr): 5,000,000 × 5% = 250,000 VNĐ
- Bậc 2 (>5tr): 61,364 × 10% = 6,136 VNĐ
- Tổng thuế: 256,136 VNĐ

TỔNG KHẤU TRỪ:
= Bảo hiểm + Thuế + Phạt
= 1,575,000 + 256,136 + 100,000
= 1,931,136 VNĐ

LƯƠNG THỰC LĨNH:
= 17,636,364 - 1,931,136
= 15,705,228 VNĐ

Trạng thái: Đã tính
```

##### 4.6. Duyệt và thanh toán

```
Click button "XÁC NHẬN"
→ Trạng thái: Đã duyệt

Tab "Thanh toán": Nhập thông tin
- Phương thức: Chuyển khoản
- Ngân hàng: Vietcombank
- Số tài khoản: 1234567890
- Ngày thanh toán: 05/02/2026

Click button "THANH TOÁN"
→ Trạng thái: Đã thanh toán
```

#### GIAI ĐOẠN 5: XEM BÁO CÁO

##### 5.1. Báo cáo lương

```
Tính lương > Báo cáo > Báo cáo lương

View Tree (Bảng):
- Hiển thị danh sách lương đã tính
- Lọc theo: Phòng ban, Tháng, Năm
- Tìm kiếm nhân viên

View Pivot (Tổng hợp):
- Hàng: Phòng ban
- Cột: Tháng
- Giá trị: Lương thực lĩnh
- Tổng: Theo phòng ban, theo tháng

View Graph (Biểu đồ):
- Biểu đồ cột: Lương theo phòng ban
- Biểu đồ đường: Lương theo tháng
- Biểu đồ tròn: Tỷ lệ lương các phòng
```

---


## 📊 Schema Database

### Core Tables

```sql
-- Module Nhân sự
nhan_vien               (10 fields)
phong_ban               (5 fields)
chuc_vu                 (4 fields)
hop_dong_lao_dong       (12 fields)
danh_gia_nhan_vien      (8 fields)
tai_san                 (10 fields)

-- Module Chấm công
dot_dang_ky             (10 fields)
dang_ky_ca_lam_theo_ngay (6 fields)
bang_cham_cong          (15 fields)
tong_hop_cong_thang     (18 fields)
ca_lam_viec             (8 fields)
don_tu                  (12 fields)

-- Module Tính lương
bang_luong              (35 fields)
chi_tiet_luong          (10 fields)
loai_phu_cap            (5 fields)
phu_cap_nhan_vien       (8 fields)
bac_thue_tncn           (6 fields)
cau_hinh_luong          (10 fields)
bao_cao_luong           (20 fields - SQL View)
```

## 📰 Poster
<p align="center">
  <img src="images/poster.jpg" alt="System Architecture" width="100%"/>
</p>

## 🤝 Đóng góp

### Nhóm phát triển

<table>
<tr>
<th width="25%">Chu Văn Huy</th>
<th width="25%">Phạm Ngọc Minh</th>
<th width="25%">Nguyễn Thành Trung</th>
<th width="25%">Nguồn tham khảo</th>
</tr>
<tr>
<td valign="top">

**Vai trò:** Trưởng nhóm

**Công việc:**
- ✅ Thiết kế kiến trúc hệ thống
- ✅ Phát triển module Nhân sự (10 models)
- ✅ Quản lý dự án
- ✅ Tích hợp 3 modules
- ✅ Viết tài liệu kỹ thuật
- ✅ Kiểm thử tổng thể
- ✅ Deploy và maintenance

**Kỹ năng:**
- Python, Odoo ORM
- PostgreSQL
- Git, GitHub
- Project Management

</td>
<td valign="top">

**Vai trò:** Thành viên

**Công việc:**
- ✅ Phát triển module Chấm công (7 models)
- ✅ Thiết kế database
- ✅ Logic tính toán công
- ✅ Workflow đăng ký ca làm
- ✅ Tổng hợp công tháng
- ✅ Kiểm thử module chấm công
- ✅ Viết tài liệu người dùng

**Kỹ năng:**
- Python, Odoo
- Database Design
- SQL
- API Development

</td>
<td valign="top">

**Vai trò:** Thành viên

**Công việc:**
- ✅ Phát triển module Tính lương (7 models)
- ✅ Logic tính thuế TNCN (7 bậc)
- ✅ Logic tính bảo hiểm
- ✅ Báo cáo lương
- ✅ Pivot & Graph views
- ✅ Kiểm thử tích hợp
- ✅ Xử lý lỗi và debug

**Kỹ năng:**
- Python, Odoo
- Business Logic
- Report Development
- Testing

</td>
<td valign="top">

**Khóa trước:**
CNTT 15-01

**Thành viên:**
- Hoàng Thị Kim Ngân
- Nguyễn Ngọc Ánh
- Đinh Tuấn Anh

**Đề tài gốc:**
Hệ thống quản lý nhân sự cơ bản

**Cảm ơn:**
Đề tài của các anh/chị đã cung cấp ý tưởng và hướng phát triển cho dự án của chúng em.

</td>
</tr>
</table>



---

## 📞 Liên hệ

### Thông tin nhóm

**Nhóm 11 - CNTT 16-05**  
**Trường Đại học Đại Nam**

| Thành viên | Email | Role |
|------------|-------|------|
| Chu Văn Huy | chuvanhuy@student.dainam.edu.vn | Trưởng nhóm |
| Phạm Ngọc Minh | phamngocminh@student.dainam.edu.vn | Thành viên |
| Nguyễn Thành Trung | nguyenthanhtrung@student.dainam.edu.vn | Thành viên |

### Giảng viên hướng dẫn

**[ThS. Lê Tuấn Anh]**   
**[Ths. Nguyễn Thế Huy Hoàng]**   
Bộ môn: Thực tập doanh nghiệp
---

## 🎯 Kế hoạch phát triển

### Version 2.0 (Tương lai)

**Tính năng mới:**
- [ ] Module Tuyển dụng
- [ ] Module Đào tạo
- [ ] Tích hợp máy chấm công vân tay
- [ ] Mobile App (iOS/Android)
- [ ] AI phân tích dự đoán
- [ ] Chatbot hỗ trợ
- [ ] Dashboard analytics
- [ ] Export PDF/Excel reports

**Cải tiến:**
- [ ] Performance optimization
- [ ] Unit testing (coverage > 80%)
- [ ] API documentation (Swagger)
- [ ] Multi-company support
- [ ] Role-based access control
- [ ] Audit log

---

<div align="center">


### 👨‍🎓 Nhóm 11 - Lớp CNTT 16-05

| STT | Họ và tên | MSV | Vai trò |
|-----|-----------|------|---------|
| 1 | **Chu Văn Huy** | 1671020136 | Trưởng nhóm |
| 2 | Phạm Ngọc Minh | 1671020205 | Thành viên |
| 3 | Nguyễn Thành Trung | 1671020327 | Thành viên |

---

### 📚 Nguồn tham khảo

**Đề tài gốc:** Hệ thống quản lý nhân sự  
**Khóa:** CNTT 15-01  
**Sinh viên:**
- Hoàng Thị Kim Ngân
- Nguyễn Ngọc Ánh
- Đinh Tuấn Anh

---

© 2025 NHÓM 11, CNTT 16-05, TRƯỜNG ĐẠI HỌC ĐẠI NAM

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://github.com/yourusername/hrms-odoo15)
[![Odoo](https://img.shields.io/badge/Powered%20by-Odoo%2015-714B67?style=for-the-badge&logo=odoo)](https://www.odoo.com)

**⭐ Nếu dự án hữu ích, hãy cho chúng em 1 star! ⭐**

</div>
