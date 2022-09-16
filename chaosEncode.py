import sys
from pathlib import Path
from PIL import Image
import numpy as np


def arnoldEncode(Matrix, a, b, time):
    h, w = Matrix.shape[0], Matrix.shape[1]
    zeroMatrix = np.zeros(shape=Matrix.shape)
    for i in range(time):
        for x in range(h):
            for y in range(w):
                newX = (1 * x + b * y) % h
                newY = (a * x + (a * b + 1) * y) % h
                zeroMatrix[newX, newY, :] = Matrix[x, y, :]
        Matrix = zeroMatrix.copy()
    return Image.fromarray(Matrix.astype('uint8'))


def arnoldDecode(Matrix, a, b, time):
    h, w = Matrix.shape[0], Matrix.shape[1]
    zeroMatrix = np.zeros(shape=Matrix.shape)
    for i in range(time):
        for x in range(h):
            for y in range(w):
                newX = ((a * b + 1) * x + (-b) * y) % h
                newY = ((-a) * x + y) % h
                zeroMatrix[newX, newY, :] = Matrix[x, y, :]
        Matrix = zeroMatrix.copy()
    return Image.fromarray(Matrix.astype('uint8'))


def fillBlack(path):
    image = Image.open(path)
    image = image.convert('RGBA')
    w, h = image.size
    background = Image.new('RGBA', size=(max(w, h), max(w, h)), color=(0, 0, 0))
    box = (0, 0)  # 粘贴的位置
    background.paste(image, box)
    Path('pwd1.txt').write_text(
        f'python chaosEncode.py {sys.argv[4]} {sys.argv[2]} {sys.argv[3]} decoding.png {sys.argv[5]} {sys.argv[6]} {sys.argv[7]} {w} {h}')
    return background


def cutBlack(img, w, h):
    img.crop((0, 0, int(w), int(h))).save(sys.argv[4])


def logicEncrypt(img, x0, mu):
    xsize, ysize = img.size
    print(img.size)
    img = np.array(img).flatten()
    num = len(img)
    for i in range(100):
        x0 = mu * x0 * (1 - x0)
    E = np.zeros(num)
    E[0] = x0
    for i in range(0, num - 1):
        E[i + 1] = mu * E[i] * (1 - E[i])
    E = np.round(E * 255).astype(np.uint8)
    img = np.bitwise_xor(E, img)
    img = img.reshape(xsize, ysize, -1)
    img = np.squeeze(img)
    img = Image.fromarray(img)
    return img


if __name__ == '__main__':
    if len(sys.argv) == 8:
        imgM = np.asarray(fillBlack(sys.argv[1]))
        img = arnoldEncode(imgM, int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        imgEncode = logicEncrypt(img, float(sys.argv[2]), float(sys.argv[3]))
        imgEncode.save(sys.argv[4])
    elif len(sys.argv) == 10:
        img = Image.open(sys.argv[1])
        imgP = logicEncrypt(img, float(sys.argv[2]), float(sys.argv[3]))
        imgDecode = arnoldDecode(np.asarray(imgP), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        cutBlack(imgDecode, sys.argv[8], sys.argv[9])
    else:
        print('解谜：请依次输入 图片路径 x0 mu 新命名 a b time w h')
        print('加密：请依次输入 图片路径 x0 mu 新命名 a b time')
        sys.exit(0)
