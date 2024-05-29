# 在AutoDL平台部署


## 一、注册AutoDL

[AutoDL官网](https://www.autodl.com/home) 注册账户好并充值，自己选择机器，我觉得如果正常跑一下，5元已经够了

![注册AutoDL](https://pic1.zhimg.com/v2-f56bc692a0d22fb1ae749b7697ff5d0f.png)

## 二、创建实例

### 2.1 登录AutoDL，进入算力市场，选择机器

这一部分实际上我觉得12g都OK的，无非是速度问题而已

![选择RTX 3090机器](https://picx.zhimg.com/v2-824956d591eead5d3ed4de87c59258a6.png)



### 2.2 配置基础镜像

选择镜像，最好选择2.0以上可以体验克隆声音功能，其他无所谓

![配置基础镜像](https://pic1.zhimg.com/v2-8d064d809e15673dc6f2be8f2ef83ae7.png)



### 2.3 无卡模式开机

创建成功后为了省钱先关机，然后使用无卡模式开机。
无卡模式一个小时只需要0.1元，比较适合部署环境。

![无卡模式开机](https://picx.zhimg.com/v2-118eead549c35ad06d946b00cd93c668.png)

## 三、部署环境

### 3.1 进入终端

打开jupyterLab，进入数据盘（autodl-tmp），打开终端，将Linly-Talker模型下载到数据盘中。

![进入终端](https://pica.zhimg.com/v2-7c29a3f68c04b9af0963d4acaa63f59c.png)



### 3.2 下载代码文件

根据Github上的说明，使用命令行下载模型文件和代码文件，利用学术加速会快一点

```bash
# 开启学术镜像，更快的clone代码 参考 https://www.autodl.com/docs/network_turbo/
source /etc/network_turbo

cd /root/autodl-tmp/
# 下载代码
git clone https://github.com/Kedreamix/Linly-Talker.git

# 取消学术加速
unset http_proxy && unset https_proxy
```



### 3.3 下载模型文件

安装git lfs

```sh
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

![安装git lfs](https://pic1.zhimg.com/v2-084b5f048d1a70d8712bd6a6891c673c.png)

根据 [https://www.modelscope.cn/Kedreamix/Linly-Talker](https://www.modelscope.cn/Kedreamix/Linly-Talker) 下载模型文件，走modelscope还是很快的，不过文件有点多，还是得等一下，记住是在Edubot代码路径下执行这个文件

```bash
cd /root/autodl-tmp/Edubot/
git lfs install
git lfs clone https://github.com/caixukun-jinitaimei/Edubot.git
```

![下载模型文件](https://picx.zhimg.com/v2-1f61be9be69053ebe16c72762c350d18.png)

等待一段时间下载完以后，利用命令将模型移动到指定目录，直接复制即可

```bash
# 移动所有模型到当前目录
# checkpoint中含有SadTalker和Wav2Lip
mv Linly-Talker/checkpoints/* ./checkpoints

# SadTalker的增强GFPGAN
# pip install gfpgan
# mv Edubot/gfpan ./

# 语音克隆模型
mv Edubot/GPT_SoVITS/pretrained_models/* ./GPT_SoVITS/pretrained_models/

# Qwen大模型
mv Edubot/Qwen ./
```



## 四、Edubot项目

### 4.1 环境安装

进入代码路径，进行安装环境，由于选了镜像是含有pytorch的，所以只需要进行安装其他依赖即可

```bash
cd /root/autodl-tmp/Edubot

conda install -q ffmpeg # ffmpeg==4.2.2

# 安装Linly-Talker对应依赖
pip install -r requirements_app.txt

# 安装语音克隆对应的依赖
pip install -r VITS/requirements_gptsovits.txt
```



### 4.2 端口设置

由于似乎autodl开放的是6006端口，所以这里面的端口映射也可以改一下成6006，这里吗只需要修改configs.py文件里面的port为6006即可

![端口设置](https://picx.zhimg.com/v2-d9516998de3e6ffea282c4c6776c126f.png)

除此之外，我发现其实对于autodl来说，不是很支持https的端口映射，所以需要注释掉几行代码即可，在webui.py的最后几行注释掉代码ssl相关代码

```bash
    demo.launch(server_name="127.0.0.1", # 本地端口localhost:127.0.0.1 全局端口转发:"0.0.0.0"
                server_port=port,
                # 似乎在Gradio4.0以上版本可以不使用证书也可以进行麦克风对话
                # ssl_certfile=ssl_certfile,
                # ssl_keyfile=ssl_keyfile,
                # ssl_verify=False,
                debug=True,
                )
```

如果使用app.py同理

![http设置](https://picx.zhimg.com/v2-fd4aed3c765b8a4a425e12520a1461ae.png)

### 4.3 有卡开机

进入autodl容器实例界面，执行关机操作，然后进行有卡开机，开机后打开jupyterLab。

查看配置

```bash
nvidia-smi
```

![有卡开机](https://pic1.zhimg.com/v2-baff41e6634fd25fb5d39806b86b1c40.png)



### 4.4 运行网页版对话webui

需要有卡模式开机，执行下边命令，这里面就跟代码是一模一样的了

```bash
python webui.py
```

![运行网页版对话webui](https://pic1.zhimg.com/v2-c1c8a2653cef9d4b044fb85555411928.png)



### 4.4 端口映射

这可以直接打开autodl的自定义服务，默认是6006端口，我们已经设置了，所以直接使用即可

![端口映射](https://picx.zhimg.com/v2-19a51c44478a1fad9e0de593ee4d547f.png)



### 4.5 体验Edubot（成功）

点开网页，即可正确执行Edubot，这一部分就跟视频一模一样了

![体验Linly-Talker](https://picx.zhimg.com/v2-1b67099f2903fdcac732b784477851aa.png)





ssh端口映射工具：windows：[https://autodl-public.ks3-cn-beijing.ksyuncs.com/tool/AutoDL-SSH-Tools.zip](https://autodl-public.ks3-cn-beijing.ksyuncs.com/tool/AutoDL-SSH-Tools.zip)

**！！！注意：不用了，一定要去控制台=》容器实例，把镜像实例关机，它是按时收费的，不关机会一直扣费的。**

**建议选北京区的，稍微便宜一些。可以晚上部署，网速快，便宜的GPU也充足。白天部署，北京区的GPU容易没有。**
