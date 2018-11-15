
import codecs
import sys
import re

def make_sentence(input_file, output_file):
    '''将语料提取成完整句子，供海量分词使用'''
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file,'w', 'utf-8')
    is_pinyin_line = False

    for line in input_data.readlines():
        if is_pinyin_line:
            is_pinyin_line = False
            continue
        else:
            is_pinyin_line = True

        words = line.strip().split()[1]
        # 替换所有韵律标记为空字符串
        sentence = re.sub('#[0-4]', '', words)
        output_data.write(sentence + '\n')
    
    input_data.close()
    output_data.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = '../../data/raw/007001-010000.txt'
        output_file = '../../data/tmp/007001-010000_sentence_data.txt'
    make_sentence(input_file, output_file)
        