'''
    此脚本用于创建不同模板对应的模型
'''

import subprocess
import codecs
import create_template

L1_cols = (0, 1, 2)  #L1标签训练有词，分词列1，分词列2的可知数据，对应序号0，1，2
L3_cols = (0, 1, 2, 3)  #L3标签训练有词，分词列1，分词列2，L1列的可知数据，对应序号0，1，2，3
# step_choose = (5, 7, 10)  #函数模板的函数数量，这里只用到5，7，10
step_choose = (5, 8, 10)

# U00:%x[-2,0]
# U01:%x[-1,0]
# U02:%x[0,0]
# U03:%x[1,0]
# U04:%x[2,0]     =============>> 上面的step_choose 5 意思只有U00-U04的特征函数
# U05:%x[-1,0]/%x[0,0]
# U06:%x[0,0]/%x[1,0]  =================>> 上面的step_choose 7 意思有U00-U06的特征函数
# U07:%x[-2,0]/%x[-1,0]/%x[0,0]
# U08:%x[-1,0]/%x[0,0]/%x[1,0]
# U09:%x[0,0]/%x[1,0]/%x[2,0]  ==============>> 上面的step_choose 10 意思有U07-U09的特征函数

model_path = '../model/'
template_path = './template/'

def get_models(L1_cols, L3_cols, step_choose, template_path, model_path):
    '''
    descript:
        获取多个L1,L3训练模型
    '''
    template_list = []
    template_list += get_L1_templates(L1_cols, step_choose, template_path, model_path)
    template_list += get_L3_templates(L3_cols, step_choose, template_path, model_path)
    get_template_model(template_list, template_path, model_path)

def get_L1_templates(L1_cols, step_choose, template_path, model_path):
    '''
    descript:
        将词列数据和分词列数据组合使用，按不同的特征函数的数量创建L1模板，
        对不同的模板用 template_L1_w:i_s:j 命名
        上面的 :i = 5|7|10, 对应特征函数数量
        上面的 :j = 0|5|7|10, 对应特征函数数量

    return:
        返回模板名列表
    '''
    time = 0
    template_list = []  #存储模板文件名的列表

    # 只用word，没用分词
    for i in step_choose:
        type = 'L1_w'+str(i)+'_s0'
        time += 1
        name = 'template_'+type+'_'+str(time)
        unigram = [(0, i)]
        create_template.create_template(type, time, unigram)  #创建模板
        template_list.append(name)
    
    # 用word和分词的数据
    for i in step_choose:
        for j in step_choose:
            type = 'L1_w'+str(i)+'_s'+str(j)
            time += 1
            name = 'template_'+type+'_'+str(time)
            unigram = [(0,i), (1,j), (2,j)]
            create_template.create_template(type, time, unigram)  #创建模板
            template_list.append(name)
    
    return template_list
    

def get_L3_templates(L3_cols, step_choose, template_path, model_path):
    '''
    descript:
        将词列数据，分词列数据和L1列数据组合使用，按不同的特征函数的数量创建L3模板，
        对不同的模板用 template_L3_w:i_s:j_L:k 命名
        上面的 :i = 5|7|10, 对应特征函数数量
        上面的 :j = 0|5|7|10, 对应特征函数数量
        上面的 :k = 0|5|7|10, 对应特征函数数量
        
    return:
        返回模板名列表
    '''
    time = 0
    template_list = []  #存储模板文件名的列表

    # 只用word，没用分词和L1
    for i in step_choose:
        type = 'L3_w'+str(i)+'_s0_L0'
        time += 1
        name = 'template_'+type+'_'+str(time)
        unigram = [(0, i)]
        create_template.create_template(type, time, unigram)  #创建模板
        template_list.append(name)
    
    # 用word和分词的数据
    for i in step_choose:
        for j in step_choose:
            type = 'L3_w'+str(i)+'_s'+str(j)+'_L0'
            time += 1
            name = 'template_'+type+'_'+str(time)
            unigram = [(0,i), (1,j), (2,j)]
            create_template.create_template(type, time, unigram)  #创建模板
            template_list.append(name)
    
    # 用word和L1的数据
    for i in step_choose:
        for j in step_choose:
            type = 'L3_w'+str(i)+'_s0_L'+str(j)
            time += 1
            name = 'template_'+type+'_'+str(time)
            unigram = [(0,i), (3,j)]
            create_template.create_template(type, time, unigram)  #创建模板
            template_list.append(name)
    
    # 用word、分词和L1的数据
    for i in step_choose:
        for j in step_choose:
            for k in step_choose:
                type = 'L3_w'+str(i)+'_s'+str(j)+'_L'+str(k)
                time += 1
                name = 'template_'+type+'_'+str(time)
                unigram = [(0,i), (1,j), (2,j), (3,k)]
                create_template.create_template(type, time, unigram)  #创建模板
                template_list.append(name)
    
    return template_list
    

def get_template_model(template_list, template_path, model_path):
    '''
    descript:
        按不同模板训练产生模型
        直接调用系统命令 'crf_learn -f 3 -c 4.0 template tran_data.txt model'
        -f 3：表示频数至少为3的词可被录用训练
        -c 4.0：表示代价参数 ？？，过大可能会过拟合
    '''
    for name in template_list:
        m = r'crf_learn -f 3 -c 4.0 ' \
            + template_path + name \
            +' ../data/train/train_label_L3_data.txt ' \
            + model_path + name + '_model'
        child = subprocess.Popen(m, shell=True)
        child.wait()
        print('ok')

    # name = r'template_L1_w5_s0_1'
    # m = r'crf_learn -f 3 -c 4.0 ' \
    #     + template_path + name \
    #     + r' ../data/train/train_label_L3_data.txt ' \
    #     + model_path + name + r'_model'
    # child = subprocess.Popen(m, shell=True)
    # child.wait()
    # print('ok')

if __name__ == '__main__':
    get_models(L1_cols, L3_cols, step_choose, template_path, model_path)
    # get_template_model([], template_path, model_path)
