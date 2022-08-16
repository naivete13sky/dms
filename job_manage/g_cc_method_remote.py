#coding=utf-8

import os,shutil
import sys
import json
import subprocess
import time
import linecache
import gl as gl
from job_manage import job_operation

LAYER_COMPARE_JSON = 'layer_compare.json'
# from job_manage import models

class Asw():
    def __init__(self,gateway_path):
        # gateway_path=os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")),"method\g\gateway.exe")
        self.gateway_path=gateway_path
        # print(gateway_path)
        command = '{} 1'.format(self.gateway_path)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    def __del__(self):
        os.system('taskkill /f /im gateway.exe')

    def exec_cmd(self, cmd):
        self.process.stdin.write((cmd + '\n').encode())
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        print(line)
        ret = int(line.decode().strip())
        # print("*"*100,ret)
        return ret
        
    def layer_compare_g1(self, paras, _type):
        print("*" * 100)
        result=""
        try:
            jobpath1 = paras['jobpath1']
            job_name_1=jobpath1.split("\\")[-1]
            step1 = paras['step1']
            #layer1 = paras['layer1']
            jobpath2 = paras['jobpath2']
            step2 = paras['step2']
            #layer2 = paras['layer2']
            #layer2_ext = paras['layer2_ext']
            tol = paras['tol']
            #map_layer = paras['map_layer']
            #map_layer_res = paras['map_layer_res']            
        except Exception as e:
            print(e)
            print("*"*100)
            return result

        if not os.path.exists(jobpath1):
            print('{} does not exist'.format(jobpath1))
            return result
        if not os.path.exists(jobpath2):
            print('{} does not exist'.format(jobpath2))
            return result

        job1 = os.path.basename(jobpath1)
        job2 = os.path.basename(jobpath2)
        layer_cp = ''
        # print('COM compare_layers,layer1={},job2={},step2={},layer2={},layer2_ext={},tol={},area=global,consider_sr=yes,ignore_attr=,map_layer={},map_layer_res={}'.format(
        #         layer1, job2, step2, layer2, layer2_ext, tol, map_layer, map_layer_res))
        cmd_list1 = []
        if _type == 0:
            cmd_list1 = [
                'COM import_job,db=genesis,path={},name={},analyze_surfaces=no'.format(jobpath1, job1),
                'COM import_job,db=genesis,path={},name={},analyze_surfaces=no'.format(jobpath2, job2),
                'COM check_inout,mode=out,type=job,job={}'.format(job1),
                'COM clipb_open_job,job={},update_clipboard=view_job'.format(job1),
                'COM open_job,job={}'.format(job1),
                'COM open_entity,job={},type=step,name={},iconic=no'.format(job1, step1),
                'COM units,type=inch',
                'COM open_job,job={}'.format(job2)
            ]
            cmd_list2 = [
                # 'COM editor_page_close',
                # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
                # 'COM close_job,job={}'.format(job1),
                # 'COM close_form,job={}'.format(job1),
                # 'COM close_flow,job={}'.format(job1),
                # 'COM delete_entity,job=,type=job,name={}'.format(job1),
                # 'COM close_form,job={}'.format(job1),
                # 'COM close_flow,job={}'.format(job1),
                # # 'COM close_job,job={}'.format(job2),
                # # 'COM close_form,job={}'.format(job2),
                # # 'COM close_flow,job={}'.format(job2),
                # 'COM delete_entity,job=,type=job,name={}'.format(job2),
                # 'COM close_form,job={}'.format(job2),
                # 'COM close_flow,job={}'.format(job2)
            ]
        elif _type == 1:
            layer1 = paras['layer1']
            layer2 = paras['layer2']
            map_layer = paras['map_layer']
            layer2_ext = paras["layer2_ext"]
            map_layer_res = paras['map_layer_res']
            layer_cp = layer2 + layer2_ext
            cmd_list1 = [
                'COM compare_layers,layer1={},job2={},step2={},layer2={},layer2_ext={},tol={},area=global,consider_sr=yes,ignore_attr=,map_layer={},map_layer_res={}'.format(
                    layer1, job2, step2, layer2, layer2_ext, tol, map_layer, map_layer_res)
            ]
            cmd_list2 = [
            ]
        else:
            cmd_list1 = [
                'COM save_job,job={},override=no'.format(job1),
                'COM editor_page_close',
                'COM check_inout,mode=out,type=job,job={}'.format(job1),
                'COM close_job,job={}'.format(job1),
                'COM close_form,job={}'.format(job1),
                'COM close_flow,job={}'.format(job1),
                'COM close_job,job={}'.format(job2),
                'COM close_form,job={}'.format(job2),
                'COM close_flow,job={}'.format(job2)
            ]
            cmd_list2 = [
            ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            if ret != 0:
                print('inner error')
                return result

        time.sleep(1)
        # features=(r"C:\genesis\fw\jobs\{}\steps\{}\layers\diff\features".format(job_name_1,step1))
        # features_Z = (r"C:\genesis\fw\jobs\{}\steps\{}\layers\diff\features.Z".format(job_name_1, step1))
        # print(features,"\n",features_Z)
        # if os.path.isfile(features_Z):
        #     pass
        #     compress=Compress()
        #     compress.uncompress_z(features_Z)


        # try:
        #     f=open(features,"r")
        # except Exception as e:
        #     print("未能比对！！！请重新执行比对！！！")
        #     result="未比对"
        #     for cmd in cmd_list2:
        #         self.exec_cmd(cmd)
        #     return result


        # shutil.copytree(r"C:\genesis\fw\jobs\{}".format(job_name_1),r"C:\cc\jobs\{}".format(job_name_1))
        # time.sleep(15)
        if _type == 1:
            # with open(features,"r") as f:
            #     s=f.readlines()
            #     print(s[3])
            # if "r0" in s[3]:
            #     print("比对发现有差异！！！！！！")
            #     result = "错误"
            # else:
            #     print("恭喜！比对通过！！！")
            #     result = "正常"

            diff = False
            # asw_dir = "C:/genesis"
            # matrix_path = os.path.join(asw_dir, 'fw/jobs/{}/matrix/matrix'.format(job1))
            matrix_path=r'C:\genesis\fw\jobs\{}\matrix\matrix'.format(job1)
            with open(matrix_path, 'r') as f:
                for var in f.readlines():
                    line = var.strip()
                    if len(line) == 0:
                        continue
                    attr = line.split('=')
                    if len(attr) == 2:
                        # print(attr)
                        if attr[0] == 'NAME' and attr[1].lower() == layer_cp:
                            diff = True
                            break
            if diff == True:
                print('Difference were found')
                result = "错误"
            else:
                print('Layers Match')
                result = "正常"
            for cmd in cmd_list2:
                self.exec_cmd(cmd)
        return result

    def import_odb_folder(self, jobpath):
        print("*" * 100,"import job")
        results=[]
        self.jobpath = jobpath
        if not os.path.exists(self.jobpath):
            print('{} does not exist'.format(self.jobpath))
            results.append('{} does not exist'.format(self.jobpath))
            return results
        job = os.path.basename(self.jobpath)
        cmd_list1 = [
            'COM import_job,db=genesis,path={},name={},analyze_surfaces=no'.format(jobpath, job),

        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            results=results.append(ret)
            if ret != 0:
                print('inner error')
                return results

        return results

    def layer_compare_g_open_2_job(self, jobpath1,step1,layer1,jobpath2,step2,layer2,layer2_ext,tol,map_layer,map_layer_res):
        print("*" * 100,"comare_open_2_job")
        results=[]
        try:
            self.jobpath1 = jobpath1
            # self.job_name_1=self.jobpath1.split("\\")[-1]
            self.step1 = step1
            self.layer1 = layer1
            self.jobpath2 = jobpath2
            self.step2 = step2
            self.layer2 = layer2
            self.layer2_ext = layer2_ext
            self.tol = tol
            self.map_layer = map_layer
            self.map_layer_res = map_layer_res
        except Exception as e:
            print(e)
            print("*"*100)
            return results

        job1 = os.path.basename(self.jobpath1)
        job2 = os.path.basename(self.jobpath2)
        layer_cp = layer2 + layer2_ext


        cmd_list1 = [
            'COM check_inout,mode=out,type=job,job={}'.format(job1),
            'COM clipb_open_job,job={},update_clipboard=view_job'.format(job1),
            'COM open_job,job={}'.format(job1),
            'COM open_entity,job={},type=step,name={},iconic=no'.format(job1, step1),
            'COM units,type=inch',
            'COM open_job,job={}'.format(job2),
            # 'COM compare_layers,layer1={},job2={},step2={},layer2={},layer2_ext={},tol={},area=global,consider_sr=yes,ignore_attr=,map_layer={},map_layer_res={}'.format(
            #     layer1, job2, step2, layer2, layer2_ext, tol, map_layer, map_layer_res),

            # 'COM save_job,job={},override=no'.format(job1),
            # 'COM editor_page_close',
            # 'COM check_inout,mode=out,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            #
            # 'COM close_job,job={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)

        ]

        cmd_list2 = [
            # 'COM editor_page_close',
            # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # 'COM delete_entity,job=,type=job,name={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # # 'COM close_job,job={}'.format(job2),
            # # 'COM close_form,job={}'.format(job2),
            # # 'COM close_flow,job={}'.format(job2),
            # 'COM delete_entity,job=,type=job,name={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)
        ]


        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            results.append(ret)
            if ret != 0:
                print('inner error')
                return results

    def layer_compare_do_compare(self, jobpath1,step1,layer1,jobpath2,step2,layer2,layer2_ext,tol,map_layer,map_layer_res):
        print("*" * 100, "do_comare")
        results = []
        try:
            self.jobpath1 = jobpath1
            # self.job_name_1=self.jobpath1.split("\\")[-1]
            self.step1 = step1
            self.layer1 = layer1
            self.jobpath2 = jobpath2
            self.step2 = step2
            self.layer2 = layer2
            self.layer2_ext = layer2_ext
            self.tol = tol
            self.map_layer = map_layer
            self.map_layer_res = map_layer_res
        except Exception as e:
            print(e)
            print("*" * 100)
            return results

        self.job1 = os.path.basename(jobpath1)
        self.job2 = os.path.basename(jobpath2)
        layer_cp = layer2 + layer2_ext

        cmd_list1 = [
            'COM compare_layers,layer1={},job2={},step2={},layer2={},layer2_ext={},tol={},area=global,consider_sr=yes,ignore_attr=,map_layer={},map_layer_res={}'.format(
                self.layer1, self.job2, self.step2, self.layer2, self.layer2_ext, self.tol, self.map_layer, self.map_layer_res),

            'COM save_job,job={},override=no'.format(job1),
            # 'COM editor_page_close',
            # 'COM check_inout,mode=out,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            #
            # 'COM close_job,job={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)

        ]

        cmd_list2 = [
            # 'COM editor_page_close',
            # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # 'COM delete_entity,job=,type=job,name={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # # 'COM close_job,job={}'.format(job2),
            # # 'COM close_form,job={}'.format(job2),
            # # 'COM close_flow,job={}'.format(job2),
            # 'COM delete_entity,job=,type=job,name={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)
        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            if ret != 0:
                print('inner error')
                return results

        time.sleep(1)

    def layer_compare_analysis(self, jobpath1,step1,layer1,jobpath2,step2,layer2,layer2_ext,tol,map_layer,map_layer_res):
        print("*" * 100, "comare")
        results = []
        try:
            self.jobpath1 = jobpath1
            # self.job_name_1=self.jobpath1.split("\\")[-1]
            self.step1 = step1
            self.layer1 = layer1
            self.jobpath2 = jobpath2
            self.step2 = step2
            self.layer2 = layer2
            self.layer2_ext = layer2_ext
            self.tol = tol
            self.map_layer = map_layer
            self.map_layer_res = map_layer_res
        except Exception as e:
            print(e)
            print("*" * 100)
            return results

        job1 = os.path.basename(jobpath1)
        job2 = os.path.basename(jobpath2)
        layer_cp = layer2 + layer2_ext

        #解压tgz
        temp_path=r'C:\cc\share\temp'
        job_operation.untgz(os.path.join(temp_path, '760_ep.tgz'),temp_path)
        # if os.path.exists(os.path.join(temp_path, str(job.file_odb_g).split('/')[-1])):
        #     os.remove(os.path.join(temp_g_path, str(job.file_odb_g).split('/')[-1]))
        # print("g_tgz_file_now:", os.listdir(temp_g_path)[0])


        features = (r"{}\{}\steps\{}\layers\{}\features".format(temp_path,job1, step1,self.map_layer))
        features_Z = (r"{}\{}\steps\{}\layers\{}\features.Z".format(temp_path,job1, step1,self.map_layer))
        print(features, "\n", features_Z)
        if os.path.isfile(features_Z):
            pass
            compress = Compress()
            compress.uncompress_z(features_Z)

        try:
            f = open(features, "r")
        except Exception as e:
            print("未能比对！！！请重新执行比对！！！")
            result = "未比对"


        # shutil.copytree(r"C:\genesis\fw\jobs\{}".format(job_name_1),r"C:\cc\jobs\{}".format(job_name_1))
        # time.sleep(15)

        with open(features, "r") as f:
            s = f.readlines()
            print(s[3])
        if "r0" in s[3]:
            print("比对发现有差异！！！！！！")
            result = "错误"
        else:
            print("恭喜！比对通过！！！")
            result = "正常"

            diff = False
            # asw_dir = "C:/genesis"
            # matrix_path = os.path.join(asw_dir, 'fw/jobs/{}/matrix/matrix'.format(job1))
            matrix_path = r'C:\genesis\fw\jobs\{}\matrix\matrix'.format(job1)
            with open(matrix_path, 'r') as f:
                for var in f.readlines():
                    line = var.strip()
                    if len(line) == 0:
                        continue
                    attr = line.split('=')
                    if len(attr) == 2:
                        # print(attr)
                        if attr[0] == 'NAME' and attr[1].lower() == layer_cp:
                            diff = True
                            break
            if diff == True:
                print('Difference were found')
                result = "错误"
            else:
                print('Layers Match')
                result = "正常"

        return result

    def layer_compare_close_job(self, jobpath1,step1,layer1,jobpath2,step2,layer2,layer2_ext,tol,map_layer,map_layer_res):
        print("*" * 100, "close job")
        results = []
        try:
            self.jobpath1 = jobpath1
            # self.job_name_1=self.jobpath1.split("\\")[-1]
            self.step1 = step1
            self.layer1 = layer1
            self.jobpath2 = jobpath2
            self.step2 = step2
            self.layer2 = layer2
            self.layer2_ext = layer2_ext
            self.tol = tol
            self.map_layer = map_layer
            self.map_layer_res = map_layer_res
        except Exception as e:
            print(e)
            print("*" * 100)
            return results

        self.job1 = os.path.basename(jobpath1)
        self.job2 = os.path.basename(jobpath2)
        layer_cp = layer2 + layer2_ext

        cmd_list1 = [

            'COM editor_page_close',
            'COM check_inout,mode=out,type=job,job={}'.format(job1),
            'COM close_job,job={}'.format(job1),
            'COM close_form,job={}'.format(job1),
            'COM close_flow,job={}'.format(job1),

            'COM close_job,job={}'.format(job2),
            'COM close_form,job={}'.format(job2),
            'COM close_flow,job={}'.format(job2)

        ]

        cmd_list2 = [
            # 'COM editor_page_close',
            # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # 'COM delete_entity,job=,type=job,name={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # # 'COM close_job,job={}'.format(job2),
            # # 'COM close_form,job={}'.format(job2),
            # # 'COM close_flow,job={}'.format(job2),
            # 'COM delete_entity,job=,type=job,name={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)
        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            if ret != 0:
                print('inner error')
                return results

        time.sleep(1)

    def layer_compare_g2(self, paras):
        print("*" * 100, "comare")
        result = ""
        try:
            jobpath1 = paras['jobpath1']
            job_name_1 = jobpath1.split("\\")[-1]
            step1 = paras['step1']
            layer1 = paras['layer1']
            jobpath2 = paras['jobpath2']
            step2 = paras['step2']
            layer2 = paras['layer2']
            layer2_ext = paras['layer2_ext']
            tol = paras['tol']
            map_layer = paras['map_layer']
            map_layer_res = paras['map_layer_res']
        except Exception as e:
            print(e)
            print("*" * 100)
            return result

        job1 = os.path.basename(jobpath1)
        job2 = os.path.basename(jobpath2)
        layer_cp = layer2 + layer2_ext

        cmd_list1 = [
            'COM check_inout,mode=out,type=job,job={}'.format(job1),
            'COM clipb_open_job,job={},update_clipboard=view_job'.format(job1),
            'COM open_job,job={}'.format(job1),
            'COM open_entity,job={},type=step,name={},iconic=no'.format(job1, step1),
            'COM units,type=inch',
            'COM open_job,job={}'.format(job2),
            'COM compare_layers,layer1={},job2={},step2={},layer2={},layer2_ext={},tol={},area=global,consider_sr=yes,ignore_attr=,map_layer={},map_layer_res={}'.format(
                layer1, job2, step2, layer2, layer2_ext, tol, map_layer, map_layer_res),

            'COM save_job,job={},override=no'.format(job1),
            'COM editor_page_close',
            'COM check_inout,mode=out,type=job,job={}'.format(job1),
            'COM close_job,job={}'.format(job1),
            'COM close_form,job={}'.format(job1),
            'COM close_flow,job={}'.format(job1),

            'COM close_job,job={}'.format(job2),
            'COM close_form,job={}'.format(job2),
            'COM close_flow,job={}'.format(job2)

        ]

        cmd_list2 = [
            # 'COM editor_page_close',
            # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # 'COM delete_entity,job=,type=job,name={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            # # 'COM close_job,job={}'.format(job2),
            # # 'COM close_form,job={}'.format(job2),
            # # 'COM close_flow,job={}'.format(job2),
            # 'COM delete_entity,job=,type=job,name={}'.format(job2),
            # 'COM close_form,job={}'.format(job2),
            # 'COM close_flow,job={}'.format(job2)
        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            if ret != 0:
                print('inner error')
                return result

        time.sleep(1)
        features = (r"C:\genesis\fw\jobs\{}\steps\{}\layers\diff\features".format(job_name_1, step1))
        features_Z = (r"C:\genesis\fw\jobs\{}\steps\{}\layers\diff\features.Z".format(job_name_1, step1))
        print(features, "\n", features_Z)
        if os.path.isfile(features_Z):
            pass
            compress = Compress()
            compress.uncompress_z(features_Z)

        try:
            f = open(features, "r")
        except Exception as e:
            print("未能比对！！！请重新执行比对！！！")
            result = "未比对"
            for cmd in cmd_list2:
                self.exec_cmd(cmd)
            return result

        # shutil.copytree(r"C:\genesis\fw\jobs\{}".format(job_name_1),r"C:\cc\jobs\{}".format(job_name_1))
        # time.sleep(15)

        with open(features, "r") as f:
            s = f.readlines()
            print(s[3])
        if "r0" in s[3]:
            print("比对发现有差异！！！！！！")
            result = "错误"
        else:
            print("恭喜！比对通过！！！")
            result = "正常"

            diff = False
            # asw_dir = "C:/genesis"
            # matrix_path = os.path.join(asw_dir, 'fw/jobs/{}/matrix/matrix'.format(job1))
            matrix_path = r'C:\genesis\fw\jobs\{}\matrix\matrix'.format(job1)
            with open(matrix_path, 'r') as f:
                for var in f.readlines():
                    line = var.strip()
                    if len(line) == 0:
                        continue
                    attr = line.split('=')
                    if len(attr) == 2:
                        # print(attr)
                        if attr[0] == 'NAME' and attr[1].lower() == layer_cp:
                            diff = True
                            break
            if diff == True:
                print('Difference were found')
                result = "错误"
            else:
                print('Layers Match')
                result = "正常"
            for cmd in cmd_list2:
                self.exec_cmd(cmd)
        return result

    def clean_g(self, paras):
        print("begin clean!")
        try:
            jobpath1 = paras['jobpath1']
            job_name_1=jobpath1.split("\\")[-1]
            step1 = paras['step1']
            layer1 = paras['layer1']
            jobpath2 = paras['jobpath2']
            step2 = paras['step2']
            layer2 = paras['layer2']
            layer2_ext = paras['layer2_ext']
            tol = paras['tol']
            map_layer = paras['map_layer']
            map_layer_res = paras['map_layer_res']
        except Exception as e:
            print(e)
            return

        job1 = os.path.basename(jobpath1)
        job2 = os.path.basename(jobpath2)
        # layer_cp = layer2 + layer2_ext



        cmd_list2 = [
            # 'COM editor_page_close',
            # 'COM check_inout,mode=in,type=job,job={}'.format(job1),
            # 'COM close_job,job={}'.format(job1),
            # 'COM close_form,job={}'.format(job1),
            # 'COM close_flow,job={}'.format(job1),
            'COM close_job,job={}'.format(job1),
            'COM close_form,job={}'.format(job1),
            'COM close_flow,job={}'.format(job1),
            'COM delete_entity,job=,type=job,name={}'.format(job1),
            'COM close_form,job={}'.format(job1),
            'COM close_flow,job={}'.format(job1),
            'COM close_job,job={}'.format(job2),
            'COM close_form,job={}'.format(job2),
            'COM close_flow,job={}'.format(job2),
            'COM close_form,job={}'.format(job2),
            'COM close_flow,job={}'.format(job2),
            'COM delete_entity,job=,type=job,name={}'.format(job2)
        ]

        # for cmd in cmd_list1:
        #     # print(cmd)
        #     ret = self.exec_cmd(cmd)
        #     if ret != 0:
        #         print('inner error')
        #         return

        # time.sleep(1)

        for cmd in cmd_list2:
            print(cmd)
            ret = self.exec_cmd(cmd)
            print(ret)
            if ret != 0:
                print('inner error')
                # return
        return "clean finish!"

    def delete_job(self,job_name):
        pass
        cmd_list = [
            'COM close_job,job={}'.format(job_name),
            'COM close_form,job={}'.format(job_name),
            'COM close_flow,job={}'.format(job_name),
            'COM delete_entity,job=,type=job,name={}'.format(job_name),
            'COM close_form,job={}'.format(job_name),
            'COM close_flow,job={}'.format(job_name)
        ]

        for cmd in cmd_list:
            print(cmd)
            ret = self.exec_cmd(cmd)
            print(ret)
            if ret != 0:
                print('inner error')
                # return
        return "clean finish!"

    def clean_g_all(self):
        pass
        cmd_list = [
            'COM info,args=-t root -m display -d JOBS_LIST,out_file=C:/tmp/job_list.txt,write_mode=replace,units=inch'
        ]

        for cmd in cmd_list:
            print(cmd)
            ret = self.exec_cmd(cmd)
            print(ret)
            if ret != 0:
                print('inner error')
                # return

        with open(r"C:/tmp/job_list.txt", "r") as f:
            s = f.readlines()
        print(s)

        for each_job in s:

            job_name = each_job.split("=")[1]
            self.delete_job(job_name)

        return "clean finish!"

    def Create_Entity(self, job, step):
        print("*"*100,job,step)
        cmd_list1 = [
            # 'COM abc',
            'COM create_entity,job=,is_fw=no,type=job,name={},db=genesis,fw_type=form'.format(job),
            'COM create_entity,job={},is_fw=no,type=step,name={},db=genesis,fw_type=form'.format(job, step),
            'COM save_job,job={},override=no'.format(job)
        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            print("*"*100,ret)
            if ret != 0:
                print('inner error')
                return False
        return True

    def Gerber2ODB(self, paras, _type):
        # print("*"*100,"gerber2odb")
        try:
            path = paras['path']
            job = paras['job']
            step = paras['step']
            format = paras['format']
            data_type = paras['data_type']
            units = paras['units']
            coordinates = paras['coordinates']
            zeroes = paras['zeroes']
            nf1 = paras['nf1']
            nf2 = paras['nf2']
            decimal = paras['decimal']
            separator = paras['separator']
            tool_units = paras['tool_units']
            layer = paras['layer']
            print("layer"*10,layer)
            layer=layer.replace(' ','-')
            print("layer" * 10, layer)
            wheel = paras['wheel']
            wheel_template = paras['wheel_template']
            nf_comp = paras['nf_comp']
            multiplier = paras['multiplier']
            text_line_width = paras['text_line_width']
            signed_coords = paras['signed_coords']
            break_sr = paras['break_sr']
            drill_only = paras['drill_only']
            merge_by_rule = paras['merge_by_rule']
            threshold = paras['threshold']
            resolution = paras['resolution']
        except Exception as e:
            print(e)
            return False

        # print("p"*100,path)

        # if not os.path.exists(path):
        #     print('{} does not exist'.format(path))
        #     return False

        trans_COM = 'COM input_manual_set,'
        trans_COM += 'path={},job={},step={},format={},data_type={},units={},coordinates={},zeroes={},'.format(path.replace("\\","/"),
                                                                                                               job,
                                                                                                               step,
                                                                                                               format,
                                                                                                               data_type,
                                                                                                               units,
                                                                                                               coordinates,
                                                                                                               zeroes)
        trans_COM += 'nf1={},nf2={},decimal={},separator={},tool_units={},layer={},wheel={},wheel_template={},'.format(
            nf1, nf2, decimal, separator, tool_units, layer, wheel, wheel_template)
        trans_COM += 'nf_comp={},multiplier={},text_line_width={},signed_coords={},break_sr={},drill_only={},'.format(
            nf_comp, multiplier, text_line_width, signed_coords, break_sr, drill_only)
        trans_COM += 'merge_by_rule={},threshold={},resolution={}'.format(merge_by_rule, threshold, resolution)

        cmd_list1 = []
        cmd_list2 = []
        # trans_COM = 'COM input_manual_set,path=C:/Users/EPSZ15/Desktop/2222/YH-DT3.9-FM1921_64X64-8SF2-04.GTL,job=6566,step=777,format=Gerber274x,data_type=ascii,units=mm,coordinates=absolute,zeroes=leading,nf1=4,nf2=4,decimal=no,separator=*,tool_units=inch,layer=yh-dt3.9-fm1921_64x64-8sf2-04.gtl,wheel=,wheel_template=,nf_comp=0,multiplier=1,text_line_width=0.0024,signed_coords=no,break_sr=yes,drill_only=no,merge_by_rule=no,threshold=200,resolution=3'
        if _type == 0:
            cmd_list1 = [
                'COM input_manual_reset',
                # 'COM input_manual_set,path={},job={},step={},format={},data_type{},units={},coordinates={},zeroes={},nf1={},nf2={},decimal={},separator={},\
                #     tool_units={},layer={},wheel={},wheel_template={},nf_comp={},multiplier={},text_line_width={},signed_coords={},break_sr={},drill_only={},\
                #     merge_by_rule={},threshold={},resolution={}'.format(path, job, step, format, data_type, units, coordinates, zeroes, nf1, nf2, decimal,
                #     separator, tool_units, layer, wheel, wheel_template, nf_comp, multiplier, text_line_width, signed_coords, break_sr, drill_only, merge_by_rule,
                #     threshold, resolution),
                trans_COM,
                ('COM input_manual,script_path={}'.format(''))
            ]
            cmd_list2 = [
                'COM input_manual_reset',
                trans_COM,
                'COM input_manual,script_path={}'.format('')
            ]
        else:
            cmd_list1 = [
                'COM save_job,job={},override=no'.format(job)
            ]
            cmd_list2 = [
                'COM save_job,job={},override=no'.format(job)
            ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            if ret != 0:
                print('inner error')
                return False
        return True

    # def Gerber2ODB2(self, paras, _type,job_id):
    #     # print("*"*100,"gerber2odb")
    #
    #
    #
    #     try:
    #         path = paras['path']
    #         job = paras['job']
    #         step = paras['step']
    #         format = paras['format']
    #         data_type = paras['data_type']
    #         units = paras['units']
    #         coordinates = paras['coordinates']
    #         zeroes = paras['zeroes']
    #         nf1 = paras['nf1']
    #         nf2 = paras['nf2']
    #         decimal = paras['decimal']
    #         separator = paras['separator']
    #         tool_units = paras['tool_units']
    #         layer = paras['layer']
    #         print("layer"*10,layer)
    #         layer=layer.replace(' ','-')
    #         print("layer" * 10, layer)
    #         wheel = paras['wheel']
    #         wheel_template = paras['wheel_template']
    #         nf_comp = paras['nf_comp']
    #         multiplier = paras['multiplier']
    #         text_line_width = paras['text_line_width']
    #         signed_coords = paras['signed_coords']
    #         break_sr = paras['break_sr']
    #         drill_only = paras['drill_only']
    #         merge_by_rule = paras['merge_by_rule']
    #         threshold = paras['threshold']
    #         resolution = paras['resolution']
    #     except Exception as e:
    #         print(e)
    #         return False
    #
    #     try:
    #         print("开始定位"*10)
    #         job_current = models.Job.objects.get(id=job_id)
    #         layer_all = models.Layer.objects.filter(job=job_current)
    #         print(layer_all)
    #         print(path.replace(' ', '-'))
    #         print(os.path.basename(path).replace(' ', '-'))
    #         layer_e2 = models.Layer.objects.get(job=job_current, layer=os.path.basename(path).replace(' ', '-'))
    #         print('*'*100,layer_e2)
    #         print("*"*100,layer_e2.layer_file_type)
    #         if layer_e2.status == 'published' and layer_e2.layer_file_type=='excellon2':
    #             pass
    #             print("我是Excellon2!!!!!")
    #             format='Excellon2'
    #             units=layer_e2.units_g.lower()
    #             zeroes=layer_e2.zeroes_omitted_g.lower()
    #             nf1 = int(layer_e2.number_format_A_g)
    #             nf2 = int(layer_e2.number_format_B_g)
    #             #g软件的tool_units没有mils选项
    #             if layer_e2.tool_units_g.lower() == 'mils':
    #                 tool_units = 'inch'
    #             else:
    #                 tool_units = layer_e2.tool_units_g.lower()
    #
    #             separator='nl'
    #         else:
    #             print("我不是孔Excellon2!")
    #
    #         print("结束定位" * 10)
    #     except:
    #         pass
    #         print("有异常啊！")
    #     # print("p"*100,path)
    #
    #     # if not os.path.exists(path):
    #     #     print('{} does not exist'.format(path))
    #     #     return False
    #
    #
    #
    #
    #     trans_COM = 'COM input_manual_set,'
    #     trans_COM += 'path={},job={},step={},format={},data_type={},units={},coordinates={},zeroes={},'.format(path.replace("\\","/"),
    #                                                                                                            job,
    #                                                                                                            step,
    #                                                                                                            format,
    #                                                                                                            data_type,
    #                                                                                                            units,
    #                                                                                                            coordinates,
    #                                                                                                            zeroes)
    #     trans_COM += 'nf1={},nf2={},decimal={},separator={},tool_units={},layer={},wheel={},wheel_template={},'.format(
    #         nf1, nf2, decimal, separator, tool_units, layer, wheel, wheel_template)
    #     trans_COM += 'nf_comp={},multiplier={},text_line_width={},signed_coords={},break_sr={},drill_only={},'.format(
    #         nf_comp, multiplier, text_line_width, signed_coords, break_sr, drill_only)
    #     trans_COM += 'merge_by_rule={},threshold={},resolution={}'.format(merge_by_rule, threshold, resolution)
    #
    #     cmd_list1 = []
    #     cmd_list2 = []
    #     # trans_COM = 'COM input_manual_set,path=C:/Users/EPSZ15/Desktop/2222/YH-DT3.9-FM1921_64X64-8SF2-04.GTL,job=6566,step=777,format=Gerber274x,data_type=ascii,units=mm,coordinates=absolute,zeroes=leading,nf1=4,nf2=4,decimal=no,separator=*,tool_units=inch,layer=yh-dt3.9-fm1921_64x64-8sf2-04.gtl,wheel=,wheel_template=,nf_comp=0,multiplier=1,text_line_width=0.0024,signed_coords=no,break_sr=yes,drill_only=no,merge_by_rule=no,threshold=200,resolution=3'
    #     if _type == 0:
    #         cmd_list1 = [
    #             'COM input_manual_reset',
    #             # 'COM input_manual_set,path={},job={},step={},format={},data_type{},units={},coordinates={},zeroes={},nf1={},nf2={},decimal={},separator={},\
    #             #     tool_units={},layer={},wheel={},wheel_template={},nf_comp={},multiplier={},text_line_width={},signed_coords={},break_sr={},drill_only={},\
    #             #     merge_by_rule={},threshold={},resolution={}'.format(path, job, step, format, data_type, units, coordinates, zeroes, nf1, nf2, decimal,
    #             #     separator, tool_units, layer, wheel, wheel_template, nf_comp, multiplier, text_line_width, signed_coords, break_sr, drill_only, merge_by_rule,
    #             #     threshold, resolution),
    #             trans_COM,
    #             ('COM input_manual,script_path={}'.format(''))
    #         ]
    #         cmd_list2 = [
    #             'COM input_manual_reset',
    #             trans_COM,
    #             'COM input_manual,script_path={}'.format('')
    #         ]
    #     else:
    #         cmd_list1 = [
    #             'COM save_job,job={},override=no'.format(job)
    #         ]
    #         cmd_list2 = [
    #             'COM save_job,job={},override=no'.format(job)
    #         ]
    #
    #     for cmd in cmd_list1:
    #         print(cmd)
    #         ret = self.exec_cmd(cmd)
    #         if ret != 0:
    #             print('inner error')
    #             return False
    #     return True

    def g_Gerber2Odb(self,gerberList, job, step):
        paras = {}
        paras['path'] = ''
        paras['job'] = job
        paras['step'] = step
        paras['format'] = 'Gerber274x'
        paras['data_type'] = 'ascii'
        paras['layer'] = ''
        paras['units'] = 'mm'
        paras['coordinates'] = 'absolute'
        paras['zeroes'] = 'leading'
        paras['nf1'] = '4'
        paras['nf2'] = '4'
        paras['decimal'] = 'no'
        paras['separator'] = '*'
        paras['tool_units'] = 'inch'
        paras['wheel'] = ''
        paras['wheel_template'] = ''
        paras['nf_comp'] = '0'
        paras['multiplier'] = '1'
        paras['text_line_width'] = '0.0024'
        paras['signed_coords'] = 'no'
        paras['break_sr'] = 'yes'
        paras['drill_only'] = 'no'
        paras['merge_by_rule'] = 'no'
        paras['threshold'] = '200'
        paras['resolution'] = '3'
        # 先创建job, step
        jobpath = r'C:\genesis\fw\jobs' + '/' + job
        # print("jobpath"*30,jobpath)
        results = []
        if os.path.exists(jobpath):
            shutil.rmtree(jobpath)
        self.Create_Entity(job, step)
        for gerberPath in gerberList:
            # print("g"*100,gerberPath)
            result = {'gerber': gerberPath}
            paras['path'] = gerberPath
            paras['layer'] = os.path.basename(gerberPath).lower()
            ret = self.Gerber2ODB(paras, 0)
            result['result'] = ret
            results.append(result)
        self.Gerber2ODB(paras, 1)
        return results

    def g_Gerber2Odb2(self,job_name, step, gerberList_path, out_path,job_id):
        paras = {}
        paras['path'] = ''
        paras['job'] = job_name
        paras['step'] = step
        paras['format'] = 'Gerber274x'
        paras['data_type'] = 'ascii'
        paras['layer'] = ''
        paras['units'] = 'mm'
        paras['coordinates'] = 'absolute'
        paras['zeroes'] = 'leading'
        paras['nf1'] = '4'
        paras['nf2'] = '4'
        paras['decimal'] = 'no'
        paras['separator'] = '*'
        paras['tool_units'] = 'inch'
        paras['wheel'] = ''
        paras['wheel_template'] = ''
        paras['nf_comp'] = '0'
        paras['multiplier'] = '1'
        paras['text_line_width'] = '0.0024'
        paras['signed_coords'] = 'no'
        paras['break_sr'] = 'yes'
        paras['drill_only'] = 'no'
        paras['merge_by_rule'] = 'no'
        paras['threshold'] = '200'
        paras['resolution'] = '3'
        # 先创建job, step
        jobpath = r'C:\genesis\fw\jobs' + '/' + job_name
        # print("jobpath"*30,jobpath)
        results = []
        if os.path.exists(jobpath):
            shutil.rmtree(jobpath)
        self.Create_Entity(job_name, step)
        for gerberPath in gerberList_path:
            # print("g"*100,gerberPath)
            result = {'gerber': gerberPath}
            paras['path'] = gerberPath
            paras['layer'] = os.path.basename(gerberPath).lower()
            ret = self.Gerber2ODB2(paras, 0,job_id)
            result['result'] = ret
            results.append(result)
        self.Gerber2ODB2(paras, 1,job_id)#保存
        return results

    def g_export(self,job,export_to_path):
        pass
        if not os.path.exists(r'C:\cc\share\temp'):
            os.mkdir(r'C:\cc\share\temp')

        'COM export_job,job=test-zm,path=Z:/share/temp,mode=tar_gzip,submode=full,overwrite=yes'
        cmd_list1 = [
            # 'COM abc',
            'COM export_job,job={},path={},mode=tar_gzip,submode=full,overwrite=yes'.format(job,export_to_path),

        ]

        for cmd in cmd_list1:
            print(cmd)
            ret = self.exec_cmd(cmd)
            print("*" * 100, ret)
            if ret != 0:
                print('inner error')
                return False
        return True


class GetParas():
    pass
    def get_paras_compare(*, jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,map_layer_res):
        pass
        paras = {}
        paras["jobpath1"] = jobpath1
        paras["step1"] = step1
        paras["layer1"] = layer1
        paras["jobpath2"] = jobpath2
        paras["step2"] = step2
        paras["layer2"] = layer2
        paras["layer2_ext"] = layer2_ext
        paras["tol"] = tol
        paras["map_layer"] = map_layer
        paras["map_layer_res"] = map_layer_res
        # print(paras)
        return paras

class Compress():


    def uncompress_z(self,file_full_name):
        # command = r'gzip.exe -d C:\cc\else\test\features.Z'
        command=r'gzip.exe -d {}'.format(file_full_name)
        print(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        # self.process.stdin.flush()
        line = self.process.stdout.readline()
        ret = (line.decode().strip())
        print(ret)
        return "uncompress finish!"


def getFlist(path):
    for root, dirs, files in os.walk(path):
        print('root_dir:', root)  #当前路径
        print('sub_dirs:', dirs)   #子文件夹
        print('files:', files)     #文件名称，返回list类型
    return files



if __name__ == '__main__':
    pass
    # asw = Asw(gl.gateway_path)
    # gerberList = [
    #                 'C:/Users/cheng.chen/Desktop/346414\\Statische Ansteuerung 18.07.21.gbl',
    #               ]
    #
    # gerberList2=getFlist(r'C:\Users\cheng.chen\Desktop\346414')
    # print(gerberList2)
    # gerberList_path=[]
    # for each in gerberList2:
    #     gerberList_path.append(os.path.join(r'C:\Users\cheng.chen\Desktop\346414',each))
    # print(gerberList_path)
    # job = 'temp_g'
    # step = "orig"
    # asw.g_Gerber2Odb(gerberList_path, job, step)
    # #
    # asw.delete_job(job)
    # asw.g_export(job,r'Z:/share/temp')

    #compare
    temp_path=r"C:\cc\share\temp"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)



    rets = []
    paras = {}
    job1 = '760_ep'
    job2 = '760_g'
    step1 = 'orig'
    step2 = 'orig'
    jobpath1 = r'C:\Users\cheng.chen\Desktop'+ '\\' + job1
    step1 = step1
    layer1 = 'bottom.art'
    jobpath2 = r'C:\Users\cheng.chen\Desktop' + '\\' + job2
    step2 = step2
    layer2 = 'bottom.art'
    layer2_ext = '_copy'
    tol = 0.1
    map_layer = layer2 + '-com'
    map_layer_res = 200

    asw = Asw(gl.gateway_path)
    asw.import_odb_folder(r'C:\Users\cheng.chen\Desktop'+ '\\' + job1)#导入要比图的资料
    asw.import_odb_folder(r'C:\Users\cheng.chen\Desktop' + '\\' + job2)  # 导入要比图的资料
    asw.layer_compare_g_open_2_job(jobpath1,step1,layer1,jobpath2,step2,layer2,layer2_ext,tol,map_layer,map_layer_res)
    asw.layer_compare_do_compare(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,map_layer_res)
    asw.g_export(job1,r'Z:/share/temp')
    asw.layer_compare_analysis(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,map_layer_res)
    asw.layer_compare_close_job(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,map_layer_res)
    asw.delete_job(job1)
    asw.delete_job(job2)



    # layers = ['statische-ansteuerung-18.07.21.gts']
    # for layer in layers:
    #     paras["layer1"] = layer
    #     paras["layer2"] = layer
    #     paras["map_layer"] = layer + '_map'
    #     ret = asw.layer_compare_g(paras, 1)
    #     rets.append(ret)
    # ret=asw.layer_compare_g(paras)
    # rets=rets.append(ret)
    # print(rets)


