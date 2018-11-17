
'''
    *********************************************
    from : https://github.com/shawntan/python-crf
    *********************************************
'''

import numpy as np
from scipy import special, optimize

START = '|-'
END = '-|'

class CRF:
    '''主要提供损失函数'''
    
    def __init__(self, feature_functions, labels, sigma=1):
        self.ft_fun = feature_functions #所有特征函数
        self.labels = [START] + labels + [END] #所有标记
        self.theta = np.random.randn(len(self.ft_fun)) #特征函数初始系数
        self.label_id = {l:i for i,l in enumerate(self.labels)} #将标记用索引表示
        
        self.sigma = sigma #正则化系数
    
    
    def all_features(self, x_vec):
        '''
        descript:
            获取一个句子的所有特征
        
        parameters:
            x_vec: 一个完整句子的切分列表
        
        return:
            一个四维张量
            axis0：t时刻或x_vec的索引
            axis1：y'，上一个的标记
            axis2：y，当前的标记
            axis3：t时刻的所有特征函数结果
        '''
        result = np.zeros((len(x_vec)+1, len(self.labels), len(self.labels), len(self.ft_fun)))
        for i in range(len(x_vec)):
            for j,yp in enumerate(self.labels):
                for k,y in enumerate(self.labels):
                    for l,f in enumerate(self.ft_fun):
                        result[i,j,k,l] = f(yp,y,x_vec,i)
        return result
    
    def create_vector_list(self, x_vecs, y_vecs):
        '''
        descript:
            将训练的词到标记的映射转换为特征集到标签id的映射
        
        parameters:
            x_vecs: 训练的句子集，里面有多条句子
            y_vecs: 对应句子的相应标记集
        
        return:
            observations: 训练数据的特征集
            labels: 训练数据对应的标签id集
        '''
        observations = [self.all_features(x_vec) for x_vec in x_vecs]
        length = len(y_vecs)
        labels = length * [None]
        
        for i in range(length):
            assert len(y_vecs[i]) == len(x_vecs[i])
            y_vecs[i].insert(0,START)
            y_vecs[i].append(END)
            labels[i] = np.array([self.label_id[y] for y in y_vecs[i]], copy=False, dtype=np.int)
        
        return (observations, labels)
    
    def forward(self, M, start=0):
        '''前向概率'''
        alphas = np.zeros((M.shape[0], M.shape[1]))
        alpha = alphas[0]
        s = alpha.shape + (1,)
        for i in range(M.shape[0]-1):
            alpha = alphas[i+1] = special.logsumexp(alpha.reshape(s)+M[i], axis=0)
        last = special.logsumexp(alpha.reshape(s)+M[-1])
        return alphas,last
    
    def backward(self, M, end=-1):
        '''后向概率'''
        betas = np.zeros((M.shape[0], M.shape[1]))
        beta = betas[-1]
        s = (1,) + beta.shape
        for i in reversed(range(M.shape[0]-1)):
            beta = betas[i] = special.logsumexp(M[i+1]+beta.reshape(s), axis=1)
        first = special.logsumexp(M[0]+beta.reshape(s), axis=1)
        return betas, first
    
    def neg_likelihood_and_deriv(self, x_vec_list, y_vec_list, theta):
        '''
        descript:
            损失函数
            
        parameters:
            x_vec_list: 训练数据的特征集，即self.create_vector_list返回的observations
            y_vec_list: 训练数据对应的标签id集，即self.create_vector_list返回的labels
            theta: 特征函数的系数
        
        return:
            loss: 误差，注：最大化条件概率等于这里最小化负对数的条件概率
        '''
        likelihood = 0 #可能性初始为0
        derivative = np.zeros(len(theta)) #导数梯度
        for x_vec,y_vec in zip(x_vec_list, y_vec_list):
            length = x_vec.shape[0] #句子长度
            yp_vec_idx = y_vec[:-1] #上一节点的label_id
            y_vec_idx = y_vec[1:] #当前节点的label_id
            all_features = x_vec
            log_M = np.dot(all_features, theta) #计算theta*f(yp,y,x_vec,i)的总和，即y'到y可能性大小
            log_alphas, last = self.forward(log_M, 0) #计算 y(i-1) --> y 的前向概率
            log_betas, first = self.backward(log_M, -1) #计算 y --> y(i+1) 的后向概率
            time, state = log_alphas.shape  #时长和标记范围
            
            log_Z = special.logsumexp(last) #"归一化因子"等于最后前向概率之和
            
            log_alphas1 = log_alphas.reshape(time,state,1) # 前向概率
            log_betas1 = log_betas.reshape(time,1,state) # 后向概率
            log_probs = log_alphas1 + log_M + log_betas1 - log_Z # 前向+转移概率+后向概率-归一化因子 ？？？
            log_probs = log_probs.reshape(log_probs.shape+(1,))
            
            exp_features = np.sum( np.exp(log_probs) * all_features, axis= (0,1,2) ) # 期望值？？
            emp_features = np.sum( all_features[range(length),yp_vec_idx,y_vec_idx], axis = 0 ) # 经验值？？
            derivative += emp_features - exp_features # 梯度？？
            
            tmp = log_M[range(length), yp_vec_idx, y_vec_idx]
            likelihood += np.sum(tmp) - log_Z
            
        loss = -likelihood + np.sum(theta**2) / (self.sigma**2) #正则化，这里不太清楚
        gradience = -derivative + np.sum(theta) / (self.sigma**2*2) # 这里也不太清楚
        return (loss, gradience)
    
    def predict(self, x_vec):
        '''
        descript:
            用viterbi算法预测句子的标记
        
        parameters:
            x_vec: 句子的单词列表
            
        return:
            单词对应的标记序列
        '''
        all_feartures = self.all_features(x_vec) #提取句子的特征函数值
        log_potential = np.dot(all_feartures, self.theta) #获取对数概率
        time = len(x_vec)
        k = len(self.labels)
        g = log_potential[1:]
        V = log_potential[0,0]
        B = np.ones((time, k), dtype=np.int)
        for t in range(1, time):
            tmp = np.zeros(k)
            for y in range(k):
                now = V + g[t-1,:,y]
                B[t,y] = b = now.argmax()
                tmp[y] = now[b]
            V = tmp
        trace = []
        y = V.argmax()
        for t in reversed(range(time)):
            trace.append(y)
            y = B[t, y]
        trace.reverse()
        return [self.labels[i] for i in trace]
        
            