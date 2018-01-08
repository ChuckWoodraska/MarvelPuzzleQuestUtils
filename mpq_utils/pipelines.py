from sqlalchemy.orm import sessionmaker
from mpq_utils.models import BaseCharacters, CharacterStats, RosterCharacters, db_connect


class BaseCharacterPipeline():
    """pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        """

        This method is called for every item pipeline component.

        """
        print(item['name'], item['secondary_name'], len(item['character_stats']))
        # session = self.Session()
        # bc = BaseCharacters()
        # bc.name = item['name']
        # bc.secondary_name = item['secondary_name']
        # bc.power1_color = item['power1_color']
        # bc.power2_color = item['power2_color']
        # bc.power3_color = item.get('power3_color', 'Hidden')
        # try:
        #     session.add(bc)
        #     session.commit()
        #     session.flush()
        #     for cs in item['character_stats']:
        #         cs = [x.strip(' \n') for x in cs]
        #         if len(cs) == 10:
        #             cs_new = CharacterStats()
        #             cs_new.character_id = bc.id
        #             cs_new.level = cs[0]
        #             cs_new.character_level_id = '{}_{}'.format(cs_new.character_id, cs_new.level)
        #             cs_new.health = cs[1]
        #             cs_new.black = cs[7]
        #             cs_new.blue = cs[4]
        #             cs_new.green = cs[6]
        #             cs_new.purple = cs[5]
        #             cs_new.red = cs[3]
        #             cs_new.yellow = cs[2]
        #             cs_new.critical = cs[8][:-1]
        #             cs_new.teamup = cs[9]
        #             session.add(cs_new)
        #             session.commit()
        #             session.flush()
        # except:
        #     session.rollback()
        #     print(bc.id)
        #     print(cs)
        #     raise
        # finally:
        #     session.close()


class RosterCharacterPipeline():
    """pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        """

        This method is called for every item pipeline component.

        """
        session = self.Session()
        rc = RosterCharacters()
        rc.level = item['level']
        # Some small discrepencies between the two data sources that have to be ironed out.
        if item['name'] == 'The Hulk' and item['secondary_name'] == 'Indestructible':
            q = session.query(BaseCharacters).filter(BaseCharacters.name == 'The Hulk', BaseCharacters.secondary_name == 'Indestructable').first()
        elif item['name'] == 'Luke Cage' and item['secondary_name'] == 'Hero For Hire':
            q = session.query(BaseCharacters).filter(BaseCharacters.name == 'Luke Cage',
                                                     BaseCharacters.secondary_name == 'Hero for Hire').first()
        elif item['name'] == 'Mockingbird' and item['secondary_name'] == 'Bobbi Moorse':
            q = session.query(BaseCharacters).filter(BaseCharacters.name == 'Mockingbird',
                                                     BaseCharacters.secondary_name == 'Bobbi Morse').first()
        elif item['name'] == 'Sandman' and item['secondary_name'] == 'Flint Marco':
            q = session.query(BaseCharacters).filter(BaseCharacters.name == 'Sandman',
                                                     BaseCharacters.secondary_name == 'Flint Marko').first()
        else:
            q = session.query(BaseCharacters).filter(BaseCharacters.name == item['name'], BaseCharacters.secondary_name == item['secondary_name']).first()
        if not q:
            print(repr(item['name']), repr(item['secondary_name']))
        else:
            rc.character_id = q.id
            rc.character_level_id = '{}_{}'.format(rc.character_id, rc.level)
            rc.power1_level = item['power1_level']
            rc.power2_level = item['power2_level']
            rc.power3_level = item['power3_level']
            rc.user_id = 1
            q.stars = item['stars']
            try:
                session.add(rc)
                session.commit()
                session.flush()
            except:
                session.rollback()
                raise
            finally:
                session.close()
