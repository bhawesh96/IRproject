import math
import time
from copy import deepcopy

def change_to_gap(dic,wrd):
    for i in range(len(dic[wrd])-1,0,-1):
        dic[wrd][i] -= dic[wrd][i-1]
def change_to_doc(dic,wrd):
    for i in range(1,len(dic[wrd])):
        dic[wrd][i] += dic[wrd][i-1]
        
def prepend(bytes, x):
    bytes.insert(0,x)
    
def extend(bytesstr, bytes):
    bytesstr = bytesstr + bytes
    return bytesstr
    
def VBEncodeNumber(n):
    bytes= []
    while(1):
        prepend(bytes, n % 4)
        if(n<4):
            break
        else:
            n=math.floor(n/4)
    bytes[-1]+=4
    return bytes

def VBEncode(numbers):
    bytesstr=[]
    for n in numbers:
        bytes= VBEncodeNumber(n)
        bytesstr=extend(bytesstr,bytes)
    return bytesstr

def VBDecode(bytestream):
    numbers=[]
    n=0
    for i in range(len(bytestream)):
        if bytestream[i] < 4:
            n = 4*n + bytestream[i]
        else:
            n = 4*n + (bytestream[i]-4)
            numbers.append(n)
            n=0
    return numbers    


def myIR_Model(q):
    n = 10
    docs_dict = {1: 't1', 2: 't2', 3: 't3', 4: 't4', 5: 't5', 6: 't6', 7: 't7', 8: 't8', 9: 't9', 10: 't10'}
    start_time = time.time()
    term_dict = {}
    for i,j in enumerate(list(docs_dict.values()),start=1):
        with open(j,'r') as f:
            for line in f:
                for word in line.split():
                    word = word.strip('.,!?:;-)("\'][').lower()
                    #print(i)
                    term_dict.setdefault(word,[]).append(i)
    for i in term_dict.keys():
        term_dict[i] = sorted(list(set(term_dict[i])))
    ##print(term_dict,end='\n\n\n\n')

    for i in term_dict.keys():
        change_to_gap(term_dict,i)
    ##print(term_dict)

    for i in term_dict.keys():
        term_dict[i] = VBEncode(term_dict[i])

    ##print(term_dict)

    #print(time.time()-start_time)
    #q = query
    q_li = q.split()
    for i,j in enumerate(q_li):
        q_li[i] = j.strip('.,!?:;-)("\'][').lower()
    #print(q_li)

    VBEncodedGaplist_dict={}
    for q_term in q_li:
        VBEncodedGaplist_dict[q_term] = term_dict.setdefault(q_term,[])

    #print(VBEncodedGaplist_dict)

    gaplist_dict = {}
    for i in q_li:
        gaplist_dict[i] = VBDecode(VBEncodedGaplist_dict[i])
    #print(gaplist_dict)

    postinglist_dict={}
    for i in q_li:
        postinglist_dict[i]=deepcopy(gaplist_dict[i])
        change_to_doc(postinglist_dict,i)
    #print(postinglist_dict)
    
    final_ans_dict = {}
    for i in q_li:
        final_ans_dict[i] = (i,VBEncodedGaplist_dict[i], gaplist_dict[i], postinglist_dict[i])
    return (final_ans_dict)