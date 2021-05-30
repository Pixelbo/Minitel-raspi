from whiptail import Whiptail
import threading

x = Whiptail("Le Minitel des Hilkens", backtitle="B.Hilkens 2021", height=24, width= 80)

def run():
  x.p.
  x.confirm("hello")
  
  
t1 = threading.Thread(target = run)

x.confirm("hello")
t1.start()
