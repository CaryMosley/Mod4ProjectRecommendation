import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import surprise
from surprise import Reader, Dataset, SVD

app = flask.Flask(__name__, template_folder='templates')

word_cloud_df = pd.read_csv('word_df_.csv')
content_matrix = pd.read_csv('content_matrix.csv')
del content_matrix['Unnamed: 0']
content_matrix = content_matrix.to_numpy()
ratings_df = pd.read_csv('ratings_df.csv')
del ratings_df['Unnamed: 0']

reader = surprise.Reader(rating_scale=(1, 5))
data = surprise.Dataset.load_from_df(ratings_df, reader)

titles = word_cloud_df[['title','genres', 'plot', 'rating']]
indices = pd.Series(word_cloud_df.index, index=word_cloud_df['title'])

def content_recommendations(title,n):
    '''This function takes in a title and a number of recs and outputs
    the number of closests films based on plot similarity'''
    idx = indices[title]
    sim_scores = list(enumerate(content_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    movies = [i[0] for i in sim_scores]
    print(content_matrix.shape)
    return titles.iloc[movies].sort_values('rating', ascending=False)

def hybrid_rec(userid, favemovie,n):
    '''this takes in a userid, favemovie and n number of recs and outputs those in a sorted list'''
    rec_hybrid = content_recommendations(favemovie,n)
    svd = SVD(n_factors=50, reg_all= 0.05, random_state=150)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    for index, row in rec_hybrid.iterrows():    
        pred = svd.predict(userid, index)
        rec_hybrid.at[index, 'score'] = pred.est
    rec_hybrid = rec_hybrid.sort_values('score', ascending=False)
    return rec_hybrid

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m_name not in indices:
            return(flask.render_template('negative.html',name=m_name))
        else:
            #print("movie found")
            result_final = hybrid_rec(343, m_name, 30)
            #result_final = content_recommendations(m_name, 10)
            result_final.columns = ['title', 'genres', 'plotsummary', 'rating', 'score']

            names = []
            names.append(result_final.iloc[0].title)
            names.append(result_final.iloc[1].title)
            names.append(result_final.iloc[2].title)
            names.append(result_final.iloc[3].title)
            names.append(result_final.iloc[4].title)
            names.append(result_final.iloc[5].title)
            names.append(result_final.iloc[6].title)
            names.append(result_final.iloc[7].title)
            names.append(result_final.iloc[8].title)
            names.append(result_final.iloc[9].title)

            genres = []
            genres.append(result_final.iloc[0].genres)
            genres.append(result_final.iloc[1].genres)
            genres.append(result_final.iloc[2].genres)
            genres.append(result_final.iloc[3].genres)
            genres.append(result_final.iloc[4].genres)
            genres.append(result_final.iloc[5].genres)
            genres.append(result_final.iloc[6].genres)
            genres.append(result_final.iloc[7].genres)
            genres.append(result_final.iloc[8].genres)
            genres.append(result_final.iloc[9].genres)

            plots = []
            plots.append(result_final.iloc[0].plotsummary)
            plots.append(result_final.iloc[1].plotsummary)
            plots.append(result_final.iloc[2].plotsummary)
            plots.append(result_final.iloc[3].plotsummary)
            plots.append(result_final.iloc[4].plotsummary)
            plots.append(result_final.iloc[5].plotsummary)
            plots.append(result_final.iloc[6].plotsummary)
            plots.append(result_final.iloc[7].plotsummary)
            plots.append(result_final.iloc[8].plotsummary)
            plots.append(result_final.iloc[9].plotsummary)

            return flask.render_template('positive.html',movie_names=names,movie_genres=genres,movie_plots=plots,search_name=m_name)

if __name__ == '__main__':
    app.run(debug=True)