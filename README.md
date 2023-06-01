# Kohya-Atelier

## Introduction

为了大量训练不同参数下的LoRA模型,我编写一个简单的脚本以实现这个需求. 该项目基于Kohya-ss的Sd-scripts项目. 本人使用该脚本测试了大概20多组实验,跑了大概一天多,得到了200多个LoRA模型,然后通过Automatic1111的WEBUI批量测试,从而让自己能快速对所有参数有个直观的理解.

EN:

In order to train a large number of LoRA models with different parameters at one time, I wrote a simple script to achieve this requirement. This project is based on the Sd-scripts project by Kohya-ss. I used this script to test about 20 sets of experiments, ran it for more than a day, obtained more than 200 LoRA models, and then tested them in batch through the WEBUI of Automatic1111, allowing me to quickly have an intuitive understanding of all parameters.

## Features

- 可以同时设定大量参数,类似不同的预训练模型,不同的dim size,不同的alpha等等,只要是kohay-ss的训练脚本的参数都可以自由设定,然后一键训练所有参数. 
- 保存所有单个训练实验的启动命令和配置,以便更好的复现实验和单个实验的调试
- 调试模式,通过设置max_train_steps=2,此模式下可以快速测试所有配置是否存在bug,通过测试则可保证训练程序能正常运行,不会因为参数设置错误而导致训练失败.

EN:

- You can set a large number of parameters at the same time, such as different pre-trained models, different dim sizes, different alphas, etc. As long as they are parameters of the kohay-ss training script, they can be freely set, and all parameters can be trained with one click.
- Save the startup commands and configurations of all individual training experiments for better reproducibility of experiments and debugging of individual experiments.
- Debug mode: by setting max_train_steps=2, this mode can quickly test whether all configurations have bugs. If the test passes, it can ensure that the training program can run normally and will not fail due to incorrect parameter settings.

## Concepts

- Recipes: 针对一个数据集的配方,包含所有实验集合
- Exp: 某个实验,例如不同的底模,不同的dim size,不同的alpha等等
- Config: 单次训练的配置,可以认为是一次kohay-ss的训练脚本的参数

EN:

- Recipes: A recipe for a dataset, including all experiment sets.
- Exp: A specific experiment, such as different base models, different dim sizes, different alphas, etc.
- Config: The configuration for a single training, which can be regarded as the parameters of a kohay-ss training script.

## Reference

- [Kohya-ss/Sd-scripts](https://github.com/kohya-ss/sd-scripts)
- [Automatic1111/webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)