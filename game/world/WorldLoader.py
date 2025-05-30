from database.world.WorldModels import SpellChain
from database.dbc.DbcModels import Spell
from database.dbc.DbcDatabaseManager import DbcDatabaseManager
from database.realm.RealmDatabaseManager import RealmDatabaseManager
from database.world.WorldDatabaseManager import WorldDatabaseManager
from game.world.managers.maps.MapManager import MapManager
from game.world.managers.objects.units.player.GroupManager import GroupManager
from game.world.managers.objects.units.player.guild.GuildManager import GuildManager
from utils.ConfigManager import config
from utils.Logger import Logger


class WorldLoader:

    @staticmethod
    def load_data():
        # Below order matters.
        WorldLoader.load_creature_templates()
        WorldLoader.load_gameobject_templates()

        # Loot related, even if not loading creatures or gameobjects, loot might be referenced.
        WorldLoader.load_gameobject_loot_templates()
        WorldLoader.load_fishing_loot_templates()
        WorldLoader.load_creature_loot_templates()
        WorldLoader.load_skinning_loot_templates()
        WorldLoader.load_item_templates()
        WorldLoader.load_reference_loot_templates()
        WorldLoader.load_pickpocketing_loot_templates()
        WorldLoader.load_item_loot_templates()

        # Spells.
        WorldLoader.load_spells()
        WorldLoader.load_creature_spells()

        #  Scripts.
        WorldLoader.load_generic_scripts()

        # Gameobject spawns
        if config.Server.Settings.load_gameobjects:
            WorldLoader.load_transport_animations()
            WorldLoader.load_gameobject_quest_starters()
            WorldLoader.load_gameobject_quest_finishers()
            WorldLoader.load_gameobject_scripts()
        else:
            Logger.info('Skipped game object loading.')

        # Creature spawns
        if config.Server.Settings.load_creatures:
            WorldLoader.load_creature_movement_scripts()
            WorldLoader.load_creature_ai_events()
            WorldLoader.load_creature_ai_scripts()
            WorldLoader.load_creature_movement()
            WorldLoader.load_creature_movement_templates()
            WorldLoader.load_creature_movement_special()
            WorldLoader.load_creature_groups()
            WorldLoader.load_creature_equip_templates()
            WorldLoader.load_creature_on_kill_reputation()
            WorldLoader.load_creature_quest_starters()
            WorldLoader.load_creature_quest_finishers()
            WorldLoader.load_creature_display_info()
            WorldLoader.load_creature_model_info()
            WorldLoader.load_creature_families()
            WorldLoader.load_npc_gossip()
            WorldLoader.load_npc_text()
            WorldLoader.load_broadcast_text()
        else:
            Logger.info('Skipped creature loading.')

        WorldLoader.load_area_trigger_quest_relations()
        WorldLoader.load_quests()
        WorldLoader.load_spell_chains()
        WorldLoader.load_default_profession_spells()
        WorldLoader.load_trainer_spells()
        WorldLoader.load_skills()
        WorldLoader.load_skill_line_abilities()
        WorldLoader.load_char_base_infos()
        WorldLoader.load_taxi_nodes()
        WorldLoader.load_taxi_path_nodes()
        WorldLoader.load_factions()
        WorldLoader.load_faction_templates()
        WorldLoader.load_locks()
        WorldLoader.load_conditions()

        # Character related data
        WorldLoader.load_groups()
        WorldLoader.load_guilds()

        # Maps.
        MapManager.initialize_world_and_pvp_maps()
        MapManager.initialize_area_tables()

    # World data holders

    @staticmethod
    def load_gameobject_scripts():
        gameobject_scripts = WorldDatabaseManager.gameobject_scripts_get_all()
        length = len(gameobject_scripts)
        count = 0

        for gameobject_script in gameobject_scripts:
            WorldDatabaseManager.GameobjectScriptHolder.load_gameobject_script(gameobject_script)
            count += 1
            Logger.progress('Loading gameobject scripts...', count, length)

        return length

    @staticmethod
    def load_creature_ai_scripts():
        creature_ai_scripts = WorldDatabaseManager.creature_ai_scripts_get_all()
        length = len(creature_ai_scripts)
        count = 0

        for creature_ai_script in creature_ai_scripts:
            WorldDatabaseManager.CreatureAIScriptHolder.load_creature_ai_script(creature_ai_script)
            count += 1
            Logger.progress('Loading creature ai scripts...', count, length)

        return length

    @staticmethod
    def load_creature_movement_scripts():
        creature_movement_scripts = WorldDatabaseManager.creature_movement_scripts_get_all()
        length = len(creature_movement_scripts)
        count = 0

        for creature_movement_script in creature_movement_scripts:
            WorldDatabaseManager.CreatureMovementScriptHolder.load_creature_movement_script(creature_movement_script)
            count += 1
            Logger.progress('Loading creature movement scripts...', count, length)

        return length

    @staticmethod
    def load_creature_ai_events():
        creature_ai_avents = WorldDatabaseManager.creature_ai_event_get_all()
        length = len(creature_ai_avents)
        count = 0

        for creature_ai_event in creature_ai_avents:
            WorldDatabaseManager.CreatureAiEventHolder.load_creature_ai_event(creature_ai_event)
            count += 1
            Logger.progress('Loading creature ai events...', count, length)

        return length

    @staticmethod
    def load_generic_scripts():
        generic_scripts = WorldDatabaseManager.generic_scripts_get_all()
        length = len(generic_scripts)
        count = 0

        for generic_script in generic_scripts:
            WorldDatabaseManager.GenericScriptsHolder.load_generic_script(generic_script)
            count += 1
            Logger.progress('Loading generic scripts...', count, length)

        return length

    @staticmethod
    def load_conditions():
        conditions = WorldDatabaseManager.conditions_get_all()
        length = len(conditions)
        count = 0

        for condition in conditions:
            WorldDatabaseManager.ConditionHolder.load_condition(condition)
            count += 1
            Logger.progress('Loading conditions...', count, length)

        return length

    @staticmethod
    def load_gameobject_templates():
        gobject_templates = WorldDatabaseManager.gameobject_template_get_all()
        length = len(gobject_templates)
        count = 0

        for gobject_template in gobject_templates:
            WorldDatabaseManager.GameobjectTemplateHolder.load_gameobject_template(gobject_template)
            count += 1
            Logger.progress('Loading gameobject templates...', count, length)

        return length

    @staticmethod
    def load_transport_animations():
        transport_animations = DbcDatabaseManager.transport_animation_get_all()
        length = len(transport_animations)
        count = 0

        for transport_animation in transport_animations:
            DbcDatabaseManager.TransportAnimationHolder.load_transport_animation(transport_animation)
            count += 1
            Logger.progress('Loading transport animations...', count, length)

        return length

    @staticmethod
    def load_gameobject_quest_starters():
        gameobject_quest_starters = WorldDatabaseManager.gameobject_quest_starter_get_all()
        length = len(gameobject_quest_starters)
        count = 0

        for gameobject_quest_starter in gameobject_quest_starters:
            WorldDatabaseManager.QuestRelationHolder.load_gameobject_starter_quest(gameobject_quest_starter)
            count += 1
            Logger.progress('Loading gameobject quest starters...', count, length)

        return length

    @staticmethod
    def load_gameobject_quest_finishers():
        gameobject_quest_finishers = WorldDatabaseManager.gameobject_quest_finisher_get_all()
        length = len(gameobject_quest_finishers)
        count = 0

        for gameobject_quest_finisher in gameobject_quest_finishers:
            WorldDatabaseManager.QuestRelationHolder.load_gameobject_finisher_quest(gameobject_quest_finisher)
            count += 1
            Logger.progress('Loading gameobject quest finishers...', count, length)

        return length

    @staticmethod
    def load_creature_groups():
        creature_groups = WorldDatabaseManager.creature_groups_get_all()
        length = len(creature_groups)
        count = 0

        for group in creature_groups:
            WorldDatabaseManager.CreatureGroupsHolder.load_creature_groups(group)
            count += 1
            Logger.progress('Loading creature group...', count, length)

        return length

    @staticmethod
    def load_creature_movement():
        creature_movements = WorldDatabaseManager.creature_movement_get_all()
        length = len(creature_movements)
        count = 0

        for creature_movement in creature_movements:
            WorldDatabaseManager.CreatureMovementHolder.load_creature_movement(creature_movement)
            count += 1
            Logger.progress('Loading creature movement...', count, length)

        return length

    @staticmethod
    def load_creature_movement_templates():
        movements_templates = WorldDatabaseManager.creature_movement_template_get_all()
        length = len(movements_templates)
        count = 0

        for movement_template in movements_templates:
            WorldDatabaseManager.CreatureMovementHolder.load_creature_movement_template(movement_template)
            count += 1
            Logger.progress('Loading creature movement template...', count, length)

        return length

    @staticmethod
    def load_creature_movement_special():
        movements_special = WorldDatabaseManager.creature_movement_special_get_all()
        length = len(movements_special)
        count = 0

        for movement_special in movements_special:
            WorldDatabaseManager.CreatureMovementHolder.load_creature_movement_special(movement_special)
            count += 1
            Logger.progress('Loading creature movement special...', count, length)

        return length

    @staticmethod
    def load_creature_equip_templates():
        creature_equip_templates = WorldDatabaseManager.creature_equip_template_get_all()
        length = len(creature_equip_templates)
        count = 0

        for creature_equip_template in creature_equip_templates:
            WorldDatabaseManager.CreatureEquipmentHolder.load_creature_equip_template(creature_equip_template)
            count += 1
            Logger.progress('Loading creature equipment templates...', count, length)

        return length

    @staticmethod
    def load_creature_on_kill_reputation():
        creature_on_kill_reputations = WorldDatabaseManager.creature_on_kill_reputation_get_all()
        length = len(creature_on_kill_reputations)
        count = 0

        for creature_on_kill_reputation in creature_on_kill_reputations:
            WorldDatabaseManager.CreatureOnKillReputationHolder.load_creature_on_kill_reputation(
                creature_on_kill_reputation)
            count += 1
            Logger.progress('Loading creature on kill reputations...', count, length)

        return length

    @staticmethod
    def load_creature_spells():
        creature_spells = WorldDatabaseManager.creature_get_spell()
        length = len(creature_spells)
        count = 0

        for creature_spell in creature_spells:
            WorldDatabaseManager.CreatureSpellHolder.load_creature_spells(creature_spell)
            count += 1
            Logger.progress('Loading creature spells...', count, length)

        return length

    @staticmethod
    def load_creature_loot_templates():
        creature_loot_templates = WorldDatabaseManager.creature_get_loot_templates()
        length = len(creature_loot_templates)
        count = 0

        for loot_template in creature_loot_templates:
            WorldDatabaseManager.CreatureLootTemplateHolder.load_creature_loot_template(loot_template)
            count += 1
            Logger.progress('Loading creature loot templates...', count, length)

        return length

    @staticmethod
    def load_skinning_loot_templates():
        skinning_loot_templates = WorldDatabaseManager.skinning_get_loot_templates()
        length = len(skinning_loot_templates)
        count = 0

        for loot_template in skinning_loot_templates:
            WorldDatabaseManager.SkinningLootTemplateHolder.load_skinning_loot_template(loot_template)
            count += 1
            Logger.progress('Loading skinning loot templates...', count, length)

        return length

    @staticmethod
    def load_fishing_loot_templates():
        fishing_loot_templates = WorldDatabaseManager.fishing_get_loot_templates()
        length = len(fishing_loot_templates)
        count = 0

        for loot_template in fishing_loot_templates:
            WorldDatabaseManager.FishingLootTemplateHolder.load_fishing_loot_template(loot_template)
            count += 1
            Logger.progress('Loading fishing loot templates...', count, length)

        return length

    @staticmethod
    def load_creature_templates():
        creature_templates = WorldDatabaseManager.creature_template_get_all()
        length = len(creature_templates)
        count = 0

        for creature_template in creature_templates:
            WorldDatabaseManager.CreatureTemplateHolder.load_creature_template(creature_template)
            count += 1
            Logger.progress('Loading creature templates...', count, length)

        return length

    @staticmethod
    def load_gameobject_loot_templates():
        gameobject_loot_templates = WorldDatabaseManager.gameobject_get_loot_templates()
        length = len(gameobject_loot_templates)
        count = 0

        for loot_template in gameobject_loot_templates:
            WorldDatabaseManager.GameObjectLootTemplateHolder.load_gameobject_loot_template(loot_template)
            count += 1
            Logger.progress('Loading gameobject loot templates...', count, length)

        return length

    @staticmethod
    def load_item_templates():
        item_templates = WorldDatabaseManager.item_template_get_all()
        length = len(item_templates)
        count = 0

        for item_template in item_templates:
            WorldDatabaseManager.ItemTemplateHolder.load_item_template(item_template)

            count += 1
            Logger.progress('Loading item templates...', count, length)

        return length

    @staticmethod
    def load_item_loot_templates():
        item_loot_templates = WorldDatabaseManager.item_get_loot_template()
        length = len(item_loot_templates)
        count = 0

        for item_loot_template in item_loot_templates:
            WorldDatabaseManager.ItemLootTemplateHolder.load_item_loot_template(item_loot_template)
            count += 1
            Logger.progress('Loading item loot templates...', count, length)

        return length

    @staticmethod
    def load_pickpocketing_loot_templates():
        pickpocketing_loot_templates = WorldDatabaseManager.pickpocketing_loot_template_get_all()
        length = len(pickpocketing_loot_templates)
        count = 0

        for pickpocketing_loot_template in pickpocketing_loot_templates:
            WorldDatabaseManager.PickPocketingLootTemplateHolder.load_pickpocketing_loot_template(
                pickpocketing_loot_template)
            count += 1
            Logger.progress('Loading pickpocketing loot templates...', count, length)

        return length

    @staticmethod
    def load_reference_loot_templates():
        reference_loot_templates = WorldDatabaseManager.reference_loot_template_get_all()
        length = len(reference_loot_templates)
        count = 0

        for reference_loot_template in reference_loot_templates:
            WorldDatabaseManager.ReferenceLootTemplateHolder.load_reference_loot_template(reference_loot_template)
            count += 1
            Logger.progress('Loading reference loot templates...', count, length)

        return length

    @staticmethod
    def load_locks():
        locks = DbcDatabaseManager.locks_get_all()
        length = len(locks)
        count = 0

        for lock in locks:
            DbcDatabaseManager.LocksHolder.load_lock(lock)

            count += 1
            Logger.progress('Loading locks...', count, length)

        return length

    @staticmethod
    def load_factions():
        factions = DbcDatabaseManager.faction_get_all()
        length = len(factions)
        count = 0

        for faction in factions:
            DbcDatabaseManager.FactionHolder.load_faction(faction)

            count += 1
            Logger.progress('Loading factions...', count, length)

        return length

    @staticmethod
    def load_faction_templates():
        faction_templates = DbcDatabaseManager.faction_template_get_all()
        length = len(faction_templates)
        count = 0

        for faction_template in faction_templates:
            DbcDatabaseManager.FactionTemplateHolder.load_faction_template(faction_template)

            count += 1
            Logger.progress('Loading faction templates...', count, length)

        return length

    @staticmethod
    def load_quests():
        quest_templates = WorldDatabaseManager.quest_template_get_all()
        length = len(quest_templates)
        count = 0

        for quest_template in quest_templates:
            WorldDatabaseManager.QuestTemplateHolder.load_quest_template(quest_template)

            count += 1
            Logger.progress('Loading quest templates...', count, length)

        return length

    @staticmethod
    def load_spells():
        spells: list[Spell] = DbcDatabaseManager.spell_get_all()
        length = len(spells)
        count = 0

        for spell in spells:
            DbcDatabaseManager.SpellHolder.load_spell(spell)

            count += 1
            Logger.progress('Loading spells...', count, length)

        return length

    @staticmethod
    def load_spell_chains():
        spell_chains: list[SpellChain] = WorldDatabaseManager.spell_chain_get_all()
        length = len(spell_chains)
        count = 0

        for spell_chain in spell_chains:
            WorldDatabaseManager.SpellChainHolder.load_spell_chain(spell_chain)

            count += 1
            Logger.progress('Loading spell chains...', count, length)

        return length

    @staticmethod
    def load_default_profession_spells():
        default_profession_spells = WorldDatabaseManager.default_profession_spell_get_all()
        length = len(default_profession_spells)
        count = 0

        for profession_spell in default_profession_spells:
            WorldDatabaseManager.DefaultProfessionSpellHolder.load_default_profession_spell(profession_spell)

            count += 1
            Logger.progress('Loading default profession spells...', count, length)

        return length

    @staticmethod
    def load_trainer_spells():
        trainer_spells = WorldDatabaseManager.trainer_spell_get_all()
        length = len(trainer_spells)
        count = 0

        for trainer_spell in trainer_spells:
            WorldDatabaseManager.TrainerSpellHolder.load_trainer_spell(trainer_spell)

            count += 1
            Logger.progress('Loading trainer spells...', count, length)

        return length

    @staticmethod
    def load_skills():
        skills = DbcDatabaseManager.skill_get_all()
        length = len(skills)
        count = 0

        for skill in skills:
            DbcDatabaseManager.SkillHolder.load_skill(skill)

            count += 1
            Logger.progress('Loading skill...', count, length)

        return length

    @staticmethod
    def load_skill_line_abilities():
        skill_line_abilities = DbcDatabaseManager.skill_line_ability_get_all()
        length = len(skill_line_abilities)
        count = 0

        for skill_line_ability in skill_line_abilities:
            DbcDatabaseManager.SkillLineAbilityHolder.load_skill_line_ability(skill_line_ability)

            count += 1
            Logger.progress('Loading skill line abilities...', count, length)

        return length

    @staticmethod
    def load_char_base_infos():
        char_base_infos = DbcDatabaseManager.char_base_info_get_all()
        length = len(char_base_infos)
        count = 0

        for char_base_info in char_base_infos:
            DbcDatabaseManager.CharBaseInfoHolder.load_base_info(char_base_info)

            count += 1
            Logger.progress('Loading char base infos...', count, length)

        return length

    @staticmethod
    def load_taxi_nodes():
        taxi_nodes = DbcDatabaseManager.taxi_nodes_get_all()
        length = len(taxi_nodes)
        count = 0

        for taxi_node in taxi_nodes:
            DbcDatabaseManager.TaxiNodesHolder.load_taxi_node(taxi_node)

            count += 1
            Logger.progress('Loading taxi nodes...', count, length)

        return length

    @staticmethod
    def load_taxi_path_nodes():
        taxi_path_nodes = DbcDatabaseManager.taxi_path_nodes_get_all()
        length = len(taxi_path_nodes)
        count = 0

        for taxi_path_node in taxi_path_nodes:
            DbcDatabaseManager.TaxiPathNodesHolder.load_taxi_path_node(taxi_path_node)

            count += 1
            Logger.progress('Loading taxi path nodes...', count, length)

        return length

    @staticmethod
    def load_area_trigger_quest_relations():
        area_trigger_quest_relations = WorldDatabaseManager.area_trigger_quest_relations_get_all()
        length = len(area_trigger_quest_relations)
        count = 0

        for area_trigger_relation in area_trigger_quest_relations:
            WorldDatabaseManager.QuestRelationHolder.load_area_trigger_quest_relation(area_trigger_relation)

            count += 1
            Logger.progress('Loading area trigger quest relations...', count, length)

        return length

    @staticmethod
    def load_creature_quest_starters():
        creature_quest_starters = WorldDatabaseManager.creature_quest_starter_get_all()
        length = len(creature_quest_starters)
        count = 0

        for creature_quest_starter in creature_quest_starters:
            WorldDatabaseManager.QuestRelationHolder.load_creature_starter_quest(creature_quest_starter)

            count += 1
            Logger.progress('Loading creature quest starters...', count, length)

        return length

    @staticmethod
    def load_creature_quest_finishers():
        creature_quest_finishers = WorldDatabaseManager.creature_quest_finisher_get_all()
        length = len(creature_quest_finishers)
        count = 0

        for creature_quest_finisher in creature_quest_finishers:
            WorldDatabaseManager.QuestRelationHolder.load_creature_finisher_quest(creature_quest_finisher)

            count += 1
            Logger.progress('Loading creature quest finishers...', count, length)

        return length

    @staticmethod
    def load_creature_display_info():
        creature_display_infos = DbcDatabaseManager.creature_display_info_get_all()
        length = len(creature_display_infos)
        count = 0

        for creature_display_info in creature_display_infos:
            DbcDatabaseManager.CreatureDisplayInfoHolder.load_creature_display_info(creature_display_info)

            count += 1
            Logger.progress('Loading creature display info...', count, length)

        return length

    @staticmethod
    def load_creature_model_info():
        creature_model_infos = WorldDatabaseManager.creature_model_info_get_all()
        length = len(creature_model_infos)
        count = 0

        for creature_model_info in creature_model_infos:
            WorldDatabaseManager.CreatureModelInfoHolder.load_creature_model_info(creature_model_info)

            count += 1
            Logger.progress('Loading creature model info...', count, length)

        return length

    @staticmethod
    def load_creature_families():
        creature_families = DbcDatabaseManager.creature_family_get_all()
        length = len(creature_families)
        count = 0

        for creature_family in creature_families:
            DbcDatabaseManager.CreatureFamilyHolder.load_creature_family(creature_family)

            count += 1
            Logger.progress('Loading creature families...', count, length)

        return length

    @staticmethod
    def load_npc_gossip():
        npc_gossips = WorldDatabaseManager.npc_gossip_get_all()
        length = len(npc_gossips)
        count = 0

        for npc_gossip in npc_gossips:
            WorldDatabaseManager.QuestGossipHolder.load_npc_gossip(npc_gossip)

            count += 1
            Logger.progress('Loading npc gossip...', count, length)

        return length

    @staticmethod
    def load_npc_text():
        npc_texts = WorldDatabaseManager.npc_text_get_all()
        length = len(npc_texts)
        count = 0

        for npc_text in npc_texts:
            WorldDatabaseManager.QuestGossipHolder.load_npc_text(npc_text)

            count += 1
            Logger.progress('Loading npc gossip texts...', count, length)

        return length

    @staticmethod
    def load_broadcast_text():
        broadcast_texts = WorldDatabaseManager.broadcast_text_get_all()
        length = len(broadcast_texts)
        count = 0

        for broadcast_text in broadcast_texts:
            WorldDatabaseManager.BroadcastTextHolder.load_broadcast_text(broadcast_text)

            count += 1
            Logger.progress('Loading broadcast texts...', count, length)

        return length        

    # Character data holders

    @staticmethod
    def load_groups():
        groups = RealmDatabaseManager.group_get_all()
        length = len(groups)
        count = 0

        for group in groups:
            GroupManager.load_group(group)

            count += 1
            Logger.progress('Loading groups...', count, length)

        return length

    @staticmethod
    def load_guilds():
        guilds = RealmDatabaseManager.guild_get_all()
        length = len(guilds)
        count = 0

        for guild in guilds:
            if guild.name not in GuildManager.GUILDS:
                GuildManager.load_guild(guild)

                count += 1
                Logger.progress('Loading guilds...', count, length)

        return length
