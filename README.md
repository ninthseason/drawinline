##  DrawInline - 你画我猜辅助工具

三步玩转你画我猜：

1. 线稿生成器

   基于OpenCV的图像处理，由原图得到线稿

2. 笔画生成器

   利用搜索算法分析线稿，生成笔画数据

3. 鼠标自动控制

   通过笔画数据控制鼠标，实现自动绘图

![](./rendering.gif)

### 使用指南

#### 注意事项

DrawInline 使用剪切板内的图片作为目标图片

请搭配能将图片暂存至剪切板的截图软件使用

#### 命令说明

`:threshold` 查看当前 threshold 值

`:threshold [整数]` 设置 threshold 值

threshold 会影响图片转为线稿的效果，过小线条不连贯，过大产生噪点

`:start-point` 将当前鼠标设置为画板原点

将鼠标移动至画布左上角执行:start-point

`show` 显示当前剪切板图片的线稿形态

用于查看当前 threshold 的效果，以便调整 threshold

`draw` 控制鼠标，进行绘图

`quit` 退出程序

源代码及问题反馈: https://github.com/ninthseason/drawinline