# OptionPricing
A dashboard built with Dash and Plotly to visualize the Greek surface of listed European options.

This repo contains a library to price european calls and puts using Black-Scholes models. It can retrieve listed options of any underlying using [MarketWatch](https://www.marketwatch.com/).
Implied volatility is computed using market prices and greeks are then calculated.

Finally an interactive dashboard using dash plotly can run on your computer or on a docker container.


![image](https://user-images.githubusercontent.com/45851831/212221613-d27e0b15-0363-4adc-83d1-cefeb992f9db.png)

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
- Python 3.10+
- Dash and Plotly (can be installed via pip)

'''pip install dash plotly'''

## Running the app locally
1. Clone the repository
```git clone https://github.com/Haha89/OptionPricing```

2. Navigate to the project directory
```cd OptionPricing```
3. Run the app
```python app.py```

The app will be running on http://localhost:8050/

# Running the app on a docker container
Run the following commands
- ```docker build -t dashboard .```
- ```docker run -p 8050:8050 dashboard```
The app will be running on http://localhost:8050/

# Data
The Greek surface data is pulled from a data source of your choice, you can use an API or read it from a CSV file. You will need to modify the code accordingly to retrieve the data and pass it to the Plotly Scatter3d plot.

# Built With
- Dash - Main framework used to build the dashboard
- Plotly - Used to create the Greek surface visualization

# License
This project is licensed under the MIT License - see the LICENSE.md file for details

# Next steps
For now the pricing model is very simple. Adding jump diffusion, a dividend yield will be interesting. Adding other numerical techniques to price options like Monte-Carlo is planned.
