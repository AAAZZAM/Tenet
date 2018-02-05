# Tenet (www.adamazzam.com)
Political Language Processing 


## What is Tenet?

Tenet is a Natural Language Processing tool to parse topics from political rhetoric. It employs Guided Latent Dirichlet Analysis trained on over 100,000 congressional press releases from the 115th congress to discover important political topics, and combines it with sentiment analysis to extract opinion and generate one-sentence summaries of press releases.

In this repo, you will find the code used to scrape, clean, process, and load the data into our model. The model itself is too large to host on github, and is available by request. 


## What can someone do now that they couldn't do before?

Users can now enter topics that matter to them, and Tenet will find them the congresspeople that are most outspoken about their issue. This lets voters identify congresspeople most likely to be an ally or obstacle in congress.

## What are the business applications of a project like this?

Unsupervised topic discovery is a mainstay of businesses trying to discover themes in customer feedback. GuidedLDA is a semi-supervised topic discovery model, which allows you to leverage the power of unsupervised learning to complement a business's domain knowledge. 

For example: An airline company trying to automate parts of its customer service experience may want to automatically classify customer complaints. With a purely unsupervised approach, they are often left with nonsensical categories that don't reflect their domain knowledge. With a semi-supervised approach, they can seed topics like {delayed, hours, missed, connection} and {cancelled, rebook} and {attendant, service, experience} to populate topics correponding to delayed and cancelled flights, customer experience, in addition to discovering topics they didn't anticipate. 


## What is Guided Latent Dirichlet Analysis?

See here for an excellent write-up. (https://medium.freecodecamp.org/how-we-changed-unsupervised-lda-to-semi-supervised-guidedlda-e36a95f3a164)

## How did you validate this model?

A few members of congress release their press-releases with tagged topics. If two press releases were classified as a part of the same category, the model gave them the same label 88% of the time. 

We applied the scramble and split test for consistency. Documents had their sentences scrambled, and were split in two. We fed both halves into the model, and computed the cosine similarity of the two topic vectors. For 90% of our testing set of documents, we had a cosine similarity of .95 or above. 

