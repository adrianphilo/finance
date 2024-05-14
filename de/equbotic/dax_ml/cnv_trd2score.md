erstellen time/score table
----------------------------------
die Idee ist mehrere Trade-Einträge zu bündeln und ein score für das bündel zu vergeben.
in den score gehen ein: pricechange, size, time und direction.

beispiel:
pro 5 trades:
highscore = max_prcdiff * timefactor * sizefactor
lowscore  = min_prcdiff * timefactor * sizefactor
score = if     (4 mal down) lowscore
        elseif (4 mal up)   hisghscore
        else   (highscore + lowscore) / 2

timefactor = 60sec / timediff_sec
sizefactor = size /10

erstellen einer datei mit : time, score, avg_prc

erstellen attribute table
-------------------------------
idee ist die letzten n-päckchen in einer zeile zu schreiben und dazu den price in 50päckchen, 100 päckchen

time, scores[10], prcfutur1, prcfutur2

ml trainings mit attribute table
--------------------------------
untersuchen der score-tabelle
und probieren von ml methoden





