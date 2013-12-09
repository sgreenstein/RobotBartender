#-------------------------------------------------------------------------------
# Name:        novel_drink
# Purpose:     Produces a new drink using conceptual blending
#
# Author:      MKhan
#
# Created:     30/11/2013
# Copyright:   (c) MKhan 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from drink import Drink
import create_presets
from ingredient import Ingredient
from random import choice,randint
from collections import Counter, defaultdict
from array import *
import heapq

class NovelDrink:
	"""Takes a list of drinks as an input, produces an adjacency matrix of
        ingredients that shows how compatible two ingredients are, picks a
        random drink A from the list of drinks, picks the drink B with the most
        compatible ingredients from the list of drinks (drink A != drink B),
        blends the two together and outputs a novel drink
	"""

        def __init__(self):
            drinks = create_presets.getdrinks()
            adj = defaultdict(Counter)

            # produces an adjacency matrix of ingredients
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
            drink1 = drinks[choice(drinks.keys())] #chooses a drink at random
            bestsim = 0
            similarity_list = {}
            """ Iterates through the list of drinks and computes a similarity value
                of the two drinks based on the ingredients present in both drinks.
                The second drink is chosen from the top 5 most similar drinks.
            """
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
            """ For each flavor computes the difference between the two drinks and
                chooses the top 3 flavors with the most disparity in them
            """
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

            """ Copies all of drink A's and drink B's ingredients into the list
                of ingredients for the novel drink unless they are exactly the
                same in which case it takes the average. If the number of ingredients
                exceeds a certain number, the list is pruned to delete "similar
                flavored" ingredients.
            """
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
                #new_drink_ings contains all the ingredients we need for our blend
            for ingr,part in new_drink_ings.iteritems():
                print ingr.name , part
            new_drink_ings_final = {}
            alcohol = 0
            if len(new_drink_ings) > 6:
                while len(new_drink_ings_final) < 5: #prunes the list of ingredients
                    ingr = choice(new_drink_ings.keys())
                    if ingr.alcohol()>0:
                        alcohol+=1
                        if alcohol <4:
                            part = new_drink_ings[ingr]
                            new_drink_ings_final[ingr] = part
                    else:
                        part = new_drink_ings[ingr]
                        new_drink_ings_final[ingr] = part
                new_drink_name = "Drink " + str(randint(1,999));
                new_drink = Drink(new_drink_name,new_drink_ings_final)
                while alcohol==0: #makes sure that there is atleast one alcoholic ingredient present in the blend
                    ingr = choice(new_drink_ings.keys())
                    part = new_drink_ings[ingr]
                    if ingr.alcohol()>0:
                        new_drink_ings_final[ingr] = part
                        alcohol += 1
            else:
                new_drink_name = "Drink " + str(randint(1,999));
                new_drink = Drink(new_drink_name,new_drink_ings)
            print "New drink is: ", new_drink.name
            for ingr, part in new_drink.ingredients.iteritems():
                print ingr.name, part
            return new_drink
