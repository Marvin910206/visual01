import jieba
from collections import Counter
# 開啟紀錄檔
with open('D:\\marvin\Desktop\\Programming\\專案\\recordanalysis\\record.txt', 'r', encoding='utf8') as f:
    record = f.read()

# 文本處理
def record_preprocess():
    # 載入jieba
    jieba.set_dictionary('D:\\marvin\Desktop\\Programming\\專案\\recordanalysis\\dict.txt')
    with open('D:\\marvin\Desktop\\Programming\\專案\\recordanalysis\\stops.txt', 'r', encoding='utf8') as f:
        stops = f.read().split()
    # 載入自定義症狀
    with open('D:\\marvin\Desktop\\Programming\\專案\\recordanalysis\\symptom.txt', encoding="utf-8") as f:
        symptom = f.read().split()
    stops.append('\n')
    stops.append('\n\n')
    new_stopwords = ['月','度','歲']
    stops.extend(new_stopwords)
    terms = [t for t in jieba.cut(record, cut_all=False) if t not in stops and t in symptom]

# 提取症狀
def record_analysis():
    # 呼叫文本處理
    record_preprocess()
    # 方法一
    wordcount = {}
    for word in terms:
        wordcount[word] = wordcount.get(word, 0)+1
    sorted(wordcount.items(), key=lambda x: x[1], reverse=True)[:10]
    # 方法二
    wordcount = Counter(terms)
    print(wordcount.most_common(10))

if __name__=="__main__":
    record_analysis()