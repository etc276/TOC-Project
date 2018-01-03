# chatBot

## how to run
1. install python3
2. install python3-pip
3. `pip3 install -r requirement.txt`
4. `./ngrok http 5000`
5. paste bot API and url to `app.py`
6. `python3 run.py`

* if you have trouble in install pygraphviz
  * [Setup pygraphviz on Ubuntu](https://www.jianshu.com/p/a3da7ecc5303)

## how to talk
1. send `start` to start
2. send `cancel` to cancel (back to init)
3. other option will show on keyboard

![image](https://github.com/etc276/TOC-Project-2017/blob/master/img/show-fsm.png)

## Features
* get today's beautiful pictures
* get newest deck code of hearthstone
* get lol joke ^^

## Bonus
* **one-time keyboard**, easy to use
* **send images** with telegram api
* **dynamic data** by parsing website (using beautifulsoup)
* **regular expression** to determine user input and parsing data
