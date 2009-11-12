import matplotlib
import pymc
from pymc.Matplot import plot


around_noon = pymc.DiscreteUniform("around_noon", 1100, 1300, value=1200)

before_ten = pymc.DiscreteUniform("before_ten", 800, 1000, value=900)

after_five = pymc.DiscreteUniform("after_five", 1700, 1900, value=1700)

preferences = pymc.Categorical("ranking", [0.6, 0.3, 0.1])

@pymc.deterministic
def time_pref(value=None, ranking=preferences, windows=[around_noon, before_ten, after_five]):
   return windows[ranking]


M = pymc.MCMC([around_noon, before_ten, after_five, preferences, time_pref])

M.sample(iter=10000, burn=1000, thin=10)

#plot(M)

M.stats()

