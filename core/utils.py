from pathlib import Path
import os
import datetime

def format_size(size_bytes):
    """Hàm chuyển đổi Byte sang KB, MB, GB..."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{round(size_bytes, 1)} {size_name[i]}"

def get_recent_files(directory_path, limit=4):
    """Hàm quét và lấy ra các tệp tin được sửa đổi gần đây nhất"""
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        return []

    files = []
    try:
        for item in path.iterdir():
            if item.is_file():
                stat = item.stat()
                files.append({
                    'name': item.name,
                    'size': format_size(stat.st_size),
                    'date': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y'),
                    'timestamp': stat.st_mtime
                })
    except Exception:
        pass

    # Sắp xếp theo thời gian (timestamp) giảm dần (mới nhất lên đầu)
    files.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Trả về số lượng file theo giới hạn (limit)
    return files[:limit]

def get_file_properties(file_path):
    """Hàm trích xuất thông tin chi tiết của một file"""
    path = Path(file_path)
    
    # Kiểm tra xem đường dẫn có tồn tại và có phải là file không
    if not path.is_file():
        return {"error": "Đường dẫn không hợp lệ hoặc không phải là file."}
        
    # 1. Lấy tên file (Bao gồm cả đuôi)
    file_name = path.name
    
    # 2. Lấy định dạng file (Đuôi file, ví dụ: .mp4, .docx)
    file_extension = path.suffix.lower() 
    
    # 3. Lấy kích thước file
    size_bytes = path.stat().st_size
    size_formatted = format_size(size_bytes)
    
    return {
        "name": file_name,
        "extension": file_extension,
        "size_formatted": size_formatted,
        "size_bytes": size_bytes 
    }

def get_directory_size(directory_path):
    """Tính tổng dung lượng của một thư mục (bao gồm cả thư mục con)"""
    path = Path(directory_path)
    total_size = 0
    
    if not path.is_dir():
        return 0
        
    for f in path.rglob('*'):
        if f.is_file():  # Kiểm tra nếu là file thì mới cộng dung lượng
            total_size += f.stat().st_size
            
    return total_size

# ==========================================
# KHỐI TEST CODE (Chỉ chạy khi chạy trực tiếp file này)
# ==========================================
if __name__ == "__main__":
    # Bạn có thể thay đường dẫn này bằng một file thực tế trên máy để test thử
    test_file = r"C:\MMM\file_test.txt"
    
    # ket_qua = get_file_properties(test_file)
    #- print(ket_qua)