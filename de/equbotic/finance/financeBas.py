import math

#gute Artikel/Code > Links
#https://www.linkedin.com/pulse/python-bootstrapping-zero-curve-sheikh-pancham/
#https://www.r-bloggers.com/2021/07/bootstrapping-the-zero-curve-from-irs-swap-rates-using-r-code/

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
  zeroRate = -math.log(df) * (365/days)
  return zeroRate

def PV_ofCoupon(cpn, years): #, frq): 
  """calcs the PresentValue of a fixed Coupon Cashflow
     :param cpn: the coupon as factor
     :param years: Maturity in Years
     :return: the present value of face value 1 
  """
  #pv of the face value
  pv = 1 / math.pow( (1+cpn), years)
  #plus sum of pvs of cpns
  for ii in range(1, years):
    pv = pv + cpn / math.pow( (1+cpn), years)
  return pv

def zero_ofCurve(CurveDates, CurveDFs, date):
  """returns the zero rate out of the curve at a given date
  """
  
def fwd_ofCurve(CurveDates, CurveDFs, start, end, base):
  """returns the fwd_rate from the given curve
  """
