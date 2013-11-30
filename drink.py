class Drink:
    """A mixed drink with a list of ingredients and amounts"""
    def __init__(self, name, ings):
        """Return a new instance of Drink.

        Keyword arguments:
        name -- string, the name of the drink
        ings -- dictionary of Ingredients (keys) and no. of parts (value)
        """
        #set attributes
        self.name = name
        self.ingredients = ings
        #find total number of parts in drink
        self.total_parts = 0
        for ingredient in self.ingredients:
            self.total_parts += self.ingredients[ingredient]
        self.total_parts = float(self.total_parts)

    def make(self, size = 100):
        """Print the actions of making a drink

        Keyword arguments:
        size -- int, size of drink in mL (default 100)
        """
        #add each ingredient
        for ingredient in self.ingredients:
            ingredient.add(int((size * self.ingredients[ingredient]) / self.total_parts))
        print "Your", self.name, "is ready."

    def alter_recipe(self, flavor, amount):
        """Alter the ingredient ratios to increase or decrease a flavor

        Keyword arguments:
        flavor -- string, the name of the flavor to alter
        amount -- how much to alter it. Range -1 (less) to 1 (more)
        """
        #print what we're doing
        if amount > 0:
            changing = "Increasing"
        else:
            changing = "Decreasing"
        print changing, "the", flavor, "of the", self.name
        #find the current flavor level
        level = 0
        for ingredient in self.ingredients:
            level += ingredient.get_flavor(flavor) * self.ingredients[ingredient]
        level /= self.total_parts
        for ingredient in self.ingredients:
            #increase ingredients that are above the average strength, decrease others
            #all in proportion to how far they are from the average
            self.ingredients[ingredient] += amount * ((ingredient.get_flavor(flavor) - level) / level)
            #print what we did
            if (ingredient.get_flavor(flavor) - level) * amount > 0:
                changing = "Increasing"
            else:
                changing = "Decreasing"
            print changing, "the amount of", ingredient.name
