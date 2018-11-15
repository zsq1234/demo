
import jpype
import os.path
import sys, time
import os
import codecs

def get_seg_data(input_file, output_file):
    """用海量分词对语料进行分词处理，获取分词的数据"""

    # jar包的路径
    hl_path = os.path.abspath('../../tool/hlSeg-5.2.15')
    jar_path = os.path.join(hl_path, u'lib')
    hlSegJarPath = os.path.join(jar_path, u'hlSegment-5.2.15.jar')

    jvmPath = jpype.getDefaultJVMPath()
	# 如果系统里安装了多个版本的java,则可以直接用下面的语句指定jvm版本
    # jvmPath = "/usr/local/jdk/jdk1.8.0_162/jre/lib/amd64/server/libjvm.so"
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % hlSegJarPath, "-Djava.ext.dirs=%s" % jar_path)
    if not jpype.isJVMStarted():
        print('JVM启动失败')
        sys.exit()
    
    # 取得类定义
    BasicSegmentor = jpype.JClass('com.hylanda.segmentor.BasicSegmentor')
    SegOption = jpype.JClass('com.hylanda.segmentor.common.SegOption')
    SegGrain = jpype.JClass('com.hylanda.segmentor.common.SegGrain')
    SegResult = jpype.JClass('com.hylanda.segmentor.common.SegResult')

	#创建分词对象
    segmentor = BasicSegmentor()
	
    dict_path = os.path.join(hl_path, 'dictionary/CoreDict.dat')
	#加载词典, 如果没有用户自定义词典，可以用下面的语句加载，自定义词典需要注意文件码制
	# if not segmentor.loadDictionary("../dictionary/CoreDict.dat", "../dictionary/userDict_utf8.txt"):
    if not segmentor.loadDictionary(dict_path, None):
        print("字典加载失败！")
        exit()
    
    #创建SegOption对象，如果使用默认的分词选项，也可以直接传空
    option = SegOption()
    option.mergeNumeralAndQuantity = False
	#可以使用下面的语句调整分词颗粒度
    # option.grainSize = SegGrain.LARGE

    # 打开文件
    try:
        input_data = codecs.open(input_file, 'r', 'utf-8')
        output_data = codecs.open(output_file, 'w', 'utf-8')

        for line in input_data.readlines():
            # 分词
            segResult = segmentor.segment(line, option)

            # 遍历存储分词结果
            word = segResult.getFirst()
            print('\n')
            while(word != None):
                output_data.write(word.wordStr + ' ')
                word = word.next
            output_data.write('\n')
        
        input_data.close()
        output_data.close()

    except:
        print('程序运行错误')
    finally:
        jpype.shutdownJVM()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = '../../data/tmp/007001-010000_sentence_data.txt'
        output_file = '../../data/tmp/007001-010000_seg_data.txt'
    get_seg_data(input_file, output_file)