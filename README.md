# How to Rank on the Billboard Top 100 using Linear Regression

After being denied a spot on the Billboard top 100 Country charts, Old Town Road by Lil Nas X grabbed the number 1 spot on the Billboard Hot 100 chart over all genres. The song is odd but catchy meeting at the intersection of rap and country. Something that has not really been done before, in this fashion. Not only is the song different from its predecessors, it is also the shortest number 1 song on the Hot 100 since 1965. 

The story of Old Town Road and its journey to the top made me wonder, “What does it take for a song to become number 1 on Billboard’s Hot 100?” 

To answer this question, I decided to figure out what aspects of a song are useful in predicting a song’s ranking on the top 100. To do that, I did the following: 

1. Scrape Billboard.com to grab the Billboard Hot 100 from April 2015 to April 2019 (see [Billboard Web Scraper jupyter notebook](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/Billboard%20Web%20Scaper.ipynb) for more information)
2. Utilize Spotify’s API to grab the Billboard Hot 100 songs’ audio features (see [Spotify API script](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/spotify_api.py) for more information)
3. Perform EDA, clean the data for analysis, and feature engineering (see [Data Cleaning and Feature Engineering jupyter notebook](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/Data%20Cleaning%20and%20Feature%20Engineering.ipynb))
3. Create a linear regression to predict a song’s ranking on the Billboard chart (see [Linear Regression notebook](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/Linear%20Regression%20-%20All%20Features.ipynb) for more information)

## EDA

While doing some initial EDA, I found that the following artists had the most songs on the Billboard Charts over the last 7 years.

![Top 20 Artists from 2012 to 2019](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/top_20_artists_by_year.png)
<sup>created using Tableau</sup>

I also looked at the correlations between the features and my target variable. 
![Correlation Heatmap](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/corr.png)
<sup>created using Seaborn</sup>

Because a lower rank is better in this case, a negative correlation means that as the rank goes down (which is a good thing), the feature goes up and vice versa. For a positive correlation, as the rank goes up (which is a bad thing) the feature goes up and vice versa.

Another interesting insight we get from this correlation plot is how year is negatively correlated to duration, meaning songs are getting shorter as the years increases, which directly supports many reports that songs are getting shorter and shorter due to streaming services and their payout system. Additionally, the energy of songs are also decreasing, but acousticness and danceability are increasing.

Looking at our correlations, we can automatically delete the average rank as this might cause multicollinearity as they are too related. As such, let's create a smaller df without that column while also labelling our features and target variables.

## Linear regression modeling

Using skLearn, I split my data into test, train, and validation sets using the train_test_split function.  I then tried five different models, a regular linear regression with no transformations, a ridge regression, a degree 2 polynomial regression with ridge cross validation, lasso regression, and a degree 2 polynomial regression with lasso cross validation. Because my data is right skewed, I also standardized my data so that all the feautres are on the same scale. This is also necessary when using regularization, which was part of the models used. Using our polynomial regression and lasso regularization, I got a .624 R<sup>2</sup> score.

## Results and Conclusion

With my model, I found that the following feautres had the highest coefficients:

![Lasso Coefficients](https://github.com/amyksu/predicting_billboard_charts_ranking/blob/master/Coefficients_lasso.png)
<sup>created using Seaborn</sup>

In addition, I used the Mean Absolute Error (MAE) to calculate my error. MAE measures the average magnitude of the errors in a set of predictions, without considering their direction. As my prediction only has positive values and the magnitude of my errors is not as important, this makes the most sense for me to use. I found that my model has a errors of around 14.3, meaning that my prediction model will be around 14.3 ranks off. 
Based on the above, we can gather the following conclusions:

To have a higher rank on the charts,
  - stay on the chart longer, but not too long or else it has the opposite effect
  - have more songs on the chart 
  - have more songs previously on the chart 

Interestingly enough, none of the spotify audio features had a high coefficient in my model. What this could mean is that the actual art of music is not a big contributor in charting on Billboard. It's the business side of music, including the marketing, building an audience and brand, engaging the audience, that is important. Becuase of the way we are consuming music nowadays, as my data shows, the more songs you release, the more likely you are going to end up on the chart. 
  
## Future Work

This project was done with the goal to learn how to scrape a website and use a linear regression model, I pigeonholed myself into those techniques. For future work, I would try using this data with an ordinal logistic regression which is more appropriate for rank data. 

In addition, I would try gathering more data such as radio plays, spotify stream counts, and social media information including aritst interaction with fans, follower counts, number of posts, and mentions. 
