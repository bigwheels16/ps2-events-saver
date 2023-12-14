import config
from db import DB

db = DB()
db.connect(
    config.DB_DRIVERNAME(),
    config.DB_USERNAME(),
    config.DB_PASSWORD(),
    config.DB_NAME(),
    config.DB_HOST(),
    config.DB_IP_TYPE())


if not db.table_exists("player_login_event"):
    with open("./resources/tables.sql", "rt") as sql_file:
        db.exec(sql_file.read())


def insert_player_login_event(character_id, world_id, timestamp):
    return db.exec("INSERT INTO player_login_event (character_id, world_id, timestamp) VALUES (:character_id, :world_id, :timestamp)",
        {
            "character_id": character_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_player_logout_event(character_id, world_id, timestamp):
    return db.exec("INSERT INTO player_logout_event (character_id, world_id, timestamp) VALUES (:character_id, :world_id, :timestamp)",
        {
            "character_id": character_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_gain_experience_event(amount, loadout_id, experience_id, other_id, character_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO gain_experience_event (amount, loadout_id, experience_id, other_id, character_id, zone_id, world_id, timestamp) "
                    "VALUES (:amount, :loadout_id, :experience_id, :other_id, :character_id, :zone_id, :world_id, :timestamp)",
        {
            "amount": amount,
            "loadout_id": loadout_id,
            "experience_id": experience_id,
            "other_id": other_id,
            "character_id": character_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_death_event(is_headshot, attacker_loadout_id, attacker_fire_mode_id, attacker_weapon_id, attacker_vehicle_id, attacker_character_id, character_loadout_id, character_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO death_event (is_headshot, attacker_loadout_id, attacker_fire_mode_id, attacker_weapon_id, attacker_vehicle_id, attacker_character_id, character_loadout_id, character_id, zone_id, world_id, timestamp) "
                    "VALUES (:is_headshot, :attacker_loadout_id, :attacker_fire_mode_id, :attacker_weapon_id, :attacker_vehicle_id, :attacker_character_id, :character_loadout_id, :character_id, :zone_id, :world_id, :timestamp)",
        {
            "is_headshot": is_headshot,
            "attacker_loadout_id": attacker_loadout_id,
            "attacker_fire_mode_id": attacker_fire_mode_id,
            "attacker_weapon_id": attacker_weapon_id,
            "attacker_vehicle_id": attacker_vehicle_id,
            "attacker_character_id": attacker_character_id,
            "character_loadout_id": character_loadout_id,
            "character_id": character_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_vehicle_destroy_event(faction_id, attacker_loadout_id, attacker_weapon_id, attacker_vehicle_id, attacker_character_id, character_vehicle_id, character_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO vehicle_destroy_event (faction_id, attacker_loadout_id, attacker_weapon_id, attacker_vehicle_id, attacker_character_id, character_vehicle_id, character_id, zone_id, world_id, timestamp) "
                    "VALUES (:faction_id, :attacker_loadout_id, :attacker_weapon_id, :attacker_vehicle_id, :attacker_character_id, :character_vehicle_id, :character_id, :zone_id, :world_id, :timestamp)",
        {
            "faction_id": faction_id,
            "attacker_loadout_id": attacker_loadout_id,
            "attacker_weapon_id": attacker_weapon_id,
            "attacker_vehicle_id": attacker_vehicle_id,
            "attacker_character_id": attacker_character_id,
            "character_vehicle_id": character_vehicle_id,
            "character_id": character_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_facility_defend_event(character_id, outfit_id, facility_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO facility_defend_event (character_id, outfit_id, facility_id, zone_id, world_id, timestamp) "
                    "VALUES (:character_id, :outfit_id, :facility_id, :zone_id, :world_id, :timestamp)",
        {
            "character_id": character_id,
            "outfit_id": outfit_id,
            "facility_id": facility_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_facility_capture_event(character_id, outfit_id, facility_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO facility_capture_event (character_id, outfit_id, facility_id, zone_id, world_id, timestamp) "
                    "VALUES (:character_id, :outfit_id, :facility_id, :zone_id, :world_id, :timestamp)",
        {
            "character_id": character_id,
            "outfit_id": outfit_id,
            "facility_id": facility_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )

def insert_facility_control_event(duration_held, facility_id, old_faction_id, new_faction_id, outfit_id, zone_id, world_id, timestamp):
    return db.exec("INSERT INTO facility_control_event (duration_held, facility_id, old_faction_id, new_faction_id, outfit_id, zone_id, world_id, timestamp) "
                    "VALUES (:duration_held, :facility_id, :old_faction_id, :new_faction_id, :outfit_id, :zone_id, :world_id, :timestamp)",
        {
            "duration_held": duration_held,
            "facility_id": facility_id,
            "old_faction_id": old_faction_id,
            "new_faction_id": new_faction_id,
            "outfit_id": outfit_id,
            "zone_id": zone_id,
            "world_id": world_id,
            "timestamp": timestamp,
        }
    )
