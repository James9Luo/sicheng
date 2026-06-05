# 场景 6：Zeus CLI 测试调试

## 触发条件

当 `sicheng\chinese_time\watchface\index.js` 文件被更改后，自动启动此流程。

## 工作流程

### 步骤 1：API 规范检查

- 检查 `index.js` 使用的 API 是否 100% 符合官方定义
- 参考路径：`zeppos-docs/docs/watchface/api`
- 常用 Widget API：
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_TIME.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_WEEK.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_DATE.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_POINTER.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_STATUS.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_LEVEL.mdx`
  - `zeppos-docs/docs/watchface/api/hmUI/widget/IMG_ANIM.mdx`

### 步骤 2：执行调试检查清单

逐项检查表盘功能是否正常

### 步骤 3：选择调试方式

询问用户选择真机调试或仿真器调试

## 调试检查清单

- [ ] 背景图片显示正常
- [ ] 数字时间正确显示
- [ ] 星期随日期正确切换
- [ ] 日期显示正确
- [ ] 指针旋转正常
- [ ] 状态图标显示正常
- [ ] 息屏模式（AOD）正常
- [ ] 不同分辨率适配正确

## 调试方式

### 真机调试

```bash
zeus preview
```

### 仿真器调试

```bash
zeus dev
```

---

## 常见错误与解决方案

### 1. TIME 传感器事件错误

**错误代码：**
```javascript
// ❌ SECONDEND 事件不存在
timeSensor.addEventListener(timeSensor.event.SECONDEND, function() {
  updateDisplay();
});
```

**正确做法：**
```javascript
// ✅ 方式 1：使用 MINUTEEND 事件
timeSensor.addEventListener(timeSensor.event.MINUTEEND, function() {
  updateDisplay();
});

// ✅ 方式 2：使用 timer.createTimer 每秒更新
timer.createTimer(0, 1000, function(ts) {
  updateDisplay();
}, timeSensor);
```

### 2. 息屏唤醒后不更新

**错误代码：**
```javascript
// ❌ 息屏唤醒后数据不刷新
```

**正确做法：**
```javascript
// ✅ 添加 WIDGET_DELEGATE 恢复回调
hmUI.createWidget(hmUI.widget.WIDGET_DELEGATE, {
  resume_call: function() {
    updateDisplay();
    updateDate();
    updateLunar();
    updateBattery();
  }
});
```

### 3. 手动刷新时间 vs 组件自动刷新

| 场景 | 推荐方式 |
|------|----------|
| 使用 TEXT 组件显示时间 | 使用 `timer.createTimer` 或事件监听 |
| 使用 IMG_TIME 组件 | 组件自动跟随系统时间，无需手动刷新 |
| 使用 IMG_WEEK/IMG_DATE | 组件自动跟随系统时间，无需手动刷新 |
| 使用 TIME_POINTER | 组件自动旋转，无需手动刷新 |

---

## API 验证方法

### 传感器事件检查

搜索官方文档确认事件是否存在：
```bash
# 检查 TIME 传感器事件
zeppos-docs/docs/watchface/api/hmSensor/sensorId/TIME.mdx

# 检查其他传感器事件
zeppos-docs/docs/watchface/api/hmSensor/sensorId/BATTERY.mdx
zeppos-docs/docs/watchface/api/hmSensor/sensorId/HEART.mdx
```

### 官方示例参考优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | `sicheng/watchface/1.0/simple/` | 使用 TEXT + 事件监听，与自定义表盘类似 |
| 2 | `sicheng/watchface/1.0/timer/` | 使用 timer.createTimer |
| 3 | `zeppos-docs/docs/samples/watchface/` | 官方示例 |
| 4 | `zeppos-docs/docs/reference/` | API 官方文档 |

### 常用 API 文档路径

| API 类型 | 文档路径 |
|----------|----------|
| 传感器 | `zeppos-docs/docs/watchface/api/hmSensor/sensorId/` |
| Widget | `zeppos-docs/docs/watchface/api/hmUI/widget/` |
| 定时器 | `zeppos-docs/docs/watchface/api/timer/` |
| 全局 API | `zeppos-docs/docs/reference/device-app-api/newAPI/global/` |

---

## 调试检查清单（详细版）

### 基础检查
- [ ] 背景图片路径是否正确（相对于 assets 目录）
- [ ] 传感器是否正确创建（`hmSensor.createSensor`）
- [ ] 事件监听是否使用正确的 API
- [ ] 定时器是否正确使用（`timer.createTimer`）

### 时间显示检查
- [ ] 数字时间是否每秒更新
- [ ] 星期是否正确切换
- [ ] 日期是否正确显示
- [ ] 农历是否正确显示（仅中文系统）

### 息屏模式检查
- [ ] AOD 组件是否配置 `show_level: ONLY_AOD`
- [ ] 息屏唤醒后数据是否刷新
- [ ] 息屏模式显示内容是否正确

### 资源文件检查
- [ ] 背景图片是否存在
- [ ] 图标文件是否存在
- [ ] 字体文件是否正确配置
