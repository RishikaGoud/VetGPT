from flask import Flask, request, render_template
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Load your dataset
df = pd.read_csv('../VetGPT/Data/merged_file.csv')

def search_dataset_fuzzy(df, query, threshold=70):
    query_lower = query.lower()
    results = []
    
    for _, row in df.iterrows():
        title = row.get('Title', '')
        description = row.get('Field', '')
        title_score = fuzz.partial_ratio(query_lower, str(title).lower())
        description_score = fuzz.partial_ratio(query_lower, str(description).lower())
        
        if title_score >= threshold or description_score >= threshold:
            url = row.get('Title_URL', 'No URL available')
            results.append({
                'title': title,
                'url': url,
                'description': description,
                'score': max(title_score, description_score)
            })

    # Sort results by score and return the best match
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    if results:
        best_match = results[0]
        return best_match
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    response = search_dataset_fuzzy(df, query)
    return render_template('index.html', query=query, response=response)

if __name__ == '__main__':
    app.run(debug=True)
