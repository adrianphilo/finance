import math

def DF_ofCash(cashRate, days, base):
  '''returns the Discountfactor for a CashRate
     :param cashRate: the Cash Interestrate to be converted as a Factor
     :param days: the number of days in the period
     :param base: the DayCountBase of the Rate (e.g. 360 or 365)
     :return: the DiscountFactor at the end of the period
     '''
  discountFactor = 1.0 / (1.0 + (cashRate * (days / base)))
  return discountFactor

def ZeroRate_ofDF(df, days):
  '''returns the continously compounded ZeroRate for a DiscountFactor (as Factor on Base 365)
     :param DiscountFactor: to be converted
     :param days: the number of days in the period
     :return: the ZeroRate for the period
  '''
  zeroRate = -math.log(df) / (days/365)
  return zeroRate
