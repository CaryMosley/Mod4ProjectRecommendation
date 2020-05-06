import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df = pd.read_csv('df.csv')
raw_matrix = pd.read_csv('raw_matrix.csv')
raw_matrix = raw_matrix.to_numpy()

titles = df[['title','genres', 'plot', 'rating']]
indices = pd.Series(df.index, index=df['title'])

def get_recommendations(title,n):
    '''This function takes in a title and a number of recs and outputs
    the number of closests films based on plot similarity'''
    idx = indices[title]
    sim_scores = list(enumerate(raw_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    movies = [i[0] for i in sim_scores]
    return titles.iloc[movies].sort_values('rating', ascending=False)

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
            result_final = get_recommendations(m_name, 10)
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
            #names = ['Game of Thrones', 'Lord of the Rings', 'Harry Potter', 'Heat', 'Grease', 'Lost', 'Prison', 'Superman', 'Batman', 'Emoji']

            return flask.render_template('positive.html',movie_names=names,movie_genres=genres,search_name=m_name)

if __name__ == '__main__':
    app.run()