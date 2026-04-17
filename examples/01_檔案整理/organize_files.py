#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檔案分類整理工具
根據檔案類型將檔案分類到不同的資料夾
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

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

def organize_files(source_dir, dry_run=True):
    """
    按類型分類檔案
    
    Args:
        source_dir: 來源資料夾路徑
        dry_run: 如果 True，只顯示預覽不實際移動；如果 False，實際執行移動
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ 資料夾不存在: {source_dir}")
        return
    
    # 統計檔案分類
    files_by_category = defaultdict(list)
    
    # 掃描所有檔案
    for file_path in sorted(source_path.iterdir()):
        if file_path.is_file() and file_path.name != 'README.md':
            category = get_file_category(file_path.name)
            files_by_category[category].append(file_path.name)
    
    # 顯示分類結果
    print("\n" + "="*60)
    print("📊 檔案分類預覽")
    print("="*60)
    
    for category in ['文件', '圖片', '影片', '其他']:
        if category in files_by_category:
            files = files_by_category[category]
            print(f"\n📁 {category} ({len(files)} 個檔案)")
            for filename in files:
                print(f"   └─ {filename}")
    
    print("\n" + "="*60)
    
    if dry_run:
        print("\n💡 預覽模式 - 檔案未實際移動")
        print("✅ 確認無誤後，請執行: python organize_files.py --execute")
        return True
    else:
        print("\n🚀 開始執行檔案分類...")
        
        # 建立資料夾並移動檔案
        for category, files in files_by_category.items():
            category_dir = source_path / category
            category_dir.mkdir(exist_ok=True)
            
            for filename in files:
                src_file = source_path / filename
                dst_file = category_dir / filename
                
                try:
                    shutil.move(str(src_file), str(dst_file))
                    print(f"   ✓ {filename} → {category}/")
                except Exception as e:
                    print(f"   ✗ {filename} 移動失敗: {e}")
        
        print("\n✅ 檔案分類完成！")
        return True

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
            organize_files(test_dir, dry_run=False)
        else:
            print("❌ 已取消操作")
    else:
        print("🔍 預覽模式\n")
        organize_files(test_dir, dry_run=True)
