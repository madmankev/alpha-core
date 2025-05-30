from struct import unpack
from game.world.managers.maps.MapManager import MapManager
from game.world.opcode_handling.HandlerValidator import HandlerValidator
from network.packet.PacketWriter import PacketWriter, OpCode
from utils.GuidUtils import GuidUtils
from utils.constants.MiscCodes import HighGuid, ScriptTypes
from utils.Logger import Logger


class QuestGiverAcceptQuestHandler(object):

    @staticmethod
    def handle(world_session, socket, reader):
        # Validate world session.
        player_mgr, res = HandlerValidator.validate_session(world_session, reader.opcode)
        if not player_mgr:
            return res

        if len(reader.data) >= 12:  # Avoid handling empty quest giver accept quest packet.
            guid, quest_id = unpack('<QI', reader.data[:12])

            is_item = False
            quest_giver = None
            # Use player known objects first.
            if guid in player_mgr.known_objects:
                quest_giver = player_mgr.known_objects[guid]
            else:
                high_guid = GuidUtils.extract_high_guid(guid)
                if high_guid == HighGuid.HIGHGUID_ITEM:
                    is_item = True
                    quest_giver = player_mgr.inventory.get_item_by_guid(guid)
                elif high_guid == HighGuid.HIGHGUID_UNIT:
                    quest_giver = MapManager.get_surrounding_unit_by_guid(player_mgr, guid)
                elif high_guid == HighGuid.HIGHGUID_GAMEOBJECT:
                    quest_giver = MapManager.get_surrounding_gameobject_by_guid(player_mgr, guid)

            if not quest_giver:
                Logger.error(f'Error in {reader.opcode_str()}, could not find quest giver with guid of: {guid}.')
                return 0
            elif not is_item and player_mgr.is_hostile_to(quest_giver):
                Logger.warning(f'{reader.opcode_str()}, quest giver with guid: {guid} is hostile.')
                return 0
            elif player_mgr.quest_manager.is_quest_log_full():
                player_mgr.enqueue_packet(PacketWriter.get_packet(OpCode.SMSG_QUESTLOG_FULL))
            elif is_item or quest_giver.is_within_interactable_distance(player_mgr):
                player_mgr.quest_manager.handle_accept_quest(quest_id, guid, shared=False, quest_giver=quest_giver,
                                                             is_item=is_item)
                # TODO: This shouldn't be needed at all, it's only useful for escort quests. EscortAI is needed (or use
                #  ScriptedMadEvent for them instead, need to think about it).
                if not is_item:
                    quest_giver.quest_target = player_mgr

        return 0
