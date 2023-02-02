
# TCGA API based on Docker

## Docker

Using Docker to run this App

```sh
docker run -w /API/ -v /data/aliyun/TCGA/:/TCGA/ -dp 8090:8090 tcgaapi:latest python3 -m uvicorn --host=0.0.0.0 --port=8090 main:app --reload
# -w workdirectory in Container
# -v mount local database to the Container
# -dp Local port and Container port
# python3 ...., 执行的命令
```

## TCGA data

you need to download TCGA expression data in to `TCGA` directory and `sample.sheet.csv`; Besides, `test/example data` are also provied in this `git`
if possible, you also need to check `main.py` in case of bugging.


## Web access

you can try to access the API : `localhost:8090/`

## Rstudio Access

[TCGAExpression](https://github.com/dming1024/TCGAExpression)

+ installation of this R package: 

```R
devtools::install_github("dming1024/TCGAExpression")
library(TCGAExpression)
```

+ getting genes' expression in R: 

```R
m1=getExpression("TP53","TCGA-LUAD")
head(m1)
     gene         Group
1 40.4928 Primary Tumor
2 41.4006 Primary Tumor
3 59.3452 Primary Tumor
4 43.3803 Primary Tumor
5 21.6654 Primary Tumor
6 10.5691 Primary Tumor

#导出表达结果
write.csv(m1,"LUAD_TP53.csv")
```

