#!/usr/bin/env python3
"""
图标尺寸调整器
将Canva生成的1024x1024图标调整为iOS应用所需的各种尺寸
"""

import os
from PIL import Image

def resize_icon_to_all_sizes(input_path, output_dir="resized_icons"):
    """
    将单个图标调整为所有需要的iOS尺寸
    """
    # iOS应用图标尺寸
    icon_sizes = {
        'AppStore': 1024,      # App Store
        'iPhone-180': 180,     # iPhone @3x
        'iPhone-120': 120,     # iPhone @2x  
        'iPad-167': 167,       # iPad Pro @2x
        'iPad-152': 152,       # iPad @2x
        'iPad-76': 76,         # iPad @1x
        'iPhone-60': 60,       # iPhone @1x (备用)
        'iPad-40': 40,         # iPad Spotlight @1x
        'iPad-80': 80,         # iPad Spotlight @2x
        'iPhone-58': 58,       # iPhone Spotlight @2x
        'iPhone-87': 87,       # iPhone Spotlight @3x
    }
    
    try:
        # 打开原图
        original_image = Image.open(input_path)
        print(f"📁 原图尺寸: {original_image.size}")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        print("🔄 开始调整图标尺寸...")
        
        for name, size in icon_sizes.items():
            print(f"调整 {name} ({size}x{size})...")
            
            # 高质量缩放
            resized_image = original_image.resize(
                (size, size), 
                Image.Resampling.LANCZOS  # 高质量缩放算法
            )
            
            # 保存文件
            filename = f"{output_dir}/icon_{name}_{size}x{size}.png"
            resized_image.save(filename, 'PNG', optimize=True, quality=95)
            
            print(f"✅ 已保存: {filename}")
        
        print(f"\n🎉 所有尺寸调整完成！")
        print(f"📁 输出目录: {os.path.abspath(output_dir)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def batch_resize_icons(input_dir=".", output_dir="resized_icons"):
    """
    批量处理目录中的所有图片文件
    """
    # 支持的图片格式
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp')
    
    # 查找图片文件
    image_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith(supported_formats):
            image_files.append(os.path.join(input_dir, file))
    
    if not image_files:
        print("❌ 未找到支持的图片文件")
        return
    
    print(f"📁 找到 {len(image_files)} 个图片文件")
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n处理第 {i}/{len(image_files)} 个文件: {os.path.basename(image_path)}")
        
        # 为每个文件创建单独的输出目录
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        file_output_dir = f"{output_dir}/{file_name}_icons"
        
        resize_icon_to_all_sizes(image_path, file_output_dir)

def main():
    print("🎨 iOS图标尺寸调整器")
    print("=" * 40)
    
    # 检查当前目录是否有图片文件
    current_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if current_files:
        print(f"找到以下图片文件:")
        for i, file in enumerate(current_files, 1):
            print(f"{i}. {file}")
        
        print("\n选择处理方式:")
        print("1. 处理单个文件")
        print("2. 批量处理所有文件")
        
        try:
            choice = input("\n请选择 (1/2): ").strip()
            
            if choice == "1":
                file_index = int(input(f"请选择文件序号 (1-{len(current_files)}): ")) - 1
                if 0 <= file_index < len(current_files):
                    selected_file = current_files[file_index]
                    print(f"\n处理文件: {selected_file}")
                    resize_icon_to_all_sizes(selected_file)
                else:
                    print("❌ 无效的文件序号")
            
            elif choice == "2":
                print("\n批量处理所有文件...")
                batch_resize_icons()
            
            else:
                print("❌ 无效选择")
                
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 操作取消")
    
    else:
        print("❌ 当前目录没有找到图片文件")
        print("请将Canva下载的图标文件放到当前目录，然后重新运行此脚本")

if __name__ == "__main__":
    main() 