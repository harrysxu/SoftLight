//
//  ContentView.swift
//  SoftLight
//
//  Created by 徐晓龙 on 2025/6/1.
//

import SwiftUI

struct ContentView: View {
    @State private var brightness: Double = 0.6 // 调整初始亮度为60%，避免启动就是最亮
    @State private var lightRatio: Double = 0.0 // 柔光/强光比例 (-1.0 到 1.0，-1.0为最柔光，1.0为最强光)
    @State private var dragOffset: CGSize = .zero
    @State private var baseBrightness: Double = 0.6 // 手势开始时的基准亮度
    @State private var baseLightRatio: Double = 0.0 // 手势开始时的基准光比例
    @State private var showInstructions: Bool = true // 控制操作说明的显示
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // 根据lightRatio计算背景色
                backgroundColorForRatio()
                    .brightness(brightness - 1.0) // SwiftUI的brightness修饰符
                    .ignoresSafeArea(.all)
                
                // 手势处理区域（透明）
                Rectangle()
                    .fill(Color.clear)
                    .contentShape(Rectangle())
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                // 用户开始滑动时隐藏操作说明
                                if showInstructions {
                                    withAnimation(.easeOut(duration: 0.3)) {
                                        showInstructions = false
                                    }
                                }
                                
                                let translation = value.translation
                                
                                // 上下滑动控制亮度（基于手势开始时的基准值）
                                let verticalChange = -translation.height / geometry.size.height
                                let newBrightness = max(0.1, min(1.0, baseBrightness + verticalChange * 1.2))
                                brightness = newBrightness
                                
                                // 左右滑动控制柔光/强光比例（基于手势开始时的基准值）
                                let horizontalChange = translation.width / geometry.size.width
                                let newRatio = max(-1.0, min(1.0, baseLightRatio + horizontalChange * 2.0))
                                lightRatio = newRatio
                                
                                dragOffset = value.translation
                            }
                            .onEnded { _ in
                                dragOffset = .zero
                                // 更新基准值为当前值，准备下次手势
                                baseBrightness = brightness
                                baseLightRatio = lightRatio
                            }
                    )
                    .onTapGesture {
                        // 点击屏幕切换操作说明显示状态
                        withAnimation(.easeInOut(duration: 0.3)) {
                            showInstructions.toggle()
                        }
                    }
                
                // 操作说明
                if showInstructions {
                    VStack {
                        VStack(spacing: 8) {
                            HStack {
                                Image(systemName: "hand.draw")
                                    .foregroundColor(.gray)
                                Text("操作说明")
                                    .font(.headline)
                                    .foregroundColor(.gray)
                                Spacer()
                                Button("×") {
                                    withAnimation(.easeOut(duration: 0.3)) {
                                        showInstructions = false
                                    }
                                }
                                .foregroundColor(.gray)
                                .font(.title2)
                            }
                            
                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Image(systemName: "arrow.up.arrow.down")
                                        .foregroundColor(.blue)
                                        .frame(width: 20)
                                    Text("上下滑动调节亮度")
                                        .font(.subheadline)
                                        .foregroundColor(.gray)
                                }
                                
                                HStack {
                                    Image(systemName: "arrow.left.arrow.right")
                                        .foregroundColor(.orange)
                                        .frame(width: 20)
                                    Text("左右滑动调节色温")
                                        .font(.subheadline)
                                        .foregroundColor(.gray)
                                }
                                
                                HStack {
                                    Image(systemName: "hand.tap")
                                        .foregroundColor(.green)
                                        .frame(width: 20)
                                    Text("点击屏幕显示/隐藏说明")
                                        .font(.subheadline)
                                        .foregroundColor(.gray)
                                }
                            }
                        }
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.black.opacity(0.7))
                        )
                        .padding(.horizontal)
                        .padding(.top, 50)
                        
                        Spacer()
                    }
                    .transition(.opacity.combined(with: .move(edge: .top)))
                }
                
                // 状态指示器（显示当前模式和亮度）
                VStack {
                    Spacer()
                    HStack {
                        Text("模式: \(modeDescription())")
                        Spacer()
                        Text("亮度: \(Int(brightness * 100))%")
                    }
                    .font(.caption)
                    .foregroundColor(.gray)
                    .opacity(0.3)
                    .padding()
                }
            }
        }
        .onAppear {
            // 设置屏幕常亮
            UIApplication.shared.isIdleTimerDisabled = true
            // 设置初始亮度为100%
            UIScreen.main.brightness = brightness
            
            // 3秒后自动隐藏操作说明
            DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
                if showInstructions {
                    withAnimation(.easeOut(duration: 0.5)) {
                        showInstructions = false
                    }
                }
            }
        }
        .onDisappear {
            // 恢复正常的息屏设置
            UIApplication.shared.isIdleTimerDisabled = false
        }
        .onChange(of: brightness) { _, newValue in
            // 实时更新系统屏幕亮度
            UIScreen.main.brightness = newValue
        }
    }
    
    // 根据lightRatio计算背景颜色
    private func backgroundColorForRatio() -> Color {
        if lightRatio < 0 {
            // 柔光模式：从白色渐变到淡黄色
            let yellowIntensity = abs(lightRatio) // 0.0 到 1.0
            let red = 1.0
            let green = 1.0
            let blue = 1.0 - yellowIntensity * 0.3 // 减少蓝色分量来产生黄色效果
            return Color(red: red, green: green, blue: blue)
        } else {
            // 强光模式：纯白色
            return Color.white
        }
    }
    
    // 生成模式描述文本
    private func modeDescription() -> String {
        if lightRatio < -0.7 {
            return "深度柔光"
        } else if lightRatio < -0.3 {
            return "柔光"
        } else if lightRatio < 0.3 {
            return "中性"
        } else if lightRatio < 0.7 {
            return "强光"
        } else {
            return "最强光"
        }
    }
}

#Preview {
    ContentView()
}
