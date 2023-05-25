# flip_bot
Bot that throws a coin



## **Configuration**
 
First you need to create a .env file in the directory with the rest. There you need to enter the token of your bot that was issued to you later by @BotFather

**Example**
```env
TOKEN=123654789:ADJnndj77da88dJJDnnakkdNNAkkAuE
```

## Configuration in config.py
DB_NAME - database name

TOKEN - token which gets in .env file

## **Running the bot**
Installing necessary modules
```
pip3 install -r requirements.txt
```
Run the bot
```
python3 flip.py
```

## Bot commands:
/start — Greet the bot

/coin - Flip the coin

/stats - Show flip statistics
