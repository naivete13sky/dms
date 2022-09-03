import os
import rarfile
import tarfile as tf
import os
from django.apps import apps


class Tgz:
    pass
    def maketgz(self,ofn, ifn):
        with tf.open(ofn, 'w:gz') as tar:
            tar.add(ifn, arcname=os.path.basename(ifn))
        return 1


class DjangoMethod:

    def getmodelfield(self,appname, modelname, exclude):
        """
        获取model的verbose_name和name的字段
        """
        modelobj = apps.get_model(appname, modelname)
        filed = modelobj._meta.fields
        print(filed)
        fielddic = {}

        params = [f for f in filed if f.name not in exclude]

        for i in params:
            fielddic[i.name] = i.verbose_name
        return fielddic





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
