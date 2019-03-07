# QuakeLogParser

- To run the log parser, use:

```bash
python parser/core.py
```

The output will be in a file called data.json

- To run the unit tests, use:

```bash
python parser/test.core.py
```


- In order to make this code, I made the assumption that the name of the players may not be unique.
This makes some names appear more than one time in some games (when the player disconnects than reconnects, for example).
Since we don't have an unique id for each player, we can't be 100% sure if the player connecting is the same or another one with the same name.