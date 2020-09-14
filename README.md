# verification_code_identification
基于机器学习算法的验证码识别脚本

## imgs 文件夹

存放生成的验证码图片

## chars文件夹

存放分割后的验证码图片，以作为训练集数据使用

## test 文件夹

存放api临时生成的图片内容

## api.py

已经完成的验证码识别脚本接口，调用`api.yzm_api('验证码图片路径')`即可使用，也可以在代码中添加图片路径，直接运行

## make_code.py

用于生成图片验证码，直接运行即可，可在命令行中输入需要生成的验证码数量

## split_code.py

用于将`make_code.py`生成的验证码图片进行清洗与分割

## train_model.py

将`split_code.py`生成的数据集数值化，并使用了knn算法进行了模型训练

## knn_model.pkl

由`train_model.py`生成的knn模型

