WatchFace({
  onInit() {
    console.log('十二时辰表盘 onInit');
  },

  build() {
    console.log('十二时辰表盘 build');
    
    // 十二时辰数据
    const SHICHEN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    
    // 动态元素引用
    let timeText = null;
    let shichenText = null;
    let timeSensor = null;

    // 计算当前时辰索引 (0-11)
    function getShichenIndex(hour, minute) {
      const totalMinutes = hour * 60 + minute;
      let offset = totalMinutes - 1380; // 子时开始于 23:00 = 1380 分钟
      if (offset < 0) offset += 1440; // 跨天处理
      return Math.floor(offset / 120) % 12;
    }

    // 获取时辰刻分文本
    function getShichenText(hour, minute) {
      const shichenIndex = getShichenIndex(hour, minute);
      const shichen = SHICHEN[shichenIndex];
      const keMinute = minute % 60;
      const ke = Math.floor(keMinute / 15);
      
      let text = '';
      if (ke === 0) {
        text = shichen + '\n初\n一\n刻';
      } else if (ke === 1) {
        text = shichen + '\n初\n二\n刻';
      } else if (ke === 2) {
        text = shichen + '\n初\n三\n刻';
      } else {
        const nextShichen = SHICHEN[(shichenIndex + 1) % 12];
        text = '入\n' + nextShichen + '\n初';
      }
      return text;
    }

    // 更新显示
    function updateDisplay() {
      if (!timeSensor) return;
      
      const hour = timeSensor.hour;
      const minute = timeSensor.minute;
      
      if (timeText) {
        const hourStr = String(hour).padStart(2, '0');
        const minuteStr = String(minute).padStart(2, '0');
        timeText.setProperty(hmUI.prop.MORE, {
          text: hourStr + ':' + minuteStr
        });
      }
      
      if (shichenText) {
        shichenText.setProperty(hmUI.prop.MORE, {
          text: getShichenText(hour, minute)
        });
      }
    }

    // 创建背景图片
    hmUI.createWidget(hmUI.widget.IMG, {
      x: 0,
      y: 0,
      w: 480,
      h: 480,
      src: 'background.png'
    });

    // 创建数字时间显示 (居中上方)
    timeText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 0,
      y: 160,
      w: 480,
      h: 80,
      text: '00:00',
      color: 0xFFFFFF,
      text_size: 56,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      font_family: 'Trajan Pro'
    });

    // 创建时辰刻分文本 (右侧竖排)
    shichenText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 320,
      y: 120,
      w: 100,
      h: 160,
      text: '子\n初\n一\n刻',
      color: 0xFFFFFF,
      text_size: 24,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      line_spacing: 0
    });

    // 创建时间传感器
    timeSensor = hmSensor.createSensor(hmSensor.id.TIME);
    
    // 监听分钟变化
    timeSensor.addEventListener(timeSensor.event.MINUTEEND, function() {
      updateDisplay();
    });

    // 初始化显示
    updateDisplay();
  },

  onDestroy() {
    console.log('十二时辰表盘 onDestroy');
  }
})