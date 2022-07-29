import os
import rarfile
import tarfile as tf
import os
class Tgz:
    pass
    def maketgz(self,ofn, ifn):
        with tf.open(ofn, 'w:gz') as tar:
            tar.add(ifn, arcname=os.path.basename(ifn))
        return 1


if __name__ == '__main__':
    ifn = r'C:\cc\share\temp\760_ep'
    try:
        ifn = ifn.split(sep='"')[1]
        # print(ifn)
    except:
        pass
    ofn = ifn + '.tgz'
    if  Tgz().maketgz(ofn, ifn):
        print('压缩成功！')
