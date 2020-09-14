import joblib
import numpy as np
from PIL import Image
from split_code import image_clean, split_image


def read_img():
    """
    将分割好的验证码数值化
    :return x_list: 数值化的验证码
    """
    x_list = list()
    for i in range(4):
        img = Image.open(f'./test/{str(i)}.jpg')
        img_arr = np.array(img).tolist()
        xx = list()
        for arr in img_arr:
            for a in arr:
                xx.append(a)
        x_list.append(xx)

    return x_list


def image_save(img, letters):
    """
    :param img: 验证码图片对象
    :param letters: 图片分割坐标
    :return : True/False
    """
    try:
        for i, v in enumerate(letters):
            # 切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度
            img_split = img.crop((v[0], 0, v[1], img.size[1]))
            # 将图片size进行统一
            i_m_g = img_split.resize((40, 60), Image.ANTIALIAS)
            i_m_g.save(f'./test/{i}.jpg')
    except Exception as e:
        print(f'错误信息:{str(e)}')
        return False

    return True


def yzm_api(path):
    """
    api函数，验证码识别
    :param path: 验证码图片路径
    :return : None
    """
    model = joblib.load('./knn_model.pkl')
    img, filename = image_clean(path)
    letters = split_image(img)
    if letters is None:
        print('该验证码似乎有些难度，无法读取......')
    else:
        res = image_save(img, letters)
        if res:
            x_list = read_img()
            result = model.predict(x_list)
            print('预测结果：', result)
        else:
            print('对不起，似乎遇上了一些未知的错误......')


if __name__ == '__main__':
    yzm_api('../yzm/acF3.jpg')