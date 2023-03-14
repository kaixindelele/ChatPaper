# ChatPaper

<div style="font-size: 1.5rem;">
  <a href="./README.md">中文</a> |
  <a href="./readme_en.md">English</a>
</div>
</br>

To keep up with the huge ArXiv papers and AI’s fast progress, we humans need to evolve. We download the latest papers on arxiv based on user keywords, and use ChatGPT3.5 API’s powerful summarization to condense them into a fixed format with minimal text and easy readability. 
We provide the most information for everyone to choose which papers to read deeply.

## TODO list:
1. Change all prompts to English.  --completed!
2. Use a more robust method to parse the Method section.
3. If there is a brother who wants to build a website, we can cooperate. --completed!
4. Implement a ChatReview version for everyone to refer to when reviewing (but there may be academic ethics issues?)
5. Output English mode! just set lauguage as "en"!

## Motivation

Facing the massive arXiv papers every day, and AI's rapid evolution, we humans must also evolve together in order not to be eliminated.

As a PhD student in Reinforcement Learning at USTC, I feel anxious. My brain holes can even not keep up with the speed of AI evolution now.

Therefore I developed this **ChatPaper**, trying to use magic to defeat magic.

**ChatPaper is a paper summary tool**: AI summarizes papers in one minute, and users read papers summarized by AI in one minute.

It can automatically download the latest papers from arXiv based on the keywords entered by the user, and then use ChatGPT3.5's powerful API interface summary ability to summarize the paper into a fixed format, with minimal text and lowest reading threshold to provide you with maximum information volume to decide which articles should be read carefully.

You can also provide local PDF document addresses for direct processing.

Generally speaking, you can quickly pass through a small field of latest articles in one night. I have tested it for two days myself.

I wish everyone can evolve with AI in this rapidly changing era!

Although this code is not much, it took me nearly a week to get through the whole process and share it with you today.

Your support is the motivation for my continuous update!

<div style="text-align: center;">
  <img src=https://user-images.githubusercontent.com/28528386/224465754-6f886e48-8626-419f-a154-e5d187fd22f9.jpg width="200" height="250"/>
</div>

<div style="text-align: center;">
  <img src=https://user-images.githubusercontent.com/28528386/224335122-1e87eb7b-a922-4c2f-b2aa-9612f62a6314.jpg width="200" height="250"/>
</div>


## How to use:
Windows, MAC and Ubuntu systems should be fine;

python version is best 3.9, other versions should not have any problems

1. Fill in your openai key in apikey.ini. Note that this code is a pure local project, your key is very safe!

2. The process must ensure global proxy! (Non-Chinese users may not have this problem)

3. Install dependencies:
``` bash
pip install -r requirements.txt
```
4. Run chat_paper.py, for example:

```python
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --max_results 1 --language en
```

5. Parameter introduction:
```
[--pdf_path Whether to directly read local pdf documents? If not set, download directly from arxiv with query] 
[--query The keywords searched on the arxiv website, some abbreviations are demonstrated: all, ti(title), au(author), an example query: all: ChatGPT robot] 
[--key_word The keywords of your interested field, not very important] 
[--filter_keys The keywords you need to search in the abstract text, each word must appear to be your target paper] 
[--max_results The maximum number of articles searched each time, after the above filtering, it is your target number of papers, chat only summarizes filtered papers] 
[--sort arxiv sorting method, default is relevance, can also be time , arxiv.SortCriterion.LastUpdatedDate or arxiv.SortCriterion.Relevance , don't add quotation marks] 
[--save_image Whether to save pictures , if you haven't registered gitee's picture bed , default is false ] 
[--file_format File save format , default is markdown's md format , can also be txt ] 
```

## Tips for using the project:
Quickly brush papers with specific keywords, without illustrations, each article takes a minute, reading time is about a minute.

This project can be used to track the latest papers in a field, or pay attention to papers in other fields, can batch generate summaries, up to 1000 (if you can wait).
Although Chat may have some nonsense elements, but under my standardized questioning framework, its main information is valuable.

The digital parts need everyone to go back to check in the original text!

After finding a good article, you can read this article carefully.

Recommend two other AI-assisted websites for reading papers: https://typeset.io/ and chatpdf.
My tutorial: [Reinforcement Apprentice: Paper Reading Artifact SciSpace(Typeset.io) Evaluation-Evolve with AI](https://zhuanlan.zhihu.com/p/611874187)

The main advantage over these two tools is that ChatPaper can automatically summarize the latest papers in batches, which can greatly reduce the reading threshold, especially for us Chinese.
The disadvantage is also obvious. ChatPaper has no interactive function and cannot ask questions continuously. But I think this is not very important~


## Summary Demo:

<h2>Paper:1</h2>
<ol>
<li>
<p>Title: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion 中文标题: 通过行为扩散的视觉运动策略学习</p>
</li>
<li>
<p>Authors: Haonan Lu, Yufeng Yuan, Daohua Xie, Kai Wang, Baoxiong Jia, Shuaijun Chen</p>
</li>
<li>
<p>Affiliation: 中南大学</p>
</li>
<li>
<p>Keywords: Diffusion Policy, Visuomotor Policy, robot learning, denoising diffusion process</p>
</li>
<li>
<p>Urls: http://arxiv.org/abs/2303.04137v1, Github: None</p>
</li>
<li>
<p>Summary:</p>
</li>
</ol>
<p>(1): 本文研究的是机器人视觉动作策略的学习。机器人视觉动作策略的学习是指根据观察到的信息输出相应的机器人运动动作，这一任务较为复杂和具有挑战性。</p>
<p>(2): 过去的方法包括使用高斯混合模型、分类表示，或者切换策略表示等不同的动作表示方式，但依然存在多峰分布、高维输出空间等挑战性问题。本文提出一种新的机器人视觉运动策略模型 - Diffusion Policy，其结合了扩散模型的表达能力，克服了传统方法的局限性，可以表达任意分布并支持高维空间。本模型通过学习代价函数的梯度，使用随机Langevin动力学算法进行迭代优化，最终输出机器人动作。</p>
<p>(3): 本文提出的机器人视觉动作策略 - Diffusion Policy，将机器人动作表示为一个条件去噪扩散过程。该模型可以克服多峰分布、高维输出空间等问题，提高了策略学习的表达能力。同时，本文通过引入展望控制、视觉诱导和时间序列扩散变换等技术，继续增强了扩散策略的性能。</p>
<p>(4): 本文的方法在11个任务上进行了测试，包括4个机器人操纵基准测试。实验结果表明，Diffusion Policy相对于现有的机器人学习方法，表现出明显的优越性和稳定性，平均性能提升了46.9%。</p>
<p><img alt="Fig" src="https://gitee.com/chatpaper/chatpaper/raw/master/images/Diffusion Policy: Visuomotor Policy Learning via Action Diffusion-2023-03-08-21-55-53.jpeg" /></p>
<p>7.Methods:
本文提出的视觉动作策略学习方法，即Diffusion Policy，包括以下步骤：</p>
<p>(1) 建立条件去噪扩散过程：将机器人动作表示为一个含有高斯噪声的源的条件随机扩散过程。在该过程中，机器人状态作为源，即输入，通过扩散过程输出机器人的运动动作。为了将其变为条件随机扩散模型，我们加入了代价函数，它在路径积分中作为条件。</p>
<p>(2) 引入随机Langevin动力学：将学习代价函数的梯度转换为基于随机Langevin动力学的迭代优化问题。该方法可以避免显示计算扩散过程，并且可以满足无导数优化器的要求，使其受益于渐近高斯性质以及全局收敛性质。</p>
<p>(3) 引入扩散策略增强技术：使用展望控制技术，结合决策网络，对由扩散产生的动作进行调整，从而增强策略的性能。同时，引入视觉诱导以及时间序列扩散变换，来进一步提高扩散策略的表达能力。</p>
<p>(4) 在11个任务上进行测试：测试结果表明，该方法相对于现有的机器人学习方法，在机器人操纵基准测试中表现出明显的优越性和稳定性，平均性能提升了46.9%。</p>
<p>7.Conclusion: </p>
<p>(1):本文研究了机器人视觉动作策略的学习方法，提出了一种新的机器人视觉运动策略模型 - Diffusion Policy，通过引入扩散模型的表达能力，克服了传统方法的局限性，可以表达任意分布并支持高维空间。实验结果表明，该方法在11个任务上均表现出明显的优越性和稳定性，相对于现有机器人学习方法，平均性能提高了46.9%，这一研究意义巨大。</p>
<p>(2):虽然本文提出了一种新的机器人视觉动作策略学习方法，并在实验中取得了良好的表现，但该方法的优化过程可能比较耗时。此外，该方法的性能受到多种因素的影响，包括演示的质量和数量、机器人的物理能力以及策略架构等，这些因素需在实际应用场景中加以考虑。</p>
<p>(3):如果让我来推荐，我会给这篇文章打9分。该篇文章提出的Diffusion Policy方法具有较高的可解释性、性能表现良好、实验结果稳定等优点，能够为机器人视觉动作策略学习等领域带来很大的启发与借鉴。唯一的不足可能是方法的优化过程需要投入更多的时间和精力。</p>


