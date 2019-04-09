# HomeWork1
## Dynamic YinYang Picture
### Project Title
The demo bases on Turtle-example-suite.This is a Taiji Picture which can be drew by part(from demo) and rotate to a full circle.

### Requirements
Test Project:Python 3.6.2 + Turtle 1.1b.

### Detail
#### def yin:
 From Demo,the half of TaiJi picture is drew by this function.
 It include three semicircle forming Outline and a full cirle.
 Two parameters is filled color and radius.
#### def  gradient:
 The Function is aimed at a demo how make a animation by turtle. I used `tracer(0)` and `update()`  to control turtle's drawing.Two parameters is filled color and radius.

 ### GitHub
[Repository](https://github.com/qyxlxr/HomeworkForPy)

### Output
![Output](https://github.com/qyxlxr/HomeworkForPy/blob/master/HomeWork1/2019_03_17_23_21_39_198.gif)

# HomeWork2
## 爬取的智联招聘的招聘信息的词频统计
### 需求说明：
    因某软件建设需要，我们通过爬虫爬取了某招聘网站上的3178个招聘信息，并将这些信息进行分词统计词频，希望查找雇主最需要的个人能力要求。
    统计了所有用“”和【】括起来的包括要求二字的段落，存在CleanedRequire.txt 中，然后重新进行了词频统计，见 RequireFrequency.txt
### 可用方法：

1. #### cut_word(data, filter=False):
    调用jieba进行分词

    data:输入字符串数据

    filter：是否过滤标点，各种括号冒号等中英文标记

    返回值：包括分词的可迭代的 generator

    ps：jieba.enable_parallel(6)在Linux下可开启，并行分词，6位系统cpu核心数量，可加快分词速度。
    

2. #### statistic_top_word(word_list, top=0):统计词频并排序
    
    word_list：上一步cut_word的返回结果

    top是获取前top个结果，默认参数为返回全部结果
    #### 返回值：包括词典和词频的元祖组成的列表



3. #### get_all_text(path, get_wordnumber=False):获得该文件夹下的所有文本
    #### get_filename():获取所有文件名
    path：文件夹名（相对路径或绝对路径）

    get_wordnumber：统计每个txt内的文字数量（去空格）

4. #### clean_text(include_text, data, save_name=None):数据清洗，提取所有含有要求的句子
    include_text:包括的文本
    
    data：清理的数据
    save_name=None
    将提取数据保存为文件的文件名，默认为不保存
 