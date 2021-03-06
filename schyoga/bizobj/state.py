
class State():

    nameForURL = 'new-york'

    @classmethod
    def createFromUrlName(self, stateUrlName='new-york'):
        cls = self()

        stateName = cls.__convertNameFromURLToHuman(stateUrlName)

        if (stateName not in cls.__allStates.values()):
            return None

        cls.nameForURL = stateUrlName
        return cls

    @property
    def name(self):
        return self.__convertNameFromURLToHuman(self.nameForURL)


    def __convertNameFromURLToHuman(self, stateUrlName):
        return stateUrlName.strip().replace("-"," ").title()


    __allStates = dict({'AL': "Alabama",
              'AK': "Alaska",
              'AZ': "Arizona",
              "AR": "Arkansas",
              "CA": "California",
              "CO": "Colorado",
              "CT": "Connecticut",
              "DE": "Delaware",
              "FL": "Florida",
              "GA": "Georgia",
              "HI": "Hawaii",
              "ID": "Idaho",
              "IL": "Illinois",
              "IN": "Indiana",
              "IA": "Iowa",
              "KS": "Kansas",
              "KY": "Kentucky",
              "LA": "Louisiana",
              "ME": "Maine",
              "MD": "Maryland",
              "MA": "Massachusetts",
              "MI": "Michigan",
              "MN": "Minnesota",
              "MS": "Mississippi",
              "MO": "Missouri",
              "MT": "Montana",
              "NE": "Nebraska",
              "NV": "Nevada",
              "NH": "New Hampshire",
              "NJ": "New Jersey",
              "NM": "New Mexico",
              "NY": "New York",
              "NC": "North Carolina",
              "ND": "North Dakota",
              "OH": "Ohio",
              "OK": "Oklahoma",
              "OR": "Oregon",
              "PA": "Pennsylvania",
              "RI": "Rhode Island",
              "SC": "South Carolina",
              "SD": "South Dakota",
              "TN": "Tennessee",
              "TX": "Texas",
              "UT": "Utah",
              "VT": "Vermont",
              "VA": "Virginia",
              "WA": "Washington",
              "WV": "West Virginia",
              "WI": "Wisconsin",
              "WY": "Wyoming",
              "DC": "District of Columbia",
              "AS": "American Samoa",
              "GU": "Guam",
              "MP": "Northern Mariana Islands",
              "PR": "Puerto Rico",
              "VI": "Virgin Islands",
    })