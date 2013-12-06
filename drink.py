import tts
from ingredient import Ingredient

class Drink:
    """A mixed drink with a list of ingredients and amounts"""
    #constructor
    def __init__(self, name, ings, isnovel = False):
        """Return a new instance of Drink.

        Keyword arguments:
        name -- string, the name of the drink
        ings -- dictionary of Ingredients (keys) and no. of parts (value)
        isnovel -- true for conceptually-blended drinks, false for presets
        """
        #set attributes
        self.name = name
        self.ingredients = ings
        self.ingredient_names = ings.keys()
        self.isnovel = isnovel
        self.approval = 0 #changes in wasgood and wasbad methods
        #find total number of parts in drink
        self._total_parts = 0
        for ingred_amount in self.ingredients.itervalues():
            self._total_parts += ingred_amount
        self._total_parts = float(self._total_parts)
        #set size
        self._default_size = 100
        #calculate initial flavor levels
        self._levels = {} #dictionary of each flavor and its level
        self._calcflavorlevels()

    #methods
    def make(self, flavor = '', size = -1):
        """Print the actions of making a drink

        Keyword arguments:
        flavor -- the flavor this drink should have more of (default none)
        size -- int, size of drink in mL (default 100)
        """
        #set size
        if(size == -1):
            size = self._default_size
        #alter ingredients temporarily if necessary
        if(not flavor):
            ingredients = self.ingredients
        else:
            ingredients = self._altered_ingredients(flavor, 0.1)
        if(not ingredients):
            return
        #add each ingredient
        for ingredient, ingred_amount in ingredients.iteritems():
            ingredient.add(int((size * ingred_amount) / self._total_parts))
        print "Your", self.name, "is ready."

    def _calcflavorlevels(self):
        """Calculates the drink's value for each flavor
        """
        ingredients = self.ingredients
        #find the current level of each flavor
        for flavor in Ingredient.flavorlist():
            level = 0
            for ingredient, num_parts in ingredients.iteritems():
                level += ingredient.flavorvalue(flavor) * num_parts
            level /= self._total_parts
            self._levels[flavor] = level

    def _altered_ingredients(self, flavor, amount):
        """Returns a dictionary of the ingredients and their parts
        that will increase or decrease a flavor

        Keyword arguments:
        flavor -- string, the name of the flavor to alter
        amount -- how much to alter it. Range -1 (less) to 1 (more)
        """
        ingredients = self.ingredients.copy()
        level = self._levels[flavor]
        if(level == 0):
            self._cannot_alter(flavor)
            return False
        #print what we're doing
        if amount > 0:
            changing = "more"
        else:
            changing = "less"
        print "Making the", self.name, changing, flavor
        for ingredient in ingredients:
            #increase ingredients that are above the average strength, decrease others
            #all in proportion to how far they are from the average
            ingredients[ingredient] += amount * ((ingredient.flavorvalue(flavor) - level) / level)
            #print what we did
            if (ingredient.flavorvalue(flavor) - level) * amount > 0:
                changing = "Increasing"
            else:
                changing = "Decreasing"
            print changing, "the amount of", ingredient.name
        self._calcflavorlevels()
        return ingredients

    def _cannot_alter(self, flavor):
        if(self.name[0].lower() in ['a', 'e', 'i', 'o', 'u']):
            article = 'an'
        else:
            article = 'a'
        tts.speak("There are no " + flavor + " ingredients in " + article + ' ' + self.name)

    def level_of(self, flavor):
        """Returns the level of the specified flavor in this drink

        Keyword arguments:
        flavor -- string, the name of the flavor whose level to get
        """
        return self._levels[flavor]

    def alter_recipe(self, flavor, amount):
        """Alter the ingredient ratios to increase or decrease a flavor.
        Returns true if successful

        Keyword arguments:
        flavor -- string, the name of the flavor to alter
        amount -- how much to alter it. Range -1 (less) to 1 (more)
        """
        newingreds = self._altered_ingredients(flavor, amount)
        if(not newingreds):
            return False
        self.ingredients = newingreds
        return True

    def alter_size(self, amount):
        """Alter the default drink size

        Keyword arguments:
        amount -- fraction of previous size to make the new size
        """
        self._default_size *= amount

    def hasfailed(self):
        return (self.approval < 0 and self.isnovel)

    def wasbad(self):
        self.approval -= 1
        if self.hasfailed:
            pass #TODO: delete from file

    def wasgood(self):
        self.approval += 1