from drink import Drink
import create_presets
from ingredient import Ingredient
from random import choice
from collections import Counter, defaultdict
from array import *
import heapq

class NovelDrink:
	"""I do not know why we do this
	"""

        def __init__(self):
            drinks = create_presets.getdrinks()
            adj = defaultdict(Counter)


            for drink in drinks.itervalues():
                for ing1, parts1 in drink.ingredients.iteritems():
                    for ing2, parts2 in drink.ingredients.iteritems():
                        if ing1.name!=ing2.name:
                            adj[ing1.name][ing2.name]+=parts1+parts2
                            adj[ing2.name][ing1.name]+=parts1+parts2
            self._adj=adj
            self._drinks = drinks
##            for ing1, ing2 in adj.iteritems():
##                for ing2name, val in ing2.iteritems():
##                    print ing1, ing2name, val

    #methods
        def makenovel(self):
            drinks = self._drinks
            drink1 = drinks[choice(drinks.keys())]
            print "Drink 1:", drink1.name
            bestsim = 0
            for drink2 in drinks.itervalues():
                similarity = 0
                for ingredient1 in drink1.ingredient_names:
                    for ingredient2 in drink2.ingredient_names:
                        similarity += self._adj[ingredient1][ingredient2]
                similarity /= drink2.total_parts
                if(similarity > bestsim):
                    bestsim = similarity
                    bestdrink = drink2
##                print drink2.name, similarity
            drink2 = bestdrink
            diff = {}
            levels1 = drink1.levels
            levels2 = drink2.levels
            for flav in Ingredient.flavorlist():
                if not flav in levels1:
                    try:
                        diff[flav] = levels2[flav]
                    except:
                        pass
                else:
                    try:
                        diff[flav] = abs(levels1[flav] - levels2[flav])
                    except:
                        diff[flav] = levels1[flav]

            flavs = []
            for i in range(3):
                flavs.append(heapq.nlargest(i, diff, key = lambda k: diff[k]))

            print drink1.name
            print drink2.name



        def nth_largest(self, n, iter):
            return heapq.nlargest(n, iter)[-1]
