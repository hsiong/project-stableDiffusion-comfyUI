# 秋叶整合包分析

> 发布页
>
> https://www.bilibili.com/video/BV1Ew411776J/?vd_source=5de16445512bf51aa6d97e398de9b92f
>
> 2026.1.19 更新：https://www.bilibili.com/opus/1159516886456598528



## 完整打印根目录所有安装相关文件

这组命令会把根目录里最重要的安装文件**全部打印出来**，不截断。

### requirements

```
echo "================ ROOT: requirements.txt ================"
[ -f requirements.txt ] && cat requirements.txt || echo "requirements.txt 不存在"
================ ROOT: requirements.txt ================
comfyui-frontend-package==1.36.14
comfyui-workflow-templates==0.8.4
comfyui-embedded-docs==0.4.0
torch
torchsde
torchvision
torchaudio
numpy>=1.25.0
einops
transformers>=4.50.3
tokenizers>=0.13.3
sentencepiece
safetensors>=0.4.2
aiohttp>=3.11.8
yarl>=1.18.0
pyyaml
Pillow
scipy
tqdm
psutil
alembic
SQLAlchemy
av>=14.2.0
comfy-kitchen>=0.2.6

#non essential dependencies:
kornia>=0.7.1
spandrel
pydantic~=2.0
pydantic-settings~=2.0
```

### manager_requirements

```
echo "================ ROOT: manager_requirements.txt ================"
[ -f manager_requirements.txt ] && cat manager_requirements.txt || echo "manager_requirements.txt 不存在"


================ ROOT: manager_requirements.txt ================
comfyui_manager==4.0.5

```

### pyproject.toml

```
echo "================ ROOT: pyproject.toml ================"
[ -f pyproject.toml ] && cat pyproject.toml || echo "pyproject.toml 不存在"


================ ROOT: pyproject.toml ================
[project]
name = "ComfyUI"
version = "0.9.2"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.10"

[project.urls]
homepage = "https://www.comfy.org/"
repository = "https://github.com/comfyanonymous/ComfyUI"
documentation = "https://docs.comfy.org/"

[tool.ruff]
lint.select = [
  "N805", # invalid-first-argument-name-for-method
  "S307", # suspicious-eval-usage
  "S102", # exec
  "E",
  "T",    # print-usage
  "W",
  # The "F" series in Ruff stands for "Pyflakes" rules, which catch various Python syntax errors and undefined names.
  # See all rules here: https://docs.astral.sh/ruff/rules/#pyflakes-f
  "F",
]

lint.ignore = ["E501", "E722", "E731", "E712", "E402", "E741"]

exclude = ["*.ipynb", "**/generated/*.pyi"]

[tool.pylint]
master.py-version = "3.10"
master.extension-pkg-allow-list = [
  "pydantic",
]
reports.output-format = "colorized"
similarities.ignore-imports = "yes"
messages_control.disable = [
  "missing-module-docstring",
  "missing-class-docstring",
  "missing-function-docstring",
  "line-too-long",
  "too-few-public-methods",
  "too-many-public-methods",
  "too-many-instance-attributes",
  "too-many-positional-arguments",
  "broad-exception-raised",
  "too-many-lines",
  "invalid-name",
  "unused-argument",
  "broad-exception-caught",
  "consider-using-with",
  "fixme",
  "too-many-statements",
  "too-many-branches",
  "too-many-locals",
  "too-many-arguments",
  "too-many-return-statements",
  "too-many-nested-blocks",
  "duplicate-code",
  "abstract-method",
  "superfluous-parens",
  "arguments-differ",
  "redefined-builtin",
  "unnecessary-lambda",
  "dangerous-default-value",
  "invalid-overridden-method",
  # next warnings should be fixed in future
  "bad-classmethod-argument",  # Class method should have 'cls' as first argument
  "wrong-import-order",  # Standard imports should be placed before third party imports
  "ungrouped-imports",
  "unnecessary-pass",
  "unnecessary-lambda-assignment",
  "no-else-return",
  "unused-variable",
]

```



### extra_model_paths

```
echo "================ ROOT: extra_model_paths.yaml ================"
[ -f extra_model_paths.yaml ] && cat extra_model_paths.yaml || echo "extra_model_paths.yaml 不存在"


================ ROOT: extra_model_paths.yaml ================
extra_model_paths.yaml 不存在
```

extra_model_paths.yaml.example

```
echo "================ ROOT: extra_model_paths.yaml.example ================"
[ -f extra_model_paths.yaml.example ] && cat extra_model_paths.yaml.example || echo "extra_model_paths.yaml.example 不存在"


================ ROOT: extra_model_paths.yaml.example ================
#Rename this to extra_model_paths.yaml and ComfyUI will load it

#config for comfyui
#your base path should be either an existing comfy install or a central folder where you store all of your models, loras, etc.

#comfyui:
#     base_path: path/to/comfyui/
#     # You can use is_default to mark that these folders should be listed first, and used as the default dirs for eg downloads
#     #is_default: true
#     checkpoints: models/checkpoints/
#     text_encoders: |
#          models/text_encoders/
#          models/clip/  # legacy location still supported
#     clip_vision: models/clip_vision/
#     configs: models/configs/
#     controlnet: models/controlnet/
#     diffusion_models: |
#                  models/diffusion_models
#                  models/unet
#     embeddings: models/embeddings/
#     loras: models/loras/
#     upscale_models: models/upscale_models/
#     vae: models/vae/
#     audio_encoders: models/audio_encoders/
#     model_patches: models/model_patches/


#config for a1111 ui
#all you have to do is uncomment this (remove the #) and change the base_path to where yours is installed

#a111:
#     base_path: path/to/stable-diffusion-webui/
#     checkpoints: models/Stable-diffusion
#     configs: models/Stable-diffusion
#     vae: models/VAE
#     loras: |
#          models/Lora
#          models/LyCORIS
#     upscale_models: |
#                   models/ESRGAN
#                   models/RealESRGAN
#                   models/SwinIR
#     embeddings: embeddings
#     hypernetworks: models/hypernetworks
#     controlnet: models/ControlNet


# For a full list of supported keys (style_models, vae_approx, hypernetworks, photomaker,
# model_patches, audio_encoders, classifiers, etc.) see folder_paths.py.

#other_ui:
#    base_path: path/to/ui
#    checkpoints: models/checkpoints
#    gligen: models/gligen
#    custom_nodes: path/custom_nodes

```



## 看 custom_nodes 里有哪些 node

```
echo "================ custom_nodes: 节点目录 ================"
find custom_nodes -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
================ custom_nodes: 节点目录 ================
ComfyUI-GGUF
ComfyUI-Impact-Pack
ComfyUI-LTXVideo
ComfyUI-Manager
ComfyUI-RMBG
ComfyUI-VideoHelperSuite
ComfyUI-WanVideoWrapper
ComfyUI_Custom_Nodes_AlekPet
ComfyUI_IPAdapter_plus
ComfyUI_UltimateSDUpscale
comfyui_controlnet_aux
rgthree-comfy

```

#### 看哪些插件是 git 仓库

```
echo "================ custom_nodes: git 仓库状态 ================"
for d in custom_nodes/*; do
  [ -d "$d" ] || continue
  if [ -d "$d/.git" ]; then
    echo "GIT: $(basename "$d")"
    git -C "$d" remote -v | head -n 2
  else
    echo "NO_GIT: $(basename "$d")"
  fi
  echo
done
```



## 完整列出 models 里所有模型文件

这里不打印模型“内容”，而是完整列出所有模型文件路径。

```
echo "================ models: 所有模型文件路径 ================"
find models -type f | sort
echo "================ custom_nodes: git 仓库状态 ================"
for d in custom_nodes/*; do
  [ -d "$d" ] || continue
  if [ -d "$d/.git" ]; then
    echo "GIT: $(basename "$d")"
    git -C "$d" remote -v | head -n 2
  else
    echo "NO_GIT: $(basename "$d")"
  fi
  echo
done

================ models: 所有模型文件路径 ================
models/audio_encoders/put_audio_encoder_models_here
models/checkpoints/put_checkpoints_here
models/clip/put_clip_or_text_encoder_models_here
models/clip_vision/put_clip_vision_models_here
models/configs/anything_v3.yaml
models/configs/v1-inference_clip_skip_2_fp16.yaml
models/configs/v1-inference_clip_skip_2.yaml
models/configs/v1-inference_fp16.yaml
models/configs/v1-inference.yaml
models/configs/v1-inpainting-inference.yaml
models/configs/v2-inference_fp32.yaml
models/configs/v2-inference-v_fp32.yaml
models/configs/v2-inference-v.yaml
models/configs/v2-inference.yaml
models/configs/v2-inpainting-inference.yaml
models/controlnet/put_controlnets_and_t2i_here
models/diffusers/put_diffusers_models_here
models/diffusion_models/put_diffusion_model_files_here
models/embeddings/put_embeddings_or_textual_inversion_concepts_here
models/gligen/put_gligen_models_here
models/hypernetworks/put_hypernetworks_here
models/latent_upscale_models/put_latent_upscale_models_here
models/loras/put_loras_here
models/model_patches/put_model_patches_here
models/photomaker/put_photomaker_models_here
models/style_models/put_t2i_style_model_here
models/text_encoders/put_text_encoder_files_here
models/unet/put_unet_files_here
models/upscale_models/put_esrgan_and_other_upscale_models_here
models/vae_approx/put_taesd_encoder_pth_and_taesd_decoder_pth_here
models/vae/put_vae_here
```



## 其他

```
echo "================ comfy_api ================"
find comfy_api -print 2>/dev/null | sort

echo
echo "================ comfy_api_nodes ================"
find comfy_api_nodes -print 2>/dev/null | sort

echo
echo "================ middleware ================"
find middleware -print 2>/dev/null | sort
```

# 插件解析

## ComfyUI-GGUF

用途：**加载 GGUF 格式模型**

GGUF 是一种常见于 `llama.cpp` 生态的量化模型格式。
这个插件让 ComfyUI 可以读取 GGUF 模型（例如某些量化的 Flux / LLM）。

常见用途：

- 运行 GGUF 量化模型
- 支持 llama.cpp 类模型加载

------

## ComfyUI-Impact-Pack

用途：**图像增强与自动修复节点包**

这是 ComfyUI 中非常常用的一组扩展节点。

主要功能：

- 自动人脸修复
- 自动手部修复
- 自动细节增强
- 目标检测 / bbox
- segmentation
- mask 处理

常见节点：

- FaceDetailer
- ImpactDetector
- Segmentation
- Detailer

常见用途：

- 自动修脸
- 自动修手
- 自动细节增强

------

## ComfyUI-LTXVideo

用途：**LTX 视频生成模型**

支持：

- text → video
- image → video

特点：

- 视频质量较高
- 模型较大
- GPU 要求较高

常见节点：

- LTXVideoSampler
- LTXVideoLoader

------

## ComfyUI-Manager

用途：**插件与模型管理器**

主要功能：

- 安装插件
- 更新插件
- 下载模型
- 更新 ComfyUI

启动后 UI 中会出现：

```
Manager
```

用于管理插件和资源。

------

## ComfyUI-RMBG

用途：**抠图 / 图像分割**

支持：

- 背景移除
- 人物分割
- SAM
- SAM2
- SAM3
- GroundingDINO

常见节点：

- RMBG
- SegmentAnything

常见用途：

- 自动抠图
- 自动生成 mask

------

## ComfyUI-VideoHelperSuite

用途：**视频处理基础节点**

提供视频读写和帧处理能力。

主要功能：

- 视频读取
- 视频导出
- 帧提取
- 帧合成
- GIF / MP4 生成

常见节点：

- LoadVideo
- VideoCombine
- FrameExtractor
- SaveVideo

用途：

- 视频 → 图片
- 图片 → 视频

------

## ComfyUI-WanVideoWrapper

用途：**WanVideo 视频模型支持**

支持：

- text → video
- image → video

适配 Wan 系列模型，例如：

- Wan 2.1
- Wan 2.2

常见节点：

- WanVideoSampler
- WanVideoLoader

------

## ComfyUI_Custom_Nodes_AlekPet

用途：**多功能工具节点集合**

包含很多辅助工具：

- prompt 工具
- 翻译节点
- JSON 工具
- Python 执行节点
- JavaScript 执行节点

常见节点：

- Translate
- PromptTools
- IDENode

------

## ComfyUI_IPAdapter_plus

用途：**参考图生成 / 图像提示**

IPAdapter 可以使用参考图片控制生成结果。

支持：

- style transfer
- image prompt
- FaceID

常见节点：

- IPAdapter
- IPAdapterAdvanced
- IPAdapterFaceID

常见用途：

- 保持人物一致
- 参考图生成

------

## ComfyUI_UltimateSDUpscale

用途：**高分辨率图像放大**

特点：

- tile upscale（分块放大）
- 显存占用较低

常见用途：

- 1K → 4K
- 2K → 8K

主要节点：

- UltimateSDUpscale

------

## comfyui_controlnet_aux

用途：**ControlNet 预处理器**

生成 ControlNet 需要的控制图。

支持：

- OpenPose
- Depth
- Canny
- Lineart
- HED
- MLSD

常见节点：

- OpenPosePreprocessor
- DepthPreprocessor
- LineartPreprocessor

用途：

- 生成 ControlNet 控制图

------

## rgthree-comfy

用途：**工作流工具节点**

用于优化和控制 ComfyUI 工作流。

主要功能：

- Switch 节点
- 调试节点
- workflow 工具

常见节点：

- FastSwitch
- AnySwitch
- ContextSwitch
- Debug

用途：

- 简化 workflow
- 实现逻辑控制

# 模型解析

# 安装依赖

## 拉取 comfyUI

```
git clone https://github.com/comfyanonymous/ComfyUI.git
git tag
# 1) 固定 ComfyUI 本体版本
git fetch --tags
# git checkout v0.9.2
```



## 安装 ComfyUI 根依赖

```
cd comfy-workspace
cat > requirements.txt <<'EOF'
comfyui-frontend-package==1.36.14
comfyui-workflow-templates==0.8.4
comfyui-embedded-docs==0.4.0
torch
torchsde
torchvision
torchaudio
numpy>=1.25.0
einops
transformers>=4.50.3
tokenizers>=0.13.3
sentencepiece
safetensors>=0.4.2
aiohttp>=3.11.8
yarl>=1.18.0
pyyaml
Pillow
scipy
tqdm
psutil
alembic
SQLAlchemy
av>=14.2.0
comfy-kitchen>=0.2.6

#non essential dependencies:
kornia>=0.7.1
spandrel
pydantic~=2.0
pydantic-settings~=2.0
EOF

# 3) 严格覆盖 manager_requirements.txt
cat > manager_requirements.txt <<'EOF'
comfyui_manager==4.0.5
EOF

```



```
# 4) 严格覆盖 pyproject.toml
cat > pyproject.toml <<'EOF'
[project]
name = "ComfyUI"
version = "0.9.2"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.10"

[project.urls]
homepage = "https://www.comfy.org/"
repository = "https://github.com/comfyanonymous/ComfyUI"
documentation = "https://docs.comfy.org/"

[tool.ruff]
lint.select = [
  "N805", # invalid-first-argument-name-for-method
  "S307", # suspicious-eval-usage
  "S102", # exec
  "E",
  "T",    # print-usage
  "W",
  # The "F" series in Ruff stands for "Pyflakes" rules, which catch various Python syntax errors and undefined names.
  # See all rules here: https://docs.astral.sh/ruff/rules/#pyflakes-f
  "F",
]

lint.ignore = ["E501", "E722", "E731", "E712", "E402", "E741"]

exclude = ["*.ipynb", "**/generated/*.pyi"]

[tool.pylint]
master.py-version = "3.10"
master.extension-pkg-allow-list = [
  "pydantic",
]
reports.output-format = "colorized"
similarities.ignore-imports = "yes"
messages_control.disable = [
  "missing-module-docstring",
  "missing-class-docstring",
  "missing-function-docstring",
  "line-too-long",
  "too-few-public-methods",
  "too-many-public-methods",
  "too-many-instance-attributes",
  "too-many-positional-arguments",
  "broad-exception-raised",
  "too-many-lines",
  "invalid-name",
  "unused-argument",
  "broad-exception-caught",
  "consider-using-with",
  "fixme",
  "too-many-statements",
  "too-many-branches",
  "too-many-locals",
  "too-many-arguments",
  "too-many-return-statements",
  "too-many-nested-blocks",
  "duplicate-code",
  "abstract-method",
  "superfluous-parens",
  "arguments-differ",
  "redefined-builtin",
  "unnecessary-lambda",
  "dangerous-default-value",
  "invalid-overridden-method",
  # next warnings should be fixed in future
  "bad-classmethod-argument",  # Class method should have 'cls' as first argument
  "wrong-import-order",  # Standard imports should be placed before third party imports
  "ungrouped-imports",
  "unnecessary-pass",
  "unnecessary-lambda-assignment",
  "no-else-return",
  "unused-variable",
]
EOF
```



```
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple \
--extra-index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt -r manager_requirements.txt
```



## 批量安装所有插件依赖



```

# 7) 拉齐 custom_nodes 仓库
[ -d custom_nodes/ComfyUI-GGUF/.git ] || git clone https://github.com/city96/ComfyUI-GGUF custom_nodes/ComfyUI-GGUF
[ -d custom_nodes/ComfyUI-Impact-Pack/.git ] || git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack custom_nodes/ComfyUI-Impact-Pack
[ -d custom_nodes/ComfyUI-LTXVideo/.git ] || git clone https://github.com/Lightricks/ComfyUI-LTXVideo custom_nodes/ComfyUI-LTXVideo
[ -d custom_nodes/ComfyUI-Manager/.git ] || git clone https://github.com/Comfy-Org/ComfyUI-Manager custom_nodes/ComfyUI-Manager
[ -d custom_nodes/ComfyUI-RMBG/.git ] || git clone https://github.com/1038lab/ComfyUI-RMBG custom_nodes/ComfyUI-RMBG
[ -d custom_nodes/ComfyUI-VideoHelperSuite/.git ] || git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite custom_nodes/ComfyUI-VideoHelperSuite
[ -d custom_nodes/ComfyUI-WanVideoWrapper/.git ] || git clone https://github.com/kijai/ComfyUI-WanVideoWrapper custom_nodes/ComfyUI-WanVideoWrapper
[ -d custom_nodes/ComfyUI_Custom_Nodes_AlekPet/.git ] || git clone https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet custom_nodes/ComfyUI_Custom_Nodes_AlekPet
[ -d custom_nodes/ComfyUI_IPAdapter_plus/.git ] || git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus custom_nodes/ComfyUI_IPAdapter_plus
[ -d custom_nodes/ComfyUI_UltimateSDUpscale/.git ] || git clone https://github.com/ssitu/ComfyUI_UltimateSDUpscale custom_nodes/ComfyUI_UltimateSDUpscale
[ -d custom_nodes/comfyui_controlnet_aux/.git ] || git clone https://github.com/Fannovel16/comfyui_controlnet_aux custom_nodes/comfyui_controlnet_aux
[ -d custom_nodes/rgthree-comfy/.git ] || git clone https://github.com/rgthree/rgthree-comfy custom_nodes/rgthree-comfy

```





```
echo "================ 安装 custom_nodes 依赖 ================"
find . -type f -name 'requirements.txt' | sort | while read -r f; do
  echo "INSTALL: $f"
  pip install   --no-build-isolation -v   -i https://pypi.org/simple  -r "$f"
  echo
done
```

## 如果插件自带 install.py

不是所有插件都有，但有的话值得单独列出来：

```
echo "================ custom_nodes: install.py ================"
find custom_nodes -type f -name 'install.py' | sort
```

如果你要执行，再逐个执行：

```
find custom_nodes -type f -name 'install.py' | sort | while read -r f; do
  echo "RUN: $f"
  python "$f"
  echo
done
```

但这里我建议你**先别盲跑全部 `install.py`**，因为这类脚本可能会：

- 下载额外模型
- 改配置
- 装额外包
- 做平台相关处理

所以比起 `git pull`，**批量执行 install.py 反而更需要谨慎**。



## 复制 models

```
cp -r models ../../comfy-workspace  
```



# 启动

```
python main.py --enable-manager -port 8188
```
