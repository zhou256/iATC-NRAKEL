# -*- coding: utf-8 -*-

"""
    functions:
       1.construct trainset based on mashup output;
       2.transform format of trainset for Meka.
"""
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import csv
from numpy import hstack,vstack,array,nan

def toTrainSet(benchmark_file):
    with open('../data/Mashup_input_file/drugs.txt') as fp:
        content=fp.readlines()
    columns11=[]
    for line in content:
        temp=line.strip()
        columns11.append(temp)
    
    Group_class=['A','B','C','D','G','H','J','L','M','N','P','R','S','V']
    
    total_dict={}
    drug_list=sorted(columns11)

    for iii in range(len(drug_list)):
        total_dict[drug_list[iii]]=[]
        
    for i in range(len(benchmark_file)):
        with open('../data/benchmark_byChen/'+benchmark_file[i]+'.txt') as fp:
            content=fp.readlines()
        group1=[]
        for line in content:
            temp=line.strip().split(' ')
            group1+=temp
        group1.sort()
        #key1:[A,B]
        for iii in range(len(group1)):
            total_dict[group1[iii]].append(Group_class[i])
    
    new_druglist=[]
    for key in drug_list:
        new_druglist.append([key,total_dict[key]])
    
    def group14th(item,Group_class):
        default_value=list('00000000000000')
        for i in range(len(item)):
            try:
                index_drug=Group_class.index(item[i])
                default_value[index_drug]=1
            except:
                continue
        group14_for_vect=list(map(int,default_value))
        return group14_for_vect
    dimension1=[700]
    
    for dim in dimension1:
        df2=pd.read_csv('../data/Mashup_output_file/drug3883_'+str(dim)+'.csv',header=None)
        df2.columns=columns11
        Trainset=[]
        for i in range(len(new_druglist)): #3883
            try:
                vect_combound=array(df2[new_druglist[i][0]])
                group14_for_vect=array(group14th(new_druglist[i][1],Group_class))
                vect_total=array(np.hstack((group14_for_vect,vect_combound)))
                Trainset.append(vect_total)
            except:
                print(new_druglist[i][0]+'not find!!!')
        df3=pd.DataFrame(Trainset)
        
        columns1=[]
        for i in range(1,15):
            columns1.append('t'+str(i))
        for i in range(1,1+dim):
            columns1.append('f'+str(i))
        df3.columns=columns1
        for i in range(14):
            df3[columns1[i]]=df3[columns1[i]].astype('int64')
        df3.info()
        df3.to_csv('../data/Meka_input/Meka3883_'+str(dim)+'_pinjie.csv',index=False,header=True)
        df3.info()
        
def csv2arff1():
    dimension1=[700]
    for dim in dimension1:
        data=pd.read_csv('../data/Meka_input/Meka3883_'+str(dim)+'_pinjie.csv')
        columns=data.columns.tolist()    

        for i in range(14):
            data[columns[i]]=data[columns[i]].apply(lambda x:str(x))
        def csv2arff(path,df,columns):
            with open(path,"w") as fw:
                fw.write("@relation 'ATC_L1_{} : -C 14'".format(str(dim)))
                fw.write('\n')
                fw.write('\n')
                for i in range(14):
                    fw.write('@attribute ')
                    fw.write(columns[i])
                    fw.write(' {0,1}')
                    fw.write('\n')
                for i in range(14,14+dim):
                    fw.write('@attribute ')
                    fw.write(columns[i]) 
                    fw.write(' ')
                    fw.write('numeric')
                    fw.write('\n')
                fw.write('\n')
                fw.write('\n')
                fw.write('@data')
                fw.write('\n')
                for i in range(df.shape[0]):
                    item=df.loc[i,:]
                    item=item.apply(lambda x:str(x))
                    str1=''
                    for j in range(len(item)-1): 
                        str1+=str(item[j])+','
                    str1+=str(item[len(item)-1])
                    fw.write(str1)
                    fw.write('\n')
            print('csv2arff is OK!!!  {}'.format(str(dim)) )
        
        csv_path='../data/Meka_input/Meka3883_'+str(dim)+'_pinjie.arff'
        csv2arff(csv_path,data,columns)
        
if __name__=="__main__":
    benchmark_file_list=[
            'alimentary tract and metabolism',
            'blood and blood forming organs',
            'cardiovascular system',
            'dermatologicals',
            'genitourinary system and sex hormones',
            'systemic hormonal preparations, excluding sex hormones and insulins',
            'anti-infectives for systemic use',
            'antineoplasticand--immunomodulating agents',
            'musculoskeletal system',
            'nervous system',
            'antiparasitic products, insecticides and repellents',
            'respiratory system',
            'sensory organs',
            'various'
            ]
    toTrainSet(benchmark_file_list)   
    csv2arff1()


























