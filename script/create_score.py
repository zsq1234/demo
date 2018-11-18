'''
    此脚本用来计算模型的精准度、召回率和f-score值
'''

import sys
import os
import codecs
import re

file_path = r'../data/test/'
tag_dir_choose = {'L1':'L1tag/', 'L3':'L3tag/'}  #用模型产生的标记文件目录
goal_file = r'../data/test/test_goal_data.txt'  #要对比的目标文件


def score(file_path, tag_dir_choose, goal_file):
    '''
    descript:
        分别计算L1和L3标记的预测准确度
    '''
    L1_tags = []
    try:
        #获取所有L1模型产生的文件名列表
        tmp = os.listdir(file_path+tag_dir_choose['L1'])
        for i in tmp:
            if re.search(r'template_', i):
                L1_tags.append(i)
        del tmp
    except FileNotFoundError:
        print('路径错误')
    for tag_file in L1_tags:  #计算所有L1模型的准确率，每个模型对应一个模型产生的标记文件
        L1_score(file_path+tag_dir_choose['L1']+tag_file, 
                 goal_file, 
                 file_path+'L1_score.txt')
    
    L3_tags = []
    try:
        #获取所有L3模型产生的文件名列表
        tmp = os.listdir(file_path+tag_dir_choose['L3'])
        for i in tmp:
            if re.search(r'template_', i):
                L3_tags.append(i)
        del tmp
    except FileNotFoundError:
        print('路径错误')
    for tag_file in L3_tags:  #计算所有L3模型的准确率，每个模型对应一个模型产生的标记文件
        L3_score(file_path+tag_dir_choose['L3']+tag_file, 
                 goal_file, 
                 file_path+'L3_score.txt')
                 
    return ('L1_score.txt', 'L3_score.txt')

def L1_score(tag_file, goal_file, score_file):
    '''
    descript:
        L1模型准确率计算，将所有L1模型的测试数据写到同个scroe记录文件
    '''
    tag_data = codecs.open(tag_file, 'r', 'utf-8')
    goal_data = codecs.open(goal_file, 'r', 'utf-8')
    score_data = codecs.open(score_file, 'a', 'utf-8')

    score_data.write('\n================ %s 结果==================\n' % tag_file.split('/')[-1])
    # score 第一行第一列位置存储模型的预测正确的个数，第一行第二列存储模型预测错误的个数
    #       第二行第一列存储模型没有预测到的而实际应该标记的个数
    score = [[0,0], [0,0]]  

    for (tag_line, goal_line) in zip(tag_data, goal_data):  #逐行读取文件并比较标记
        if tag_line == '\n':
            continue
        
        tag_words = tag_line.strip().split('\t')
        goal_words = goal_line.strip().split('\t')

        if tag_words[4] == 'E' or tag_words[4] == 'S':  #只考虑L1划分位置，不比较BMO，因为ES便是标记的划分位置
            if goal_words[3] == 'E' or goal_words[3] == 'S':
                score[0][0] += 1
            else:
                score[0][1] += 1
        else:
            if goal_words[3] == 'E' or goal_words[3] == 'S':
                score[1][0] += 1
            else:
                score[1][1] += 1
    print(score)
    precision = score[0][0] /float(score[0][0] + score[0][1])  #计算准确率
    recall = score[0][0] / float(score[0][0] + score[1][0])  #计算召回率
    f_score = 2*precision*recall / float(precision+recall)  #计算f-score

    all = score[0][0] + score[1][0]
    score_data.write('总共划分数：' + str(all) + '\n')
    score_data.write('实验划分正确：' + str(score[0][0]) + '\n')
    score_data.write('实验划分错误：' + str(score[0][1]) + '\n')
    score_data.write('遗漏的划分：' + str(score[1][0]) + '\n\n')
    score_data.write('预准率：' + str(precision) + '\n')
    score_data.write('召回率：' + str(recall) + '\n')
    score_data.write('f-score: '+str(f_score)+'\n')
    score_data.write('===========================================\n')

    # print('预准率：' + str(precision))
    # print('召回率：' + str(recall))
    # print('f-score: '+str(f_score))

    tag_data.close()
    goal_data.close()
    score_data.close()

def L3_score(tag_file, goal_file, score_file):
    '''
    descript:
        L3模型准确率计算，将所有L3模型的测试数据写到同个scroe记录文件
    '''
    tag_data = codecs.open(tag_file, 'r', 'utf-8')
    goal_data = codecs.open(goal_file, 'r', 'utf-8')
    score_data = codecs.open(score_file, 'a', 'utf-8')

    score_data.write('================ %s 结果==================\n' % tag_file.split('/')[-1])
    # score 第一行第一列位置存储模型的预测正确的个数，第一行第二列存储模型预测错误的个数
    #       第二行第一列存储模型没有预测到的而实际应该标记的个数
    score = [[0,0], [0,0]]

    for (tag_line, goal_line) in zip(tag_data, goal_data):  #逐行读取文件并比较标记
        if tag_line == '\n':
            continue
        
        tag_words = tag_line.strip().split('\t')
        goal_words = goal_line.strip().split('\t')

        if tag_words[5] == 'E' or tag_words[5] == 'S':  #只考虑L1划分位置，不比较BMO，因为ES便是标记的划分位置
            if goal_words[4] == 'E' or goal_words[4] == 'S':
                score[0][0] += 1
            else:
                score[0][1] += 1
        else:
            if goal_words[4] == 'E' or goal_words[4] == 'S':
                score[1][0] += 1
            else:
                score[1][1] += 1
    print(score)
    precision = score[0][0] /float(score[0][0] + score[0][1])  #计算准确率
    recall = score[0][0] / float(score[0][0] + score[1][0])  #计算召回率
    f_score = 2*precision*recall / float(precision+recall)  #计算f-score

    all = score[0][0] + score[1][0]
    score_data.write('总共划分数：' + str(all) + '\n')
    score_data.write('实验划分正确：' + str(score[0][0]) + '\n')
    score_data.write('实验划分错误：' + str(score[0][1]) + '\n')
    score_data.write('遗漏的划分：' + str(score[1][0]) + '\n\n')
    score_data.write('预准率：' + str(precision) + '\n')
    score_data.write('召回率：' + str(recall) + '\n')
    score_data.write('f-score: '+str(f_score)+'\n')
    score_data.write('===========================================\n')

    # print('预准率：' + str(precision))
    # print('召回率：' + str(recall))
    # print('f-score: '+str(f_score))

    tag_data.close()
    goal_data.close()
    score_data.close()

if __name__ == '__main__':
    # score(file_path, tag_dir_choose, goal_file)
    L1_score('../data/test/tag_data.txt', '../data/test/test_goal_data.txt', '../data/test/a.txt')
