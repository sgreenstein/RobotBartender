class Ingredient:
    """A liquid ingredient of a mixed drink"""
    #constructor
    def __init__(self, name, flavs = {}):
        """Returns a new Ingredient instance.

        Keyword arguments:
        flavs -- dictionary of string keys, the flavors, and number values:
            name -- string, name of ingredient
            sweet -- scale of 0 to 1 (default 0)
            alcoholic -- proof, 0 to 200 (default 0)
            bitter -- scale of 0 to 1 (default 0)
            sour -- scale of 0 to 1 (default 0)
            flavor_strength -- how flavorful in general, scale of 0 to 1 (default 0)
            carbonated -- scale of 0 to 1 (default 0)
            creamy -- scale of 0 to 1 (default 0)
        """
        self.name = name
		flavs = noun_to_adj(flavs)
		assert flavs.issubset(['name', 'sweet', 'alcoholic', 'bitter', 'sour',
			'flavor_strength', 'carbonated', 'creamy'])
        self.flavors = flavs
        
    @staticmethod
    def flavorlist():
        """ returns a list of all the flavors an ingredient can have
        """
        return ['name', 'sweet', 'alcoholic', 'bitter', 'sour',
            'flavor_strength', 'carbonated', 'creamy']

	@staticmethod
	def noun_to_adj(flavors):
		"""converts the noun form of anything in the list (e.g. sweetness)
		to the adjective form (e.g. sweet)
		"""
		equivalencies = {'sweetness':'sweet', 'alcohol':'alcoholic', 'bitterness':'bitter',
			'sourness':'sour', 'carbonation':'carbonated', 'creaminess':'creamy'}
		for index, flavor in enumerate(flavors):
			if flavor in equivalencies:
				flavors[index] = equivalencies[flavor]
		return flavors
		
    #methods
    def add(self, amnt):
        """Returns a string detailing the adding of an ingredient

        Keyword arguments:
        amnt -- amount to add, in mL
        """
        print "Adding", amnt, "mL of", self.name

    #different getters
    def flavorvalue(self, flavor):
        """Returns the value of the flavor, 0 if no value

        Keyword arguments:
        flavor -- string, flavor name
        """
		flavor = noun_to_adj(flavor)
        if(self.flavors.has_key(flavor)):
            return self.flavors[flavor]
        return 0

    def alcohol(self):
        return self.getFlavor("alcoholic")

    def sweetness(self):
        return self.getFlavor("sweet")

    def bitterness(self):
        return self.getFlavor("bitter")

    def sourness(self):
        return self.getFlavor("sour")

    def flavor_strength(self):
        return self.getFlavor("flavor_strength")

    def carbonation(self):
        return self.getFlavor("carbonated")

    def creaminess(self):
        return self.getFlavor("creamy")
