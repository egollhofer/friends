# Intimacy, emotionality, and sentiment among *Friends*
I'm a huge fan of the TV show *Friends*, so when I found a dialogue dataset from all ten seasons I just had to play with it.  I decided to use some NLP methods to quantify a handful of language aspects to see what they revealed about the main characters in the show. 

The first thing I wanted to see was how often each of the different characters speak to each other, which I thought was easiest to see in the following heatmap:

<p align="center">
  <img src='figures/speaker_count.png' width='500'>
</p>

The darker green colors show characters who speak to each other the most often.  Looking at this, it's clear that even though this show is called *Friends*, the romantic partners are the ones who converse the most.  Ross and Rachel are the most frequent conversational partners, followed by Monica and Chandler.  What I thought was really interesting, though, was that the pairings who speak to each other the *least* often are the non-romantic mixed-gender pairs.  All of the medium-green boxes represent women talking to other women or men talking to other men, and the very pale green boxes are men talking to women they aren't romantically involved with (or vice versa). Outside of romantic relationships, the women tend to talk to the women, and the men tend to talk to the men.

I quantified three aspects of language - intimacy, sentiment, and emotionality - and evaluated how those aspects vary amongst the characters.

<p align="center">
  <img src='figures/sentiment.png' width='500'>
</p>

Sentiment was quantified using the package VADER Sentiment Analysis (https://github.com/cjhutto/vaderSentiment).  

<p align="center">
  <img src='figures/emotionality.png' width='500'>
</p>

Emotionality was quantified using methods laid out in the paper CITATION HERE.  Vector representations were made based on words that represented two poles of emotionality - high emotionality vs low emotionality - and a vector representation was made based on the words in each utterance in the dialogue corpus.  The strength of emotionality was quantified based on whether the utterance vector was more similar to the highly-emotional vector or the low-emotional vector.

<p align="center">
  <img src='figures/intimacy.png' width='500'>
</p>

Intimacy was quantified using the package Question-Intimacy (https://github.com/Jiaxin-Pei/Quantifying-Intimacy-in-Language).
