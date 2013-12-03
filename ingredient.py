class Ingredient:
    """A liquid ingredient of a mixed drink"""
    #constructor
    def __init__(self, name, flavs = {}):
        """Returns a new Ingredient instance.

        Keyword arguments:
        flavs -- dictionary of string keys, the flavors, and number values:
            name -- string, name of ingredient
            sweetness -- scale of 0 to 1 (default 0)
            alcohol -- proof, 0 to 200 (default 0)
            bitterness -- scale of 0 to 1 (default 0)
            sourness -- scale of 0 to 1 (default 0)
            flavor_strength -- how flavorful in general, scale of 0 to 1 (default 0)
            carbonation -- scale of 0 to 1 (default 0)
            creaminess -- scale of 0 to 1 (default 0)
        """
        self.name = name
        self.flavors = flavs
        
    @staticmethod
    def flavorlist():
        """ returns a list of all the flavors an ingredient can have
        """
        return ['name', 'sweetness', 'alcohol', 'bitterness', 'sourness',
            'flavor_strength', 'carbonation', 'creaminess']

    #methods
    def add(self, amnt):
        """Returns a string detailing the adding of an ingredient

        Keyword arguments:
        amnt -- amount to add, in mL
        """
        print "Adding", amnt, "mL of", self.name

    #different getters
    def get_flavor(self, flavor):
        """Returns the value of the flavor, 0 if no value

        Keyword arguments:
        flavor -- string, flavor name
        """
        if(self.flavors.has_key(flavor)):
            return self.flavors[flavor]
        return 0

    def alcohol(self):
        return self.getFlavor("alcohol")

    def sweetness(self):
        return self.getFlavor("sweetness")

    def bitterness(self):
        return self.getFlavor("bitterness")

    def sourness(self):
        return self.getFlavor("sourness")

    def flavor_strength(self):
        return self.getFlavor("flavor_strength")

    def carbonation(self):
        return self.getFlavor("carbonation")

    def creaminess(self):
        return self.getFlavor("creaminess")
