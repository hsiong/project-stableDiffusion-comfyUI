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
================ custom_nodes: git 仓库状态 ================
GIT: ComfyUI-GGUF
origin	https://github.com/city96/ComfyUI-GGUF (fetch)
origin	https://github.com/city96/ComfyUI-GGUF (push)

GIT: ComfyUI-Impact-Pack
origin	https://github.com/ltdrdata/ComfyUI-Impact-Pack (fetch)
origin	https://github.com/ltdrdata/ComfyUI-Impact-Pack (push)

GIT: ComfyUI-LTXVideo
origin	https://github.com/Lightricks/ComfyUI-LTXVideo (fetch)
origin	https://github.com/Lightricks/ComfyUI-LTXVideo (push)

GIT: ComfyUI-Manager
origin	https://github.com/Comfy-Org/ComfyUI-Manager (fetch)
origin	https://github.com/Comfy-Org/ComfyUI-Manager (push)

GIT: ComfyUI-RMBG
origin	https://github.com/1038lab/ComfyUI-RMBG (fetch)
origin	https://github.com/1038lab/ComfyUI-RMBG (push)

GIT: ComfyUI-VideoHelperSuite
origin	https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite (fetch)
origin	https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite (push)

GIT: ComfyUI-WanVideoWrapper
origin	https://github.com/kijai/ComfyUI-WanVideoWrapper (fetch)
origin	https://github.com/kijai/ComfyUI-WanVideoWrapper (push)

GIT: ComfyUI_Custom_Nodes_AlekPet
origin	https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet (fetch)
origin	https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet (push)

GIT: ComfyUI_IPAdapter_plus
origin	https://github.com/cubiq/ComfyUI_IPAdapter_plus (fetch)
origin	https://github.com/cubiq/ComfyUI_IPAdapter_plus (push)

GIT: ComfyUI_UltimateSDUpscale
origin	https://github.com/ssitu/ComfyUI_UltimateSDUpscale (fetch)
origin	https://github.com/ssitu/ComfyUI_UltimateSDUpscale (push)

GIT: comfyui_controlnet_aux
origin	https://github.com/Fannovel16/comfyui_controlnet_aux (fetch)
origin	https://github.com/Fannovel16/comfyui_controlnet_aux (push)

GIT: rgthree-comfy
origin	https://github.com/rgthree/rgthree-comfy (fetch)
origin	https://github.com/rgthree/rgthree-comfy (push)

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



# 安装依赖

## 拉取 comfyUI



## 安装 ComfyUI 根依赖

```
pip install -r requirements.txt manager_requirements.txt
```



## 批量安装所有插件依赖

```
echo "================ 安装 custom_nodes 依赖 ================"
find custom_nodes -type f -name 'requirements.txt' | sort | while read -r f; do
  echo "INSTALL: $f"
  pip install -r "$f"
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
