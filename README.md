# OptionPricing
This repo contains a library to price european calls and puts using Black-Scholes models. It can retrieve listed options of any underlying using [MarketWatch](https://www.marketwatch.com/).
Implied volatility is computed using market prices and greeks are then calculated.

Finally an interactive dashboard using dash plotly can run on your computer or on a docker container.


![image](https://user-images.githubusercontent.com/45851831/212221613-d27e0b15-0363-4adc-83d1-cefeb992f9db.png)


# Setup on your computer (Python 3.10+)
Install the requirements and execute app.py.

# Setup on a docker container
Run the following commands
- docker build -t dashboard .
- docker run -p 8050:8050 dashboard

Then open your localhost:8050 to see the application

# Next steps
For now the pricing model is very simple. Adding jump diffusion, a dividend yield will be interesting. Adding other numerical techniques to price options like Monte-Carlo is planned.
