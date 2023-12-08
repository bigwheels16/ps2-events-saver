import threading
import time
import rel
import json
import websocket
import logging
from service import Service
import config


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

last_message_received_at = 0
alt_login_threshold_seconds = 15
min_zone_id = config.MIN_ZONE_ID()

char_list = {}

service = Service()


def on_message(ws, message):
    last_message_received_at = int(time.time())

    obj = json.loads(message)
    _type = obj.get("type")

    if _type == "serviceMessage":
        #logger.info(message)

        payload = obj.get("payload")
        event_name = payload.get("event_name")
        
        if event_name == "GainExperience":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_gain_experience_event(
                    payload["amount"],
                    payload["loadout_id"],
                    payload["experience_id"],
                    payload["other_id"],
                    payload["character_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "Death":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_death_event(
                    payload["is_headshot"],
                    payload["attacker_loadout_id"],
                    payload["attacker_fire_mode_id"],
                    payload["attacker_weapon_id"],
                    payload["attacker_vehicle_id"],
                    payload["attacker_character_id"],
                    payload["character_loadout_id"],
                    payload["character_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "VehicleDestroy":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_vehicle_destroy_event(
                    payload["faction_id"],
                    payload["attacker_loadout_id"],
                    payload["attacker_weapon_id"],
                    payload["attacker_vehicle_id"],
                    payload["attacker_character_id"],
                    payload["vehicle_id"],
                    payload["character_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "PlayerLogin":
            service.insert_player_login_event(
                payload["character_id"],
                payload["world_id"],
                payload["timestamp"])
        elif event_name == "PlayerLogout":
            service.insert_player_logout_event(
                payload["character_id"],
                payload["world_id"],
                payload["timestamp"])
        elif event_name == "PlayerFacilityDefend":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_facility_defend_event(
                    payload["character_id"],
                    payload["outfit_id"],
                    payload["facility_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "PlayerFacilityCapture":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_facility_capture_event(
                    payload["character_id"],
                    payload["outfit_id"],
                    payload["facility_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "FacilityControl":
            if int(payload["zone_id"]) > min_zone_id:
                service.insert_facility_control_event(
                    payload["duration_held"],
                    payload["facility_id"],
                    payload["old_faction_id"],
                    payload["new_faction_id"],
                    payload["outfit_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        else:
            raise Exception("Unknown event: %s" % obj)
        
    elif _type == "heartbeat":
        pass
    elif obj.get("connected") == "true":
        logger.info(obj)
        ws.send(json.dumps({
            "service": "event",
            "action": "subscribe",
            "characters": ["all"],
            "worlds": config.PS2_STREAMING_API_SUBSCRIBE_WORLDS(),
            "eventNames": config.PS2_STREAMING_API_SUBSCRIBE_EVENTS(),
            "logicalAndCharactersWithWorlds": True,
        }))
    else:
        logger.info("Received ws: %s", obj)


def on_error(ws, error):
    logger.error(error)


def on_close(ws, close_status_code, close_msg):
    logger.warning(close_status_code, close_msg)


def on_open(ws):
    logger.info("connected!")


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        config.PS2_STREAMING_API_URL(),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()
