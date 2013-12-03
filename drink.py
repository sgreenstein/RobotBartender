import tts

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
        self.isnovel = isnovel
        self.approval = 0 #changes in wasgood and wasbad methods
        #find total number of parts in drink
        self._total_parts = 0
        for ingred_amount in self.ingredients.itervalues():
            self._total_parts += ingred_amount
        self._total_parts = float(self._total_parts)
        self._default_size = 100

    #methods
    def make(self, flavor, size = -1):
        """Print the actions of making a drink

        Keyword arguments:
        flavor -- the flavor this drink should have more of
        size -- int, size of drink in mL (default 100)
        """
        #set size
        if (size == -1):
            size = self._default_size
        #alter ingredients temporarily if necessary
        if(not flavor):
            ingredients = self.ingredients
        else:
            ingredients = self._altered_ingredients(flavor, 0.1)
        if(not ingredients):
            return
        #add each ingredient
        print "Flavor:", flavor, "Ingredients:", ingredients
        for ingredient, ingred_amount in ingredients.iteritems():
            ingredient.add(int((size * ingred_amount) / self._total_parts))
        print "Your", self.name, "is ready."

    def _altered_ingredients(self, flavor, amount):
        """Returns a dictionary of the ingredients and their parts
        that will increase or decrease a flavor

        Keyword arguments:
        flavor -- string, the name of the flavor to alter
        amount -- how much to alter it. Range -1 (less) to 1 (more)
        """
        ingredients = self.ingredients
        #find the current level of that flavor
        level = 0
        for ingredient, num_parts in ingredients.iteritems():
            level += ingredient.flavorvalue(flavor) * num_parts
        level /= self._total_parts
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
            print "Amount:",amount
            print "Level:",level
            ingredients[ingredient] += amount * ((ingredient.flavorvalue(flavor) - level) / level)
            #print what we did
            if (ingredient.flavorvalue(flavor) - level) * amount > 0:
                changing = "Increasing"
            else:
                changing = "Decreasing"
            print changing, "the amount of", ingredient.name
        return ingredients

    def _cannot_alter(self, flavor):
        if(self.name[0].lower() in ['a', 'e', 'i', 'o', 'u']):
            article = 'an'
        else:
            article = 'a'
        tts.speak("There are no " + flavor + " ingredients in " + article + ' ' + self.name)

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
        if hasfailed:
            pass #TODO: delete from file

    def wasgood(self):
        self.approval += 1