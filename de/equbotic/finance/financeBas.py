def DF_ofCash(cashRate, days, base):
  zeroRate = 1 / ((1 + (float(cashRate)) * ((float(days) / float(base))) ))
  return zeroRate
