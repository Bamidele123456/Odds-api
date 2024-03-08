import requests
from datetime import datetime, date
import pytz

def convert_to_est(utc_time):
    # Convert the string to a datetime object
    datetime_utc = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")

    # Define the UTC timezone
    utc_timezone = pytz.timezone("UTC")

    # Convert UTC time to EST time
    est_timezone = pytz.timezone("US/Eastern")
    datetime_est = datetime_utc.replace(tzinfo=utc_timezone).astimezone(est_timezone)

    # Format the datetime as a string
    formatted_est_time = datetime_est.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_est_time

def convert_to_ests(utc_time):
    # Convert the string to a datetime object
    datetime_utc = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")

    # Define the UTC timezone
    utc_timezone = pytz.timezone("UTC")

    # Convert UTC time to EST time
    est_timezone = pytz.timezone("US/Eastern")
    datetime_est = datetime_utc.replace(tzinfo=utc_timezone).astimezone(est_timezone)

    # Format the datetime as a string with time only
    formatted_est_time = datetime_est.strftime("%H:%M:%S")

    return formatted_est_time

def query(data):
    API_URL = "https://hh0pa0lb9sed7tc5.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "inputs": f"Objective: Develop a strategic analysis framework to identify a list of 20+ theoretical high-risk on this data {data}, high-value opportunities across various sports, focusing on maximizing the theoretical cash-out value. This analysis will strictly avoid considering live games or outcomes that are dependent on actual winning or losing, emphasizing pre-event conditions and strategic insights. Historical Insight Gathering: Analyze patterns in pre-event odds movements, team/player conditions, and market sentiments that historically lead to undervalued opportunities..3. Predictive Engagement Strategy:- Optimal Theoretical Engagement: Use predictive modeling to forecast the most advantageous moments for a theoretical cash-out based on pre-event analysis, avoiding any reliance on live game developments.4. Theoretical Cash-Out Strategy Development:- Compile the identified opportunities into a strategic plan that outlines the rationale for each selection and projects optimal timing for the highest theoretical cash-out value, all while ensuring the analysis remains within a purely theoretical and strategic context.Output:- A detailed strategic plan listing 20+ theoretical high-risk, high-value selections across sports, with each entry including:- Theoretical Moneyline odds- Strategic insight based on historical and pre-event data- A projection of the optimal theoretical timing for cash-outs, aiming to maximize value based on comprehensive, data-driven insights, without the need for live game outcomes.End Goal:To leverage a data-driven approach for strategic planning and analysis in sports, providing theoretical insights into optimizing cash-out strategies. This framework is intended for educational, research, or strategic decision-making purposes, focusing on pre-event analysis and historical data to explore theoretical betting dynamics without engaging in actual betting activities.","parameters": {"temperature": 0.1}}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


sports = [
    'soccer_epl',
    'basketball_nba',
    'americanfootball_nfl',
    'baseball_mlb',
    'icehockey_nhl',
    'aussierules_afl',
    'golf_us_open_winner',
    'cricket_test_match',
    'golf_masters_tournament_winner',
    'golf_the_open_championship_winner',
    'mma_mixed_martial_arts',
    'rugbyleague_nrl',
    'soccer_australia_aleague',
    'soccer_brazil_campeonato',
    'soccer_uefa_european_championship',
    'soccer_usa_mls',
    'tennis_wta_french_open',
    'tennis_atp_french_open',
    'soccer_sweden_superettan',
    'soccer_sweden_allsvenskan',
    'soccer_spain_segunda_division',
    'soccer_norway_eliteserien',
    'soccer_league_of_ireland',
    'soccer_japan_j_league',
    'soccer_finland_veikkausliiga',
    'soccer_denmark_superliga',
]
data = []
for sport in sports:
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
    params = {
        'apiKey': "ca53c9d2e482209df1604ea50bbcddcb",
        'regions': 'us,uk,eu,au',
        'oddsFormat': 'decimal'
    }
    response = requests.get(url, params=params)
    data.append(response.json())
filtered_data = []

for outer_list in data:
    for inner_dict in outer_list:
        if 'bookmakers' in inner_dict and isinstance(inner_dict['bookmakers'], list):
            for bookmaker in inner_dict['bookmakers']:
                if 'markets' in bookmaker and isinstance(bookmaker['markets'], list):
                    for market in bookmaker['markets']:
                        if market['key'] == 'h2h' and 'outcomes' in market and isinstance(market['outcomes'], list):
                            for outcome in market['outcomes']:
                                if 'price' in outcome and isinstance(outcome['price'], (int, float)) and outcome[
                                    'price'] > 5.0:
                                    commence_time = convert_to_est(inner_dict.get('commence_time', ''))
                                    today = date.today()
                                    # Check if the commence_time is on the current day
                                    if datetime.strptime(commence_time, "%Y-%m-%d %H:%M:%S").date() == today:
                                        filtered_data.append({
                                            'sport_key': inner_dict.get('sport_key', ''),
                                            'key': bookmaker.get('key', ''),
                                            'sport_title': inner_dict.get('sport_title', ''),
                                            'sport_team': f"{inner_dict.get('home_team', '')} vs {inner_dict.get('away_team', '')}",
                                            'commence_time': convert_to_ests(inner_dict.get('commence_time', '')),
                                            'outcome_name': outcome.get('name', ''),
                                            'outcome_price': outcome.get('price', 0.0)
                                        })




answer = query(filtered_data)
print(answer)