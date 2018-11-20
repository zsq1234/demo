import sys
import re
import codecs

def make_crf_tested_label_L1_data(sentence_file, output_file, has_nature=False):
    """将数据转为CRF可识别的L1被测试数据"""
    sentence_data = codecs.open(sentence_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    
    # 按每条句子顺序处理
    for sentence in sentence_data.readlines():

        sentence = sentence.strip()

        for char in sentence:
            if has_nature:
                t = char + '\t1\t1\tB\to'
            t = char + '\t1\t1\tB'
            output_data.write()
        output_data.write('\n')
    
    sentence_data.close()
    output_data.close()

def make_crf_tested_label_L3_data(sentence_file, output_file):
    """将数据转为CRF可识别的L3被测试数据"""
    sentence_data = codecs.open(sentence_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    
    # 按每条句子顺序处理
    for sentence in sentence_data.readlines():

        sentence = sentence.strip()

        for char in sentence:
            output_data.write(char + '\t1\t1\tB\tB\n')
        output_data.write('\n')
    
    sentence_data.close()
    output_data.close()

def make_test_data(sentence_file, output_file):
    """将数据转为CRF可识别的L3被测试数据"""
    sentence_data = codecs.open(sentence_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    
    # 按每条句子顺序处理
    for sentence in sentence_data.readlines():

        sentence = sentence.strip()

        for char in sentence:
            output_data.write(char + '\n')
        output_data.write('\n')

    sentence_data.close()
    output_data.close()


if __name__ == '__main__':
    make_test_data('../../data/tmp/000001-007000.txt',
                    '../../data/test/test.txt')
