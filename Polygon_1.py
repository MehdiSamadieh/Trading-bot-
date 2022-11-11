import datetime
import time
from polygon import RESTClient


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def main():
    key = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
     price =[]

     start_time = time.time()
     seconds = 5



     nw_price=[]
     flag=0


        #f = open("my.txt", "r")
    with open('my.txt', 'r') as file:
            chosen = []

            for line in file:

               for word in line.split():
                   chosen.append(word)
                   print("----------------")
                   print(word)

    from_ = "2021-06-23"
    to = "2021-06-23"
    for st in chosen:
      print("chosen[i]=",st)
      print(chosen)
      resp = client.stocks_equities_aggregates(st, 1, "minute", from_, to, unadjusted=False)
      flag=flag+1
      print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")

      for result in resp.results:
            dt = ts_to_datetime(result["t"])
            print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
      nw_price.append(resp.results[-1]['h'])
      if flag>len(price):

        price.append(resp.results[-1]['h'])

            ##############################getting price for the first time
    print("price",price)

    print("new price",nw_price)


if __name__ == '__main__':
    main()