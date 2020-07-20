import csv

# shield
tsv_file = open("unit_shield_types_tables_unit_shield_types.tsv")

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
tsv_file = open("melee_weapons_tables_melee_weapons.tsv")

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
tsv_file = open("unit_armour_types_tables_unit_armour_types.tsv")

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
tsv_file = open("projectiles_tables_projectiles.tsv")

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
tsv_file = open("special_ability_phase_stat_effects_tables_special_ability_phase_stat_effects.tsv")

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
tsv_file = open("projectiles_explosions_tables_projectiles_explosions.tsv")

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
tsv_file = open("missile_weapons_tables_missile_weapons.tsv")

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
tsv_file = open("missile_weapons_to_projectiles_tables_missile_weapons_to_projectiles.tsv")

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
tsv_file = open("battlefield_engines_tables_battlefield_engines.tsv")

read_tsv = csv.reader(tsv_file, delimiter="\t")
engine_weapon = {}

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
  return "[[col:yellow]]" + str(stat) +"[[/col]]"

# unit descriptions
tsv_file = open("unit_description_short_texts.loc.tsv")
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
tsv_file = open("unit_description_short_texts_tables_unit_description_short_texts.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_description_ids = []
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  #if rowid <= 2:
  new_unit_description_ids.append(row)

# units
tsv_file = open("land_units_tables_land_units.tsv")
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

      stats["health"] = str(100 + int(unit[units_keys['bonus_hit_points']]))
      stats["campaign_range"] = unit[units_keys['campaign_action_points']]
      if unit[units_keys['shield']] != 'none':
        stats["missile_block"] = shields[unit[units_keys['shield']]] + "%"
      if unit[units_keys['primary_melee_weapon']] != '':
          meleeid = unit[units_keys['primary_melee_weapon']]
          meleerow = melee[meleeid]
          if meleerow[melee_keys['armour_piercing']] == 'true':
            stats["melee_wpn_half_enemy_armor_piercing"] = 'true'
          if meleerow[melee_keys['shield_piercing']] == 'true':
            stats["melee_wpn_full_enemy_shield_piercing"] = 'true'
          stats["melee_ap_dmg"] = meleerow[melee_keys['ap_damage']]
      if unit[units_keys['armour']] != '':
          armourid = unit[units_keys['armour']]
          armourrow = armour[armourid]
          if armourrow[armour_keys['weak_vs_missiles']] == '1':
            stats["armour_weak_v_missiles"] = 'true'
          if armourrow[armour_keys['bonus_vs_missiles']] == '1':
            stats["armour_bonus_v_missiles"] = 'true'
      missileweapon = unit[units_keys['primary_missile_weapon']]
      if unit[units_keys['engine']] != '':
        missileweapon = engine_weapon[unit[units_keys['engine']]]
      if missileweapon != '':
          stats["accuracy"] = unit[units_keys['accuracy']]
          stats["reload"] = unit[units_keys['reload']]

      for stat in stats:
          desc[descriptions_keys["text"]] = " " + desc[descriptions_keys["text"]] + " " + stat + " [[col:yellow]]" + stats[stat]+"[[/col]]\\\\n"
      if unit[units_keys['mount']] != '' and unit[units_keys['class']] != 'elph':
        dismounteddiff = ""
        md = int(unit[units_keys['dismounted_melee_defense']]) - int(unit[units_keys['melee_defence']])
        if md != 0:
          dismounteddiff += " melee_def " + difftostr(md)
        ma = int(unit[units_keys['dismounted_melee_attack']]) - int(unit[units_keys['melee_attack']])
        if ma != 0:
          dismounteddiff += " melee_att " + difftostr(ma)
        cb = int(unit[units_keys['dismounted_charge_bonus']]) - int(unit[units_keys['charge_bonus']])
        if cb != 0:
          dismounteddiff += " charge_bonus " + difftostr(cb)
        if dismounteddiff != "":
          desc[descriptions_keys["text"]] += " dismounted stats: " + dismounteddiff+ ";"

      if missileweapon != '':
          projectiletext = " default shot:\\\\n"
          projectileid = weapon_projectile[missileweapon]
          projectilerow = projectiles[projectileid]
          projectiletext += " ap_dmg " + statstr(projectilerow[projectiles_keys['ap_damage']])
          projectiletext += " marksmanship " + statstr(projectilerow[projectiles_keys['marksmanship_bonus']])
          if projectilerow[projectiles_keys['bonus_v_infantry']] != '0':
            projectiletext += " bonus_v_inf " + statstr(projectilerow[projectiles_keys['bonus_v_infantry']])
          if projectilerow[projectiles_keys['bonus_v_cavalry']] != '0':
            projectiletext += " bonus_v_large " + statstr(projectilerow[projectiles_keys['bonus_v_cavalry']])
          if projectilerow[projectiles_keys['explosion_type']] != '':
            explosionrow = projectiles_explosions[projectilerow[projectiles_keys['explosion_type']]]
            projectiletext += " explosion_dmg " + statstr(explosionrow[projectiles_explosions_keys['detonation_damage']])
            projectiletext += " explosion_radius " + statstr(explosionrow[projectiles_explosions_keys['detonation_radius']])
          
          debuff = projectilerow[projectiles_keys['overhead_stat_effect']]
          debufftype = "overhead"
          if debuff == '':
            debuff = projectilerow[projectiles_keys['contact_stat_effect']]
            debufftype = "contact"
          #if debuff != '':
            # effects = ability_phase_stats[debuff]
            # projectiletext += " " + debufftype + " debuff ("
            # for effect in effects:
            #   how = "*" if effect[ability_phase_stats_keys["how"]] == 'mult' else '+'
            #   if how == '+' and float(effect[ability_phase_stats_keys["value"]]) < 0:
            #     how = ""
            #   projectiletext += effect[ability_phase_stats_keys["stat"]] + " " + statstr(how + effect[ability_phase_stats_keys["value"]]) + " "
            # projectiletext += ")"
          #projectiletext += "; "
          if missileweapon in weapon_alt_projectile:
            projectiletext += "\\\\n alt shot: "
            for altprojectileid in weapon_alt_projectile[missileweapon]:
              altprojectilerow = projectiles[altprojectileid]
              name = altprojectilerow[projectiles_keys['shot_type']].split("_")[-1]
              if name == 'default':
                name = altprojectileid
              projectiletext += name + ": \\\\n"
              s = int(altprojectilerow[projectiles_keys['damage']]) - int(projectilerow[projectiles_keys['damage']])
              if s != 0:
                projectiletext += " dmg " + difftostr(s)
              s = int(altprojectilerow[projectiles_keys['ap_damage']]) - int(projectilerow[projectiles_keys['ap_damage']])
              if s != 0:
                projectiletext += " ap_dmg " + difftostr(s)
              s = float(altprojectilerow[projectiles_keys['marksmanship_bonus']]) - float(projectilerow[projectiles_keys['marksmanship_bonus']])
              if s != 0:
                projectiletext += " marksmanship " + difftostr(s)
              s = int(altprojectilerow[projectiles_keys['bonus_v_infantry']]) - int(projectilerow[projectiles_keys['bonus_v_infantry']])
              if s != 0:
                projectiletext += " bonus_v_inf " + difftostr(s)
              s = int(altprojectilerow[projectiles_keys['bonus_v_cavalry']]) - int(projectilerow[projectiles_keys['bonus_v_cavalry']])
              if s != 0:
                projectiletext += " bonus_v_cav " + difftostr(s)
              s = int(altprojectilerow[projectiles_keys['effective_range']]) - int(projectilerow[projectiles_keys['effective_range']])
              if s != 0:
                projectiletext += " range " + difftostr(s)
              s = float(altprojectilerow[projectiles_keys['base_reload_time']]) - float(projectilerow[projectiles_keys['base_reload_time']])
              if s != 0:
                projectiletext += " base_reload_time " + negdifftostr(s)
              s = float(altprojectilerow[projectiles_keys['calibration_area']]) - float(projectilerow[projectiles_keys['calibration_area']])
              if s != 0:
                projectiletext += " calibration_area " + negdifftostr(s)
              if altprojectilerow[projectiles_keys['explosion_type']] != '':
                explosionrow = projectiles_explosions[altprojectilerow[projectiles_keys['explosion_type']]]
                projectiletext += " explosion_dmg " + statstr(explosionrow[projectiles_explosions_keys['detonation_damage']])
                projectiletext += " explosion_radius " + statstr(explosionrow[projectiles_explosions_keys['detonation_radius']])

              debuff = altprojectilerow[projectiles_keys['overhead_stat_effect']]
              debufftype = "overhead"
              if debuff == '':
                debuff = altprojectilerow[projectiles_keys['contact_stat_effect']]
                debufftype = "contact"
              #if debuff != '':
                # effects = ability_phase_stats[debuff]
                # projectiletext += " " + debufftype + " debuff ("
                # for effect in effects:
                #   how = "*" if effect[ability_phase_stats_keys["how"]] == 'mult' else '+'
                #   if how == '+' and float(effect[ability_phase_stats_keys["value"]]) < 0:
                #     how = ""
                #   projectiletext += effect[ability_phase_stats_keys["stat"]] + " " + statstr(how + effect[ability_phase_stats_keys["value"]]) + " "
                # projectiletext += ")"
              #projectiletext += "; "
          desc[descriptions_keys["text"]] += projectiletext
      desc[descriptions_keys["text"]] += "\\\\n\\\\n" + desc_text
tsv_file.close()

# new units
with open('new_land_units_tables_land_units.tsv', 'w', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_units:
      tsv_writer.writerow(unit)

# new descriptions
with open('new_unit_description_short_texts.loc.tsv', 'w', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_descriptions:
      tsv_writer.writerow(unit)

# new description ids
with open('new_unit_description_short_texts_tables_unit_description_short_texts.tsv', 'w', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for unit in new_unit_description_ids:
      tsv_writer.writerow(unit)