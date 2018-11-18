'''
    此脚本用来启动训练，原理是先写出多个特征模板，
    用这些模板训练多个模型，接着用模型产生对应的标
    记文件，用这些标记文件和test文件对比计算模型的
    准确率，找出最大的f-score
'''

import create_models
import create_crf_tag_data
import create_score
import find_max_score

L1_cols = (0, 1, 2)  #L1训练有词列，分词列1，分词列2，对应序号0，1，2
L3_cols = (0, 1, 2, 3)  #L3训练有词列，分词列1，分词列2，L1标记列，对应序号0，1，2，3
# step_choose = (5, 7, 10)  #特征函数有5，7，10的数量选择
step_choose = (5, 8, 10)  #发现5，7，10的训练后结果都不是很好，改用5，8，10

model_path = r'../model/'  #模型的存储路径
template_path = r'./template/'  #模板的存储路径

file_path = r'../data/test/'  #测试文件的存储路径
file_choose = {'L1':'be_tested_label_L1_data.txt', 'L3':'be_tested_label_L3_data.txt'}  #L1的要被模型标记的文件，L3的要被模型标记的文件

tag_dir_choose = {'L1':'L1tag/', 'L3':'L3tag/'}  #标记文件的存储目录
goal_file = r'../data/test/test_goal_data.txt'  #要对比的目标文件
record_file = r'max_score.txt'  #记录分数的最大情况

# 1. 训练多个模型
create_models.get_models(L1_cols,
                         L3_cols, 
                         step_choose, 
                         template_path,
                         model_path)
# 2. 用训练的模型标记文件
create_crf_tag_data.create_tag_data(model_path, file_path, file_choose)
# 3. 让标记文件与目标文件对比，计算准确率等数
score_files = create_score.score(file_path, tag_dir_choose, goal_file)
# 4. 查找最大分数模型
find_max_score.find_max(file_path, score_files, record_file)
