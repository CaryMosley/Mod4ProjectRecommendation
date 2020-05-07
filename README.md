# Hidden Gems - Movie Recommendation System
By: **Cary Mosley** and **Bryan Santos**


This projects presents a recommendation system for movies. Our aim is to ensure that our recommendation engine is not biased towards popular movies. We want to be able to recommend **hidden gems** based on multiple criteria. Our goal is to build a hybrid model that will focus on content based recommendations when we do not have enough data for a user profile and weight our recommendations more towards similar users as we gather more data about our consumers. As ratings tend to be skewed towards popular movies we want to focus on movies that have high ratings but are not simply the most popular movies.

Dataset: 
- https://grouplens.org/datasets/movielens/100k
- API calls from http:themoviedatabase.org

Our presentation deck is located here: https://docs.google.com/presentation/d/1ke-who9ST1NDQN7wbLq2o_EI8LS4KzWqLAtPsbv5U7w/edit?ts=5eb2fe5a

## Objectives

The main issue with recommendation systems based on other user reviews (collaborative-filtering) are cold start and sparsity. As seen in the image below, movies being recommended by traditional movies are skewed towards the popular ones. The goal is to tap into this long tail and be able to recommend quality but less popular movies.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/longtail.png)

## Preprocessing and EDA

### Data Sources

We loaded in various datasets provided by movielens and then ran an API call to grab plot summaries for each of our films. Once we had this we grabbed the union of films where we had movieId and plot summaries as well as dropped the handful of duplicates from our dataset. This resulted in 9573 total films and 100293 total ratings.

### EDA
Below we can see the ratings count as well as the distrubtio of ratings. THe most common ratings values were 4.0 and 3.0, with perfect films being significantly more common than very poorly rated films.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/ratings.png)

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/ratingsdist.png)

We can see that most users rated only a handful of films with a few super users rating over a thousand. This is likely to introduce bias as our model is going to be very skewed towards the rating preference of these power users.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/userdist.png)

When we examile genre, Film-Noir has the highest rating of all genres followed by War, Documentary and Crime. Comedy and Horror are the lowest rated.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/genres.png)

In this particular sample of dataset provided from Movielens, we see a sudden resurgence in the number of available ratings beginning from the year 2015.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/yeardist.png)

As we showed in our problem statement there is a long-tail in movie popularity.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/longtail.png)

We grouped our films into ratings buckets of top, average, and low and then created word clouds to see if plot could be useful in classifying our films. Based on these word clouds they will not perform well as the most common words seem to be very similar. 

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/wordcloudtop.png)

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/wordcloudavg.png)

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/wordcloudlow.png)

## Feature Engineering

### Plot

* We added plot summaries of each movie to run content-based models based on Natural Language Processing (NLP) and as foundation for Hybrid Models. We then crated a bag of words and TF-IDF feature for content similarity.

Genres were included to ensure they play a factor in making the recommendation because chances are, people will like movies in the similar genre


### Popularity Index

We added popularity index based on the count of reviews on each movie

## Models

The following models were built and compared against each other using different performance metrics (AUC Score, RMSE, MAE, Hit Rate, and even just through domain knowledge or eye-test)

### Collaborative-Filtering
* Item-Item Filterting
* User-User Filtering
* Memory-Based Methods (KNN and SVD)

Based on RMSE and Hit-Rate we chose the SVD model as our best collaborative-filtering based model. RMSE evaluates how far our rating is from the predicted. Hit-rate is a method in which we predict a number of films and then check to see how many if any were present in the user's list. This metric can run into issues with sparsity as if were looking predicting 10 movies and the user has only rated 5 then clearly the max hit rate can be is .5. However this metric is still useful when comparing between models. Next we will combine our SVD Collaborative-Flitering model with our chosen content-based model to create a final hybrid model.

### Content-Based
* Bag of Words
* TF-IDF

We build 4 different classification models to see if TF-IDF combining plot and genre would be enough to group movies into top, average, and low ratings bucket. We used Naive Bayes, Logistic, SGD, and a neural net classifier. The Naive Bayes, SGD and neural net simply classified everything into the majority class, while the logisitic model did make some specific rankings. Although the accuray of the logistic model was lowest, when we look at the confusion matrix we can see that it is creating groupings into these distinct classes. However, as we saw from the word clouds, plot summary does not seem to be able to classify movie rankings alone. This is in-line with what we would expect and we then moved on to create a content based recommendation system using cosine similarty of our TF-IDF feature.

### Hybrid Models
* **Hybrid Model 1** - running the TF-IDF model (content-based) first to get initial recommendations then the rating of each one is predicted through our best-performing SVD model (collaborative-filtering) which is then sorted

* **Hybrid Model 2** - calculate the aggregate of cosine-similarity of movies based on TF-IDF model (content-based) and our best-performing SVD model (collaborative-filtering). We weight the similarity metrics of content and collaborative-filtering based on how popular the input movie is. Since our goal is to reach the long tail, we weight our results more towards content the higher the popularity of the film is. 

* **Hybrid Model 3**- use LightFM, a python package well-known for hybrid modeling

Once we built these models we played around using some of our favorite movies to attempt to evaluate which one we believed was giving us the best results. Based on this we decided to implement the first hybrid model in a front-end UI.

## Conclusion and Future Steps

Our final model is our Hybrid Model 1 which gets content-based recommendations and then predicts and sorts the results using our colabortive-filtering SVD model.

### Next Steps

* Use the entire movielens dataset (2M) and not just (100k) to be able to cover most movies in the recommendation. Having significantly more ratings will help us avoid being biased towards the preferences of a few power users. We will also have more breadth in the type of movies we cna recommend 

* Add more features and create a better ratings predictor for our hybrid model

* Compile a user profile that is not solely based on ratings they have made but information about the users themselves.

## Live Front-End
We have a live web-based front-end created through Flask. The engine under the hood is Hybrid Model 1.

**Search Page**

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/live1.png)

**Results Page**

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/CaryM/images/live2.png)

