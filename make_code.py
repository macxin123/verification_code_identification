import os
import time
import threading
from random import randint
from concurrent.futures import ThreadPoolExecutor
from captcha.image import ImageCaptcha


def make_code(chars):
    """
    生成验证码图片，图片名为:验证码内容.jpg
    :param chars: 验证码内容
    :return: None
    """
    image = ImageCaptcha().generate_image(chars)
    # 验证码图片保存到./imgs/文件夹下
    filename = './imgs/' + chars + '.jpg'
    image.save(filename)
    print(f'{threading.current_thread().name}_done:{filename}')


def main(num, digit=4):
    """
    主函数
    :param num: 需要生成的验证码数量
    :param digit: 验证码的位数，默认为4位验证码
    :return: None
    """
    # 小写字母列表
    word_lower_list = [chr(i) for i in range(97,123)]
    # 大写字母列表
    word_upper_list = [chr(i).upper() for i in range(97,123)]
    # 数字列表
    num_list = [str(i) for i in range(10)]
    # 验证码内容：大小写字母+数字
    yzm_list = [yzm for yzm in word_lower_list + word_upper_list + num_list]

    # 若不存在./imgs/文件夹则新建
    if not os.path.exists('./imgs/'):
        os.makedirs('./imgs/')

    for n in range(int(num)):
        chars = ''
        # 随机生成验证码内容
        for i in range(digit):
            chars += yzm_list[randint(0, 61)]
        # 线程任务
        thread_pool.submit(make_code, chars)


if __name__ == '__main__':
    # 创建线程池
    thread_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="task")
    yzm_num = input('请输入您要生成的多少验证码：')
    start = time.time()
    # 运行主函数
    main(yzm_num)
    # 阻塞任务
    thread_pool.shutdown(wait=True)
    end = time.time()
    print(f'完成任务！用时：{round(end - start)}秒！')
    