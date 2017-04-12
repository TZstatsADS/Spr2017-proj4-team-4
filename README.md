# Project 4: Who Is Who -- Entity Resolution

### [Project Description](doc/project4_desc.md)

Term: Spring 2017

+ Team #4
+ Project title: Who is Who? (Author Disambiguation)
+ Team members
	+ Bowen Huang (presenter)
	+ Chengcheng Yuan
	+ Sean Reddy
	+ Zhilin Fan
	+ Zishuo (Jason) Li
+ Project summary: Author disambiguation is a prominent problem in text analysis. Being able to distinguish whether two articles both written by "John Smith" are truly written by the same person is a non-trivial problem in natural language processing. In this project we explore two papers focusing on this problem of author disambiguation and attempt to emulate their experimental processes.

The first (referred to throughout as "Paper 4") is authored by Song, Yang, et al. entitled "Efficient topic-based unsupervised name disambiguation.".

The second paper (referred to throughout as "Paper 5") is authored by Culotta, Aron, et al. entitled "Author Disambiguation using Error-driven Machine Learning with a Ranking Loss Function". Specificially within this paper we refer to the C/E/Mr experimental process.
	
**Contribution statement**: 

CY and ZF cleaned the raw data, analyzed the paper 4 and developed the LDA model represented within the paper.

BH, ZL and SR analyzed paper 5, focusing on the C/E/Mr workflow. BH worked on the MIRA ranking function (Mr). SR and ZL worked on the clusterwise scoring function (C) in R and Python respectively. ZL implemented the error-driven training function (E).

All team members contributed equally in all stages of this project. All team members approve our work presented in this GitHub repository including this contributions statement. 

Following [suggestions](http://nicercode.github.io/blog/2013-04-05-projects/) by [RICH FITZJOHN](http://nicercode.github.io/about/#Team) (@richfitz). This folder is orgarnized as follows.

```
proj/
├── lib/
├── data/
├── doc/
├── figs/
└── output/
```

Please see each subfolder for a README file.
