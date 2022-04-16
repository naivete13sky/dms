from django.shortcuts import render
from django.http import StreamingHttpResponse
import os
# Create your views here.
def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

def file_download_org(request,order):
    # do something
    print(request.path_info)
    print("*"*30,order)
    excel_name = str(request.path_info).replace("/media/router_job_org/","")
    print(excel_name)
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\media\router_job_org\\" + excel_name
    # filename=request.path_info
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response