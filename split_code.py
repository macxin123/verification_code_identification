import os
import time
import random
import threading
import numpy as np
from PIL import Image, ImageFilter
from concurrent.futures import ThreadPoolExecutor


def image_clean(path):
    """
    清洗图片
    :param path: 图片路径
    :return img_end, filename: 清洗好的图片以及图片名称 
    """
    # 读取图片
    img = Image.open(path)

    # 将图片转换为灰度图
    img_l = img.convert('L')
    # 将灰度图转换为数组形式
    img_arr = np.array(img_l)
    # 求出该数组的平均值
    means = img_arr.mean() 
    # 调整平均值，作为清洗参数
    if means > 227:
        means = means + 30
    # print('means:', means) 
    
    # 清洗灰度图中的“雀斑”
    img_clean = img_l.point(lambda i: i>means-40, mode='1')
    # 使用中值滤波再次清洗
    img_end = img_clean.filter(ImageFilter.MedianFilter(size=3))
    # print(im_f.size) (160, 60)
    filename = img.filename.split('.')[1].rsplit('/')[-1]

    return img_end, filename


def split_image(img):
    """
    将验证码中的字符进行拆分
    :param img: 验证码图片对象
    :return real_letters: 图片分割坐标
    """
    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = list()
    # 遍历图片中的像素点，进行切割位置识别
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix = img.getpixel((x, y))
            if pix != 1:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = x
        if foundletter == True and inletter == False:
            foundletter = False
            end = x
            letters.append((start, end))
        inletter = False
    real_letters = list()
    # 切割后的图片宽度小于15，大概率为没有清洗好的像素点，所以直接舍弃
    for n in letters:
        if abs(n[0] - n[1]) > 15:
            real_letters.append(n)
    # 如果real_letters为3，代码有2个字符被分割到了一起
    if len(real_letters) == 3:
        res = max(real_letters, key=max_pro)
        res_index = real_letters.index(res)
        le = list()
        for i in range(4):
            if len(le) == 4:
                break
            if i == res_index:
                # 再次分割图片
                ca = round(abs(real_letters[i][1] - real_letters[i][0]) / 2)
                le.append((real_letters[i][0], real_letters[i][0] + ca))
                le.append((real_letters[i][0] + ca +1, real_letters[i][1]))
            else:
                le.append(real_letters[i])     
        real_letters = le
    # 如果real_letters为2，代码有3个字符被分割到了一起
    elif len(real_letters) == 2:
        res = max(real_letters, key=max_pro)
        res_index = real_letters.index(res)
        le = list()
        for i in range(4):
            if len(le) == 4:
                break
            if i == res_index:
                # 再次分割图片
                ca = round(abs(real_letters[i][1] - real_letters[i][0]) / 3)
                le.append((real_letters[i][0], real_letters[i][0] + ca))
                le.append((real_letters[i][0] + ca + 1, real_letters[i][0] + ca + ca))
                le.append((real_letters[i][0] + ca + ca +1, real_letters[i][1]))
            else:
                le.append(real_letters[i])     
        real_letters = le
    # 4为正确分割，此时什么都不用做
    elif len(real_letters) == 4:
        pass
    # 出现其他情况，则放弃该验证码
    else:
        return None
    
    return real_letters


def max_pro(x):
    """
    返回两点间的绝对值距离
    """
    return abs(x[0] - x[1])


def save_image(img, filename, letters):
    """
    :param img: 验证码图片对象
    :param filename: 验证码图片名称(真实值)
    :param letters: 图片分割坐标
    :return : None
    """
    for i, v in enumerate(letters):
        # 切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度
        img_split = img.crop((v[0], 0, v[1], img.size[1]))
        # 将图片size进行统一
        i_m_g = img_split.resize((40, 60), Image.ANTIALIAS)
        # windows文件夹名不区分大小写，所以文件夹名需要更改
        if filename[i].isupper():
            dir_name = filename[i] + '_Upper'
            i_m_g.save(f'./chars/{dir_name}/{filename[i] + str(random.randint(1, 999)) + str(time.time())[:8]}.jpg')
        else:
            i_m_g.save(f'./chars/{filename[i]}/{filename[i] + str(random.randint(1, 999)) + str(time.time())[-6:]}.jpg')


def make_dir():
    """
    创建程序需要的文件夹
    """
    # 分割验证码的文件夹
    os.makedirs('./chars/')
    # 小写字母列表
    word_lower_list = [chr(i) for i in range(97,123)]
    # 大写字母列表
    word_upper_list = [chr(i).upper() + '_Upper' for i in range(97,123)]
    # 数字列表
    num_list = [str(i) for i in range(10)]
    # 验证码内容：大小写字母+数字
    yzm_list = [yzm for yzm in word_lower_list + word_upper_list + num_list]
    # 创建字符列表中的文件夹
    for i in yzm_list:
        os.makedirs('./chars/' + i)


def run(path):
    """
    线程任务函数
    """
    img, filename = image_clean(path)
    letters = split_image(img)
    if letters is None:
        pass
    else:
        save_image(img, filename, letters)
        print(f'{threading.current_thread().name}:分割{filename}完成!!!')


def main():
    """
    主函数
    """
    img_list = os.listdir('./imgs/')
    for i in img_list: 
        path = './imgs/' + i 
        # 线程任务
        thread_pool.submit(run, path)


if __name__ == '__main__':
    # 创建线程池
    thread_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="task")
    # 创建需要的文件夹
    make_dir()
    start = time.time()
    # 运行主函数
    main()
    # 阻塞任务
    thread_pool.shutdown(wait=True)
    end = time.time()
    print(f'用时：{round(end - start)}秒！')
    
    