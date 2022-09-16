-------------2022/9/16------------
新增logistics映射加密

运行方法：
　　　プログラム名　オリジナル画像  logistics映射のパラメタ　暗号化された画像の名前と　アーノルド変換のパラメタ
python chaosEncode.py originalImg.png 0.51 3.7 decoding.png 2 3 3

復号化（自動生成されたコマンドを実行してください）
python chaosEncode.py encoding.png 0.51 3.7 decoding.png 2 3 3 1920 1200



-------------------------------------

# Arnold变换

-----------------2022/6/2---------------

情報セキュリティシステム論の画像暗号化処理

---------9/19--------

更新加密次数（time），效果更好

高分辨率不推荐5次以上（执行时间会变长）

3次效果已经很好了


---------------------
使用方法

安装numpy， PIL库之后

运行Arnold.py 

确保文件根目录存在img文件夹，解密时存在key.ini

根据提示 选择加密（1）or解密（2）

加密：输入文件全路径--->输入a b time（中间空格）--->查看img文件夹

-------------
变换矩阵为
[[1,b],
[a,ab+1]]

逆矩阵为
[[ab+1,-b],
[-a, 1]]

-------------
解密：输入文件全路径--->确保存在key.ini--->查看img文件夹

-------------

原理：
加密：
根据图片信息使用黑色将文件补为正方形

使用上述矩阵进行变换之后转为加密图片，并将原图分辨率和加密（a b）写入key.ini

解密：

读取key.ini，使用逆矩阵变换回有黑色背景的正方形图片，根据文件中的分辨都再进行截取

