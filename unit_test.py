import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data into a DataFrame
df = pd.read_csv('yokyo.log', sep=" ", header=None,
                 names=["Timestamp", "IP Address", "HTTP Method",
                        "Path", "Status Code","HTTP Version", "Traffic Source", "User Agent", "Country"],
                 usecols=["Timestamp", "IP Address", "HTTP Method",
                        "Path", "Status Code","HTTP Version","Traffic Source", "User Agent", "Country"])


    # Define aliases for User Agent and Path
user_agent_aliases = {
    # Desktop devices
    "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/90.0.4430.212-Safari/537.36": "Windows Chrome",
    "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Edge/90.0.818.62-Safari/537.36": "Windows Edge",
    "Mozilla/5.0-(Macintosh;-Intel-Mac_OS-X-10_15_7)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/90.0.4430.212-Safari/537.36": "Mac Chrome",
    "Mozilla/5.0-(Macintosh;-Intel-Mac_OS-X-10_15_7)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Version/14.1-Safari/537.36": "Mac Safari",
    "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/90.0.4430.93-YaBrowser/21.5.1.174-Yowser/2.5-Safari/537.36": "Windows Yandex",
    "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64;-rv:88.0)-Gecko/20100101-Firefox/88.0": "Windows Firefox",
    
    # Mobile Devices
    "Mozilla/5.0-(Linux;-Android-11;-SM-G975F)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/88.0.4324.181-Mobile-Safari/537.36": ["Android 11 - Samsung Galaxy S10"],
    "Mozilla/5.0-(iPhone;-CPU-iPhone-OS-14_4-like-Mac-OS-X)-AppleWebKit/605.1.15-(KHTML,-like-Gecko)-Version/14.0.3-Mobile/15E148-Safari/604.1": ["iOS 14 - iPhone"],
    "Mozilla/5.0-(Linux;-Android-11;-SM-G986B)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/90.0.4430.210-Mobile-Safari/537.36-EdgA/46.3.2.5155": ["Android 11 - Samsung Galaxy S20"],
    "Mozilla/5.0-(iPad;-CPU-OS-14_4-like-Mac-OS-X)-AppleWebKit/605.1.15-(KHTML,-like-Gecko)-Version/14.0-Mobile/15E148-Safari/604.1": ["iOS 14 - iPad"],
    "Mozilla/5.0-(Linux;-Android-11;-SM-A515F)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/89.0.4389.105-Mobile-Safari/537.36": ["Android 11 - Samsung Galaxy A51"],

    # TV devices
    "Mozilla/5.0-(SMART-TV;-Linux;-Tizen-5.0)-AppleWebKit/537.36-(KHTML,-like-Gecko)-SamsungBrowser/2.2-Chrome/63.0.3239.84-TV-Safari/537.36": ["Samsung Smart TV - Tizen 5.0"],
    "Mozilla/5.0-(SMART-TV;-X11;-Linux-x86_64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Version/4.0-Chrome/78.0.3904.108-Safari/537.36": ["Smart TV - Linux x86_64"],
    "Mozilla/5.0-(SMART-TV;-Linux;-Tizen-3.0)-AppleWebKit/538.1-(KHTML,-like-Gecko)-Version/3.0-TV-Safari/538.1": ["Samsung Smart TV - Tizen 3.0"],
    "Mozilla/5.0-(SMART-TV;-Linux;-Tizen-5.5)-AppleWebKit/537.36-(KHTML,-like-Gecko)-SamsungBrowser/2.2-Chrome/63.0.3239.84-TV-Safari/537.36": ["Samsung Smart TV - Tizen 5.5"],
    "Mozilla/5.0-(SMART-TV;-X11;-Linux-armv7l)-AppleWebKit/537.42-(KHTML,-like-Gecko)-Safari/537.42": ["Smart TV - Linux armv7l"],

 }
    # Replace User Agent values with aliases
df["User Agent"] = df["User Agent"].replace(user_agent_aliases)
# Create a DataTable component to display the data
table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)

# Create a Modal component to display the table
modal = dbc.Modal(
    [
        dbc.ModalHeader("Data Table"),
        dbc.ModalBody(table),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ml-auto")
        ),
    ],
    id="modal",
    size="xl",
)

# Create a button to open the modal
button = dbc.Button("View Data", id="open")

app.layout = html.Div([button, modal])

# Callback to open the modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True)
