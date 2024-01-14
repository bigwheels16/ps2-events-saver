from multiprocessing import Queue
import threading
import time
import sys
import rel
import json
import websocket
import logging
import service
import config
import metrics
import signal


logging.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

num_messages_received = 0
last_player_event_received = int(time.time())


def process_message(ws, message, min_zone_id, max_zone_id):
    obj = json.loads(message)
    _type = obj.get("type")

    global num_messages_received
    num_messages_received += 1

    global last_player_event_received
                
    #logger.debug(message)

    if _type == "serviceMessage":
        payload = obj.get("payload")
        event_name = payload.get("event_name")
        
        if event_name == "GainExperience":
            last_player_event_received = int(time.time())
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
            last_player_event_received = int(time.time())
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
            last_player_event_received = int(time.time())
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
            last_player_event_received = int(time.time())
            if min_zone_id < int(payload["zone_id"]) < max_zone_id:
                service.insert_facility_defend_event(
                    payload["character_id"],
                    payload["outfit_id"],
                    payload["facility_id"],
                    payload["zone_id"],
                    payload["world_id"],
                    payload["timestamp"])
        elif event_name == "PlayerFacilityCapture":
            last_player_event_received = int(time.time())
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
    

def on_error(ws, error):
    logger.error("error on web socket", exc_info=error)


def on_open(ws):
    logger.info("connected!")


def verify_messages_received(abort_func):
    global last_player_event_received
    if (int(time.time()) - last_player_event_received) > 60:
        logger.error(f"no player events recieved in last 60 seconds, stopping")
        abort_func(-1)
    else:
        return True


def log_num_messages_received():
    try:
        metrics.publish_time_series("total_events_received", num_messages_received)
    except Exception as e:
        logger.error("error sending metrics", exc_info=e)

    return True


def main():
    q = Queue(50)
    min_zone_id = config.MIN_ZONE_ID()
    max_zone_id = 10000000
    
    def add_message(ws, msg):
        try:
            q.put(msg, block=False)
        except Exception as e:
            logger.error("error adding message", exc_info=e)

    def on_close(ws, close_status_code, close_msg):
        logger.warning("websocket closed: %s %s", close_status_code, close_msg)
        q.close()

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        config.PS2_STREAMING_API_URL(),
        on_open=on_open,
        on_message=add_message,
        on_error=on_error,
        on_close=on_close)
    
    def abort(signal_code):
        logger.warning(f"shutting down due to signal '{signal_code}'")
        ws.close()
        q.close()
        #log_num_messages_received()
        rel.abort()
    
    def worker():
        try:
            while True:
                msg = q.get()
                process_message(ws, msg, min_zone_id, max_zone_id)
        except EOFError:
            logger.info("queue closed")
        except Exception as e:
            logger.error("error in worker", exc_info=e)

    threading.Thread(target=worker).start()

    rel.set_sleep(0.003)
    #rel.set_turbo(0.0001)

    ws.run_forever(dispatcher=rel)
    rel.signal(signal.SIGINT, abort, signal.SIGINT)
    rel.signal(signal.SIGTERM, abort, signal.SIGTERM)
    rel.timeout(21, verify_messages_received, abort)
    rel.timeout(60, log_num_messages_received)
    rel.dispatch()
 

if __name__ == "__main__":
   main() 