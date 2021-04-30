# 2021海华AI挑战赛复赛提交指南
 
比赛要求选手在"最终提交"页面上传**压缩为tar.gz格式的Docker镜像**. 这篇指南会一步步引导选手创建自己的Docker镜像.

## 准备工作

我们将使用Docker来封装选手的模型, 这样以便选手可以任选自己熟悉的编程语言和环境来复现自己的模型. 在 [这里](https://docs.docker.com/get-docker/) 查看如何在自己的系统里安装Docker.


## 测试样例提交

### 下载这个Git Repo

```
git clone https://github.com/biendata-com/haihua2021_sample.git
```

### 进入路径

```
cd haihua2021_sample
```

### Build Docker镜像

```
docker build -t sample_image .
```

_请注意命令最后的"." 意味着以当前所在路径build镜像. 这里应该与Dockerfile这个文件为同一个路径._

### 在本地测试镜像

可以尝试将验证集文件validation.json放在local_test/test_input路径下, 并且将"/path/to/cloned/repo"这部分替换成你的环境中的路径. 如果以下的docker run命令没有报错并成功在
local_test/test_output下生成了submission.csv文件, 说明镜像成功通过了测试.


```
docker run --rm -it \
 -v /path/to/cloned/repo/local_test/test_input:/data/input \
 -v /path/to/cloned/repo/local_test/test_output:/data/output \
 sample_image \
 -input /data/input/validation.json -output /data/output/submission.csv
```

## 创建自己的镜像



### 切换当前路径至你的项目路径

```
cd my_haihua_submission
```

### 创建一个main文件

main文件需要接收两个参数:

- `-input` 为包含路径的输入文件名,例如: /data/input/test.json
- `-output` 为包含路径的生成结果文件名,例如: /data/output/submission.csv

main文件需要完成的任务有:

1. 通过 `-input` 参数读取需要预测的文件.
2. 调用你的模型, 预测结果.
3. 将预测结果输出为 `-output` 参数所指定的文件. 结果文件格式跟初赛一致.

可以参考样例中的[`main.py`](main.py)作为main文件的例子. 你可以将random_result函数替换为调用你自己模型的代码.

### 创建Dockerfile

你可以参考样例中的[sample Dockerfile](Dockerfile), 注意需要将你所使用的库添加的requirements文件中. 另外, 如果你想使用自己创建的main文件的话, 需要在ENTRYPOINT中第二个参数替换成你自己的main文件. 你可以使用任何脚本程序来作为你的ENTRYPOINT, 例如如果你想使用shell脚本的话:

```
ENTRYPOINT ["bash","/path/to/your/main.sh"]
```

_如果你对Dockerfile的语法不熟悉或者想使用更多Dockerfile提供的功能, 请参考[official documentation](https://docs.docker.com/engine/reference/builder/)._

_TIPS: 如果想使用支持GPU的镜像, 最简单的办法是使用FROM语句引入一个nvidia cuda的docker镜像. 可以参考[nvidia/cuda](https://hub.docker.com/r/nvidia/cuda). 如果想使用更多的nvidia docker功能, 可以参考[nvidia-docker](https://github.com/NVIDIA/nvidia-docker)._
### 使用 [docker build](https://docs.docker.com/engine/reference/commandline/build/) 命令创建你的Docker镜像 

```
docker build -t your_image .
```

_类似的, 请注意命令最后的"." 意味着以当前所在路径build镜像. 这里应该与Dockerfile这个文件为同一个路径._

### 在本地测试你的镜像

#### 1. 创建镜像测试用文件夹, 注意这些文件夹应该在你的项目路径之外

```
mkdir local_test && cd local_test
```

#### 2. 在其中创建测试文件夹

```
mkdir test_input test_output
```

#### 3. 将验证集validation.json文件复制到 test_input 路径下

#### 4. 使用[docker run](https://docs.docker.com/engine/reference/run/)命令来测试你的镜像

注意请将下面命令中 "/path/to/test/dir" 替换为你的环境路径. 如果以下的docker run命令没有报错并成功在 local_test/test_output 下生成了submission.csv文件, 说明镜像成功通过了测试.

```
docker run --rm -it --gpus all \
 -v /path/to/test/dir/local_test/test_input:/data/input \
 -v /path/to/test/dir/local_test/test_output:/data/output \
 your_image \
 -input /data/input/validation.json -output /data/output/submission.csv
```

_以上docker run命令等于在你的容器中运行:_

```
python /app/main.py -input /data/input/validation.json -output /data/output/submission.csv
```

### 使用 [docker save](https://docs.docker.com/engine/reference/commandline/save/) 命令保存你的镜像并压缩为一个tar.gz文件

```
docker save your_image:latest | gzip > your_image.tar.gz
```

_之后可以将保存好的 `your_image.tar.gz` 文件在"最终提交"页面上传_
