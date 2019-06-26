# How to Rank on the Billboard Top 100 using Linear Regression

After being denied a spot on the Billboard top 100 Country charts, Old Town Road by Lil Nas X grabbed the number 1 spot on the Billboard Hot 100 chart over all genres. The song is odd but catchy meeting at the intersection of rap and country. Something that has not really been done before, in this fashion. Not only is the song different from its predecessors, it is also the shortest number 1 song on the Hot 100 since 1965. 

The story of Old Town Road and its journey to the top made me wonder, “What does it take for a song to become number 1 on Billboard’s Hot 100?” 

To answer this question, I decided to figure out what aspects of a song are useful in predicting a song’s ranking on the top 100. To do that, I did the following: 

1. Scrape Billboard.com to grab the Billboard Hot 100 from April 2015 to April 2019 - code found in the [Billboard Web Scraper jupyter notebook](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/Billboard%20Web%20Scaper.ipynb)
2. Utilize Spotify’s API to grab the Billboard Hot 100 songs’ audio features
3. Create a linear regression to predict a song’s ranking on the Billboard chart

