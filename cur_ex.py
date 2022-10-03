from dataclasses import dataclass
from functools import total_ordering
from queue import PriorityQueue
from typing import Union

@dataclass
@total_ordering
class ExchangeRate:
  curTo: str
  rate: float
  visited: bool = False

  def _is_valid_operand(self, other):
    return hasattr(other, "rate")
  def __eq__(self, other):
    if not self._is_valid_operand: return NotImplemented
    return self.rate == other.rate
  def __lt__(self, other):
    if not self._is_valid_operand: return NotImplemented
    return self.rate < other.rate

class Exchanger:
  rates = {}

  def setRate(self, curFrom: str, curTo: str, rate: float) -> None:
    if not self.rates.get(curFrom): self.rates[curFrom] = []
    self.rates[curFrom].append(ExchangeRate(curTo, rate))
    if not self.rates.get(curTo): self.rates[curTo] = []
    self.rates[curTo].append(ExchangeRate(curFrom, round(1/rate, 2)))

  def findConvertionRate(self, curFrom: str, curTo: str) -> Union[float, None]:

    ##TODO: Fix this Workaround to be able to findConvertion again for the second time
    ## Potential fix is to use additional type or something
    for values in self.rates.values():
      for j in values:
        j.visited = False
    ##

    ratesToProcess = PriorityQueue()
    possibleConvertions = {}

    for i in self.rates.get(curFrom):
      ratesToProcess.put(i)
      i.visited = True
    while not ratesToProcess.empty():
      currentRate = ratesToProcess.get()
      ##DEBUG: print(possibleConvertions)
      possibleConvertions[currentRate.curTo] = currentRate.rate
      if self.rates.get(currentRate.curTo):
        for i in self.rates.get(currentRate.curTo):
          if not i.visited:
            i.visited = True
            # If it is possible to convert to another currency, let's multiply
            # how many money we get converting from initial currency
            # by convertion rate from current currency to next one
            ratesToProcess.put(ExchangeRate(i.curTo,
                               round(i.rate * currentRate.rate, 2)))

    ##DEBUG: print(possibleConvertions)
    if possibleConvertions.get(curTo):
      return possibleConvertions[curTo]
    return None


def main():
  exchanger = Exchanger()
  exchanger.setRate('eur', 'usd', 0.98)
  exchanger.setRate('chf', 'usd', 1.01)
  exchanger.setRate('usd', 'uah', 36.74)
  exchanger.setRate('chf', 'gbp', 0.89)
  ##DEBUG: print(exchanger.rates)
  print(f"chf to uah: {exchanger.findConvertionRate('chf', 'uah')}")
  print(f"chf to eur: {exchanger.findConvertionRate('chf', 'eur')}")
  print(f"gbp to uah: {exchanger.findConvertionRate('gbp', 'uah')}")
  print(f"gbp to czk: {exchanger.findConvertionRate('gbp', 'czk')}")


if __name__ == "__main__":
  main()
