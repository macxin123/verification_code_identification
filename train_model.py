import os
import joblib
import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def data():
    """
    将所有的图片数据进行数据集划分
    :return x_list, y_list: 样本特征集, 样本标签
    """
    x_list = list()
    path = './chars/'
    dir_list = os.listdir(path)
    y_list = list()
    for p in dir_list:
        dir_path = path + p + '/'
        lst = os.listdir(dir_path)
        for jpg in lst:
            img = Image.open(dir_path + jpg)
            filename = img.filename.rsplit('/')[-1].split('.')[0][0]
            y_list.append(list(filename))
            img_arr = np.array(img).tolist()
            xx = list()
            for arr in img_arr:
                for a in arr:
                    xx.append(a)
            x_list.append(xx)

    return x_list, y_list


def main():
    """
    主函数
    """
    x_list, y_list = data()
    # 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(x_list, y_list, test_size=0.3, random_state=42)
    # 实例化knn算法模型
    knn = KNeighborsClassifier()
    # 训练数据
    knn.fit(x_train, y_train)
    # 测试准确率
    score = knn.score(x_test, y_test)
    print(f'准确率为：{score}')
    # 生成本地模型
    joblib.dump(knn, './knn_model.pkl')


if __name__ == '__main__':
    main()
    