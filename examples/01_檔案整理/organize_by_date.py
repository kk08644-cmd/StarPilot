#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檔案按類型和日期分類工具
先按檔案類型分類，再在每個類別下按修改日期的月份分類
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import time

# 定義檔案類型分類
FILE_CATEGORIES = {
    '文件': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls'],
    '圖片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    '影片': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
}

def get_file_category(filename):
    """根據檔案副檔名判斷分類"""
    ext = Path(filename).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return '其他'

def get_file_month(file_path):
    """獲取檔案的修改日期月份 (YYYY-MM 格式)"""
    try:
        mtime = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(mtime)
        return dt.strftime('%Y-%m')
    except:
        return '未知日期'

def organize_files_by_category_and_date(source_dir, dry_run=True):
    """
    按類型和日期分類檔案
    
    Args:
        source_dir: 來源資料夾路徑
        dry_run: 如果 True，只顯示預覽不實際移動；如果 False，實際執行移動
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ 資料夾不存在: {source_dir}")
        return
    
    # 統計檔案分類和日期
    files_structure = defaultdict(lambda: defaultdict(list))
    
    # 掃描所有檔案
    for file_path in sorted(source_path.iterdir()):
        if file_path.is_file() and file_path.name != 'README.md':
            category = get_file_category(file_path.name)
            month = get_file_month(file_path)
            files_structure[category][month].append(file_path.name)
    
    # 顯示分類結果
    print("\n" + "="*70)
    print("📊 檔案按類型和日期分類預覽")
    print("="*70)
    
    total_files = 0
    for category in ['文件', '圖片', '影片', '其他']:
        if category in files_structure:
            category_files = files_structure[category]
            total_category = sum(len(files) for files in category_files.values())
            print(f"\n📁 {category} ({total_category} 個檔案)")
            
            for month in sorted(category_files.keys()):
                files = category_files[month]
                print(f"   📅 {month} ({len(files)} 個)")
                for filename in files:
                    print(f"      └─ {filename}")
            
            total_files += total_category
    
    print("\n" + "="*70)
    print(f"📊 總計: {total_files} 個檔案")
    print("="*70)
    
    if dry_run:
        print("\n💡 預覽模式 - 檔案未實際移動")
        print("✅ 確認無誤後，請執行: python organize_by_date.py --execute")
        return True
    else:
        print("\n🚀 開始執行檔案分類...")
        
        # 建立資料夾並移動檔案
        for category in files_structure:
            category_dir = source_path / category
            category_dir.mkdir(exist_ok=True)
            
            for month in files_structure[category]:
                month_dir = category_dir / month
                month_dir.mkdir(exist_ok=True)
                
                for filename in files_structure[category][month]:
                    src_file = source_path / filename
                    dst_file = month_dir / filename
                    
                    try:
                        shutil.move(str(src_file), str(dst_file))
                        print(f"   ✓ {filename} → {category}/{month}/")
                    except Exception as e:
                        print(f"   ✗ {filename} 移動失敗: {e}")
        
        print("\n✅ 檔案分類完成！")
        print("\n📁 最終結構:")
        print_tree(source_path, prefix="")
        return True

def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """遞迴顯示資料夾樹狀結構"""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(directory.iterdir())
        dirs = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        # 顯示資料夾
        for i, dir_path in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            print(f"{prefix}{'└── ' if is_last_dir else '├── '}📁 {dir_path.name}/")
            new_prefix = prefix + ("    " if is_last_dir else "│   ")
            print_tree(dir_path, new_prefix, max_depth, current_depth + 1)
        
        # 顯示檔案數量（不逐個列出，因為可能太多）
        if files and current_depth < max_depth - 1:
            for i, file_path in enumerate(files):
                is_last = i == len(files) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}📄 {file_path.name}")
    except PermissionError:
        pass

if __name__ == "__main__":
    import sys
    
    # 測試資料夾路徑
    test_dir = Path(__file__).parent / "測試資料_待整理"
    
    # 檢查命令行參數
    execute = "--execute" in sys.argv or "-x" in sys.argv
    
    if execute:
        print("⚠️  確認將執行檔案移動操作...")
        response = input("請輸入 'yes' 確認: ").strip().lower()
        if response == 'yes':
            organize_files_by_category_and_date(test_dir, dry_run=False)
        else:
            print("❌ 已取消操作")
    else:
        print("🔍 預覽模式\n")
        organize_files_by_category_and_date(test_dir, dry_run=True)
