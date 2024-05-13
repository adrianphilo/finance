Aus der Tagesdatei soll TICKPRIC/TICKSIZE_LAST behalten werden.
Es soll in eine csv geschrieben werden: Format row:
time, price, size  
….

todo:
vorbereiten dateien
vorbereiten 3-long-array (lasttrade) for row.
bis eof
  lesen row
  if TICKSIZE_LAST  -> merken size in lasttrade[2]   
  if TICKPRIC_LAST -> 
      merken time in lsttrade[0]
      merken price*10 in lasttrade[1]
      schreiben row to csv

input-file example:
TICKPRIC_LAST: 1712647020255 18483.0
TICKSIZE_LAST: 1712647020256 1
TICKSIZE__BID: 1712647020570 5
TICKSIZE__ASK: 1712647020570 4
TICKPRIC__BID: 1712647021198 18481.0
9:17:1 26221198 mid: 18482.0 >>>order?>>> time: 6385 midchg: 0.0 chgPerS: 0.0 dirOf4: 0 avgall: 2.01902343109861E-4 timall: 1712647021198 avg2: 2.01902343109861E-4 time2: 1712647021198 avg0: 2.01902343109861E-4 vola: 0.7196933112363292 gavg: 18481.282608695652 time0: 1712647021198
TICKSIZE__BID: 1712647021199 14
TICKSIZE__BID: 1712647021199 14
TICKSIZE__ASK: 1712647021199 7
TICKSIZE__BID: 1712647021822 12
TICKSIZE__ASK: 1712647021823 10
TICKPRIC_LAST: 1712647022552 18481.0
TICKSIZE_LAST: 1712647022552 1
TICKSIZE__ASK: 1712647023725 9
TICKPRIC_LAST: 1712647023825 18483.0
TICKSIZE_LAST: 1712647023825 1
TICKPRIC_LAST: 1712647024074 18481.0
TICKSIZE_LAST: 1712647024075 1
TICKSIZE__BID: 1712647024075 10
TICKSIZE__BID: 1712647024825 11
TICKSIZE__ASK: 1712647024825 8
TICKPRIC__BID: 1712647025430 18479.0
9:17:5 26225430 mid: 18481.0 >>>order?>>> time: 10349 midchg: -1.5 chgPerS: -0.14494154024543435 dirOf4: -2 avgall: 2.4757189555363524E-4 timall: 1712647025430 avg2: 2.4757189555363524E-4 time2: 1712647025430 avg0: 2.4757189555363524E-4 vola: 0.7067998433654258 gavg: 18481.270833333332 time0: 1712647025430
TICKSIZE__BID: 1712647025431 12
TICKPRIC__ASK: 1712647025431 18481.0
9:17:5 26225431 mid: 18480.0 >>>order?>>> time: 6570 midchg: -2.0 chgPerS: -0.30441400304414 dirOf4: -2 avgall: 2.4758268645186355E-4 timall: 1712647025431 avg2: 2.4758268645186355E-4 time2: 1712647025431 avg0: 2.4758268645186355E-4 vola: 0.7359347722029297 gavg: 18481.22 time0: 1712647025431
TICKSIZE__ASK: 1712647025432 6
TICKSIZE__BID: 1712647025432 12
TICKSIZE__ASK: 1712647025432 6
TICKSIZE_LAST: 1712647026076 11
TICKPRIC__ASK: 1712647026077 18480.0
9:17:6 26226077 mid: 18479.5 >>>order?>>> time: 7009 midchg: -3.0 chgPerS: -0.428021115708375 dirOf4: -4 avgall: 2.545532295108189E-4 timall: 1712647026077 avg2: 2.545532295108189E-4 time2: 1712647026077 avg0: 2.545532295108189E-4 vola: 0.793837198589087 gavg: 18481.153846153848 time0: 1712647026077
TICKSIZE__ASK: 1712647026078 7
TICKSIZE__BID: 1712647026078 2
TICKSIZE__ASK: 1712647026079 7
TICKSIZE__BID: 1712647026577 6
TICKSIZE__ASK: 1712647026577 6
TICKSIZE_LAST: 1712647026828 1
TICKPRIC__ASK: 1712647026829 18481.0
9:17:6 26226830 mid: 18480.0 >>>order?>>> time: 5632 midchg: -2.0 chgPerS: -0.35511363636363635 dirOf4: -2 avgall: 2.626781163616006E-4 timall: 1712647026830 avg2: 2.626781163616006E-4 time2: 1712647026830 avg0: 2.626781163616006E-4 vola: 0.8089011524814258 gavg: 18481.11111111111 time0: 1712647026830
TICKSIZE__ASK: 1712647026831 13
TICKSIZE__BID: 1712647026831 8
TICKSIZE__ASK: 1712647026831 13
TICKSIZE__ASK: 1712647027578 10
TICKPRIC_LAST: 1712647028181 18480.0
TICKSIZE_LAST: 1712647028182 2
TICKSIZE_LAST: 1712647028182 2
TICKSIZE__BID: 1712647028182 13
TICKSIZE__ASK: 1712647028183 7
TICKSIZE__BID: 1712647028830 9
TICKSIZE__ASK: 1712647028831 13
TICKSIZE__BID: 1712647029581 10
TICKSIZE__ASK: 1712647029582 11
TICKSIZE__BID: 1712647030431 13
TICKSIZE__ASK: 1712647030431 8
TICKSIZE__BID: 1712647031139 10
TICKPRIC_LAST: 1712647031432 18481.0
TICKSIZE_LAST: 1712647031432 5
TICKSIZE_LAST: 1712647031432 5
TICKSIZE__ASK: 1712647031432 7
TICKSIZE__ASK: 1712647032085 9
TICKPRIC__ASK: 1712647032335 18480.0