## 量化交易辅助决策平台后端

推荐使用anaconda

### 创建环境

conda create -n stock python=3.10.0

### 激活环境

conda activate stock

## 安装依赖

pip install django

pip install django-cors-headers

pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

下面的是计算macd需要的库

pip install TA-Lib

**TA-Lib这东西在windows上不好装，如果安装失败，在下方链接下载whl，手动pip安装**

https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

**TA-Lib这东西在mac上也不好装，如果安装失败，尝试如下命令**

conda install -c conda-forge ta-lib

### 运行服务

python manage.py runserver