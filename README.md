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

The code passed the test on Python 3.8 and 3.9. In addition to [typing and dataclass], earlier versions should also support
<br>

Most of the code follows the paper, except for the following

* Maybe it's my understanding. I think the denominator of the following formula may be 0 (when the layer has only one attribute), so I added 1 after it

![image-20210820211851363](http://lbj.wiki/static/images/fed2e018-01b9-11ec-9928-00163e30ead3.png)

## use

1. ```shell
   cd HALO/
   pip install requirements.txt      //Installation dependency
   ```

2. ```shell
   cd HALO/
   python3 main.py					  //test case
   ```



 

## other

Because the entropy relationship of the sample data provided in the paper is inconsistent with AHG, several values of API Attr are modified in the test data to increase its entropy. But there are still some small differences between the final results and the paper.

<img src="http://lbj.wiki/static/images/3516b80a-01bc-11ec-9928-00163e30ead3.png" alt="image-20210820214039749" style="zoom:50%;" />

<img src="http://lbj.wiki/static/images/44be877e-01bc-11ec-9928-00163e30ead3.png" alt="image-20210820214106031" style="zoom:50%;" />
