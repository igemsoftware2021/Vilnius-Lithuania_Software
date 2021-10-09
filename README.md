<!-- PROJECT SHIELDS -->
<!--
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<p align="center">
  <a href="https://github.com/iGEM-Vilnius/Software/graphs/contributors" ><img src="https://img.shields.io/github/contributors/iGEM-Vilnius/Software.svg?style=for-the-badge"></a>
  <a href="https://github.com/iGEM-Vilnius/Software/network/members" ><img src="https://img.shields.io/github/forks/iGEM-Vilnius/Software.svg?style=for-the-badge"></a>
  <a href="https://github.com/iGEM-Vilnius/Software/stargazers" ><img src="https://img.shields.io/github/stars/iGEM-Vilnius/Software.svg?style=for-the-badge"></a>
  <a href="https://github.com/iGEM-Vilnius/Software/issues" ><img src="https://img.shields.io/github/issues/iGEM-Vilnius/Software.svg?style=for-the-badge"></a>
  <a href="https://github.com/iGEM-Vilnius/Software/blob/main/TEA/LICENSE.txt" ><img src="https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge"></a>
</p>



<p align="center">
  <img src="TEA/images/logo_no_background.png" alt="Logo" width="30%" height="30%">

  <p align="center">
    An jumpstart to fit aptamers!
    <br />
    <a href="https://2021.igem.org/Team:Vilnius-Lithuania"><strong>Explore Our Wiki »</strong></a>
    <br />
    <a href="https://github.com/iGEM-Vilnius/Software/issues">Create Issue</a>
  </p>
  
</p>



## Motivation

Our team this year decided to create an aptamer-based detection method to diagnose amebiasis disease caused by Entamoeba histolytica. Nevertheless, SELEX (Systematic evolution of ligands by exponential enrichment) was chosen as the main approach used to find aptamers for the protein target indicating the presence of E. histolytica. Finding a suitable aptamer by the well-established SELEX method requires the establishment of appropriate protocols, and might be a laborious and costly procedure. Keeping these reasons in mind, we started to look for in silico approaches for aptamer generation. After studying existing literature resources we found methods like M.A.W.S. (Making aptamers without SELEX), which was implemented by Heidelberg iGEM 2015 team. Based on this approach, we released an updated version that is described on the Software page. We decided to take a step further and apply a novel transformer-based neural network model  combined with a genetic algorithm to make aptamer generation in silico a more resource-efficient process that has the higher potential to output an affine aptamer sequence. The key part of the model is that it has a property of transfer learning that lets anyone fine-tune the model almost instantly for modified tasks.


