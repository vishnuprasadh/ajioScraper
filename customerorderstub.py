import numpy as np
import pandas as pd
import os
from random import randint
import time
from time import localtime
from datetime import datetime
from datetime import timedelta
import math

class customerorderstub:
    df = pd.DataFrame()
    products = pd.Series()
    def __init__(self):
        prdunique = pd.Series()
        self.df = pd.read_csv( os.path.join(os.path.dirname(__file__), 'products.csv'))
        self.products = pd.Series(self.df["productid"]).unique()

    basket = list()

    def generate(self):
        userprodmatrix = dict()
        for user in range(1000,12000):
            np.random.seed()
            ordercount = np.random.randint(1,10)
            print("User {} has {} orders".format(user,ordercount))
            basket = list()
            for orderrange in range(0,ordercount):
                np.random.seed()
                prodid = np.random.choice(self.products,1)[0]

                if userprodmatrix and userprodmatrix.get(user) == prodid:
                    orderrange = orderrange -1
                    pass
                else:
                    self.basket.append({"customerid": user, "productid": prodid, "qty": np.random.randint(1, 8),
                           "ordereddate": self._getrandomdate()})


        df = pd.DataFrame(self.basket)
        df.to_csv(os.path.join(os.path.dirname(__file__),"customerorder.csv"))


    def _getrandomdate(self,randseed=0):
        if randseed >0:
            np.random.seed()
        randdays = np.random.randint(1, 720)
        randhrs = np.random.randint(1, 24)
        randminutes = np.random.randint(1, 59)
        randsecs = np.random.randint(3, 42)
        nowtime = datetime.today() - timedelta(days=randdays, hours=randhrs, minutes=randminutes,
                                                        seconds=randsecs)
        return nowtime.isoformat()


c = customerorderstub()
c.generate()