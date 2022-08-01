import sys
import json
from time import sleep
import pytest
from os.path import dirname, abspath
import os,sys,json,shutil
path = os.path.dirname(os.path.realpath(__file__)) + r'/epcam'
sys.path.append(path)
import epcam
import epcam_api
import job_operation
import layer_info
import re
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
import gl as gl
from job_manage import models

class EpGerberToODB:
    pass

    def is_chinese(self,string):
        """判断是否有中文
        :param     string(str):所有字符串
        :returns   :False
        :raises    error:
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


    def Traverse_Gerber(self,job, step, file_path, index):
        """转换Gerber文件
        :param     job(str):job名
        :param     step(str):step名
        :param     file_path(str):文件路径
        :param     index(int):序号
        :returns   :None
        :raises    error:
        """
        for root, dirs, files in os.walk(file_path):
            epcam_api.file_translate_init(job)
            for file in files:
                if self.is_chinese(file):
                    os.rename(file_path + r'/' + file, file_path + r'/''unknow' + str(index))
                    file = 'unknow' + str(index)
                    index = index + 1
                ret = epcam_api.file_identify(os.path.join(root, file))
                data = json.loads(ret)
                file_format = data['paras']['format']
                file_param = data['paras']['parameters']
                # file_param = {'Coordinates':'Absolute',
                #               'Decimal_numbers':True,
                #               'Number_format_integer':2,
                #               'Number_format_decimal':4,
                #               'data_type':'Ascii',
                #               'file_size':1391.0,
                #               'format':'Excellon2',
                #               'separator_char':'nl',
                #               'text_line_width':0.0,
                #               'tool_units':'Inch',
                #               'units':'Inch',
                #               'zeroes_omitted':'Leading'}
                if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
                    print(file)
                    re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '',
                                                  [])  # translate
            for dir_name in dirs:
                self.Traverse_Gerber(job, step, os.path.join(root, dir_name), index)

    def Traverse_Gerber2(self,job, step, file_path, index,job_id):
        # print("*"*30,job_id)
        job_current = models.Job.objects.get(id=job_id)
        layer_all = models.Layer.objects.filter(job=job_current)
        # print(layer_all)

        """转换Gerber文件
        :param     job(str):job名
        :param     step(str):step名
        :param     file_path(str):文件路径
        :param     index(int):序号
        :returns   :None
        :raises    error:
        """
        for root, dirs, files in os.walk(file_path):
            epcam_api.file_translate_init(job)
            for file in files:
                if self.is_chinese(file):
                    os.rename(file_path + r'/' + file, file_path + r'/''unknow' + str(index))
                    file = 'unknow' + str(index)
                    index = index + 1
                ret = epcam_api.file_identify(os.path.join(root, file))
                data = json.loads(ret)
                file_format = data['paras']['format']
                file_param = data['paras']['parameters']
                # file_param = {'Coordinates':'Absolute',
                #               'Decimal_numbers':True,
                #               'Number_format_integer':2,
                #               'Number_format_decimal':4,
                #               'data_type':'Ascii',
                #               'file_size':1391.0,
                #               'format':'Excellon2',
                #               'separator_char':'nl',
                #               'text_line_width':0.0,
                #               'tool_units':'Inch',
                #               'units':'Inch',
                #               'zeroes_omitted':'Leading'}



                if file_format == 'Excellon2':
                    print(file)
                    try:
                        layer_e2= models.Layer.objects.get(job=job_current,layer=file)
                        # print(layer_e2.layer)
                        # print(file_param)
                        file_param['units']=layer_e2.drill_excellon2_units
                        file_param['zeroes_omitted'] = layer_e2.drill_excellon2_zeroes_omitted
                        file_param['Number_format_integer'] = layer_e2.drill_excellon2_number_format_A
                        file_param['Number_format_decimal'] = layer_e2.drill_excellon2_number_format_B
                        file_param['tool_units'] = layer_e2.drill_excellon2_tool_units
                        print(file_param)
                    except:
                        re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '',
                                                  [])

                # if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
                #     print(file)
                #     re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '',
                #                                   [])  # translate


    def ep_gerber_to_odb(self,job, step, file_path, out_path):
        """Gerber转ODB
        :param     job(str):job名
        :param     step(str):step名
        :param     file_path(str):gerber文件夹路径
        :param     out_path:输出odb路径
        :returns   :None
        :raises    error:
        """
        # epcam.init()
        new_job_path = os.path.join(out_path, job)  # job若存在则删除
        if os.path.exists(new_job_path):
            shutil.rmtree(new_job_path)
        epcam_api.create_job(out_path, job)
        job_operation.open_job(out_path, job)
        job_operation.create_step(job, step)
        job_operation.save_job(job)
        index = 1
        self.Traverse_Gerber(job, step, file_path, index)
        job_operation.save_job(job)
        all_layer = layer_info.get_all_layer_name(job)  # 获得料号下所有layer
        gl.all_layer=all_layer


    def ep_vs(self,job, step, file_path, out_path):
        pass
        # 比对
        tol = 0.9 * 25400
        isGlobal = True
        consider_sr = True
        map_layer_res = 200 * 25400
        all_result = {}  # 存放所有层比对结果
        all_layer=gl.all_layer
        for layer in all_layer:
            layer_result = epcam_api.layer_compare_point(job, step, layer, job, step, layer, tol, isGlobal, consider_sr,
                                                         map_layer_res)
            all_result[layer] = layer_result
        print("*" * 100)
        print(all_result)
        print("*" * 100)

    def ep_gerber_to_odb2(self,job, step, file_path, out_path,job_id):
        """Gerber转ODB
        :param     job(str):job名
        :param     step(str):step名
        :param     file_path(str):gerber文件夹路径
        :param     out_path:输出odb路径
        :returns   :None
        :raises    error:
        """
        # epcam.init()
        new_job_path = os.path.join(out_path, job)  # job若存在则删除
        if os.path.exists(new_job_path):
            shutil.rmtree(new_job_path)
        epcam_api.create_job(out_path, job)
        job_operation.open_job(out_path, job)
        job_operation.create_step(job, step)
        job_operation.save_job(job)
        index = 1
        self.Traverse_Gerber2(job, step, file_path, index,job_id)
        job_operation.save_job(job)
        all_layer = layer_info.get_all_layer_name(job)  # 获得料号下所有layer
        gl.all_layer=all_layer


if __name__ == "__main__":
    pass
    epcam.init()
    job = 'test1'
    step = 'orig'
    file_path = r'C:\job\test\gerber\760'
    out_path = r'C:\job\test\odb'
    cc=EpGerberToODB()
    cc.ep_gerber_to_odb(job, step, file_path, out_path)