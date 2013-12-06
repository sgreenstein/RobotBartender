from drink import Drink
import create_presets
from ingredient import Ingredient
import random
from collections import Counter, defaultdict
from array import *
import heapq

class NovelDrink:
	"""I do not know why we do this
	"""
	
	def __init__(self):
		drinks = create_presets.getdrinks()
		adj = defaultdict(Counter())
		
		
		for drink in drinks:
			for ing1 in drink.ingredient_names():
				for ing2 in drink.ingredients_names():
					if ing1!=ing2:
						adj[ing1][ing2]+=1
						adj[ing2][ing1]+=1
		self._adj=adj
		self._drinks = drinks
		
	#methods
	def makenovel(self):
		drink1 = random.choose(self._drinks)
		for drink2 in drinks:
			similarity = 0
			for ingredient1 in drink1.ingredient_names():
				for ingredient2 in drink2.ingredient_names():
					similarity += adj[ingredient1][ingredient2]
			if(similarity > bestsim):
				bestsim = similarity
				bestdrink = drink2
				
		diff = []
		levels1 = drink1.getflavors()
		levels2 = drink2.getflavors()
		for i in levels1:
			diff[i] = levels1[i] - levels2[i]
		flav1 = nth_largest(1,diff)
		flav2 = nth_largest(2,diff)
		flav3 = nth_largest(3,diff)
		
	
	def nth_largest(n, iter):
		return heapq.nlargest(n, iter)[-1]
