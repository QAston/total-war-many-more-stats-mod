import csv

# shield
tsv_file = open("unit_shield_types_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
shields = {}

rowid = 0
shields_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        shields_keys[key] = i
        i = i + 1
  if rowid > 2:
      shields[row[shields_keys["key"]]] = row[shields_keys["missile_block_chance"]]
tsv_file.close()

# melee
tsv_file = open("melee_weapons_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
melee = {}

rowid = 0
melee_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        melee_keys[key] = i
        i = i + 1
  if rowid > 2:
      melee[row[melee_keys["key"]]] = row
tsv_file.close()

# armour
tsv_file = open("unit_armour_types_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
armour = {}

rowid = 0
armour_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        armour_keys[key] = i
        i = i + 1
  if rowid > 2:
      armour[row[armour_keys["key"]]] = row
tsv_file.close()

# projectiles
tsv_file = open("projectiles_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
projectiles = {}

rowid = 0
projectiles_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        projectiles_keys[key] = i
        i = i + 1
  if rowid > 2:
      projectiles[row[projectiles_keys["key"]]] = row
tsv_file.close()

# ability phase stats
tsv_file = open("special_ability_phase_stat_effects_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_phase_stats = {}

rowid = 0
ability_phase_stats_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_phase_stats_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[ability_phase_stats_keys["phase"]]
    if key not in ability_phase_stats:
      ability_phase_stats[key] = []
    ability_phase_stats[key].append(row)
tsv_file.close()

# projectiles_explosions_tables_projectiles_explosions
tsv_file = open("projectiles_explosions_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
projectiles_explosions = {}

rowid = 0
projectiles_explosions_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        projectiles_explosions_keys[key] = i
        i = i + 1
  if rowid > 2:
      projectiles_explosions[row[projectiles_explosions_keys["key"]]] = row
tsv_file.close()

# weapon_to_projectile
tsv_file = open("missile_weapons_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
weapon_projectile = {}

rowid = 0
weapon_projectile_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        weapon_projectile_keys[key] = i
        i = i + 1
  if rowid > 2:
      weapon_projectile[row[weapon_projectile_keys["key"]]] = row[weapon_projectile_keys["default_projectile"]]
tsv_file.close()

# weapon additional projectiles
tsv_file = open("missile_weapons_to_projectiles_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
weapon_alt_projectile = {}

rowid = 0
weapon_alt_projectile_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        weapon_alt_projectile_keys[key] = i
        i = i + 1
  if rowid > 2:
      key = row[weapon_alt_projectile_keys["missile_weapon"]]
      if key not in weapon_alt_projectile:
        weapon_alt_projectile[key] = []
      weapon_alt_projectile[key].append(row[weapon_alt_projectile_keys["projectile"]])
tsv_file.close()

# engine_to_weapon
tsv_file = open("battlefield_engines_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
engine_weapon = {}
engine_entity = {}

rowid = 0
engine_weapon_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        engine_weapon_keys[key] = i
        i = i + 1
  if rowid > 2:
      engine_weapon[row[engine_weapon_keys["key"]]] = row[engine_weapon_keys["missile_weapon"]]
      engine_entity[row[engine_weapon_keys["key"]]] = row[engine_weapon_keys["battle_entity"]]
tsv_file.close()

# mount_to_entity
tsv_file = open("mounts_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
mount_entity = {}

rowid = 0
mount_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        mount_keys[key] = i
        i = i + 1
  if rowid > 2:
      mount_entity[row[mount_keys["key"]]] = row[mount_keys["entity"]]
tsv_file.close()

def difftostr(stat):
  if stat > 0:
    return "[[col:green]]+" + str(stat) +"[[/col]]"
  if stat < 0:
    return "[[col:red]]" + str(stat) +"[[/col]]"
  return ""

def negdifftostr(stat):
  if stat > 0:
    return "[[col:red]]+" + str(stat) +"[[/col]]"
  if stat < 0:
    return "[[col:green]]" + str(stat) +"[[/col]]"
  return ""

def statstr(stat):
  return "[[col:ancillary_rare]]" + str(stat) +"[[/col]]"

# unit descriptions
tsv_file = open("unit_description_short_texts__.loc.tsv", encoding="utf-8")
read_tsv = csv.reader(tsv_file, delimiter="\t")
descriptions_keys = {}
descriptions = {}
rowid = 0
new_descriptions = []
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        descriptions_keys[key] = i
        i = i + 1
  #if rowid <= 2:
  new_descriptions.append(row)
  if rowid > 2:
      descid = row[descriptions_keys["key"]].replace("unit_description_short_texts_text_", "", 1)
      descriptions[descid] = row

# description id keys
tsv_file = open("unit_description_short_texts_tables_data__.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_description_ids = []
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  #if rowid <= 2:
  new_unit_description_ids.append(row)

# main unit table
tsv_file = open("main_units_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
main_units = {}

rowid = 0
main_units_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        main_units_keys[key] = i
        i = i + 1
  if rowid > 2:
      main_units[row[main_units_keys["land_unit"]]] = row
tsv_file.close()

# battle entities
tsv_file = open("battle_entities_tables_data__.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
battle_entities = {}

rowid = 0
battle_entities_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        battle_entities_keys[key] = i
        i = i + 1
  if rowid > 2:
      battle_entities[row[battle_entities_keys["key"]]] = row
tsv_file.close()

def missile_stats(projectilerow, unit):
  projectiletext = ""
  projectiletext += " ap_dmg " + statstr(projectilerow[projectiles_keys['ap_damage']])
  projectiletext += " accuracy " + statstr(float(projectilerow[projectiles_keys['marksmanship_bonus']]) + float(unit[units_keys['accuracy']]))
  if projectilerow[projectiles_keys['bonus_v_infantry']] != '0':
    projectiletext += " bonus_v_inf " + statstr(projectilerow[projectiles_keys['bonus_v_infantry']])
  if projectilerow[projectiles_keys['bonus_v_large']] != '0':
    projectiletext += " bonus_v_large " + statstr(projectilerow[projectiles_keys['bonus_v_large']])
  #todo: homing, projectile num, penetration, etc
  if projectilerow[projectiles_keys['explosion_type']] != '':
    projectiletext += " explosion: "
    explosionrow = projectiles_explosions[projectilerow[projectiles_keys['explosion_type']]]
    projectiletext += " dmg " + statstr(explosionrow[projectiles_explosions_keys['detonation_damage']])
    projectiletext += " radius " + statstr(explosionrow[projectiles_explosions_keys['detonation_radius']])
  #s = float(altprojectilerow[projectiles_keys['calibration_area']]) - float(projectilerow[projectiles_keys['calibration_area']])
  #if s != 0:
    #projectiletext += " calibration_area " + negdifftostr(s)
  projectiletext += ";"
  return projectiletext

# units
tsv_file = open("land_units_tables_data__.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

new_units = []

units_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        units_keys[key] = i
        i = i + 1
  if rowid <= 2:
    new_units.append(row)
  if rowid > 2:
      descid = row[units_keys['short_description_text']]
      unit = row.copy()
      desc = descriptions[descid].copy()
      newdescid = unit[units_keys['key']] + "_statdesc"
      unit[units_keys['short_description_text']] = newdescid
      desc[descriptions_keys["key"]] = "unit_description_short_texts_text_" + newdescid
      new_unit_description_ids.append([newdescid])
      new_units.append(unit)
      new_descriptions.append(desc)

      stats = {}
      desc_text = desc[descriptions_keys["text"]]
      desc[descriptions_keys["text"]] = ""
      if unit[units_keys['campaign_action_points']] != "2100":
        stats["campaign_range"] = unit[units_keys['campaign_action_points']]
      if unit[units_keys['shield']] != 'none':
        stats["missile_block"] = shields[unit[units_keys['shield']]] + "%"
      
      main_unit_entry = main_units[unit[units_keys['key']]]
      
      # aka. is high threat
      if main_unit_entry[main_units_keys["is_high_threat"]] == "true":
        desc[descriptions_keys["text"]]  += statstr("focuses_enemy_splash_dmg")

      entity = battle_entities[unit[units_keys['man_entity']]]

      if entity[battle_entities_keys["hit_reactions_ignore_chance"]] != "0":
        stats["hit_reactions_ignore"] = entity[battle_entities_keys["hit_reactions_ignore_chance"]] + "%"

      if entity[battle_entities_keys["knock_interrupts_ignore_chance"]] != "0":
        stats["knock_interrupts_ignore"] = entity[battle_entities_keys["knock_interrupts_ignore_chance"]] + "%"

      if main_unit_entry[main_units_keys["num_men"]] != "1":
        mount_health = 0
        if unit[units_keys['mount']] != '':
          mount = battle_entities[mount_entity[unit[units_keys['mount']]]]
          mount_health = int(mount[battle_entities_keys["hit_points"]])

        engine_health = 0
        if unit[units_keys['engine']] != '':
          engine = battle_entities[engine_entity[unit[units_keys['engine']]]]
          engine_health = int(engine[battle_entities_keys["hit_points"]])
        stats["health"] = str(engine_health + mount_health + int(entity[battle_entities_keys["hit_points"]]) + int(unit[units_keys['bonus_hit_points']]))
        
      if unit[units_keys['primary_melee_weapon']] != '':
          meleeid = unit[units_keys['primary_melee_weapon']]
          meleerow = melee[meleeid]
          stats["melee_ap_dmg"] = meleerow[melee_keys['ap_damage']]
          stats["melee_interval"] = meleerow[melee_keys['melee_attack_interval']]
          if meleerow[melee_keys['bonus_v_infantry']] != "0":
            stats["bonus_v_inf"] = meleerow[melee_keys['bonus_v_infantry']]
          # never set:stats["bonus_v_cav"] = meleerow[melee_keys['bonus_v_cavalry']]
          if meleerow[melee_keys['bonus_v_large']] != "0":
            stats["bonus_v_large"] = meleerow[melee_keys['bonus_v_large']]
          if meleerow[melee_keys['splash_attack_target_size']] != "":
            desc[descriptions_keys["text"]] += " splash dmg:"
            # confirmed by ca: blank means no splash damage
            desc[descriptions_keys["text"]] += " target_size " + statstr("<=" + meleerow[melee_keys['splash_attack_target_size']])
            desc[descriptions_keys["text"]] += " max_targets " + statstr(meleerow[melee_keys['splash_attack_max_attacks']])
            if float(meleerow[melee_keys['splash_attack_power_multiplier']]) != 1.0: 
              desc[descriptions_keys["text"]] += " power multiplier "+ statstr(round(float(meleerow[melee_keys['splash_attack_power_multiplier']]), 1))
            desc[descriptions_keys["text"]] += "; "
          if meleerow[melee_keys['collision_attack_max_targets']] != "0":
            desc[descriptions_keys["text"]]  += " collision: max targets " + statstr(meleerow[melee_keys['collision_attack_max_targets']]) + " cooldown " + statstr(meleerow[melee_keys['collision_attack_max_targets_cooldown']]) + "; "
      if unit[units_keys['armour']] != '':
          armourid = unit[units_keys['armour']]
          armourrow = armour[armourid]
      if int(unit[units_keys['secondary_ammo']]) != 0:
        stats["secondary_ammo"] = unit[units_keys['secondary_ammo']]
      for stat in stats:
          desc[descriptions_keys["text"]] = " " + desc[descriptions_keys["text"]] + " " + stat + " [[col:ancillary_rare]]" + stats[stat]+"[[/col]]"
      missileweapon = unit[units_keys['primary_missile_weapon']]
      if unit[units_keys['engine']] != '':
        missileweapon = engine_weapon[unit[units_keys['engine']]]
      if missileweapon != '':
          projectiletext = " ranged:"
          projectileid = weapon_projectile[missileweapon]
          projectilerow = projectiles[projectileid]
          projectiletext += missile_stats(projectilerow, unit)
          if missileweapon in weapon_alt_projectile:
            
            for altprojectileid in weapon_alt_projectile[missileweapon]:
              projectiletext += " ranged ("
              altprojectilerow = projectiles[altprojectileid]
              name = altprojectilerow[projectiles_keys['shot_type']].split("_")[-1]
              if name == 'default':
                name = altprojectileid
              projectiletext += name + "): "
              projectiletext += missile_stats(altprojectilerow, unit)
          desc[descriptions_keys["text"]] += projectiletext
      #desc[descriptions_keys["text"]] += "\\\\n\\\\n" + desc_text
tsv_file.close()

# new units
with open('new_land_units_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_units:
      tsv_writer.writerow(unit)

# new descriptions
with open('new_unit_description_short_texts__.loc.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_descriptions:
      tsv_writer.writerow(unit)

# new description ids
with open('new_unit_description_short_texts_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_unit_description_ids:
      tsv_writer.writerow(unit)