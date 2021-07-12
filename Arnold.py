from pathlib import Path
from PIL import Image
import configparser
import numpy as np

config = configparser.ConfigParser()


# Methods
# [[1,b],
# [a,ab+1]]
#
# [[ab+1,-b],
# [-a, 1]]


# 图片转化为数组
def loadImage(path: str):
    img = Image.open(path)
    return np.array(img)


# 数组转化为图片
def toImage(Matrix, name):
    img = Image.fromarray(Matrix)
    img.save(name)


def arnoldEncode(Matrix, a, b):
    config.add_section('password')
    config.set('password', 'a', str(a))
    config.set('password', 'b', str(b))
    config.write(open("key.ini", "w"))
    h, w = Matrix.shape[0], Matrix.shape[1]
    zeroMatrix = np.zeros(shape=Matrix.shape)
    for x in range(h):
        for y in range(w):
            newX = (1 * x + b * y) % h
            newY = (a * x + (a * b + 1) * y) % h
            zeroMatrix[newX, newY, :] = Matrix[x, y, :]

    return zeroMatrix


def arnoldDecode(Matrix, a=None, b=None):
    h, w = Matrix.shape[0], Matrix.shape[1]
    zeroMatrix = np.zeros(shape=Matrix.shape)
    config.read('key.ini')
    a = int(config.get('password', 'a'))
    b = int(config.get('password', 'b'))
    for x in range(h):
        for y in range(w):
            newX = ((a * b + 1) * x + (-b) * y) % h
            newY = ((-a) * x + y) % h
            zeroMatrix[newX, newY, :] = Matrix[x, y, :]

    return zeroMatrix


def fillBlack(path):
    image = Image.open(path)
    image = image.convert('RGB')
    w, h = image.size
    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(0, 0, 0))
    length = int(abs(w - h))
    box = (0, 0)  # 粘贴的位置
    background.paste(image, box)
    config.add_section('image')
    config.set('image', 'w', str(w))
    config.set('image', 'h', str(h))
    config.write(open("key.ini", "w"))
    background.save('img/background.png')


def cutBlack():
    config.read('key.ini')
    w = config.get('image', 'w')
    h = config.get('image', 'h')
    img = Image.open('img/originalBlack.png')
    img.crop((0, 0, int(w), int(h))).save('img/original.png')


if __name__ == '__main__':
    print('请确保同目录下存在key.ini文件')
    useMethod = int(input('加密（1）/解密（2）：'))
    if useMethod == 1:
        path = input('请输入文件路径：')
        a, b = map(int, input('输入加密key：a,b（空格隔开）:').split())
        fillBlack(path)
        toImage(arnoldEncode(loadImage('img/background.png'), a, b).astype('uint8'), 'img/encode.png')
    elif useMethod == 2:
        path = input('请输入文件路径：')
        toImage(arnoldDecode(loadImage(path)).astype('uint8'), 'img/originalBlack.png')
        cutBlack()
    else:
        print('我看你是在难为我胖虎')
