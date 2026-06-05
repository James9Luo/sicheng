# 场景 3：PNG 资源批量生成

## 工作流程

### 步骤 1：读取设计布局方案

- 从 `design/` 目录读取表盘设计布局方案
- 提取资源清单和技术指标

### 步骤 2：遍历资源清单

- 根据布局方案中的组件清单
- 确定需要生成的模板类型和数量

### 步骤 3：生成 SVG 文件

- 创建 SVG 模板文件
- 使用模板变量配置样式

### 步骤 4：转换为 PNG 格式

- 调用 svg-to-png 技能批量转换
- 输出到 `assets/` 目录

### 步骤 5：验证输出质量

- 检查 PNG 文件尺寸和格式
- 确认资源完整性

## 模板类型

根据 Zepp OS 表盘设计规范，表盘设计需要有如下核心模板：

| 模板类型 | 用途 | 必需数量 | 变量参数 | 对应 Widget |
|----------|------|----------|----------|-------------|
| **数字模板** | 时间数字 0-9 | 10 | fontSize, fontFamily, color, strokeColor, strokeWidth, padding | IMG_TIME |
| **分隔符模板** | 冒号(:)、斜杠(/)、负号(-)、点(.)、百分号(%) | 5 | size, color | IMG_TIME |
| **星期模板** | MON-SUN 缩写 | 7 | fontSize, fontFamily, color, strokeColor, strokeWidth | IMG_WEEK |
| **月份模板** | JAN-DEC 缩写 | 12 | fontSize, fontFamily, color, strokeColor, strokeWidth | 自定义 |
| **指针模板** | 时针、分针、秒针 | 3 | width, height, centerX, centerY, color | IMG_POINTER |
| **AM/PM 模板** | 上午、下午图标 | 2 | size, color | IMG_TIME |
| **状态图标模板** | 电池、蓝牙、勿扰、锁屏、闹钟 | 若干 | size, color, strokeWidth | IMG_STATUS |
| **年份数字模板** | 四位年份数字 0-9 | 10 | fontSize, fontFamily, color, strokeColor, strokeWidth | IMG_DATE |
| **月份数字模板** | 月份数字 1-12 | 12 | fontSize, fontFamily, color, strokeColor, strokeWidth | IMG_DATE |
| **日期数字模板** | 日期数字 1-31 | 31 | fontSize, fontFamily, color, strokeColor, strokeWidth | IMG_DATE |
| **电量层级模板** | 电量 0-100% | 101 | size, color | IMG_LEVEL |
| **动画帧模板** | 动态效果帧 | N帧 | width, height, color | IMG_ANIM |

## SVG 模板结构

```svg
<!-- 数字 SVG 模板 -->
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{{canvasSize}}" 
     height="{{canvasSize}}" 
     viewBox="0 0 {{canvasSize}} {{canvasSize}}">
  <rect width="100%" height="100%" fill="transparent"/>
  <text x="50%" y="50%" 
        font-family="{{fontFamily}}" 
        font-size="{{fontSize}}" 
        fill="{{color}}" 
        stroke="{{strokeColor}}" 
        stroke-width="{{strokeWidth}}"
        text-anchor="middle" 
        dominant-baseline="central">{{content}}</text>
</svg>

<!-- 汉字 SVG 模板 -->
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{{canvasSize}}" 
     height="{{canvasSize}}" 
     viewBox="0 0 {{canvasSize}} {{canvasSize}}">
  <rect width="100%" height="100%" fill="transparent"/>
  <text x="50%" y="50%" 
        font-family="{{fontFamily}}" 
        font-size="{{fontSize}}" 
        fill="{{color}}" 
        stroke="{{strokeColor}}" 
        stroke-width="{{strokeWidth}}"
        text-anchor="middle" 
        dominant-baseline="central">{{content}}</text>
</svg>