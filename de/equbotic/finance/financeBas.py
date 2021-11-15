import math

#gute Artikel/Code > Links
#https://www.linkedin.com/pulse/python-bootstrapping-zero-curve-sheikh-pancham/
#https://www.r-bloggers.com/2021/07/bootstrapping-the-zero-curve-from-irs-swap-rates-using-r-code/

# -------------------------------------------------------------------
def DF_ofCash(cashRate, days, base):
  '''returns the Discountfactor for a CashRate
     :param cashRate: the Cash Interestrate to be converted as a Factor
     :param days: the number of days in the period
     :param base: the DayCountBase of the Rate (e.g. 360 or 365)
     :return: the DiscountFactor at the end of the period
  '''
  discountFactor = 1.0 / (1.0 + (cashRate * (days / base)))
  return discountFactor

# -------------------------------------------------------------------
def DF_ofZerorate(zeroRate, days):
  '''returns the Discountfactor for a continously compounded ZeroRate
     :param cashRate: the zeroRateto be converted as a Factor
     :param days: the number of days form today
     :return: the DiscountFactor 
  '''
  discountFactor = 1.0 / ( pow(1.0+zeroRate, (days/365)) )
  return discountFactor

# -------------------------------------------------------------------
def ZeroRate_ofDF(df, days):
  '''returns the continously compounded ZeroRate for a DiscountFactor (as Factor on Base 365)
     :param DiscountFactor: to be converted
     :param days: the number of days in the period
     :return: the ZeroRate for the period (Base is 365)
  '''
  zeroRate = -math.log(df) * (365/days)
  return zeroRate

# -------------------------------------------------------------------
def PV_ofCoupon(cpn, years): #, frq):  <todo
  """calcs the PresentValue of a fixed Coupon Cashflow (yearly)
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

# -------------------------------------------------------------------
def addRateToCurve(dates, dfs, zeros, cashRate, days, base, fwdstart):
  """adds a rate or forward rate to the curve (lists of dates, dfs, zeros)
     :param dates: list of the Dates in the Curve (Buckets)
     :param dfs:   list of the DiscountFactor at each Date
     :param zeros: list of Zero Rate at each Date
     :param days:  days of period
     :param base:  the DayCountBase of the Rate (e.g. 360 or 365)
     :param fwdstart: start date of period
  """
  df   = fiB.DF_ofCash(cashRate, days, base)
  if (fwdstart > 0):
    ii = dates.index(fwdstart)
    df = df * dfs[ii]

  days0 = days + fwdstart
  zero  = fiB.ZeroRate_ofDF(df, days0)

  dates.append( days0 ) 
  dfs  .append( df )  
  zeros.append( zero )

# -------------------------------------------------------------------
def addParCpnToCurve(dates, dfs, zeros, cpn, years, mtrdays, lastcpndays):
  """adds a ParCoupon Rate (SwapRate) ro the curve. 
     only yearly and the last cpn date must be known and in the curve.
     swap starts at spot date.
     :param dates: list of the Dates in the Curve (Buckets)
     :param dfs:   list of the DiscountFactor at each Date
     :param zeros: list of Zero Rate at each Date
     :param cpn:   par coupon of the Bond or Swap Rate
     :param years: number of Years 
     :param mtrdays: date of the maturity
     :param lastcpndays: ist the days from today to coupondate before matirity
  """
  pv_spot = fiB.PV_ofCoupon(cpn, years)
  ii_spot = dates.index(2)
  print("pv_spot ",pv_spot)
  pv = pv_spot * dfs[ii_spot]   #present value at today
  print("pv ",pv)

  ii_lastcpn = dates.index(lastcpndays)
  df_lastcpn = dfs[ii_lastcpn]     #df at lastcpn date
  print("df_lastcpn ",df_lastcpn)
  pv_lastcpn = pv / df_lastcpn  #pf updisc. ro last cpn date
  print("pv_lastcpn ",pv_lastcpn) 

  df_lastprd = 1 / (1+cpn)      #df for last cpn for 1 year
  print("df_lastprd ",df_lastprd)

  df_mtr = df_lastprd * df_lastcpn
  print("df_mtr ",df_mtr) 

  zero  = fiB.ZeroRate_ofDF(df_mtr, mtrdays)

  dates.append( mtrdays ) 
  dfs  .append( df_mtr )  
  zeros.append( zero )

# -------------------------------------------------------------------
def ZeroRate_ofCurve(CurveDates, CurveDFs, date):
  """returns the linear interpolatet zeroRate out of the curve at a given date
     :param CurveDates: list of the Dates in the Curve (Buckets)
     :param CurveDFs:   list of the DiscountFactor at each Date
     :param date: date for ZeroRate
     :return: the continously compounded ZeroRate at date
  """
  ll = len(CurveDates)
  for ii in range(1, ll):
    #print (CurveDates[ii-1], CurveDates[ii])
    if CurveDates[ii-1] <= date and CurveDates[ii] > date:

      if CurveDates[ii-1] == date:              #date is a bucket
        return ZeroRate_ofDF(CurveDFs[ii-1], date) 
      else:                         #interpolate between buckets by zerorate
        dist = CurveDates[ii] - CurveDates[ii-1]
        fct1 = (date - CurveDates[ii-1]) / dist
        zy1  = ZeroRate_ofDF(CurveDFs[ii-1], CurveDates[ii-1])
        zy2  = ZeroRate_ofDF(CurveDFs[ii],   CurveDates[ii])
        zy0  = (zy2 - zy1) * fct1
        return zy1 + zy0

  #nothing > extrapolate last zerorate
  return ZeroRate_ofDF(CurveDFs[ll-1], CurveDates[ll-1])

# -------------------------------------------------------------------
def Fwd_ofCurve(CurveDates, CurveDFs, start, end, base):
  """returns the Forward Cash Rate from the given curve
     :param CurveDates: list of the Dates in the Curve (Buckets)
     :param CurveDFs:   list of the DiscountFactor at each Date
     :param start: start date for Forward Rate
     :param end:  end   date for Forward Rate
     :param base: the DayCountBase of the Rate (e.g. 360 or 365)
     :return: the Forward Cash Rate
  """
  zy1 = ZeroRate_ofCurve(CurveDates, CurveDFs, start)
  df1 = DF_ofZerorate(zy1, start)
  #print(df1)
  zy2 = ZeroRate_ofCurve(CurveDates, CurveDFs, end)
  df2 = DF_ofZerorate(zy2, end)
  #print(df2)
  fwdrate = (df1 / df2 -1) * (base/(end-start))
  return fwdrate
  
