#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import Counter
import os
import re
import jieba
import jieba.analyse
from chardet import UniversalDetector
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_tag(all_text):
    # 获取所有标签
    tag_info = re.findall('[\\u4e00-\\u9fa5]{2,}:| 【[\\u4e00-\\u9fa5]{2,}】', all_text)
    i = 0
    while i < len(tag_info):
        # tag_info[i] = tag_info[i].strip(":：【】[]")
        tag_info[i] = re.sub(r"[:： 【】\[\]]+", "", tag_info[i])
        i = i + 1
    # tag_info_str="、".join(tag_info)
    # # print(set(tag_info))
    return tag_info


def cut_word(data, filter=False):
    # 对文件中的非法字符进行过滤
    if filter is True:
        data = re.sub(r"[\s+!/_$%^*(【】：\]\[\-;\"\']+|[+—！。？~@#￥%…&*（）]+|[0-9]+", "", data)
    # jieba.enable_parallel(6)
    word_list = jieba.cut(data, HMM=True)
    # print(word_list)
    return word_list


# 词频统计模块
def statistic_top_word(word_list, top=0):
    # 统计每个单词出现的次数，别将结果转化为键值对（即字典）
    result = dict(Counter(word_list))
    for key in list(result):
        if len(key) < 2:
            result.pop(key)
    # sorted对可迭代对象进行排序
    # items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    # 排序后的结果是一个列表，列表中的每个元素是一个将原字典中的键值对转化为的元祖
    sort_list = sorted(result.items(), key=lambda item: item[1], reverse=True)
    # 获取前top个结果
    if top is not 0:
        result_list = []
        for i in range(0, top):
            result_list.append(sort_list[i])
        return result_list

    return sort_list


# 获得该文件夹下的所有文件
def get_all_text(path, get_wordnumber=False):
    def get_filename():
        a = []
        for fpathe, dirs, fs in os.walk(path):
            for f in fs:
                if f.find("txt") != -1:
                    a.append(os.path.join(fpathe, f))
        return a

    txt_path = get_filename()
    all_text = ""
    detector = UniversalDetector()  # 初始化一个UniversalDetector对象
    all_num = 0
    for txt in txt_path:
        with open(txt, "r", encoding='GB2312', errors='replace') as file:
            try:
                a = file.read()
                all_text = all_text + a
                if get_wordnumber is not False:
                    words = a.rstrip()
                    num_words = len(words)
                    print(file.name, num_words)
                    all_num += num_words
                # this_text = str(a).lower()
            except UnicodeError:
                detector.reset()
                for temp in file:
                    detector.feed(temp)
                    if detector.done is True:
                        break
                detector.close()
                print(file, detector.result)
    if get_wordnumber is not False:
        print(path, all_num)
    return all_text

    # 统计标签
    # tag_text = get_tag(all_text)
    # # tag_text = cut_word(tag_text)
    # tag_result = statistic_top_word(tag_text)
    # with open("tag.txt", "w") as f:
    #     print(tag_result, file=f)


# 数据清洗，提取所有含有要求的句子
def clean_text(include_text, data, save_name=None):
    require_list = re.findall(f"[\\u4e00-\\u9fa5]+{include_text}+[:：【】\[\]\s]+.+?[【】\[\]\n]+", data)
    result = ""
    for i in require_list:
        i = re.sub("[【】]", "", i)
        result = result + i
    if save_name is not None:
        with open(save_name, "a", encoding='utf-8') as f:
            print(result, file=f)
    return result


def main_recruit():
    # 获取该文件夹下所有文本
    all_text = get_all_text("yanjiuzhongxin")
    #
    require_text = clean_text("要求", all_text, "CleanedRequire.txt")
    # 统计文本中的词频
    word_list = cut_word(require_text)
    statistic_result = statistic_top_word(word_list)
    # 输出统计结果
    # with open("frequency3.txt", "w") as f:
    #     print(statistic_result, file=f)


# 词频展示
def get_wordcloud(text_fre):
    # lower max_font_size
    wc = WordCloud(
        font_path='C:/Windows/Fonts/Deng.ttf',  # 设置字体格式
        height=1080,
        width=1920,
        max_words=400,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )
    wordcloud = wc.generate_from_frequencies(text_fre)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def 绘图(statistic_result):
    a = []
    for i in statistic_result:
        a.append(i[1])
    plt.loglog(a)
    plt.show()


def main_tjss():
    # all_text = get_all_text("唐家三少作品合集", True)

    # with open("唐家三少原素材集合.txt", "w", encoding='utf-8') as f:
    #     print(all_text, file=f)
    with open("唐家三少原素材集合.txt", "r", encoding='utf-8') as f:
        all_text = f.read()
    word_list = cut_word(all_text)
    statistic_result = statistic_top_word(word_list)
    绘图(statistic_result)
    # print(jieba.analyse.extract_tags(all_text, 200, ['nr', 'v', 'a']))
    # wordcloud = wc.generate(all_text)
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
    # get_wordcloud(statistic_result)
    # with open("唐家三少.txt", "w") as f:
    #     print(statistic_result, file=f)


if __name__ == '__main__':
    # 招聘信息统计
    # main_recruit()
    # 唐家三少小说统计
    main_tjss()
    # print(__name__)
