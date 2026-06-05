# 场景 4：项目框架搭建

#### 工作流程

1. **检查项目状态**
   - 检查用户是否已通过 `zeus create` 创建项目
   - 如果未创建，提示用户执行：`zeus create watchface <项目名>`

2. **检查并完善项目结构**
   - 检查 `assets/` 目录下的子目录是否完整
   - 根据表盘设计需求，创建缺失的子目录
   - 推荐的 assets 子目录结构：
     ```
     assets/
     ├── background/          # 背景图片
     ├── digits/              # 数字图标 (0-9)
     ├── week/                # 星期图标 (MON-SUN)
     ├── month/               # 月份图标 (JAN-DEC)
     ├── pointers/            # 指针图片 (时针/分针/秒针)
     ├── icons/               # 状态图标 (电池/蓝牙等)
     └── anim/                # 动画帧
     ```

3. **输出项目信息**
   - 列出项目的目录结构
   - 标注已创建和待创建的目录
   - 给出下一步操作建议

#### 项目目录结构（参考）

```
watchface-project/
├── app.js                    # 应用入口
├── app.json                  # 应用配置
├── assets/                   # 资源目录
│   ├── background/          # 背景图片
│   ├── digits/              # 数字图标
│   ├── week/                # 星期图标
│   ├── month/               # 月份图标
│   ├── pointers/            # 指针图片
│   ├── icons/               # 状态图标
│   └── anim/                # 动画帧
├── watchface/               # 表盘配置
│   └── default-target/
│       └── index.js         # 表盘主配置
└── i18n/                    # 国际化
    └── en-US.json
```

#### 检查命令

```bash
# 查看项目结构
ls -la watchface-project/

# 查看 assets 目录
ls -la watchface-project/assets/

# 检查特定资源目录
ls -la watchface-project/assets/digits/
```

#### app.json 配置示例

```json
{
  "configVersion": "v2",
  "app": {
    "appIdType": 0,
    "appId": 23960,
    "appName": "My Watchface",
    "appType": "watchface",
    "version": {
      "code": 1,
      "name": "1.0.0"
    },
    "vender": "zepp",
    "description": "Custom watchface",
    "icon": "assets/icon.png",
    "cover": ["assets/cover.png"]
  },
  "permissions": [],
  "runtime": {
    "apiVersion": {
      "compatible": "4.0.0",
      "target": "4.0.0",
      "minVersion": "4.0.0"
    }
  },
  "module": {
    "watchface": {
      "path": "watchface/default-target/index",
      "main": 1,
      "editable": 1,
      "lockscreen": 0,
      "hightCost": 0
    }
  },
  "platforms": [
    {
      "name": "Amazfit T-Rex 3",
      "deviceSource": "8716544*"
    }
  ],
  "designWidth": 480
}
```

---
