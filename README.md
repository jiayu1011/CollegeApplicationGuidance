## College Application Guidance高考志愿填报推荐(基于中山大学数据分析)

#### Tools:

- jupyter notebook

- python 3.8.5

- pandas 1.1.3

#### Dependencies Tree:

```
│  CollegeApplicationGuiding.ipynb(task3's code)
│  CollegeApplicationGuiding.py(task3's runnable code)
│  FillingMissingAdmissionData.ipynb(task2's code)
│  MajorHotRanking.ipynb(task1's code)
│  README.md
│  需求.jpg
|  requirements.txt(需求包列表)
│      
├─data(source data)
│      2018广东省高考一分一段数据.txt
│      2019广东省高考一分一段数据.txt
│      2020广东省高考一分一段数据.txt
│      2021年广东省高考普通类（物理）一分一段数据.txt
│      中山大学2018-2020年本科批次录取统计（广东）.txt
│      中山大学2021年分专业招生计划（广东）.txt
│      
└─result(outputs)
        中山大学文科报考专业热度排行（近三年）.xlsx
        中山大学理科报考专业热度排行（近三年）.xlsx
        中山大学近三年本科批次录取数据（含排名）.xlsx
        全省排名为800的2021年中山大学专业推荐依据.xlsx
        全省排名为800的2021年中山大学报考专业推荐.xlsx
```



#### Task3 running method

1. Ensure your machine has an avaliable envoirment of `python3`
2. Use command `pip install -r requirements.txt` to install all the required packages
3. Use command `python CollegeApplicationGuiding.py `  to run the task3's code
4. Input your score or rank
5. The program will put the results in `./results`, go and explore them!





###### **Viewing jupyter notebook  by nbviewer:

task1:

 https://nbviewer.jupyter.org/github/jiayu1011/CollegeApplicationGuidance/blob/master/MajorHotRanking.ipynb

task2:

https://nbviewer.jupyter.org/github/jiayu1011/CollegeApplicationGuidance/blob/master/FillingMissingAdmissionData.ipynb

task3:

https://nbviewer.jupyter.org/github/jiayu1011/CollegeApplicationGuidance/blob/master/CollegeApplicationGuiding.ipynb



### Recommend Algorithm





### 推荐算法
>将学生排名与近三年录取情况中的排名进行比较，计算"**性价比**"最高的报考专业

共有两个超参数`TOP_N`, `RECOMMEND_TOLERANCE`

每类推荐专业默认最多共推荐`3`个**方向**，推荐宽容度默认为`100`
###### 所设计的报考专业分为两类，推荐算法大致如下：

1. 稳妥专业（学生排名在往年录取平均排名附近。报考此类专业较为稳妥，录取概率较大）
2. 摸高专业（学生排名在往年录取最低排名附近。报考此类专业可能会无法录上，录取概率较小）


*注意事项：*

*1. 因为缺少往年的招生计划数据，无法将往年与2021年的招生计划中的名额数目等进行比较，故无法预测2021录取的平均/最低排名的上浮与下跌等变化，本统计只基于往年的排名给出建议*

*2. 由于2021招生计划中的专业名称与往年录取情况中的专业名称有较大出入，故仅基于往年录取情况的专业名称给出推荐，并会一并附上2021招生计划中与之相关的专业名称供用户进行参考*

*3. 宽容度最好能够进行调整，因为宽容度大小要视学校每年招生名额的变动而变动*





**Design by jiayu1011, WHU in 2021.07**

