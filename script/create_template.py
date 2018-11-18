'''
    此脚本用来创建不同的特征函数模板文件
    这里我只考虑了 5， 7， 10 的选择，不是很全面，这需要改进，但想不到好的办法
'''

import codecs

def create_template(type='L1_w10_s0', time='1', unigram=None, bigram=None):
    '''
    descript:
        用来创建模板

    parameters:
        type: 文件名前缀
        time: 第time个模板
        unigram: 节点状态，是一个元组列表，每个元素为一个元组，元组长度为2，第一个数表示
                 选取的训练数据的列col，第二个数表示该列的特征函数数量5，7，10三种
        bigram: 用来存储转移状态，这里暂时还没用到
    '''
    if unigram == None:
        unigram = [(0,10)]

    template_data = codecs.open('./template/template_'+type+'_'+str(time), 'w', 'utf-8')
    template_data.write('# Unigram\n')

    index = -1
    for i in range(len(unigram)):  #迭代创建每个数据列的特征函数，每个列的特征函数数量不一定相等
        size = unigram[i][1]  #获取该列的特征函数的数量
        for j in range(size):  #逐个函数写入模板文件中
            index += 1
            k = str(unigram[i][0])
            t = '0' + str(index)
            unit = 'U' + t[-2:] + ':%x['
            if j == 0: unit += ('-2,%s]' % k)
            elif j == 1: unit += ('-1,%s]' % k)
            elif j == 2: unit += ('0,%s]' % k)
            elif j == 3: unit += ('1,%s]' % k)
            elif j == 4: unit += ('2,%s]' % k)
            # elif j == 5: unit += ('-1,'+k+']/%x[0,'+k+']')  #5, 7, 10型结果不是很好
            # elif j == 6: unit += ('0,'+k+']/%x[1,'+k+']')
            # elif j == 7: unit += ('-2,'+k+']/%x[-1,'+k+']/%x[0,'+k+']')
            # elif j == 8: unit += ('-1,'+k+']/%x[0,'+k+']/%x[1,'+k+']')
            # elif j == 9: unit += ('0,'+k+']/%x[1,'+k+']/%x[2,'+k+']')
            elif j == 5: unit += ('-2,'+k+']/%x[-1,'+k+']/%x[0,'+k+']')  #改用5, 8, 10型的看看
            elif j == 6: unit += ('-1,'+k+']/%x[0,'+k+']/%x[1,'+k+']')
            elif j == 7: unit += ('0,'+k+']/%x[1,'+k+']/%x[2,'+k+']')
            elif j == 8: unit += ('-1,'+k+']/%x[0,'+k+']') 
            elif j == 9: unit += ('0,'+k+']/%x[1,'+k+']')
            template_data.write(unit+'\n')
        template_data.write('\n')
    
    template_data.write('# Bigram\nB\n\n')  #模板有Bigram的特征函数区，虽然没用到但也写出该区，只是为空而已

    template_data.close()

if __name__ == '__main__':
    create_template()
            

