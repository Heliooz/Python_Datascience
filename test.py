import plotly_express as px
from src.read_data import read_data
from src.get_data import get_data

##get_data()
data = read_data()

count = data.groupby(['city']).count()['review_scores_value']

print(count)

score = data.groupby(['city', 'review_scores_value']).count()['listing_id']/count*100

print(score)

fig = px.line(score, color='city')
fig.show()