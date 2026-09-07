---
name: nano-banana-pro
version: 1.0.0
description: "AI图像生成与编辑工具，基于Gemini 3 Pro Image。支持文本生成图像、图像编辑、多分辨率输出（1K/2K/4K）。"
description_zh: "AI 图片生成与编辑（支持 4K）"
description_en: "AI image generation & editing (up to 4K)"
tags: [生成创意图像和插图, 编辑现有图片（裁剪、调整、风格转换）, 批量图像处理, 创建营销素材和UI设计稿]
tags: [image, ai, generation, editing]
difficulty: intermediate
tags: [python, uv package manager]
---

# Nano Banana Pro 图像生成与编辑

使用Google的Nano Banana Pro API（Gemini 3 Pro Image）生成新图像或编辑现有图像。

## 安装

### 依赖要求

```bash
# 确保已安装 Python 3.8+
python --version

# 安装 uv 包管理器
pip install uv
```

### API密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建API密钥
3. 设置环境变量：
```bash
export GEMINI_API_KEY="your-api-key-here"
```

或在Windows PowerShell中：
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

## 使用方法

### 基本语法

**重要提示**：始终使用绝对路径运行脚本（不要先cd到技能目录），从用户的当前工作目录运行，以便图像保存在用户工作的地方。

### 生成新图像

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "your image description" \
  --filename "output-name.png" \
  [--resolution 1K|2K|4K] \
  [--api-key KEY]
```

**示例**：
```bash
# 生成一张简单的概念图
uv run /path/to/SKILLS/nano-banana-pro/scripts/generate_image.py \
  --prompt "A futuristic city with flying cars at sunset" \
  --filename "city-concept.png" \
  --resolution 1K
```

### 编辑现有图像

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "editing instructions" \
  --filename "output-name.png" \
  --input-image "path/to/input.png" \
  [--resolution 1K|2K|4K] \
  [--api-key KEY]
```

**示例**：
```bash
# 去除背景
uv run /path/to/SKILLS/nano-banana-pro/scripts/generate_image.py \
  --prompt "Remove the background and make it transparent" \
  --filename "no-background.png" \
  --input-image "original.png" \
  --resolution 2K

# 调整风格
uv run /path/to/SKILLS/nano-banana-pro/scripts/generate_image.py \
  --prompt "Transform this photo into a watercolor painting style" \
  --filename "watercolor-style.png" \
  --input-image "photo.jpg" \
  --resolution 2K

# 添加元素
uv run /path/to/SKILLS/nano-banana-pro/scripts/generate_image.py \
  --prompt "Add a cat sitting on the sofa" \
  --filename "with-cat.png" \
  --input-image "room.png" \
  --resolution 2K
```

## 默认工作流（草稿 → 迭代 → 最终）

推荐的工作流程以节省时间和API配额：

1. **草稿阶段 (1K)**
   - 使用1K分辨率快速生成多个版本
   - 快速反馈循环，验证概念
   - 成本最低，速度最快

2. **迭代阶段**
   - 基于草稿结果微调提示词
   - 每次迭代使用新的文件名
   - 逐步改进效果

3. **最终阶段 (4K)**
   - 仅在确定满意的提示词后使用4K
   - 生成高质量最终版本
   - 成本最高，但效果最佳

**示例工作流**：
```bash
# 第1步：草稿
uv run .../generate_image.py --prompt "..." --filename "v1-draft.png" --resolution 1K

# 第2步：迭代
uv run .../generate_image.py --prompt "Better lighting, add shadows" --filename "v2-iteration.png" --resolution 1K

# 第3步：最终
uv run .../generate_image.py --prompt "Perfect composition, dramatic lighting" --filename "v3-final.png" --resolution 4K
```

## 分辨率选项

| 分辨率 | 像素尺寸 | 适用场景 | 推荐用途 |
|--------|---------|---------|---------|
| **1K** | ~1024×1024 | 快速迭代、概念验证 | 草稿、预览 |
| **2K** | ~2048×2048 | 中等质量、平衡速度与质量 | 测试、中等用途 |
| **4K** | ~4096×4096 | 最高质量、打印级别 | 最终输出、打印 |

**默认值**：1K（如果不指定分辨率参数）

## API密钥配置

### 优先级（从高到低）

1. **命令行参数**：`--api-key KEY`
2. **环境变量**：`GEMINI_API_KEY`
3. **配置文件**：脚本会查找 `.env` 文件

### 配置环境变量（推荐）

#### Linux/macOS
```bash
# 临时（当前会话）
export GEMINI_API_KEY="your-key"

# 永久（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows PowerShell
```powershell
# 临时（当前会话）
$env:GEMINI_API_KEY="your-key"

# 永久（添加到配置文件）
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-key', 'User')
```

## 图像编辑功能

### 支持的编辑类型

#### 风格转换
```bash
--prompt "Convert to black and white photography"
--prompt "Apply anime style"
--prompt "Make it look like an oil painting"
```

#### 内容修改
```bash
--prompt "Add sunglasses to the person"
--prompt "Remove the red car from the background"
--prompt "Change the sky to a sunset"
```

#### 质量提升
```bash
--prompt "Enhance the lighting and add more contrast"
--prompt "Make the colors more vibrant"
--prompt "Reduce noise and sharpen the image"
```

#### 尺寸调整
```bash
--prompt "Crop to focus on the main subject"
--prompt "Extend the canvas to the right"
```

### 编辑最佳实践

1. **明确具体的指令**：
   - ❌ "Fix this image"
   - ✅ "Increase the brightness by 20% and add a warm color tone"

2. **保持一致的输出格式**：
   - 输入PNG → 输出PNG
   - 输入JPG → 输出JPG

3. **使用适当的分辨率**：
   - 小尺寸图像编辑 → 1K足够
   - 大尺寸图像编辑 → 2K或4K

## 提示词编写技巧

### 文生图像（Text-to-Image）

#### 优秀的提示词结构
```
[主体描述] + [风格/艺术风格] + [环境/背景] + [光线/色彩] + [细节/纹理]
```

**示例**：
```
A majestic lion walking through a misty savanna at dawn,
golden hour lighting, warm orange and purple hues,
photorealistic style, sharp details, 8k quality
```

#### 风格关键词

- **摄影风格**：photorealistic, cinematic, portrait, landscape, macro
- **艺术风格**：oil painting, watercolor, sketch, anime, digital art
- **光线**：golden hour, soft lighting, dramatic lighting, neon lights
- **质量**：high detail, sharp focus, 4k, 8k, professional

### 图像编辑（Image-to-Image）

#### 编辑提示词模板
```
[动作] + [目标元素] + [预期效果]
```

**示例**：
```
"Remove the person in the background and replace with a clear sky"
"Change the lighting to be softer and more warm"
"Add reflections to the water surface"
```

## 输出说明

### 输出文件

- **格式**：PNG（保持最高质量）
- **保存位置**：当前工作目录
- **命名**：由 `--filename` 参数指定

### 输出信息

脚本执行后会输出：
```bash
✓ Image generated successfully
📁 Saved to: /full/path/to/output.png
📊 Resolution: 1024x1024 (1K)
```

### 重要提示

**不要将图像读回** - 只需要告知用户保存的路径即可。图像文件已保存在磁盘上，无需额外处理。

## 常见问题

### Q: 生成失败怎么办？

**检查清单**：
1. API密钥是否正确：`echo $GEMINI_API_KEY`
2. 网络连接是否正常
3. 是否有足够的API配额
4. 提示词是否符合内容政策

**常见错误**：
```
Error: API key not found
解决: 设置 GEMINI_API_KEY 环境变量

Error: Quota exceeded
解决: 等待配额重置或升级计划

Error: Content policy violation
解决: 修改提示词，避免违禁内容
```

### Q: 如何批量生成图像？

创建批处理脚本：

```bash
#!/bin/bash
# batch-generate.sh

SCRIPT_PATH="/path/to/SKILLS/nano-banana-pro/scripts/generate_image.py"

uv run "$SCRIPT_PATH" \
  --prompt "A mountain landscape at sunrise" \
  --filename "mountain-1.png" \
  --resolution 1K

uv run "$SCRIPT_PATH" \
  --prompt "A beach scene with palm trees" \
  --filename "beach-1.png" \
  --resolution 1K

uv run "$SCRIPT_PATH" \
  --prompt "A forest path in autumn" \
  --filename "forest-1.png" \
  --resolution 1K
```

### Q: 如何提高生成质量？

**技巧**：
1. 使用更详细的提示词
2. 指定风格和质量关键词
3. 从2K升级到4K分辨率
4. 基于满意的草稿进行编辑改进

### Q: API成本如何控制？

**成本优化策略**：
1. 从1K草稿开始，仅在满意时使用4K
2. 一次生成多个版本，选择最好的进行编辑
3. 使用编辑而非重新生成来改进图像
4. 监控API使用量和成本

## 高级用法

### 嵌入到自动化工作流

```python
import subprocess
import os

def generate_image(prompt, filename, resolution="1K"):
    script_path = "/path/to/scripts/generate_image.py"
    cmd = [
        "uv", "run", script_path,
        "--prompt", prompt,
        "--filename", filename,
        "--resolution", resolution
    ]

    if "GEMINI_API_KEY" in os.environ:
        cmd.extend(["--api-key", os.environ["GEMINI_API_KEY"]])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        raise Exception(f"Generation failed: {result.stderr}")

# 使用
generate_image(
    prompt="A beautiful sunset over mountains",
    filename="sunset.png",
    resolution="2K"
)
```

### 与其他工具集成

**配合 Obsidian**：
```bash
# 生成图像并插入到笔记
uv run .../generate_image.py --prompt "..." --filename "image.png"
# 手动将 ![](image.png) 添加到笔记中
```

**配合 Markdown 文档**：
```markdown
![Generated Image](./image.png)
```

## 示例场景

### 场景1：创建产品概念图
```bash
# 草稿
uv run .../generate_image.py \
  --prompt "Modern smartphone with curved screen, minimal design, white background, product photography style" \
  --filename "product-v1.png" \
  --resolution 1K

# 迭代 - 改进角度
uv run .../generate_image.py \
  --prompt "Same smartphone, side view, showcase the camera module" \
  --filename "product-v2.png" \
  --resolution 1K

# 最终
uv run .../generate_image.py \
  --prompt "Professional product shot, perfect lighting, studio quality" \
  --filename "product-final.png" \
  --resolution 4K
```

### 场景2：创建UI设计元素
```bash
# 生成按钮图标
uv run .../generate_image.py \
  --prompt "Simple modern download button icon, blue color, white arrow, rounded corners, transparent background, flat design" \
  --filename "download-icon.png" \
  --resolution 1K
```

### 场景3：营销素材
```bash
# 社交媒体封面
uv run .../generate_image.py \
  --prompt "Cyberpunk cityscape, neon lights, futuristic atmosphere, vibrant colors, 16:9 aspect ratio" \
  --filename "social-cover.png" \
  --resolution 2K
```

## 参考资源

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API 文档](https://ai.google.dev/docs)
- [提示词工程指南](https://prompts.ai/)

---

**最后更新**: 2026-03-24
