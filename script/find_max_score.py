
import codecs
import re

def find_max(file_path, score_choose, record_file):
    for file in score_choose:
        find_max_score(file_path+file, file_path+record_file)

def find_max_score(score_file, record_file):
    score_data = codecs.open(score_file, 'r', 'utf-8')
    record_data = codecs.open(record_file, 'a', 'utf-8')
    model = [['',0,0,0],['',0,0,0],['',0,0,0]]
    tmp = ''
    pre = 0
    rec = 0
    f_score = 0
    for score_line in score_data.readlines():
        if score_line == '\n':
            continue
        elif score_line[:6] == '======':
            score_line = re.sub(r'=', '', score_line)
            if len(score_line) > 8:
                tmp = score_line.split()[0]
            else:
                if model[0][1] < pre or model[0][1] == pre and model[0][2] < rec:
                    model[0] = [tmp, pre, rec, f_score]
                if model[1][2] < rec or model[1][2] == rec and model[1][1] < pre:
                    model[1] = [tmp, pre, rec, f_score]
                if model[2][3] < f_score or model[2][3] == f_score and (
                    model[2][1] < pre or model[2][2] < rec):
                    model[2] = [tmp, pre, rec, f_score]
            pre = rec = f_score = 0
        elif score_line.find(u'预准率：') != -1:
            pre = float(score_line.strip().split(r'：')[1])
        elif score_line.find(u'召回率：') != -1:
            rec = float(score_line.strip().split(r'：')[1])
        elif score_line.find(u'f-score: ') != -1:
            f_score = float(score_line.strip().split(r': ')[1])
    
    record_data.write('=================最大预准率模型====================\n')
    record_data.write('模型：%s\n预准率：%f\n召回率：%f\nf_score：%f\n'
                       % tuple(model[0]))
    record_data.write('==================================================\n\n')
    record_data.write('=================最大召回率模型====================\n')
    record_data.write('模型：%s\n预准率：%f\n召回率：%f\nf_score：%f\n'
                       % tuple(model[1]))
    record_data.write('==================================================\n\n')
    record_data.write('=================最大f-score模型====================\n')
    record_data.write('模型：%s\n预准率：%f\n召回率：%f\nf_score：%f\n'
                       % tuple(model[2]))
    record_data.write('==================================================\n\n')
    score_data.close()
    record_data.close()
    print(model)

if __name__ == '__main__':
    find_max_score('../data/test/L3_score_5710.txt', '../data/test/max_score.txt')

        
