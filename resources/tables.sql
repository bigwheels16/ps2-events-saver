CREATE TABLE player_login_event (id INT PRIMARY KEY AUTO_INCREMENT, character_id BIGINT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);
CREATE TABLE player_logout_event (id INT PRIMARY KEY AUTO_INCREMENT, character_id BIGINT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);

CREATE TABLE gain_experience_event (id INT PRIMARY KEY AUTO_INCREMENT, amount SMALLINT NOT NULL, loadout_id TINYINT NOT NULL, experience_id SMALLINT NOT NULL, other_id BIGINT NOT NULL, character_id BIGINT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);

CREATE TABLE death_event (id INT PRIMARY KEY AUTO_INCREMENT, is_headshot TINYINT NOT NULL, attacker_loadout_id TINYINT NOT NULL, attacker_fire_mode_id INT NOT NULL, attacker_weapon_id INT NOT NULL, attacker_vehicle_id SMALLINT NOT NULL, attacker_character_id BIGINT NOT NULL, character_loadout_id TINYINT NOT NULL, character_id BIGINT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);
CREATE TABLE vehicle_destroy_event (id INT PRIMARY KEY AUTO_INCREMENT, faction_id TINYINT NOT NULL, attacker_loadout_id TINYINT NOT NULL, attacker_weapon_id INT NOT NULL, attacker_vehicle_id SMALLINT NOT NULL, attacker_character_id BIGINT NOT NULL, character_vehicle_id SMALLINT NOT NULL, character_id BIGINT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);

CREATE TABLE facility_defend_event (id INT PRIMARY KEY AUTO_INCREMENT, character_id BIGINT NOT NULL, outfit_id BIGINT NOT NULL, facility_id INT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);
CREATE TABLE facility_capture_event (id INT PRIMARY KEY AUTO_INCREMENT, character_id BIGINT NOT NULL, outfit_id BIGINT NOT NULL, facility_id INT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);

CREATE TABLE facility_control_event (id INT PRIMARY KEY AUTO_INCREMENT, duration_held INT NOT NULL, facility_id INT NOT NULL, old_faction_id INT NOT NULL, new_faction_id INT NOT NULL, outfit_id BIGINT NOT NULL, zone_id INT NOT NULL, world_id TINYINT NOT NULL, timestamp INT NOT NULL);

CREATE TABLE character_info (character_id BIGINT PRIMARY KEY, name VARCHAR(255) NOT NULL, outfit_id BIGINT NOT NULL, member_since INT NOT NULL, created_at INT NOT NULL, minutes_played INT NOT NULL, battle_rank INT NOT NULL, is_prestige TINYINT NOT NULL, world_id TINYINT NOT NULL, last_login INT NOT NULL);
CREATE TABLE outfit_info (outfit_id BIGINT PRIMARY KEY, alias VARCHAR(4) NOT NULL, name VARCHAR(255) NOT NULL, faction_id SMALLINT NOT NULL);
CREATE TABLE weapon_info (item_id INT PRIMARY KEY, weapon_id INT, name VARCHAR(50) NOT NULL, faction_id SMALLINT NOT NULL, vehicle_id INT NOT NULL, vehicle_slot_id INT NOT NULL, is_used TINYINT NOT NULL);
--UPDATE weapon_info w JOIN (SELECT DISTINCT attacker_weapon_id FROM vehicle_destroy_event) t ON w.item_id = t.attacker_weapon_id SET is_used = 1;

CREATE TABLE facility_info (facility_id INT PRIMARY KEY, zone_id INT NOT NULL, name VARCHAR(50) NOT NULL);

--CREATE TABLE death_event_aggregate (num_kills INT NOT NULL, attacker_weapon_id INT NOT NULL, attacker_vehicle_id INT NOT NULL, character_loadout_id SMALLINT NOT NULL, world_id SMALLINT NOT NULL);

CREATE TABLE zone_info (zone_id TINYINT NOT NULL, name VARCHAR(50) NOT NULL);
INSERT INTO zone_info (zone_id, name) VALUES (2, 'Indar');
INSERT INTO zone_info (zone_id, name) VALUES (4, 'Hossin');
INSERT INTO zone_info (zone_id, name) VALUES (6, 'Amerish');
INSERT INTO zone_info (zone_id, name) VALUES (8, 'Esamir');
INSERT INTO zone_info (zone_id, name) VALUES (96, 'VR training zone (NC)');
INSERT INTO zone_info (zone_id, name) VALUES (97, 'VR training zone (TR)');
INSERT INTO zone_info (zone_id, name) VALUES (98, 'VR training zone (VS)');

CREATE TABLE world_info (world_id INT PRIMARY KEY, name VARCHAR(20) NOT NULL);
INSERT INTO world_info (world_id, name) VALUES (1, 'Connery');
INSERT INTO world_info (world_id, name) VALUES (10, 'Miller');
INSERT INTO world_info (world_id, name) VALUES (13, 'Cobalt');
INSERT INTO world_info (world_id, name) VALUES (17, 'Emerald');
INSERT INTO world_info (world_id, name) VALUES (19, 'Jaeger');
INSERT INTO world_info (world_id, name) VALUES (24, 'Apex');
INSERT INTO world_info (world_id, name) VALUES (25, 'Briggs');
INSERT INTO world_info (world_id, name) VALUES (40, 'SolTech');

CREATE TABLE matches (name VARCHAR(255) NOT NULL, zone_id INT NOT NULL);

--DROP TABLE player_login_event; DROP TABLE player_logout_event; DROP TABLE gain_experience_event; DROP TABLE death_event; DROP TABLE vehicle_destroy_event; DROP TABLE facility_capture_event; DROP TABLE facility_defend_event; DROP TABLE character_info;

CREATE TABLE vehicle_info (vehicle_id INT PRIMARY KEY, name VARCHAR(50) NOT NULL, category VARCHAR(20) NOT NULL);
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (1, 'Flash', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2, 'Sunderer', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (3, 'Lightning', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (4, 'Magrider', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (5, 'Vanguard', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (6, 'Prowler', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (7, 'Scythe', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (8, 'Reaver', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (9, 'Mosquito', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (10, 'Liberator', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (11, 'Galaxy', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (12, 'Harasser', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (14, 'Valkyrie', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (15, 'Ant', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2007, 'Colossus', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2010, 'Flash XS-1', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2019, 'Bastion Fleet Carrier', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2033, 'Javelin', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2122, 'Mosquito Interceptor', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2123, 'Reaver Interceptor', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2124, 'Scythe Interceptor', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2125, 'Javelin', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2129, 'Javelin', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2130, 'Reclaimed Sunderer', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2131, 'Reclaimed Galaxy', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2132, 'Reclaimed Valkyrie', '');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2133, 'Reclaimed Magrider', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2134, 'Reclaimed Vanguard', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2135, 'Reclaimed Prowler', 'MBT');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2136, 'Dervish', 'ESF');
INSERT INTO vehicle_info (vehicle_id, name, category) VALUES (2137, 'Chimera', 'MBT');

CREATE TABLE faction_info (faction_id INT PRIMARY KEY, name VARCHAR(50) NOT NULL, alias VARCHAR(4) NOT NULL);
INSERT INTO faction_info (faction_id, name, alias) VALUES (0, 'None', 'None');
INSERT INTO faction_info (faction_id, name, alias) VALUES (1, 'Vanu Sovereignty', 'VS');
INSERT INTO faction_info (faction_id, name, alias) VALUES (2, 'New Conglomerate', 'NC');
INSERT INTO faction_info (faction_id, name, alias) VALUES (3, 'Terran Republic', 'TR');
INSERT INTO faction_info (faction_id, name, alias) VALUES (4, 'NS Operatives', 'NSO');

CREATE TABLE loadout_info (loadout_id SMALLINT PRIMARY KEY, profile_id SMALLINT NOT NULL, profile_type VARCHAR(20), faction_id SMALLINT NOT NULL);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (1, 2, 'Infiltrator', 2);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (3, 4, 'Light Assault', 2);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (4, 5, 'Medic', 2);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (5, 6, 'Engineer', 2);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (6, 7, 'Heavy Assault', 2);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (7, 8, 'MAX', 2);

INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (8, 10, 'Infiltrator', 3);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (10, 12, 'Light Assault', 3);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (11, 13, 'Medic', 3);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (12, 14, 'Engineer', 3);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (13, 15, 'Heavy Assault', 3);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (14, 16, 'MAX', 3);

INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (15, 17, 'Infiltrator', 1);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (17, 19, 'Light Assault', 1);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (18, 20, 'Medic', 1);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (19, 21, 'Engineer', 1);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (20, 22, 'Heavy Assault', 1);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (21, 23, 'MAX', 1);

INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (28, 0, 'Infiltrator', 4);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (29, 0, 'Light Assault', 4);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (30, 0, 'Medic', 4);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (31, 0, 'Engineer', 4);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (32, 0, 'Heavy Assault', 4);
INSERT INTO loadout_info (loadout_id, profile_id, profile_type, faction_id) VALUES (45, 0, 'MAX', 4);

CREATE TABLE experience_info (experience_id INT PRIMARY KEY, description VARCHAR(255) NOT NULL);
INSERT INTO experience_info (experience_id, description) VALUES (1, 'Kill Player');
INSERT INTO experience_info (experience_id, description) VALUES (2, 'Kill Player Assist');
INSERT INTO experience_info (experience_id, description) VALUES (3, 'Kill Player Spawn Assist');
INSERT INTO experience_info (experience_id, description) VALUES (4, 'Heal Player');
INSERT INTO experience_info (experience_id, description) VALUES (5, 'Heal Assist');
INSERT INTO experience_info (experience_id, description) VALUES (6, 'MAX Repair');
INSERT INTO experience_info (experience_id, description) VALUES (7, 'Revive');
INSERT INTO experience_info (experience_id, description) VALUES (37, 'Headshot');
INSERT INTO experience_info (experience_id, description) VALUES (51, 'Heal Player - Squad');
INSERT INTO experience_info (experience_id, description) VALUES (53, 'Revive - Squad');
INSERT INTO experience_info (experience_id, description) VALUES (56, 'Squad Spawn');

INSERT INTO experience_info (experience_id, description) VALUES (30, 'Transport Assist');
INSERT INTO experience_info (experience_id, description) VALUES (142, 'MAX Repair - Squad');
INSERT INTO experience_info (experience_id, description) VALUES (201, 'Galaxy Spawn Bonus');
INSERT INTO experience_info (experience_id, description) VALUES (233, 'Sunderer Spawn Bonus');
INSERT INTO experience_info (experience_id, description) VALUES (277, 'Spawn Kill');
INSERT INTO experience_info (experience_id, description) VALUES (335, 'Savior Kill (Non MAX)');
INSERT INTO experience_info (experience_id, description) VALUES (355, 'Squad Vehicle Spawn Bonus');
INSERT INTO experience_info (experience_id, description) VALUES (592, 'Savior Kill (MAX)');


CREATE INDEX idx1 ON gain_experience_event(character_id);
CREATE INDEX idx2 ON death_event(character_id);
CREATE INDEX idx3 ON death_event(attacker_character_id);
CREATE INDEX idx4 ON vehicle_destroy_event(character_id);
CREATE INDEX idx5 ON vehicle_destroy_event(attacker_character_id);
CREATE INDEX idx6 ON player_login_event(character_id);
CREATE INDEX idx7 ON player_logout_event(character_id);
CREATE INDEX idx8 ON character_info(character_id);
CREATE INDEX idx9 ON character_info(outfit_id);
CREATE INDEX idx10 ON vehicle_destroy_event(world_id, character_vehicle_id);
CREATE INDEX idx11 ON death_event(world_id, timestamp);
CREATE INDEX idx12 ON death_event_aggregate(world_id, character_loadout_id);
CREATE INDEX idx13 ON death_event(attacker_weapon_id);
CREATE INDEX idx14 ON loadout_info(loadout_id);

CREATE INDEX idx15 ON gain_experience_event(match_id);
CREATE INDEX idx16 ON vehicle_destroy_event(match_id);
