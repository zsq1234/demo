import sys
import re
import codecs

def make_crf_train_label_L3_data(seg_file, label_file, output_file, has_nature=False):
    """将数据转为CRF可识别的L3训练数据"""
    seg_data = codecs.open(seg_file, 'r', 'utf-8')
    label_data = codecs.open(label_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    is_pinyin_sentence = False
    ch_punctuation = u"[？，。‘’：；《》【】『』（）、！～——“”]"
    
    # 按每条句子顺序处理
    for (seg_line, label_line) in zip(seg_data.readlines(),
        label_data.readlines()):

        # 语料的拼音行不读
        if is_pinyin_sentence:
            is_pinyin_sentence = False
            continue
        else:
            is_pinyin_sentence = True
        
        # 每个单词或标点的标记用字典存储，并把所有字典存储在列表中
        # 1. 获取分词数据
        crf_tmp_data = deal_segement_data(seg_line, has_nature=has_nature)

        # 2. 获取L1数据
        l1_words = re.split(r'#0|#1|#2|#3|#4', label_line.strip().split()[1])
        # 句子中对应的每个单词或标点的索引初始为0
        crf_tmp_data_idx = 0
        # print(word_l1)
        for word in l1_words:
            w_len = len(word)
            w_idx = 0
            # 判断是否为标点，并标记
            while True:
                char = word[w_idx]
                # 正则化判断是否为中文标点
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                    w_idx += 1
                    crf_tmp_data_idx += 1
                else:
                    break
                if w_len - w_idx <= 0:
                    break
            # 判断是否到词组结尾
            if (w_len - w_idx) <= 0:
                continue
            # 判断是否为单字词
            elif (w_len - w_idx) == 1:
                type(word[w_idx])
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('S')
                crf_tmp_data_idx += 1
                continue
            # 词组用BME标记
            else:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('B')
                w_idx += 1
                crf_tmp_data_idx += 1
            while w_idx < w_len-1:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('M')
                w_idx += 1
                crf_tmp_data_idx += 1
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('E')
            crf_tmp_data_idx += 1

        # 3. 获取L3数据
        l3_word = re.split(r'#3|#4', label_line.strip().split()[1])
        # 句子中对应的每个单词或标点的索引初始为0
        crf_tmp_data_idx = 0
        first = True
        for word in l3_word:
            # 将词组中的原有#1、#2等标记去掉
            word = re.sub(r'#[0-4]', '', word)
            w_len = len(word)
            w_idx = 0
            # 判断并标记中文标点符号
            while True:
                char = word[w_idx]
                # 正则化判断是否为中文标点
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                    w_idx += 1
                    crf_tmp_data_idx += 1
                else:
                    break
                if w_len - w_idx <= 0:
                    break
            # 判断是否到词组结尾
            if (w_len - w_idx) <= 0:
                continue
            # 判断是否为单字词
            elif (w_len - w_idx) == 1:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('S')
                crf_tmp_data_idx += 1
                continue
            # print(idx, tmp[idx], w[begin])
            # 进行BME标记
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('B')
            w_idx += 1
            crf_tmp_data_idx += 1
            while w_idx < w_len - 1:
                # print(idx, tmp[idx], w[i])
                char = word[w_idx]
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                else:
                    crf_tmp_data[crf_tmp_data_idx][char].append('M')
                w_idx += 1
                crf_tmp_data_idx += 1
            # print(idx, tmp[idx], w[i])
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('E')
            crf_tmp_data_idx += 1

        crf_tmp_data_len = len(crf_tmp_data)
        # 将该行的标记存储到文件中
        for i in range(0, crf_tmp_data_len):
            dict_i = crf_tmp_data[i]
            char = list(dict_i.keys())[0]
            label = list(dict_i.values())[0]
            output_data.write(char)
            for i in label:
                output_data.write('\t' + i)
            output_data.write('\n')
        output_data.write('\n')
    
    seg_data.close()
    label_data.close()
    output_data.close()

def make_crf_train_label_L2_data(seg_file, label_file, output_file, has_nature=False):
    """将数据转为CRF可识别的L2训练数据"""
    seg_data = codecs.open(seg_file, 'r', 'utf-8')
    label_data = codecs.open(label_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    is_pinyin_sentence = False
    ch_punctuation = u"[？，。‘’：；《》【】『』（）、！～——“”]"
    
    # 按每条句子顺序处理
    for (seg_line, label_line) in zip(seg_data.readlines(),
                                        label_data.readlines()):

        # 语料的拼音行不读
        if is_pinyin_sentence:
            is_pinyin_sentence = False
            continue
        else:
            is_pinyin_sentence = True

        # 每个单词或标点的标记用字典存储，并把所有字典存储在列表crf_tmp_data中
        # 1. 获取分词数据
        crf_tmp_data = deal_segement_data(seg_line, has_nature=has_nature)        

        # 2. 获取L1数据
        l1_words = re.split(r'#0|#1|#2|#3|#4', label_line.strip().split()[1])
        # 句子中对应的每个单词或标点的索引初始为0
        crf_tmp_data_idx = 0
        # print(word_l1)
        for word in l1_words:
            w_len = len(word)
            w_idx = 0
            # 判断是否为标点，并标记
            while True:
                char = word[w_idx]
                # 正则化判断是否为中文标点
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                    w_idx += 1
                    crf_tmp_data_idx += 1
                else:
                    break
                if w_len - w_idx <= 0:
                    break
            # 判断是否到词组结尾
            if (w_len - w_idx) <= 0:
                continue
            # 判断是否为单字词
            elif (w_len - w_idx) == 1:
                type(word[w_idx])
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('S')
                crf_tmp_data_idx += 1
                continue
            # 词组用BME标记
            else:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('B')
                w_idx += 1
                crf_tmp_data_idx += 1
            while w_idx < w_len-1:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('M')
                w_idx += 1
                crf_tmp_data_idx += 1
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('E')
            crf_tmp_data_idx += 1

        # 3. 获取L2数据
        l2_word = re.split(r'#2|#3|#4', label_line.strip().split()[1])
        # 句子中对应的每个单词或标点的索引初始为0
        crf_tmp_data_idx = 0
        first = True
        for word in l2_word:
            # 将词组中的原有#1等标记去掉
            word = re.sub(r'#[0-4]', '', word)
            w_len = len(word)
            w_idx = 0
            # 判断并标记中文标点符号
            while True:
                char = word[w_idx]
                # 正则化判断是否为中文标点
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                    w_idx += 1
                    crf_tmp_data_idx += 1
                else:
                    break
                if w_len - w_idx <= 0:
                    break
            # 判断是否到词组结尾
            if (w_len - w_idx) <= 0:
                continue
            # 判断是否为单字词
            elif (w_len - w_idx) == 1:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('S')
                crf_tmp_data_idx += 1
                continue
            # print(idx, tmp[idx], w[begin])
            # 进行BME标记
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('B')
            w_idx += 1
            crf_tmp_data_idx += 1
            while w_idx < w_len - 1:
                # print(idx, tmp[idx], w[i])
                char = word[w_idx]
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                else:
                    crf_tmp_data[crf_tmp_data_idx][char].append('M')
                w_idx += 1
                crf_tmp_data_idx += 1
            # print(idx, tmp[idx], w[i])
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('E')
            crf_tmp_data_idx += 1

        crf_tmp_data_len = len(crf_tmp_data)
        # 将该行的标记存储到文件中
        for i in range(0, crf_tmp_data_len):
            dict_i = crf_tmp_data[i]
            char = list(dict_i.keys())[0]
            label = list(dict_i.values())[0]
            output_data.write(char)
            for i in label:
                output_data.write('\t' + i)
            output_data.write('\n')
        output_data.write('\n')
    
    seg_data.close()
    label_data.close()
    output_data.close()

def make_crf_train_label_L1_data(seg_file, label_file, output_file, has_nature=False):
    """将数据转为CRF可识别的L1训练数据"""
    seg_data = codecs.open(seg_file, 'r', 'utf-8')
    label_data = codecs.open(label_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    is_pinyin_sentence = False
    ch_punctuation = u"[？，。‘’：；《》【】『』（）、！～——“”]"
    
    # 按每条句子顺序处理
    for (seg_line, label_line) in zip(seg_data.readlines(),
                                        label_data.readlines()):

        # 语料的拼音行不读
        if is_pinyin_sentence:
            is_pinyin_sentence = False
            continue
        else:
            is_pinyin_sentence = True
        
        # 每个单词或标点的标记用字典存储，并把所有字典存储在列表中
        # 1. 获取分词数据
        crf_tmp_data = deal_segement_data(seg_line, has_nature=has_nature)

        # 2. 获取L1数据
        l1_words = re.split(r'#0|#1|#2|#3|#4', label_line.strip().split()[1])
        # 句子中对应的每个单词或标点的索引初始为0
        crf_tmp_data_idx = 0
        for word in l1_words:
            w_len = len(word)
            w_idx = 0
            # 判断是否为标点，并标记
            while True:
                char = word[w_idx]
                # 正则化判断是否为中文标点
                if re.search(ch_punctuation, char.encode('utf-8').decode('utf-8')):
                    crf_tmp_data[crf_tmp_data_idx][char].append('O')
                    w_idx += 1
                    crf_tmp_data_idx += 1
                else:
                    break
                if w_len - w_idx <= 0:
                    break
            # 判断是否到词组结尾
            if (w_len - w_idx) <= 0:
                continue
            # 判断是否为单字词
            elif (w_len - w_idx) == 1:
                type(word[w_idx])
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('S')
                crf_tmp_data_idx += 1
                continue
            # 词组用BME标记
            else:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('B')
                w_idx += 1
                crf_tmp_data_idx += 1
            while w_idx < w_len-1:
                crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('M')
                w_idx += 1
                crf_tmp_data_idx += 1
            crf_tmp_data[crf_tmp_data_idx][word[w_idx]].append('E')
            crf_tmp_data_idx += 1

        crf_tmp_data_len = len(crf_tmp_data)
        # 将该行的标记存储到文件中
        for i in range(0, crf_tmp_data_len):
            dict_i = crf_tmp_data[i]
            char = list(dict_i.keys())[0]
            label = list(dict_i.values())[0]
            output_data.write(char)
            for i in label:
                output_data.write('\t' + i)
            output_data.write('\n')
        output_data.write('\n')
    
    seg_data.close()
    label_data.close()
    output_data.close()

def deal_segement_data(seg_line, has_nature=False):
    data = []
    seg_words = seg_line.strip().split()
    for word in seg_words:
        if has_nature:
            t = word.split('/')
            word = t[0]; nature = t[1]
        w_len = len(word)
        if w_len == 1:
            if has_nature:
                data.append({word: ['1', '1', nature]})
            else:
                data.append({word: ['1', '1']})
        else:
            for i in range(0, w_len):
                if has_nature:
                    data.append({word[i]: [str(i+1), str(w_len-i), nature]})
                else:
                    data.append({word[i]: [str(i+1), str(w_len-i)]})
    return data

if __name__ == '__main__':
    make_crf_train_label_L3_data('../../data/tmp/000001-007000_seg_data.txt', 
                                 '../../data/raw/000001-007000.txt',
                                 '../../data/train/L-000001-007000.txt', 
                                 has_nature=True)
