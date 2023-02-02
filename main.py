from typing import Union
from fastapi import FastAPI,HTTPException
import jwt
import time
import os

'''
去除token验证
'''
#https://github.com/tiangolo/fastapi
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "【医学统计园】"}


@app.get("/Gene/{Gene}")
#检索基因，并返回基因的表达值
def read_item(Gene: str, Project: Union[str, None] = None):
    TPM,Group=getGenes(Gene,Project)
    if len(TPM)<1:
        Group=list()
    return {"Gene": Gene, "Project": Project, "TPM":TPM,"Group":Group}

def extractToken(token):
    try:
        jwt_decode = jwt.decode(token, 'fanqiang1024', issuer='yxtjy',  algorithms=['HS256'])
        res=jwt_decode['exp']>time.time()
        return(res)
    except:
        res=False
        return(res)
 
'''
1. 根据项目名称获取：filename
2. 读入filename，筛选特定gene 或者通过grep检索基因表达值后，再根据filename提取表达值
3. 根据filename，选择Group信息
4. 返回gene表达和Group信息
'''

def get_files(Project: Union[str, None] = None):
    #根据项目号，获取文件名
    fileList=loadSamples()
    if Project in fileList:
        files=fileList[Project]
    else:
        files=""
    return(files)

def getGenes(gene,Project):
    genesTPM=[]
    sampleInfo=loadSamples()
    if Project in sampleInfo:
        files=sampleInfo[Project].filename
        cmd="cd /TCGA/TCGA/ && grep -w "+gene.upper()+" "+ " ".join(files)+"|grep protein_coding|cut -f2,7"
        #res= subprocess.Popen(cmd, shell=True)
        #(status, output) = commands.getstatusoutput(cmd)
        result = os.popen(cmd)
        for rs in result.readlines():
            r=rs.strip("\n").split("\t")
            genesTPM.append(r[1])
        return(genesTPM,sampleInfo[Project].sampleType)
    else:
        return([],[])
        
    


class Samples(object):
    def __init__(self,name):
        self.ProjectID=name
        self.sampleID=[]
        self.sampleType=[]
        self.filename=[]    

def loadSamples():
    with open("/TCGA/gdc_sample_sheet.2022-05-25_all.tsv","r") as freads:
        fs=freads.readlines()
        sampleInfo={}
        for f in fs:
            fname=f.strip("\n").split("\t")
            if fname[4] in sampleInfo:
                sampleInfo[fname[4]].sampleID.append(fname[5])
                sampleInfo[fname[4]].sampleType.append(fname[7])
                sampleInfo[fname[4]].filename.append(fname[1])
            else:
                sampleInfo[fname[4]]=Samples(fname[4])
                sampleInfo[fname[4]].sampleID=[fname[5]]
                sampleInfo[fname[4]].sampleType=[fname[7]]
                sampleInfo[fname[4]].filename=[fname[1]]
                
    return(sampleInfo)
    
