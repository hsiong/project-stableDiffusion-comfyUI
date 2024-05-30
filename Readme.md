

# 基础操作

## 资料

- download https://github.com/comfyanonymous/ComfyUI
- 秋叶整合包 https://www.bilibili.com/video/BV1Ew411776J/?spm_id_from=333.999.0.0&vd_source=2774965e63414d32c855e45d7fca856a
- https://www.comflowy.com/zh-CN/basics/basic-nodes

## 快捷键

+ 拖拽多个组件

  按住 ctrl 多选, 按住 shift 拖动

+ 带连线复制 ctrl + shift + v 

+ 让线更好看 utils - Reroute Primitive 

+ undo: ctrl+z

+ redo: ctrl+r

+ save: shift + s  

# 入门

https://www.youtube.com/watch?v=SPCaY1Q-P88&list=PLre94Fo0ReBLqf3yoYlnxU-dqKCg-sXTM&index=3

## 基础组件
+ 加载模型 Module: add node - loader - load checkpoint
+ 提示词 Prompt: conditioning - clip text encoder (Prompt)
+ 分组 Group: add color, add group, add general-note
+ 随机数: Primitive, choose randomize
+ 保存字符串: Save Text



## 采样器 Sampler

+ 从 clip text encoder (Prompt) CONDITIONING 拉一根线出来, KSampler
+ 或者 sampling - Ksampler

> 参数说明: 
>
> + seed: 采样器编号, fixed/randomize, 同一张图片, 同一个seed'
>   + add random: primitive node, connect to input
> + add_noise: enable
> + cfg: 与 prompt 相关程度, 建议在 10 左右
> + sampler_name: 由经典的常微分方程求解方程命名的sampler
>   + ancestral/sde: 每一step 添加随机采样, 不稳定, 随机性更强
>   + uni_pc: 适用于 10 step左右, 出现较好的效果
>   + 推荐: euler_ancestral, dpmpp_2m, dpmpp_2m_sde_gpu, uni_pc
> + scheduler: 在每一步采样器的大小
>   + normal: 线性
>   + karras: 平滑
>   + 后四个不推荐
> + denoise: 降噪百分比, 1 代表 100% steps
> + return_with_leftover_noise: 将剩余步数传递给下一个采样器
> + start_at_step/end_at_step: 与上一个采样器相关联

## 潜在空间图片 LATENT

选择空图片, 指定尺寸即可 

## 生成噪声图

+ save
+ preview

# Refiner 模型

![Screenshot 2024-02-27 at 16.27.52](/Users/vjf/Library/Application Support/typora-user-images/Screenshot 2024-02-27 at 16.27.52.png)

base模型生成小图, refiner模型生成大图  

+ base修改: 

  + add note base
  + change CLIP Text Encode to input
  + text 拉出来,  add node - utils - Primitive 
  + 采样器改为 sampling - KSampler(Advanced)
+ refiner:
  + 增加 refiner - checkpoint
  + 复制 prompt , text 连到 base text
  + base 高阶采样器输出到 refiner 高阶采样器, steps 与 base 一致, start_at_step = base end_at_step, end_at_stetp >= steps, return_with_leftover_noise false(可以使用 utils-Primitive 简化)

# Controlnet

+ \+ [万字干货！一口气掌握14种 ControlNet 官方控图模型的使用方法！](https://www.uisdc.com/stable-diffusion-guide-6)

## 轮廓类

轮廓类模型有 Canny 硬边缘、MLSD 直线、Lineart 真实线稿、Lineart_anime 动漫线稿、SoftEdge 软边缘、Segmentation 语义分割、Shuffle 随机洗牌这 7 种，且每种模型都配有相应的预处理器

![万字干货！一口气掌握14种 ControlNet 官方控图模型的使用方法！](https://image.uisdc.com/wp-content/uploads/2023/09/uisdc-sx-20230925-4.jpg)

### Canny 硬边缘

该模型源自图像处理领域的边缘检测算法，可以识别并提取图像中的边缘特征并输送到新的图像中。

+ canny（硬边缘检测）预处理器

canny 可以准确提取出画面中元素边缘的线稿，即使配合不同的主模型进行绘图都可以精准还原画面中的内容布局。

![万字干货！一口气掌握14种 ControlNet 官方控图模型的使用方法！](https://image.uisdc.com/wp-content/uploads/2023/09/uisdc-sx-20230925-6.jpg)

+ invert（白底黑线反色）的预处理器

它的功能并非是提取图像的空间特征，而是将线稿进行颜色反转。我们通过 Canny 等线稿类的预处理器提取得到的预览图都是黑底白线，但大部分的传统线稿都是白底黑线，为方便使用，很多时候我们需要将两者进行颜色转换，传统做法都是导出到 PS 等工具进行额外处理，非常繁琐。而 ControlNet 中贴心的内置了颜色反转的预处理功能，可以轻松实现将手绘线稿转换成模型可识别的预处理线稿图。

理解了 invert 的功能，我们就知道该预处理器并非 Canny 独有，而是可以配合大部分线稿模型使用。在最新版的 ControlNet 中，当我们选择 MLSD 直线、Lineart 线稿等控制类型时，预处理器中都能看到它的身影，后续就不挨个赘述了。

![万字干货！一口气掌握14种 ControlNet 官方控图模型的使用方法！](https://image.uisdc.com/wp-content/uploads/2023/09/uisdc-sx-20230925-7.jpg)



+ [Mastering ComfyUI: Creating Stunning Human Poses with ControlNet! - TUTORIAL](https://www.youtube.com/watch?v=w9fc3pIkl0w)

# animateDiff

## [Mastering AI Animation: Use Auto-Mask, ControlNet and AnimateDiff Evolved! - Video To Video](https://www.youtube.com/watch?v=7ZxsBmUm3Lg)

+ workflow: https://github.com/Nuked88/DreamingAI/blob/main/T13_video_to_video.json
+ customNode
  + ComfyUI-N-Suite
  + comfyui-reactor-node
+ model
  + Checkpoint: [MeinaMix_V10](https://huggingface.co/Meina/MeinaMix_V10/tree/main/safety_checker)
  + Controlnet: [control_v11p_sd15_lineart.pth](https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main)
  + Lora: [pytorch_lora_weights.safetensors](https://huggingface.co/Yashhhhmishra/pytorch_lora_weights.safetensors/blob/main/pytorch_lora_weights.safetensors)
  + animatediff_models: [temporaldiff-v1-animatediff.ckpt](https://huggingface.co/CiaraRowles/TemporalDiff/blob/main/temporaldiff-v1-animatediff.ckpt)
  + ReActorFaceSwap: 
    + insightface: [inswapper_128.onnx](https://huggingface.co/ezioruan/inswapper_128.onnx/tree/main)
    + facerestore_models: [codeformer.pth](https://github.com/sczhou/CodeFormer/releases)
  + comfyui_controlnet_aux\ckpts\lllyasviel/Annotators: [150_16_swin_l_oneformer_coco_100ep.pth](https://huggingface.co/lllyasviel/Annotators/blob/main/150_16_swin_l_oneformer_coco_100ep.pth)
+ Pip requirements
  + imageio-ffmpeg
  ![1710498296388_919E60E5-10D8-46fa-B10B-3CD98A7DC0DB.png](pic%2F1710498296388_919E60E5-10D8-46fa-B10B-3CD98A7DC0DB.png)

> error: 
> ERROR:root:!!! Exception during processing !!!
ERROR:root:Traceback (most recent call last):
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\execution.py", line 152, in recursive_execute
    output_data, output_ui = get_output_data(obj, input_data_all)
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\execution.py", line 82, in get_output_data
    return_values = map_node_over_list(obj, input_data_all, obj.FUNCTION, allow_interrupt=True)
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\execution.py", line 75, in map_node_over_list
    results.append(getattr(obj, func)(**slice_dict(input_data_all, i)))
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\nodes.py", line 552, in load_checkpoint
    out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\comfy\sd.py", line 448, in load_checkpoint_guess_config
    model_config = model_detection.model_config_from_unet(sd, "model.diffusion_model.", unet_dtype)
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\comfy\model_detection.py", line 164, in model_config_from_unet
    unet_config = detect_unet_config(state_dict, unet_key_prefix, dtype)
  File "D:\software\ComfyUI-aki\aki\ComfyUI-aki-v1.2\comfy\model_detection.py", line 49, in detect_unet_config
    model_channels = state_dict['{}input_blocks.0.0.weight'.format(key_prefix)].shape[0]
KeyError: 'model.diffusion_model.input_blocks.0.0.weight'
> 
> => change model
> 

> Error occurred when executing ReActorFaceSwap: This ORT build has ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'] enabled. Since ORT 1.9, you are required to explicitly set the providers parameter when instantiating InferenceSession. For example, onnxruntime.InferenceSession(..., providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'], ...)
> 
> => onnx 1.15.0 
> onnxruntime 1.16.1 
> onnxruntime-gpu 1.15.1 
> pip install onnxruntime==1.15.1 solve my issue

+ [Mastering ComfyUI: Getting Started with Video to Video!](https://www.youtube.com/watch?v=nMyiuiWjiEc)
+ [ComfyUI图片转视频📽，轻松上手AI视频制作, Image To Video ,用图像讲故事，内容更出彩！ #comfyui #aigc #videogeneration]: https://www.youtube.com/watch?v=C8IzGKMv5Wk

# ReActor: Face Swap

+  [Mastering ComfyUI: How to use ReActor for Face Swap - TUTORIAL](https://www.youtube.com/watch?v=gcLBPILYgrc)
+ 

# LDSR

+ [Upscalers Roundup + Full Workflow - LDSR, Ultimate SD, Models, HiRes Fix, Latent Upscale + Topaz](https://www.youtube.com/watch?v=9qHidG7H_8k)

# ComfyUI - API

+ [Mastering ComfyUI: Getting started with API - TUTORIAL](https://www.youtube.com/watch?v=va8Jkc7o9d4)



# Custom node

+ [How to make your own custom ComfyUI nodes](https://www.youtube.com/watch?v=tr_0qnwLQ0I)
+ [Clone a Simple Demo: ComfyUI-audio](https://github.com/eigenpunk/ComfyUI-audio)
+ 

# 人像检测

## 使用 comfyUI manager 安装 

+ open comfyUI manager
+ install Custom Nodes

## 使用 yolov8 实现人脸检测

https://github.com/zcfrank1st/Comfyui-Yolov8

+ yolov8 - detection/seg
+ mask - convert mask to image

## yolo-world
+ https://github.com/ZHO-ZHO-ZHO/ComfyUI-YoloWorld-EfficientSAM
+ https://github.com/AILab-CVC/YOLO-World
+ https://github.com/yformer/EfficientSAM

# TTS

+ [Text-to-Music is REAL with AudioCraft's Mind-Blowing AI Technology! - TUTORIAL](https://www.youtube.com/watch?v=YIjDYJQhIio&list=PLy2-ecgW7TY7OMOMEqSJY72vygltspO1_&index=4)
+ [github-audiocraft](https://github.com/facebookresearch/audiocraft)
+ [suno-tts: github-bark](https://github.com/suno-ai/bark)

# ootDiffusion

+ https://openart.ai/workflows/datou/ootdiffusion/8XE70w17xstgLBOCl4Bl

# realistic
## realisticSDXL
Stable Diffusion【真人模型】：美得令人心动亚洲女性大模型迎来SDXL版XXMix_9realisticSDXL: https://blog.csdn.net/libaiup/article/details/139318705

# 其他

## 模型
+ https://civitai.com/
+ https://www.bilibili.com/read/cv23887580/
+ https://huggingface.co/models?pipeline_tag=text-to-image&sort=trending&search=stable-diffusion

## works 
+ https://comfyanonymous.github.io/ComfyUI_examples/
+ https://comfyworkflows.com/
+ https://openart.ai/workflows

## prompt 
+ https://prompthero.com/midjourney-prompts

## 一些名词
+ SDXL
+ RAVE: https://rave-video.github.io/
+ animateDiff
  + https://www.youtube.com/watch?v=fxNqWTGh3ZM
  + https://www.youtube.com/watch?v=D3A6GeYq5LQ
  + https://heehel.com/aigc/comfyui-animationdiff.html
+ heygen: 数字人做的比较好的国外厂商/ ai avatar video
+ dreamTalk: github
+ wav2lip: github
+ sadTalk: github
+ tts
+ sag
+ controller
+ lora
+ sora
+ rag

# 一些问题
+ 看不到 workSpace  
customNodes => update workSpace
