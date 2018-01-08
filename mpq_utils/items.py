from scrapy.item import Item, Field


class MPQCharacter(Item):
    name = Field()
    secondary_name = Field()
    stars = Field()
    power1_color = Field()
    power1_cost = Field()
    power2_color = Field()
    power2_cost = Field()
    power3_color = Field()
    power3_cost = Field()
    character_stats = Field()

    def __str__(self):
        return ""


class MPQRosterCharacter(Item):
    name = Field()
    secondary_name = Field()
    level = Field()
    stars = Field()
    power1_level = Field()
    power2_level = Field()
    power3_level = Field()
