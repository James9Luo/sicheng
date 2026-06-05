# 场景 5：JSON 配置开发

## 工作流程

### 步骤 1：获取设计布局方案

- 从 `design/` 目录读取表盘设计布局方案
- 提取组件清单和技术指标

### 步骤 2：获取资源文件

- 从 `assets/` 目录读取生成的资源文件
- 确认资源完整性和路径

### 步骤 3：生成 Widget 并布局

- 根据布局方案中的组件清单
- 使用 Zepp OS API 创建 Widget
- 配置位置、大小、样式等参数

### 步骤 4：定义资源数组

- 在 `index.js` 顶部定义 digitArray、weekArray 等资源数组
- Widget 会自动使用这些数组进行时间/日期显示

### 步骤 5：添加状态图标

- 配置状态图标（蓝牙、闹钟、电量等）
- 绑定系统状态事件

## 表盘配置结构

```javascript
// watchface/default-target/index.js

// 数字资源数组 (0-9)
const digitArray = [
  'assets/digits/0.png',
  'assets/digits/1.png',
  'assets/digits/2.png',
  'assets/digits/3.png',
  'assets/digits/4.png',
  'assets/digits/5.png',
  'assets/digits/6.png',
  'assets/digits/7.png',
  'assets/digits/8.png',
  'assets/digits/9.png'
];

// 星期资源数组 (SUN-SAT，Zepp OS 使用 0-6)
const weekArray = [
  'assets/week/sun.png',
  'assets/week/mon.png',
  'assets/week/tue.png',
  'assets/week/wed.png',
  'assets/week/thu.png',
  'assets/week/fri.png',
  'assets/week/sat.png'
];

// 月份数字资源数组 (1-12)
const monthDigitArray = [
  'assets/digits/1.png',
  'assets/digits/2.png',
  'assets/digits/3.png',
  'assets/digits/4.png',
  'assets/digits/5.png',
  'assets/digits/6.png',
  'assets/digits/7.png',
  'assets/digits/8.png',
  'assets/digits/9.png',
  'assets/digits/10.png',
  'assets/digits/11.png',
  'assets/digits/12.png'
];

// 日期数字资源数组 (1-31)
const dayDigitArray = [];
for (let i = 1; i <= 31; i++) {
  dayDigitArray.push(`assets/digits/${i}.png`);
}

export default {
  // 显示配置版本
  version: 'v2',
  
  // 组件列表
  elements: [
    // 背景
    {
      type: 'image',
      x: 0,
      y: 0,
      width: 480,
      height: 480,
      src: 'assets/background.png'
    },
    
    // 数字时间显示 (IMG_TIME)
    {
      type: 'img_time',
      x: 240,
      y: 200,
      hour_zero: 1,
      hour_startX: 180,
      hour_startY: 180,
      hour_array: digitArray,
      hour_space: 8,
      hour_unit_sc: 'assets/digits/colon.png',
      hour_unit_tc: 'assets/digits/colon.png',
      hour_unit_en: 'assets/digits/colon.png',
      hour_align: hmUI.align.LEFT,
      minute_follow: 1,
      second_follow: 1
    },
    
    // 星期显示 (IMG_WEEK)
    {
      type: 'img_week',
      x: 240,
      y: 280,
      week_en: weekArray,
      week_tc: weekArray,
      week_sc: weekArray
    },
    
    // 日期显示 (IMG_DATE)
    {
      type: 'img_date',
      x: 240,
      y: 320,
      month_startX: 200,
      month_startY: 320,
      month_unit_sc: 'assets/digits/slash.png',
      month_is_character: true,
      month_en_array: monthDigitArray,
      day_follow: 1,
      day_is_character: true,
      day_en_array: dayDigitArray
    },
    
    // 指针 (IMG_POINTER)
    {
      type: 'img_pointer',
      src: 'assets/pointers/hour.png',
      center_x: 240,
      center_y: 240,
      x: 22,
      y: 121,
      angle: 0
    },
    
    // 状态图标 (IMG_STATUS)
    {
      type: 'img_status',
      x: 20,
      y: 20,
      type: hmUI.system_status.DISCONNECT,
      src: 'assets/icons/bt_disconnect.png'
    }
  ]
};
```

## 动态切换说明

> [!NOTE]
> IMG_TIME、IMG_WEEK、IMG_DATE 等 Widget 是 Zepp OS 原生组件，会自动处理时间、星期、日期的更新，无需手动编写 updateTime 函数。只需在顶部定义好资源数组，Widget 会自动根据当前时间选择对应的图片显示。