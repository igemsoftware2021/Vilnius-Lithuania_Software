<!-- PROJECT SHIELDS -->
<!--
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

<p align="center">
  <img src="images/logo.png" alt="Logo" width="160" height="160">

  <h3 align="center">Transformers Enhanced Aptamer Design Software </h3>

  <p align="center">
    An jumpstart to fit aptamers!
    <br />
    <a href="https://igem2021.vilnius.com/"><strong>Explore Our Wiki »</strong></a>
    <br />
    <a href="https://github.com/">Create Issue</a>
  </p>
  
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#motivation">Motivation</a>
    </li>
    <li>
      <a href="#model-dataflow">Model Dataflow</a>
    </li>
    <li><a href="#results">Results</a></li>
    <li><a href="#getting-starter">Getting Started</a></li>
        <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

Suggestion for future improvements

<!-- ABOUT THE PROJECT -->
## Motivation

Transformers Enhanced Aptamers (*TEA*) software is extension of the EFBALite that speedups kinetic aptamer evaluation by 40 times and enables quick iterative inference on sequences. In consequence, genetic algorithm (GA) can be introduced to help out *TEA* to generate *TOP* aptamers for target protein, also  models key property of transfer learning can be employed to fine-tune (re-train) it for any target proteins of interest without need of re-inventing the wheel which requires expensive GPUs and is reachable for anyone. To add up, many transformer-based models could fit this task however we have to be smarter about the way we use our resources hence Albert model was chosen because of its state of the Art performance with fewer parameters (11M) than threshold BERT model (110M), which takes ~10 times less time to train, fine-tune or inference, saving days of expensive GPU runtime which can cost up to 2-3k$ per month (2x`16 GB Tesla V100`). Working with massive datasets like our time is the crucial reasoning. 



## Model Dataflow

Initially N random aptamer sequences are generated employing EFBAScore, following it up, data must be specifically preprocessed to contain a pair of aptamers with a binary label that determines if the first sequence is more fit (1) or not (0). 

<p align="center">
  <img src="images/dataframe.png" alt="Logo" width="75%" height="70%">
</p>

Paired sequences dataset is obtained by comparing every aptamer in-between by fitness score which is computed with the former software, later number of classification classes labels are balanced (if needed) by flipping Label together with exhanging first aptamer with the second in places for model to master both classes equally good. 

<p align="center">
  <img src="images/dataframe_before_switch.png" alt="Logo" width="75%" height="70%">
</p>
<p align="center">
  <img src="images/dataframe_after_switch.png" alt="Logo" width="75%" height="70%">
</p>

Next, paired aptamers are put to the GA that produces new sequences from the the most fit by by well-known breeding, mutation steps, shortly speaking, GA conditions new breed to have properties of the "best". New list of aptamers are evaluated by TEA, 10 % of the best stays and we iteratively repeat the process until it converges and we are satisfied with probabilities of model to have at least few super fit sequences to target protein of interest. Final aptamers can be send to wet lab to confirm its superiority after the last EFBALite run on it. *Every result can be reproduced using seed*.

##  Modeling 

- [ ]  Trumpas aprasas is GA readme su keleta paveiksleliu ir pagrindiniu isvadu
## Results

Fine-tuning two models with various hyperparameter to try took up <12 hours which is enough for a model to learn positional embeddings difference between Natural Language and language of proteins. Dataset for the learing part consisted of 1500 different aptamer sequences from EFBAScore which were later on paired to form 433050 pairs with binary labels, 70% of it was used for training matter, 15 % for validation, and the rest for testing. 

Comparing the accuracy and other significant metrics of fine-tuned `albert-base-v2` and `albert-large-v2` models for Albumin, large version has an edge over base just by 4 % and makes inferences almost twice as long compared to its simpler version hence `albert-base-v2` is chosen.

<p align="middle">
  <img src="images/Albumin Base Confusion Matrix.png" width="40%" /> 
  <img src="images/Albumin Large Confusion Matrix.png" width="40%" />
</p>

<p align="middle">
<img src="images/Albumin ROC Curves.png" width="50%" />
</p>

Albert employed in our GA iterative process is capable of evaluating 800 aptamers per iteration which takes from 7 to 8 minutes.

###  Optimized version

- [ ] Prideti pagrindinius punktus is model README su efektyvumu ir kas padaryta

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites & Installation

To quickly install all packages required for algorithm run command
```
pip install requirements.txt
```

In case you are running on cloud there is perfect [tutorial](https://medium.com/analytics-vidhya/install-cuda-11-2-cudnn-8-1-0-and-python-3-9-on-rtx3090-for-deep-learning-fcf96c95f7a1) how to install every dependancy you can need training deep learning model, that includes `Cuda`, `CudaNN`, `PyTorch`. However if you have no access to cloud GPU instances, we strongly suggest to utilize [Google Colab](https://link-url-here.org).


<!-- USAGE EXAMPLES -->
## Usage

Project can be reused in two ways. In case you have the same type of dataset and task to work on, model is shared in the AI community [HuggingFace](https://huggingface.co/models) under name "Vilnius-Lithuania-iGEM2021/Albumin". *One command to rule them all*

```
model = AutoModel.from_pretrained('Vilnius-Lithuania-iGEM2021/Albumin')
```

and inference as with usual transformer-based model. Read more on `model README`, to get familiar with the framework visit [HuggingFace/Transformers](https://huggingface.co/transformers/). Otherwise, if task differs, for instance you are considering longer aptamer sequences or change task from classification to sequence generation, then you have to run the process described in `model` folder with changed initial `albert-case-v2` model to `Vilnius-Lithunia-iGEM2021/Albumin`.

_For more indepth ALBERT model description and explanation, please refer to the [ALBERT Documentation](https://github.com/saulius-lipkevicius/GA_Transformer/tree/main/model)_


##  Suggestion for future improvements

Albert model have been converted to ONNX framework to speed the inference process around 3 times, however there is a lot of space to make it better. Some suggestions from us:

-  Train Albert from scratch on way bigger dataset.
-  Test out other BERT alternatives like Roberta (this model specifically requires up to 10 times more data than BERT or Albert).
- To make model more precise 3 class model could be consider instead of 2 classes, the third could stand for unknown relationship between pair of aptamers.
- Freeze layers of Albert to maximize accuracy, there is a code snippet in the model fine-tuning code for expermenting.
- Play with hyperparameters: prediction threshold, learning rate and optimizer, learning rate, gradient accumulation parameter (iters_to_accumulate) and so on.
- Try out different *seeds* for the same model, sometimes random initial state can change results significantly.
- Model code can be rewriten to TensorFlow.
-  Fasten NN by diminishing parameters accuracy to INT8.
-  Create a tokenizer that would learn to seperate aptamer sequence uniquely. [Link for a head-start](https://huggingface.co/quicktour/transformers).
- If you accomplish better accuracy model, play around with GA parameters, since with accuracy we need less restrictions for GA.
- Flow can be rewritten to C++ language to speed up wok with dataframes and intermediate calculations.
- Analyze models accuracy when we compare only high affinity aptamers, for instance, model might have lower accuracy when comparing quite similar affinite sequences.
<!-- CONTRIBUTING -->
## Contributing

Contributions are what makes the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/CuteAptamer`)
3. Commit your Changes (`git commit -m 'Add my feature'`)
4. Push to the Branch (`git push origin feature/CuteAptamer`)
5. Open a Pull Request

###  Contributing to HuggingFace
Any contribution to the AI community HuggingFacce community is super valuable, find more information in [HuggingFace/Contributing](https://huggingface.co/transformers/contributing.html)


<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact
Saulius Lipkevičius - sauliuslipkevicius@gmail.com




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
