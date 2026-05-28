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
    let shichenTextAOD = null;
    let timeSensor = null;
    let weatherTypeText = null;
    let weatherIconText = null;
    let weatherSensor = null;
    let batteryText = null;
    let dateText = null;
    let lunarText = null;

    // 天气类型映射
    const WEATHER_TYPES = [
      '多云', '阵雨', '阵雪', '晴', '阴', '小雨', '小雪', '中雨',
      '中雪', '大雪', '大雨', '沙尘暴', '雨夹雪', '雾', '霾',
      '雷阵雨', '暴雪', '浮尘', '特大暴雨', '雨冰雹', '雷阵雨冰雹',
      '大暴雨', '扬尘', '强沙尘暴', '暴雨', '未知', '夜间多云', '夜间阵雨', '夜间晴'
    ];

    // 天气图标映射
    const WEATHER_ICONS = {
      0: '☁',   // 多云
      1: '🌦',   // 阵雨
      2: '🌨',   // 阵雪
      3: '☀',   // 晴
      4: '☁',   // 阴
      5: '🌧',   // 小雨
      6: '🌨',   // 小雪
      7: '🌧',   // 中雨
      8: '🌨',   // 中雪
      9: '❄',   // 大雪
      10: '🌧',  // 大雨
      11: '🌪',  // 沙尘暴
      12: '🌨',  // 雨夹雪
      13: '🌫',  // 雾
      14: '🌫',  // 霾
      15: '⛈',  // 雷阵雨
      16: '❄',  // 暴雪
      17: '🌪',  // 浮尘
      18: '🌧',  // 特大暴雨
      19: '🌨',  // 雨加冰雹
      20: '⛈',  // 雷阵雨伴有冰雹
      21: '🌧',  // 大暴雨
      22: '🌪',  // 扬尘
      23: '🌪',  // 强沙尘暴
      24: '🌧',  // 暴雨
      25: '❓',  // 未知
      26: '☁',  // 夜间多云
      27: '🌦',  // 夜间阵雨
      28: '🌙'   // 夜间晴
    };

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
      
      if (shichenTextAOD) {
        shichenTextAOD.setProperty(hmUI.prop.MORE, {
          text: getShichenText(hour, minute)
        });
      }
      
      // 更新日期和农历
      updateDate();
      updateLunar();
    }

    // 更新天气显示
    function updateWeather() {
      if (!weatherSensor) return;
      
      try {
        const weatherData = weatherSensor.getForecastWeather();
        if (!weatherData || !weatherData.forecastData || weatherData.forecastData.count === 0) {
          console.log('天气数据不可用');
          return;
        }
        
        const today = weatherData.forecastData.data[0];
        const weatherType = WEATHER_TYPES[today.index] || '未知';
        const weatherIconChar = WEATHER_ICONS[today.index] || '❓';
        const tempText = `${today.high}°`;
        
        // 将天气类型竖式显示（每个字一行）
        const verticalWeatherType = weatherType.split('').join('\n');
        
        // 更新天气类型文本（垂直中轴线下半部分）
        if (weatherTypeText) {
          weatherTypeText.setProperty(hmUI.prop.MORE, {
            text: verticalWeatherType
          });
        }
        
        // 更新天气图标和温度文本（左下部分）
        if (weatherIconText) {
          weatherIconText.setProperty(hmUI.prop.MORE, {
            text: tempText + ' ' + weatherIconChar
          });
        }
        
        console.log('天气更新:', weatherType, today.high + '°');
      } catch (error) {
        console.log('获取天气数据失败:', error);
      }
    }

    // 更新日期显示
    function updateDate() {
      if (!timeSensor) return;
      
      const now = new Date();
      const weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
      const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
      
      const weekday = weekdays[now.getDay()];
      const day = String(now.getDate()).padStart(2, '0');
      const month = months[now.getMonth()];
      
      if (dateText) {
        dateText.setProperty(hmUI.prop.MORE, {
          text: `${weekday}\n${day}-${month}`
        });
      }
    }

    // 更新农历显示（简化版，实际需要农历库）
    function updateLunar() {
      // 这里使用简化版农历显示，实际项目中需要使用农历计算库
      const lunarMonths = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月'];
      const lunarDays = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', 
                        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                        '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
      
      // 简化计算，实际需要农历转换算法
      const now = new Date();
      const lunarMonth = lunarMonths[(now.getMonth() + 11) % 12];
      const lunarDay = lunarDays[(now.getDate() - 1) % 30];
      
      if (lunarText) {
        lunarText.setProperty(hmUI.prop.MORE, {
          text: lunarMonth + lunarDay
        });
      }
    }

    // 创建传感器（移到组件创建之前）
    timeSensor = hmSensor.createSensor(hmSensor.id.TIME);
    weatherSensor = hmSensor.createSensor(hmSensor.id.WEATHER);
    
    // 创建背景图片
    hmUI.createWidget(hmUI.widget.IMG, {
      x: 0,
      y: 0,
      w: 480,
      h: 480,
      src: 'background.png'
    });

    // 创建电量显示（竖向中轴线最顶端）
    batteryText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 210,
      y: 50,
      w: 80,
      h: 40,
      text: '100%',
      color: 0xFFFFFF,
      text_size: 20,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      show_level: hmUI.show_level.ONLY_NORMAL
    });

    // 创建月份和星期显示（左上部分）
    dateText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 80,
      y: 150,
      w: 100,
      h: 80,
      text: 'WED\n26-AUG',
      color: 0xFFFFFF,
      text_size: 24,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      line_space: 0,
      show_level: hmUI.show_level.ONLY_NORMAL
    });

    // 创建数字时间显示 (横向中轴线左侧居中)
    timeText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 0,
      y: 235,
      w: 280,
      h: 40,
      text: '00:00',
      color: 0xFFFFFF,
      text_size: 56,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      font_family: 'Trajan Pro'
    });

    // 创建农历显示 (横向中轴线右侧居中)
    lunarText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 280,
      y: 235,
      w: 200,
      h: 40,
      text: '二月初三',
      color: 0xFFFFFF,
      text_size: 28,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      font_family: 'Noto Serif SC'
    });

    // 创建时辰刻分文本 (垂直中轴线上半部分) - 正常模式
    shichenText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 210,
      y: 80,
      w: 80,
      h: 140,
      text: '子\n初\n一\n刻',
      color: 0xFFFFFF,
      text_size: 28,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      line_space: -8,
      show_level: hmUI.show_level.ONLY_NORMAL
    });

    // 创建时辰刻分文本 (垂直中轴线上半部分) - 息屏模式
    shichenTextAOD = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 210,
      y: 80,
      w: 80,
      h: 140,
      text: '子\n初\n一\n刻',
      color: 0xFFFFFF,
      text_size: 26,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      line_space: -8,
      show_level: hmUI.show_level.ONLY_AOD
    });

    // 创建天气类型文本（垂直中轴线下半部分）
    weatherTypeText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 210,
      y: 300,
      w: 80,
      h: 80,
      text: '晴\n天',
      color: 0xFFFFFF,
      text_size: 28,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      line_space: -8,
      show_level: hmUI.show_level.ONLY_NORMAL
    });

    // 创建天气图标和温度文本（左下部分）
    weatherIconText = hmUI.createWidget(hmUI.widget.TEXT, {
      x: 120,
      y: 300,
      w: 120,
      h: 40,
      text: '25° ☀',
      color: 0xFFFFFF,
      text_size: 24,
      text_style: hmUI.text_style.NONE,
      align_h: hmUI.align.CENTER_H,
      align_v: hmUI.align.CENTER_V,
      show_level: hmUI.show_level.ONLY_NORMAL
    });

    // 监听秒变化（用于数字时间实时更新）
    timeSensor.addEventListener(timeSensor.event.SECONDEND, function() {
      updateDisplay();
    });
    
    // 监听分钟变化（用于时辰刻分更新）
    timeSensor.addEventListener(timeSensor.event.MINUTEEND, function() {
      updateDisplay();
    });

    // 初始化显示
    updateDisplay();
    updateWeather();
    updateDate();
    updateLunar();
  },

  onDestroy() {
    console.log('十二时辰表盘 onDestroy');
  }
})