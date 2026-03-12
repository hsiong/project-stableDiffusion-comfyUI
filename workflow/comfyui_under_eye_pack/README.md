# ComfyUI 自动下眼睑术区 mask + 双版本术后模拟

这个包做了三件事：

1. 用 **MediaPipe Face Landmarker** 自动取 478 点人脸关键点，程序化生成双侧 under-eye mask  
2. 把同一张原图 + 同一张 mask 送进 **FLUX.1 Fill dev** 做局部重绘  
3. 同一张图自动输出两个版本：  
   - **术后即刻**：轻度肿胀、轻度发红  
   - **恢复 10–30 天**：轮廓更平、红感基本退掉

## 目录

- `custom_nodes/ComfyUI_UnderEyeMask/`：自定义节点
- `workflows/under_eye_flux_fill_dual_output.json`：普通工作流 JSON
- `workflows/under_eye_flux_fill_dual_output_api.json`：API 工作流 JSON
- `workflows/under_eye_flux_fill_dual_output.png`：带 metadata 的工作流 PNG，可直接拖进 ComfyUI

## 1) 安装自定义节点

把 `custom_nodes/ComfyUI_UnderEyeMask` 整个目录放进：

```text
ComfyUI/custom_nodes/
```

然后在你的 ComfyUI Python 环境里安装依赖：

```bash
pip install -r custom_nodes/ComfyUI_UnderEyeMask/requirements.txt
```

## 2) 准备 MediaPipe 模型

把 `face_landmarker.task` 放到：

```text
ComfyUI/models/mediapipe/face_landmarker.task
```

建议模型文件名保持这个名字，和工作流默认值一致。

## 3) 准备 FLUX.1 Fill dev 模型

把这些文件放到对应目录：

```text
ComfyUI/
├── models/
│   ├── text_encoders/
│   │   ├── clip_l.safetensors
│   │   └── t5xxl_fp16.safetensors
│   ├── vae/
│   │   └── ae.safetensors
│   └── diffusion_models/
│       └── flux1-fill-dev.safetensors
```

## 4) 导入工作流

两种方式都可以：

- 直接把 `under_eye_flux_fill_dual_output.png` 拖进 ComfyUI
- 或者导入 `under_eye_flux_fill_dual_output.json`

## 5) 运行

1. 在 `Load Image` 节点放入你的原图  
2. 先执行一次，确认 `MediaPipe Under-Eye Mask` 的 `preview` 输出覆盖范围合理  
3. 再看输出目录里的三类结果：
   - `under_eye_mask_preview`
   - `under_eye_immediate`
   - `under_eye_recovered`

## 6) 常用可调参数

`MediaPipe Under-Eye Mask` 节点里最常用的 4 个参数：

- `depth_ratio`：向下扩展深度
- `width_padding_ratio`：内外眼角横向扩展
- `dilate_px`：膨胀
- `feather_px`：羽化

建议起点：

- 1024 宽图：`depth_ratio=0.22`、`width_padding_ratio=0.08`、`dilate_px=12`、`feather_px=18`
- 2048 宽图：把 `dilate_px` 和 `feather_px` 大约翻倍

## 7) Prompt 说明

这套默认 prompt 目标是“**只改 mask 内的下眼睑区域**”，尽量保留：

- 身份
- 光照
- 相机角度
- 眉眼
- 睫毛
- 妆面
- 背景

如果你想更明显一点，可以在两个正向 prompt 里分别加强：

- 即刻版：`mild to moderate swelling`, `subtle redness`
- 恢复版：`smoother tear trough`, `flatter lower eyelid contour`

## 8) 备注

这是视觉模拟工作流，不是医疗效果承诺，也不能替代医生面诊。
