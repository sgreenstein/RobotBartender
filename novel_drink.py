from drink import Drink
import create_presets
from ingredient import Ingredient
from random import choice,randint
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

    #methods
        def makenovel(self):
            drinks = self._drinks
            drink1 = drinks[choice(drinks.keys())]
            bestsim = 0
            similarity_list = {}
            for drink2 in drinks.itervalues():
                similarity = 0
                for ingredient1 in drink1.ingredient_names:
                    for ingredient2 in drink2.ingredient_names:
                        similarity += self._adj[ingredient1][ingredient2]
                similarity /= drink2.total_parts
                similarity_list[drink2.name]=similarity
                if(similarity > bestsim):
                    bestsim = similarity
                    bestdrink = drink2
##                print drink2.name, similarity
            drink2_list = heapq.nlargest(5,similarity_list,key = lambda k: similarity_list[k])
            drink2 = drinks[choice(drink2_list)]
            while drink1.name == drink2.name:
                drink2 = drinks[choice(drink2_list)]
   ##         drink2 = bestdrink
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
            for i in range(4):
                flavs.append(heapq.nlargest(i, diff, key = lambda k: diff[k]))

            new_drink_ings = {}
            new_drink2_ings = {}
            for ingredien1,part1 in drink1.ingredients.iteritems():
                new_drink_ings[ingredien1]=part1
            for ingredient2,part2 in drink2.ingredients.iteritems():
                for ingr,part in new_drink_ings.iteritems():
                    if ingredient2==ingr:
                        new_drink_ings[ingr]=(part+part2)/2
                    else:
                        new_drink2_ings[ingredient2]=part2
            for ingr,part in new_drink2_ings.iteritems():
                new_drink_ings[ingr]=part
            for ingr,part in new_drink_ings.iteritems():
                print ingr.name , part
            new_drink_ings_final = {}
            alcohol = 0
            if len(new_drink_ings) > 6:
                while len(new_drink_ings_final) < 5:
                    ingr = choice(new_drink_ings.keys())
                    if ingr.alcohol()>0:
                        alcohol+=1
                        if alcohol <4:
                            part = new_drink_ings[ingr]
                            new_drink_ings_final[ingr] = part
                    else:
                        part = new_drink_ings[ingr]
                        new_drink_ings_final[ingr] = part
                new_drink = Drink("custom_drink",new_drink_ings_final)
                while alcohol==0:
                    ingr = choice(new_drink_ings.keys())
                    part = new_drink_ings[ingr]
                    if ingr.alcohol()>0:
                        new_drink_ings_final[ingr] = part
                        alcohol += 1
            else:
                new_drink = Drink("custom_drink",new_drink_ings)
            print "New drink is: ", new_drink.name
            for ingr, part in new_drink.ingredients.iteritems():
                print ingr.name, part
            return new_drink
