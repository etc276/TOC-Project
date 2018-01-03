# chatBot

## how to run
1. install python3
2. install python3-pip
2. `pip3 install -r requirement.txt`
3. `python3 run.py`

## how to talk
1. send `start` to start
2. send `cancel` to cancel
3. other option will show on keyboard

```graphviz
digraph hierarchy {

                nodesep=1.0
                
                node [color=Red,fontname=Courier,shape=circle]
                
                edge [color=Black, style=dashed] 

                idle->{beauty deck joke}
                beauty->{ok}
                {ok, deck, joke}->{idle}
                {rank=same;deck joke beauty}
}
```

## Features
* get today's beautiful pictures
* get newest deck code of hearthstone
* get lol joke ^^

## Bonus
* **one-time keyboard**, easy to use
* **send images** with telegram api
* **dynamic data** by parsing website (using beautifulsoup)
* **regular expression** to determine user input and parsing data