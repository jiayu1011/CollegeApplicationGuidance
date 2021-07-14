#!/usr/bin/env python
# coding: utf-8

# # task3
# ## 高考志愿填报指导

# In[1]:


import numpy as np
import pandas as pd
import os
import sys


# ### 一、导入、处理数据（一分一段+招生计划+近三年录取情况（含排位））

# In[2]:


scoreRank2021DataPath = './data/2021年广东省高考普通类（物理）一分一段数据.txt'
admissionScheme2021DataPath = './data/中山大学2021年分专业招生计划（广东）.txt'
admissionDataPath = './result/中山大学近三年本科批次录取数据（含排名）.xlsx'


# In[3]:


scoreRank2021Data = {}
admissionScheme2021Data = {}

with open(scoreRank2021DataPath, 'r', encoding='utf-16') as f2021:
    linecount = 0
    columns = []
    while True:
        line = f2021.readline()
        linecount += 1
        if not line:
            break
        rowDataArr = line.strip().split('\t')

        if linecount==2:    
            columns = rowDataArr
            for (index, item) in enumerate(columns):
                scoreRank2021Data[item] = []   
        elif linecount>2:
            
            if not line.strip():
                continue
            for (index, item) in enumerate(rowDataArr):
                scoreRank2021Data[columns[index]].append(item)   
                
with open(admissionScheme2021DataPath, 'r', encoding='utf-16') as f2021:
    linecount = 0
    columns = []
    while True:
        line = f2021.readline()
        linecount += 1
        if not line:
            break
        rowDataArr = line.strip().split('\t')

        if linecount==2:    
            columns = rowDataArr
            for (index, item) in enumerate(columns):
                admissionScheme2021Data[item] = []   
        elif linecount>2:
            
            if not line.strip():
                continue
            for (index, item) in enumerate(rowDataArr):
                admissionScheme2021Data[columns[index]].append(item)                   
    


# In[4]:


df_scoreRank2021 = pd.DataFrame(data=scoreRank2021Data)
df_admissionScheme2021 = pd.DataFrame(data=admissionScheme2021Data)


# In[5]:


# 2021年分数-排位数据
df_scoreRank2021


# In[6]:


# 2021招生计划数据
df_admissionScheme2021


# In[7]:


# 对"科类"字段去重
df_admissionScheme2021.drop_duplicates(subset=['科类'], keep='first')


# 去重后发现共有历史/物理两种科类
# 由于所给的”一分一段“数据是物理类的数据，故此处仅需要保留“科类”是物理类的数据条目即可

# In[8]:


df_admissionScheme2021 = df_admissionScheme2021[df_admissionScheme2021['科类']=='物理类']
df_admissionScheme2021 = df_admissionScheme2021.reset_index(drop=True)


# In[9]:


df_admissionScheme2021


# In[10]:


# 读取录取数据，使空数据保持为 ' ' 而非NaN
df_admission = pd.read_excel(admissionDataPath, dtype='str', keep_default_na=False)


# In[11]:


# 近三年录取情况数据
df_admission


# In[12]:


# 由于只有物理普通类的一分一段数据，故只保留理科的录取情况作为参考
df_admission = df_admission[df_admission['科类']=='理科']

# 由于仅关心排名，故只保留排名
df_admission = df_admission[
    [
        '专业名称', '所属学院',
        '2020最低分排位', '2020平均分排位',
        '2019最低分排位', '2019平均分排位',
        '2018最低分排位', '2018平均分排位'
    ]
]
df_admission = df_admission.reset_index(drop=True)


# In[13]:


df_admission


# 根据招生计划中的专业名称，再往年数据中查询对应的专业名称
# 新增的专业会在推荐同类专业时一并给出，并注明为新增专业，如”计算机类（珠海，智能实验班）“

# In[14]:


df_admissionScheme2021


# In[15]:


queryKeyWordArr = []
tempIndexArr = []
for (index, item) in enumerate(df_admissionScheme2021['专业名称']):
    temp = item[:item.find('（')]
    if temp.find('类')!=-1:
        temp = temp[:temp.find('类')]
    queryKeyWordArr.append(temp)
      
queryKeyWordArr = list(set(queryKeyWordArr))    
# print(queryKeyWordArr)
for keyWord in queryKeyWordArr:
    for (index, item) in enumerate(df_admission['专业名称']):
#         print(keyWord, item)
        if keyWord  in item:
#             print(index)
            tempIndexArr.append(index)

# print(tempIndexArr)
            
df_admission = df_admission.loc[tempIndexArr]    
df_admission = df_admission.reset_index(drop=True)
df_admission


# In[16]:


tempDict = {
    '近三年最低分排位平均值': [],
    '近三年平均分排位平均值': []
}
for (index_row, row) in df_admission.iterrows():
    rank2020 = 0
    rank2019 = 0
    rank2018 = 0
    
    if row['2020最低分排位']:
        rank2020 = int(row['2020最低分排位'])
    if row['2019最低分排位']:
        rank2020 = int(row['2019最低分排位'])
    if row['2018最低分排位']:
        rank2020 = int(row['2018最低分排位'])    
    avg = (rank2020+rank2019+rank2018) // 3
    tempDict['近三年最低分排位平均值'].append(avg)
    
    if row['2020平均分排位']:
        rank2020 = int(row['2020平均分排位'])
    if row['2019平均分排位']:
        rank2020 = int(row['2019平均分排位'])
    if row['2018平均分排位']:
        rank2020 = int(row['2018平均分排位']) 
    avg = (rank2020+rank2019+rank2018) // 3
    tempDict['近三年平均分排位平均值'].append(avg)


# In[17]:


df_admission = df_admission[['专业名称', '所属学院']]
df_admission['近三年最低分排位平均值'] = tempDict['近三年最低分排位平均值']
df_admission['近三年平均分排位平均值'] = tempDict['近三年平均分排位平均值']
df_admission


# In[ ]:





# In[18]:


score = 0
rank = 0

while True:
    scoreOrRank = input('请输入您的分数或全省排名:(xxx分/xxx名)\n')
    # with open('./input/scoreOrRank.txt', 'r', encoding='utf-8') as f:
    #     f.readline()
    #     scoreOrRank = f.readline()

    # 均转化成排位来计算
    if scoreOrRank[-1:]=='分':
        score = scoreOrRank[:-1]
        rank = int(df_scoreRank2021[df_scoreRank2021['分数段']==score]['累计'].tolist()[0])
        print('对应排位为:%d' % rank)
        break
    elif scoreOrRank[-1:]=='名':
        rank = int(scoreOrRank[:-1])
        print('对应全省排位为:%d名' % rank)
        break
    else:
        print('输入有误!')
        print('--------------------')


# ### 二、推荐算法
# >将学生排名与近三年录取情况中的排名进行比较，计算"**性价比**"最高的报考专业
# 
# 共有两个超参数`TOP_N`, `RECOMMEND_TOLERANCE`
# 
# 每类推荐专业默认最多共推荐`3`个**方向**，推荐宽容度默认为`100`
# ###### 所设计的报考专业分为两类，推荐算法大致如下：
# 
# 1. 稳妥专业（学生排名在往年录取平均排名附近。报考此类专业较为稳妥，录取概率较大）
# 2. 摸高专业（学生排名在往年录取最低排名附近。报考此类专业可能会无法录上，录取概率较小）
# 
# 
# *注意事项：*
# 
# *1. 因为缺少往年的招生计划数据，无法将往年与2021年的招生计划中的名额数目等进行比较，故无法预测2021录取的平均/最低排名的上浮与下跌等变化，本统计只基于往年的排名给出建议*
# 
# *2. 由于2021招生计划中的专业名称与往年录取情况中的专业名称有较大出入，故仅基于往年录取情况的专业名称给出推荐，并会一并附上2021招生计划中与之相关的专业名称供用户进行参考*
# 
# *3. 宽容度最好能够进行调整，因为宽容度大小要视学校每年招生名额的变动而变动*

# In[19]:


# 每类推荐专业方向默认最多推荐3个
TOP_N = 3
#  推荐宽容度默认为100
RECOMMEND_TOLERANCE = 100


# In[20]:


aRankAvg = df_admission['近三年平均分排位平均值'].tolist()
lRankAvg = df_admission['近三年最低分排位平均值'].tolist()

def filterFunc(x):
    if x<rank:
        return abs(x-rank)<RECOMMEND_TOLERANCE
    else:
        return True

# 排名向前波动若在宽容度容忍范围内，则纳入考虑范围
aRankAvg = list(filter(filterFunc, aRankAvg))
aRankAvg.sort()
aRankAvg = aRankAvg[:min(TOP_N, len(lRankAvg))]


lRankAvg = list(filter(filterFunc, lRankAvg))
lRankAvg.sort()
lRankAvg = lRankAvg[:min(TOP_N, len(lRankAvg))]
    
        


# In[21]:


aRankAvg, lRankAvg


# In[22]:


# 将两类推荐专业的信息提取出来
df_admissionA = df_admission[df_admission['近三年平均分排位平均值'].isin(aRankAvg)]
df_admissionA = df_admissionA.reset_index(drop=True)
df_admissionL = df_admission[df_admission['近三年最低分排位平均值'].isin(lRankAvg)]
df_admissionL = df_admissionL.reset_index(drop=True)


# In[23]:


# 稳妥专业推荐（基于往年专业）
df_admissionA


# In[24]:


# 摸高专业推荐（基于往年专业）
df_admissionL


# In[25]:


df_recommendAccording = pd.concat(
    [df_admissionA, df_admissionL],
    keys=['稳妥专业推荐(基于往年专业)', '摸高专业推荐(基于往年专业)']
)
df_recommendAccording


# In[26]:


df_admissionScheme2021


# In[27]:


# 反关联2021招生计划中的专业
queryKeyWordArr = []
tempIndexArr = []
for (index, item) in enumerate(df_admissionA['专业名称']):
    temp = item
    if temp.find('（')!=-1:
        temp = item[:item.find('（')]
    if temp.find('类')!=-1:
        temp = temp[:temp.find('类')]
    queryKeyWordArr.append(temp)
      
queryKeyWordArr = list(set(queryKeyWordArr))    
# print(queryKeyWordArr)
for keyWord in queryKeyWordArr:
    for (index, item) in enumerate(df_admissionScheme2021['专业名称']):
#         print(keyWord, item)
        if keyWord  in item:
#             print(index)
            tempIndexArr.append(index)

# print(tempIndexArr)
            
df_recommendA = df_admissionScheme2021.loc[tempIndexArr]    
df_recommendA = df_recommendA.reset_index(drop=True)


queryKeyWordArr = []
tempIndexArr = []
for (index, item) in enumerate(df_admissionL['专业名称']):
    temp = item
    if temp.find('（')!=-1:
        temp = item[:item.find('（')]
    if temp.find('类')!=-1:
        temp = temp[:temp.find('类')]
    queryKeyWordArr.append(temp)
      
queryKeyWordArr = list(set(queryKeyWordArr))    
# print(queryKeyWordArr)
for keyWord in queryKeyWordArr:
    for (index, item) in enumerate(df_admissionScheme2021['专业名称']):
#         print(keyWord, item)
        if keyWord  in item:
#             print(index)
            tempIndexArr.append(index)

# print(tempIndexArr)
            
df_recommendL = df_admissionScheme2021.loc[tempIndexArr]    
df_recommendL = df_recommendL.reset_index(drop=True)


# In[28]:


# 稳妥专业推荐（基于2021招生计划）
df_recommendA


# In[29]:


# 摸高专业推荐（基于2021招生计划）
df_recommendL


# In[30]:


# 合并推荐信息
df_recommend = pd.concat(
    [df_recommendA, df_recommendL],
    keys=['稳妥专业推荐(基于2021招生计划)', '摸高专业推荐(基于2021招生计划)']
)
df_recommend



# In[ ]:





# In[31]:


if not os.path.exists('./result'):
    os.mkdir('./result')
    
df_recommend.to_excel('./result/全省排名为%d的2021年中山大学报考专业推荐.xlsx' % rank)    
df_recommendAccording.to_excel('./result/全省排名为%d的2021年中山大学专业推荐依据.xlsx' % rank)
    
print('专业推荐结果请见result文件夹下的\"全省排名为%d的2021年中山大学报考专业推荐.xlsx\"' % rank)
print('推荐依据请见result文件夹下的\"全省排名为%d的2021年中山大学专业推荐依据.xlsx\"' % rank)

# In[ ]:





# In[ ]:





# In[ ]:




