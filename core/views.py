import shutil
import os
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Nhớ import các hàm cũ từ file utils của chúng ta!
from .utils import get_recent_files, get_directory_size, format_size, get_file_properties

def get_folder_size(folder_path):
    """Hàm tính dung lượng thư mục (chạy đệ quy)"""
    total_size = 0
    try:
        for entry in os.scandir(folder_path):
            if entry.is_file(follow_symlinks=False):
                total_size += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                total_size += get_folder_size(entry.path)
    except Exception:
        pass
    return total_size

# Thêm "bảo vệ" bắt buộc đăng nhập cho trang chủ
@login_required(login_url='login')
def dashboard_view(request):
    """HÀM DUY NHẤT XỬ LÝ TOÀN BỘ GIAO DIỆN"""
    
    # ==========================================
    # PHẦN 1: XỬ LÝ Ổ ĐĨA & BIỂU ĐỒ TRÒN
    # ==========================================
    selected_drive = request.GET.get('drive', 'C:')
    sort_by = request.GET.get('sort', 'name_asc')
    show_modal = request.GET.get('show_modal', 'false')
    calc_size = request.GET.get('calc_size', 'false')
    
    root_path = f"{selected_drive}\\"
    current_path = request.GET.get('path', root_path)

    if not current_path.startswith(selected_drive):
        current_path = root_path

    # Quét dung lượng tổng ổ đĩa
    try:
        usage = shutil.disk_usage(root_path)
        he_so = 1024 ** 3
        tong_dung_luong = round(usage.total / he_so, 1)
        da_su_dung = round(usage.used / he_so, 1)
        phan_tram = round((usage.used / usage.total) * 100) if usage.total > 0 else 0
    except:
        tong_dung_luong, da_su_dung, phan_tram = 0, 0, 0

    # ==========================================
    # PHẦN 2: XỬ LÝ DANH SÁCH FILE TRONG MODAL CHI TIẾT
    # ==========================================
    file_list = []
    if os.path.exists(current_path):
        try:
            with os.scandir(current_path) as entries:
                for entry in entries:
                    try:
                        stat = entry.stat()
                        size_mb = 0
                        is_scanned = False
                        
                        if entry.is_dir():
                            if calc_size == 'true':
                                size_bytes = get_folder_size(entry.path)
                                size_mb = round(size_bytes / (1024 * 1024), 2)
                                is_scanned = True
                        else:
                            size_mb = round(stat.st_size / (1024 * 1024), 2)
                            is_scanned = True
                            
                        file_list.append({
                            'name': entry.name,
                            'full_path': entry.path,
                            'is_dir': entry.is_dir(),
                            'size': size_mb,
                            'is_scanned': is_scanned,
                            'date': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M'),
                            'timestamp': stat.st_mtime
                        })
                    except: pass
        except: pass

    # ==========================================
    # PHẦN 3: TỆP TIN GẦN ĐÂY 
    # ==========================================
    recent_dir = r"C:\Users\Acer\Downloads" 
    recent_files = get_recent_files(recent_dir, limit=4)

    # ==========================================
    # ĐÓNG GÓI TOÀN BỘ DỮ LIỆU GỬI RA HTML
    # ==========================================
    context = {
        'tong_dung_luong': tong_dung_luong,
        'da_su_dung': da_su_dung,
        'phan_tram': phan_tram,
        'selected_drive': selected_drive,
        'current_path': current_path,
        'file_list': file_list,
        'sort_by': sort_by,
        'show_modal': show_modal,
        'calc_size': calc_size,
        'recent_files': recent_files, 
    }
    
    return render(request, 'dashboard.html', context)
from django.shortcuts import render
from .utils import get_file_properties # Import hàm từ file utils vừa tạo

def dashboard_view(request):
    # Đường dẫn thư mục bạn muốn test (nhớ đổi thành đường dẫn thật trên máy bạn)
    test_file_path = r"C:\ThuMucCuaBan\file_test.txt" 
    
    # Gọi hàm để lấy thông tin
    file_info = get_file_properties(test_file_path)
    
    # Truyền dữ liệu này ra giao diện (template)
    context = {
        'file_info': file_info
    }
    return render(request, 'dashboard.html', context)


# ==========================================
# PHẦN 4: XỬ LÝ ĐĂNG NHẬP / ĐĂNG XUẤT (Tách biệt hoàn toàn)
# ==========================================
def login_view(request):
    """Hàm xử lý giao diện và logic đăng nhập"""
    error_msg = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user) 
            return redirect('dashboard') 
        else:
            error_msg = "Sai tên đăng nhập hoặc mật khẩu!"

    return render(request, 'login.html', {'error': error_msg})

def logout_view(request):
    """Hàm xử lý đăng xuất"""
    logout(request)
    return redirect('login')