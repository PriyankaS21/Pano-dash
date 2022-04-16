import dash
import dash_auth
import dash_bootstrap_components as dbc
import pymongo
from myBasicAuth import MyBasicAuth

client = pymongo.MongoClient(host='localhost', port=27017)
mydb = client.dxcpanodash

userdata = list(mydb.auth_user.find(
    {}, {'username': 1, 'password': 1, '_id': 0}))

formatdata = {}
for users in userdata:
    formatdata[users['username']] = users['password']

VALID_USERNAME_PASSWORD_PAIRS = formatdata

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
# mysheet = "assests\\typography.css"
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.UNITED, FA],
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale:1.2, minimum-scale:0.5,'}
])
auth = MyBasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
