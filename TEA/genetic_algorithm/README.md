#  TEA convergancy and efficiency model (Albumin)

TEA algorithm is time and resourses intensive process, if modeled decently it can be optimized to reach a list of perfect aptamers in fixed number of iterations with less disorder. Therefore we analyzed two pivotal stages of GA - how long it takes process to converge and extract fit aptamer list and how Alberts model accuracy affects a list of fit aptamers.


## Bayesian probabilistic model to determine its convergence time

We have employed *Bayesian* inferiantial approach to learn about a population **proportion** of **15s** length aptamers. Before considering analyzed data everyone has its *belief* about a
*proportion* which is called *prior*. It can take any kind of functional form of your initial beliefs about a form of proportion of your target (*any related research or collected data could help here*), also there is no best prior
only more fit so it is strongly suggest to try out multiple *priors*. After **event** have been observed we want to update our *beliefs* by *likelihood* distribution which is just distribution of observed data. Finally, *posterior* can be calculated out by "multiplication" of former distributions. *Posterior* can be used for predicting the likely outcomes of a new sample taken 
from the population or any estimate of interest.

***TEA* end-user** is interested in learning about the habits of 15s length aptamers, in other words what proportion of aptamers get at least 51 (*arbitrary value*) affinity score from **EFBA**. Let *p* represent estimate of proportion of distribution of interest which is population of 15s length aptamers (*there are more than billion aptamers this length*). *Bayesian inference* will let us locate position of p even if it is not know at beginning at all. 

From *Bayesian* viewpoint person's belief about the variation or uncertainty of the location of *p* is presented by a probability distribution placed on this value of *p*. We will denote *prior* as *f(p)*.

Our *prior belief* is that proportion *p* mean should be around value 0.003 and 90th percentile to be 0.006 which gives us prior of 

![equation](https://latex.codecogs.com/png.latex?f(p)&space;\propto&space;beta(2.94,&space;870.18)){:align="left"}
  <!-- more links here -->


 It is quite hard to determine those parameters for user himself, so it can be found by 90th percentile of the distributions and median which is 50th percentile. *R* package *LearnBayes* has in-build function to do so, follow script `bayesian_inference.R` for more information.

Next, we have to include information from observed data which is scored aptamer sequences from *EFBA*, in file `.\datasets\ga_interim_data\Albumin\position_analysis.csv`. Proportion in our case can be described in simple way, if we generate aptamer with affinity score more than or equal to 51 it is *"success"* - *s* else it is *"failure"* - *f*. From here it is obvious that the likelihood function is given by binomial distribution

<div style="text-align:center">    
  <a href="https://www.codecogs.com/eqnedit.php?latex=L(p)&space;\propto&space;binom(1500,&space;p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?L(p)&space;\propto&space;binom(1500,&space;p)" title="L(p) \propto binom(1500, p)" /></a>
  <!-- more links here -->
</div>

<div style="text-align:center">    
  <a href="https://www.codecogs.com/eqnedit.php?latex=L(p)&space;\propto&space;p^{s}(1-p)^f" target="_blank"><img src="https://latex.codecogs.com/gif.latex?L(p)&space;\propto&space;p^{s}(1-p)^f" title="L(p) \propto p^{s}(1-p)^f" /></a>
  <!-- more links here -->
</div>




Then posterior density for proportion *p*, by *Bayes*' rule is obtained by multiplying the *prior* density with the *likelihood*, refer to the table below.


<div style="text-align:center">    
  <a href="https://www.codecogs.com/eqnedit.php?latex=f(p|data)&space;\propto&space;f(p)L(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(p|data)&space;\propto&space;f(p)L(p)" title="f(p|data) \propto f(p)L(p)" /></a>
</div>

<div style="text-align:center">    
  <a href="https://www.codecogs.com/eqnedit.php?latex=f(p|data)&space;\propto&space;p^{a&plus;s-1}(1-p)^{b&plus;f-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(p|data)&space;\propto&space;p^{a&plus;s-1}(1-p)^{b&plus;f-1}" title="g(p|data) \propto p^{a+s-1}(1-p)^{b+f-1}" /></a>
</div>

<p align="center">
  <img src="./../images/posterior_Albumin.png" alt="Logo" width="" height="">
</p>

It is useful to know that with more extensive observed dataset *posteror" distribution has less uncertainty, in other words variability so it is beneficial to gather as much data as possible. Using *inverse posterior* we are able to get a density function of possible number of fit aptamers of the GA process which generates 1000 aptamers. **Figure below** shows us the outcome results:

<p align="center">
  <img src="./../images/aptamers_Albumin.png" alt="Logo" width="" height="">
</p>

It is 85.3 % probability to get number of fit aptamers from a list of {1,2,3,4,5,6}, having this we can conclude that:

  - With every new iteration of GA and NN prediction current *top* aptamers cannot/shouldn't decrease in position more than by 7 or more places.

Mean of the *posterior* distribution is ~3.4 which indicates that with large number of GA iterations every iteration algorithm will give out approximately 3.4 fit aptamer, hence
  - On average, we will need 60 iterations to bring 200 long list of fit aptamers.


##  Neural Network accuracy impact to Genetic Algorithm precision

Next pivotal parameter is *Alberts* predicting accuracy, we will modify dataset `.\datasets\ga_interim_data\Albumin\model.csv` which consists every initial aptamer compared to each other. Firstly, if *aptamer1* is better than *aptamer2* this pair will have a *label* equal to 1 however there is `1-accuracy` chances to predict it wrongly hence we *flip* *labels* by randomly flipping a pair label with probability of `1-accuracy`. Then we are able to compute ranking of a list and compare *true* and *shifted* position of aptamer in a list, this lets us analyze the variability of aptamer position on average, how many fit aptamers can be *"lost"* in prediction. (*lost* - aptamer is fit yet it is out of top 200 predicted aptamers and will be deleted).

We have simulated error accurancy with binomial distribution 100 times obtained 90 % confidence interval of possible aptamer position which is shown in **figure below**.

<p align="center">
  <img src="./../images/true_error_albumin.png" alt="Logo" width="" height="">
</p>

- It can be seen that with NN accuracy of 84.6 % aptamers position varies &#177; by 20 positions which creates a lot of uncertainty in prediction. 
- Simulational analysis also helps to determine number truely fit aptamers that are thrown out of the top liss: on average 5.2 aptamers that belong to top 200 list are removed with model accuracy of 84.6 %. Considering that on average we get 3.4 fit aptamers every iteration and might remove 5.2 is alarming.

Next step is to observe a threshold accuracy than would be sufficient to reach lesser variability and output more fit aptamers than it can remove. The same simulation was repeated with accuracy rates from interval of 88-95%. Results can be seen in **figures below**

<p align="center">
  <img src="./../images/aptamer_left_albumin.png" alt="Logo" width="45%" height="50%">
  <img src="./../images/aptamer_variability_albumin.png" alt="Logo" width="45%" height="50%">
</p>

##  Conclusion
To have a *stable* aptamer generating process we have to accomplish model with error rate of at most 6%, also this model has pretty good stability - standard deviation of 8 indicates that with probability of 95.4% our predicted position will be in *true_position* &pm; 16 places range. However even model satisfies accuracy condition (it deletes less possible fit aptamers than generates) should be analyzed for a long term steadiness which includes multiple iteration stability and what is the maximum efficiency of this kind of model to generate at least mayority of fit aptamers in *top* list.




