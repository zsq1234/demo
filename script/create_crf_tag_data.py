import subprocess
import os
import re

file_path = '../data/test/'
file_choose = {'L1':'be_tested_label_L1_data.txt', 'L3':'be_tested_label_L3_data.txt'}
model_path = '../model/'


def create_tag_data(model_path, file_path, file_choose):
    models = []
    try:
        tmp = os.listdir(model_path)
        for i in tmp:
            if re.search(r'template_', i):
                models.append(i)
        del tmp
    except FileNotFoundError:
        print('路径错误')
    # print(models)
    if not os.path.exists(file_path+'L1tag'):
        os.mkdir(file_path+'L1tag')
    if not os.path.exists(file_path+'L3tag'):
        os.mkdir(file_path+'L3tag')
    
    for model in models:
        if re.search(r'template_L1_', model):
            create_tag(model_path+model, 
                       file_path+file_choose['L1'], 
                       file_path+'L1tag/'+model+'.txt')
        elif re.search(r'template_L3_', model):
            create_tag(model_path+model, 
                       file_path+file_choose['L3'], 
                       file_path+'L3tag/'+model+'.txt')

def create_tag(model, file, output):
    m = r'crf_test -m ' \
        + model + ' ' + file \
        + ' > ' + output
    child = subprocess.Popen(m, shell=True)
    child.wait()
    print(model, 'ok')


if __name__ == '__main__':
    create_tag_data(model_path, file_path, file_choose)