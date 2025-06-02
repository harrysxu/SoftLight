#!/usr/bin/env python3
"""
SoftLight iPhone外观图标生成器
生成模仿iPhone外观的白色长方形图标，带有刘海设计
"""

import os
from PIL import Image, ImageDraw

def create_iphone_icon(size):
    """
    创建iPhone外观的图标
    """
    # 创建画布，透明背景
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算相对尺寸
    center = size // 2
    
    # iOS应用图标的圆角半径
    app_corner_radius = int(size * 0.176)
    
    # 绘制应用图标背景（深色，模仿夜间模式）
    draw.rounded_rectangle(
        [(0, 0), (size, size)], 
        radius=app_corner_radius, 
        fill=(20, 20, 25, 255)  # 深色背景
    )
    
    # iPhone屏幕的相对尺寸
    phone_width = int(size * 0.5)  # 屏幕宽度
    phone_height = int(size * 0.75)  # 屏幕高度
    phone_corner_radius = int(size * 0.08)  # 屏幕圆角
    
    # 计算iPhone屏幕位置（居中）
    phone_left = center - phone_width // 2
    phone_top = center - phone_height // 2
    phone_right = phone_left + phone_width
    phone_bottom = phone_top + phone_height
    
    # 绘制iPhone屏幕（白色发光效果）
    draw.rounded_rectangle(
        [(phone_left, phone_top), (phone_right, phone_bottom)], 
        radius=phone_corner_radius, 
        fill=(255, 255, 255, 255)  # 纯白色
    )
    
    # 添加屏幕光晕效果
    glow_padding = int(size * 0.02)
    draw.rounded_rectangle(
        [(phone_left - glow_padding, phone_top - glow_padding), 
         (phone_right + glow_padding, phone_bottom + glow_padding)], 
        radius=phone_corner_radius + glow_padding, 
        fill=(255, 255, 255, 80)  # 半透明白色光晕
    )
    
    # 刘海设计
    notch_width = int(phone_width * 0.35)  # 刘海宽度
    notch_height = int(size * 0.04)  # 刘海高度
    notch_radius = int(size * 0.015)  # 刘海圆角
    
    # 刘海位置（屏幕顶部中央）
    notch_left = center - notch_width // 2
    notch_top = phone_top
    notch_right = notch_left + notch_width
    notch_bottom = phone_top + notch_height
    
    # 绘制刘海（深色）
    draw.rounded_rectangle(
        [(notch_left, notch_top), (notch_right, notch_bottom)], 
        radius=notch_radius, 
        fill=(20, 20, 25, 255)  # 与背景同色
    )
    
    # 在刘海中添加扬声器（小椭圆）
    speaker_width = int(notch_width * 0.3)
    speaker_height = int(notch_height * 0.25)
    speaker_left = center - speaker_width // 2
    speaker_top = notch_top + (notch_height - speaker_height) // 2
    speaker_right = speaker_left + speaker_width
    speaker_bottom = speaker_top + speaker_height
    
    draw.ellipse(
        [(speaker_left, speaker_top), (speaker_right, speaker_bottom)], 
        fill=(60, 60, 70, 255)  # 深灰色扬声器
    )
    
    # 前置摄像头（小圆形）
    camera_radius = int(size * 0.015)
    camera_x = notch_right - int(notch_width * 0.25)
    camera_y = notch_top + notch_height // 2
    
    draw.ellipse(
        [(camera_x - camera_radius, camera_y - camera_radius),
         (camera_x + camera_radius, camera_y + camera_radius)], 
        fill=(40, 40, 50, 255)  # 深灰色摄像头
    )
    
    # 添加屏幕内的发光效果
    inner_glow_size = int(size * 0.15)
    inner_glow_x = center
    inner_glow_y = center + int(size * 0.05)  # 稍微向下偏移
    
    # 创建径向渐变效果的光点
    for i in range(3):
        glow_radius = inner_glow_size - i * int(inner_glow_size * 0.25)
        glow_opacity = 60 - i * 15
        
        draw.ellipse(
            [(inner_glow_x - glow_radius, inner_glow_y - glow_radius),
             (inner_glow_x + glow_radius, inner_glow_y + glow_radius)], 
            fill=(255, 248, 220, glow_opacity)  # 温暖的白光
        )
    
    return img

def generate_all_icons():
    """
    生成所有需要的图标尺寸
    """
    # iOS应用图标尺寸
    icon_sizes = {
        'AppStore': 1024,      # App Store
        'iPhone-180': 180,     # iPhone @3x
        'iPhone-120': 120,     # iPhone @2x  
        'iPad-167': 167,       # iPad Pro @2x
        'iPad-152': 152,       # iPad @2x
        'iPad-76': 76,         # iPad @1x
    }
    
    # 创建输出目录
    output_dir = 'phone_icons'
    os.makedirs(output_dir, exist_ok=True)
    
    print("📱 开始生成SoftLight iPhone外观图标...")
    
    for name, size in icon_sizes.items():
        print(f"生成 {name} ({size}x{size})...")
        
        # 创建图标
        icon = create_iphone_icon(size)
        
        # 保存PNG文件
        filename = f"{output_dir}/icon_{name}_{size}x{size}.png"
        icon.save(filename, 'PNG', optimize=True)
        
        print(f"✅ 已保存: {filename}")
    
    print(f"\n🎉 所有iPhone外观图标已生成完成！")
    print(f"📁 图标位置: {os.path.abspath(output_dir)}")
    print("\n📋 设计特点:")
    print("• 白色发光屏幕效果")
    print("• 经典iPhone刘海设计")
    print("• 深色背景突出屏幕")
    print("• 包含扬声器和前置摄像头细节")
    print("• 屏幕内温暖光晕效果")

if __name__ == "__main__":
    generate_all_icons() 