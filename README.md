# Tenet
Political Language Processing


## What is Tenet?

Tenet is a Natural Language Processing tool to parse topics from political rhetoric. It employs Guided Latent Dirichlet Analysis trained on over 100,000 congressional press releases from the 115th congress to discover important political topics, and combines it with sentiment analysis to extract opinion and generate one-sentence summaries of press releases.

In this repo, you will find the code used to scrape, clean, process, and load the data into our model. The model itself is too large to host on github, and is available by request. 

## What is Guided Latent Dirichlet Analysis?

See here for an excellent write-up. (https://medium.freecodecamp.org/how-we-changed-unsupervised-lda-to-semi-supervised-guidedlda-e36a95f3a164)

## How did you validate this model?

A few members of congress release their press-releases with tagged topics. If two press releases were classified as a part of the same category, the model gave them the same label 88% of the time. 

We applied the scramble and split test for consistency. Documents had their sentences scrambled, and were split in two. We fed both halves into the model, and computed the cosine similarity of the two topic vectors. For 90% of our testing set of documents, we had a cosine similarity of .95 or above. 

