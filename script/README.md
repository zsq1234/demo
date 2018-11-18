介绍
-------

目录
> pre_deal: 里面是一些文本转格式数据的预处理脚本

文件
> crf.py 是一个仿照的简单代码 来源：https://github.com/shawntan/python-crf
> train_and_find_best_template.py  用CRF++，通过自动创建多个函数模板训练模型，并求出模型的准确率
> create_models.py 创建模型
> create_template.py 创建函数模板
> create_crf_tag_data.py 用上面训练好的模型标记待预测的数据
> create_score.py 通过被标记的文件与目标文件比较，算出准确度，并记录
> find_max_score.py 查找记录文件，得出最大准确率的模型
