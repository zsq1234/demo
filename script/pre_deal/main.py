import os
import make_sentence, get_seg_data, make_crf_train_data, make_crf_test_data

# 相关路径配置
raw_files = ['../../data/raw/000001-007000.txt', '../../data/raw/007001-010000.txt']
tmp_path = '../../data/tmp/'
train_path = '../../data/train/'
test_path = '../../data/test/'

sentence_files = []  # 成句的文件

for file in raw_files:
    path, name = os.path.split(file)
    t = tmp_path + name 
    make_sentence.make_sentence(file, t)  # 将有标贝的语料合成完整句子
    sentence_files.append(t)

seg_files = []  # 分词的文件

for file in sentence_files:
    path, name = os.path.split(file)
    name, ext = os.path.splitext(name)
    t = tmp_path + name + '_seg_data' + ext
    get_seg_data.get_seg_data(file, t)
    seg_files.append(t)


name = os.path.split(raw_files[0])[1]
make_crf_train_data.make_crf_train_label_L1_data(seg_files[0], raw_files[0], train_path + 'L1-' + name)
make_crf_train_data.make_crf_train_label_L2_data(seg_files[0], raw_files[0], train_path + 'L2-' + name)
make_crf_train_data.make_crf_train_label_L3_data(seg_files[0], raw_files[0], train_path + 'L3-' + name)

make_crf_train_data.make_crf_train_label_L2_data(seg_files[1], raw_files[1], test_path + 'L2_goal.txt')
make_crf_train_data.make_crf_train_label_L3_data(seg_files[1], raw_files[1], test_path + 'L3_goal.txt')


make_crf_test_data.make_crf_tested_label_L1_data(sentence_files[1], test_path + 'L1_test.txt')
make_crf_test_data.make_crf_tested_label_L3_data(sentence_files[1], test_path + 'L2_or_L3_test.txt')
