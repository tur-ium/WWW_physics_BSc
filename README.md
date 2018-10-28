# Data and Tools for BSci project on "The World Wide Web as a Physical Medium"

## Abstract

Using a real-world network of wall-posting behaviour we analysed the interaction of 23,396 Facebook users in December 2008. Applying techniques from thermodynamics, statistical mechanics and network theory, we identifed a second-order phase transition in the largest component of the network and found that the network exhibited elastic hysteresis. To the model the data, we adapted three standard random network generation processes: the Erdos-Renyi, Configurational and Barabasi-Albert models to produce weighted networks and developed a fourth model, taking a friendship network as a parameter, to understand the
effects of different forms of user behaviour. We used the evolution of the Largest Component Size (LCS), the Average Clustering Coefficient (ACC) and the weighted degree distributions to compare the empirical data with the models. Different models reproduced different aspects of the  structure of social interaction on social media better than others, however further work is required to form a realistic model

## Paper

https://www.academia.edu/37613533/Phase_Transitions_on_Facebook

## Project proposal

We are accustomed to hearing the terms "social media" or "mass media" in reference to technology such as the world wide web (WWW). In physics, however this term bears different connotations involving understanding the behaviour of systems as we change its surroundings or structure. This begs the question - what parallels are there between the structure and dynamics of "social" media on the WWW and "physical" media?

Online social networks, which quantify human behaviour in a way not possible before, have become an important part of social relations worldwide, with sites such as Facebook exceeding 2 billion users. These media are of great significance in many industries ranging from government, perhaps in pushing across a certain political agenda, to marketing companies to advertise and increase sales of a product or service. 
The theory of complex networks is well-established [1] and meaningful insights have already been made by applying concepts from physics to social sciences in the context of the spread of ideas [2], thermodynamics [3], and the scaling behaviour of cities and companies [4].

Our project aims to investigate a dataset containing timestamped information on Facebook friends & wall posts from New Orleans [5]. Python code will be used to probe a model of the network to extract metrics such as centrality measures, entropy, clustering coefficients and critical thresholds to obtain an understanding of the network’s resilience, as well as to discover analogies with physical media in terms of thermodynamics and statistical mechanics.

Other considered components are:

*	Analysing the exponents of power-law distributions, for instance of the degree distribution 
*	Investigating the applicability of thermodynamics and whether state variables, such as entropy and internal energy, can be meaningfully assigned
* Using timestamped data to investigate how certain metrics of clustering vary over time

## References

[1]	M. Newman, Networks : an introduction. Oxford: Oxford University Press, 2010.

[2]	M. T. Gastner, N. Markou, G. Pruessner, and M. Draief, “Opinion Formation Models on a Gradient,” PLOS ONE, vol. 9, no. 12, p. e114088, Dec. 2014.

[3]	“Social thermodynamics: Modelling communication dynamics in social network - IEEE Conference Publication.” [Online]. Available: http://ieeexplore.ieee.org/document/6476582/?tp=&arnumber=6476582. [Accessed: 07-Dec-2017].

[4]	G. West, Scale: The Universal Laws of Life and Death in Organisms, Cities and Companies. Weidenfield and Nicolson, 2017.

[5]	B. Viswanath, A. Mislove, M. Cha, and K. P. Gummadi, “On the Evolution of User Interaction in Facebook,” in Proceedings of the 2Nd ACM Workshop on Online Social Networks, New York, NY, USA, 2009, pp. 37–42.

