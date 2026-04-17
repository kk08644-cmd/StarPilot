#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

# 資料夾路徑
folder_path = Path("/workspaces/StarPilot/examples/03_批次處理/測試資料/待重新命名")

# 取得所有圖片檔案
image_files = sorted(folder_path.glob("*.jpg"))
image_files += sorted(folder_path.glob("*.png"))
image_files += sorted(folder_path.glob("*.JPG"))
image_files += sorted(folder_path.glob("*.PNG"))

# 按修改時間排序
image_files = sorted(set(image_files), key=lambda x: x.stat().st_mtime)

print("=" * 70)
print("📋 批次重新命名預覽")
print("=" * 70)
print(f"\n資料夾：{folder_path}")
print(f"找到 {len(image_files)} 張照片\n")

rename_plan = []
for idx, old_file in enumerate(image_files, 1):
    old_name = old_file.name
    new_name = f"旅遊_{idx:03d}{old_file.suffix}"
    mod_time = datetime.fromtimestamp(old_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    rename_plan.append((old_file, new_name))
    
    print(f"{idx:2d}. {old_name:30s} → {new_name:20s} (修改時間: {mod_time})")

print("\n" + "=" * 70)
print(f"✅ 共將改名 {len(rename_plan)} 張照片")
print("=" * 70)

# 檢查是否有檔名衝突
target_names = [new_name for _, new_name in rename_plan]
duplicates = [name for name in target_names if target_names.count(name) > 1]

if duplicates:
    print("\n❌ 警告：發現重複的目標檔名！")
    for dup in set(duplicates):
        print(f"  - {dup}")
else:
    print("\n✅ 沒有檔名衝突")

# 詢問是否執行
response = input("\n是否執行重新命名？(yes/no): ").strip().lower()

if response == "yes":
    print("\n🔄 開始執行重新命名...")
    success_count = 0
    for old_file, new_name in rename_plan:
        new_path = old_file.parent / new_name
        try:
            old_file.rename(new_path)
            print(f"✅ {old_file.name} → {new_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {old_file.name} 改名失敗: {e}")
    
    print(f"\n🎉 完成！成功改名 {success_count}/{len(rename_plan)} 張照片")
else:
    print("\n⛔ 已取消操作")
