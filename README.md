# HALO

[HALO: Hierarchy-aware Fault Localization for Cloud Systems](https://dl.acm.org/doi/abs/10.1145/3447548.3467190)
<br>
I am not the author of the paper. All the content of the code comes from the paper. If you have any questions, welcome
to discuss.

## introduction

![image-20210820210415511](http://lbj.wiki/static/images/1f91ba52-01b7-11ec-9928-00163e30ead3.png)

The paper is mainly divided into two parts. 

* The first part uses the inclusion relationship of dimension attributes to generate DAG by calculating entropy and conditional entropy, and generates search path by random walk

* then defines exception score and root cause score, traverses the dimension path from top to bottom, and obtains the root cause dimension combination

## code

Most of the code follows the paper, except for the following

* Maybe it's my understanding. I think the denominator of the following formula may be 0 (when the layer has only one attribute), so I added 1 after it

![image-20210820211851363](C:\Users\cb229\AppData\Roaming\Typora\typora-user-images\image-20210820211851363.png)
$$
I_i = \frac{\sum_{j=1}\sum_{k=1}HI(H_i^j\to H_i^k)}{|H_i|*(|H_i|-1)/2}
$$


