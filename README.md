# Hidden Gems - Movie Recommendation System
By: **Cary Mosley** and **Bryan Santos**


This projects presents a recommendation system for movies. Our aim is to ensure that our recommendation engine is not biased towards popular movies. We want to be able to recommend **hidden gems** based on multiple criteria. Our goal is to build a hybrid model that will focus on content based recommendations when we do not have enough data for a user profile and weight our recommendations more towards similar users as we gather more data about our consumers. As ratings tend to be skewed towards popular movies we want to focus on movies that have high ratings but are not simply the most popular movies.

Dataset: 
- https://grouplens.org/datasets/movielens/100k
- API calls from http:themoviedatabase.org

Our presentation deck is located here: https://docs.google.com/presentation/d/1ke-who9ST1NDQN7wbLq2o_EI8LS4KzWqLAtPsbv5U7w/edit?ts=5eb2fe5a

## Objectives

The main issue with recommendation systems based on other user reviews (collaborative-filtering) are cold start and sparsity. As seen in the image below, movies being recommended by traditional movies are skewed towards the popular ones. The goal is to tap into this long tail and be able to recommend quality but less popular movies.

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/bryan-santos/images/longtail.png)

## Feature Engineering

### Plot

* We added plot summaries of each movie to run content-based models based on Natural Language Processing (NLP) and as foundation for Hybrid Models
* Bag of Words and TF-IDF were added

### Genres

Genres were included to ensure they play a factor in making the recommendation because chances are, people will like movies in the similar genre

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/bryan-santos/images/genres.png)

### Quality Index
We bucketed ratings in order to get movie clusters based on quality

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/bryan-santos/images/rating.png)

### Popularity Index
We added popularity index based on the count of reviews on each movie

## Models

The following models were built and compared against each other using different performance metrics (AUC Score, RMSE, MAE, Hit Rate, and even just through domain knowledge or eye-test)

### Collaborative-Filtering
* Item-Item Filterting
* User-User Filtering
* Memory-Based Methods (KNN and SVD)

### Content-Based
* Bag of Words
* TF-IDF

### Hybrid Models
* **Hybrid Model 1** - running the TF-IDF model (content-based) first to get initial recommendations then the rating of each one is predicted through our best-performing SVD model (collaborative-filtering) which is then sorted
* **Hybrid Model 2** - calculate the aggregate of cosine-similarity of movies based on TF-IDF model (content-based) and our best-performing SVD model (collaborative-filtering)
* **Hybrid Model 3**- use LightFM, a python package well-known for hybrid modeling

## Conclusion and Future Steps

Our final model is Hybrid Model 2 which provides a balanced recommendation between Content-Based and Collaborative-Filtering

### Next Steps
* Use the entire movielens dataset (2M) and not just (100k) to be able to cover most movies in the recommendation
* Add more features and create a better ratings predictor for our hybrid model
* Compile a user profile that is not solely based on ratings they have made but information about the users themselve

## Live Front-End
We have a live web-based front-end created through Flask. The engine under the hood is Hybrid Model 2.

**Search Page**

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/bryan-santos/images/live1.png)

**Results Page**

![models](https://github.com/CaryMosley/Mod4ProjectRecommendation/blob/bryan-santos/images/live2.png)

