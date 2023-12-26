from multiprocessing import Queue
import threading
import time
import rel
import json
import websocket
import logging
import service
import config


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

last_message_received_at = 0
num_messages_received = 0
alt_login_threshold_seconds = 15
min_zone_id = config.MIN_ZONE_ID()
max_zone_id = 10000000


def process_message(ws, message):
    global last_message_received_at, num_messages_received
    last_message_received_at = int(time.time())
    num_messages_received += 1

    obj = json.loads(message)
    _type = obj.get("type")

    logger.info(message)

    if _type == "serviceMessage":
        payload = obj.get("payload")
        event_name = payload.get("event_name")
        
        if event_name == "GainExperience":
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
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
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
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
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
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
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
                service.insert_facility_defend_event(
                    payload["character_id"],
                    payload["outfit_id"],
                    payload["facility_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "PlayerFacilityCapture":
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
                service.insert_facility_capture_event(
                    payload["character_id"],
                    payload["outfit_id"],
                    payload["facility_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "FacilityControl":
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
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
    
    #logger.info("processed msg")


def on_error(ws, error):
    logger.error("error on web socket", exc_info=error)


def on_open(ws):
    logger.info("connected!")


def verify_messages_received():
    time_since_last_message = int(time.time()) - last_message_received_at
    if time_since_last_message > 60:
        logger.error(f"no message received for {time_since_last_message}s, stopping")
        rel.abort()

    return True


def log_num_messages_received():
    logger.info(f"messages received: {num_messages_received:,}")
    #rel.timeout(1800, log_num_messages_received)
    return True


if __name__ == "__main__":
    q = Queue(50)

    def add_message(ws, msg):
        #logger.info("adding msg")
        try:
            q.put(msg, block=False)
        except Exception as e:
            logger.error("error adding message", exc_info=e)

    def on_close(ws, close_status_code, close_msg):
        logger.warning(close_status_code, close_msg)
        q.close()

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        config.PS2_STREAMING_API_URL(),
        on_open=on_open,
        on_message=add_message,
        on_error=on_error,
        on_close=on_close)
    
    def abort():
        logger.warning("shutting down")
        ws.close()
        q.close()
        rel.abort()
    
    def worker():
        try:
            while True:
                msg = q.get()
                #logger.info("processing msg")
                process_message(ws, msg)
        except EOFError:
            logger.info("queue closed")
            return
        except Exception as e:
            logger.error("error in worker", exc_info=e)

    threading.Thread(target=worker).start()

    rel.set_sleep(0.003)
    #rel.set_turbo(0.0001)

    ws.run_forever(dispatcher=rel)
    rel.signal(2, abort)
    rel.timeout(21, verify_messages_received)
    rel.timeout(1800, log_num_messages_received)
    rel.dispatch()
