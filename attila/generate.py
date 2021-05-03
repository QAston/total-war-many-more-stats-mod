import csv
import os
import shutil
import subprocess
import argparse
import math

twgame="attila"
extract_path="extract"
output_path="output"
template_path="template"
mod_name="many_more_stats"
install_path=os.path.expanduser("~") + f"/Documents/TWMods/{twgame}/{mod_name}.pack"
twgame_path="C:/Program Files (x86)/Steam/steamapps/common/Total War Attila/"

argparser = argparse.ArgumentParser(description='Generates the mod packfile to Documents/TWMods/')
argparser.add_argument('path_to_rpfm_cli',
                   help='path to rpfm_cli.exe used for extracting and creating mod files')
argparser.add_argument('-g', dest='path_to_game', default=twgame_path,
                   help=f'path to the main directory of {twgame}(default: {twgame_path})')
argparser.add_argument('-i', dest='install_path', default=install_path,
                   help=f'path where to install the mod file (default: {install_path})')

args = argparser.parse_args()

rpfmcli_path=args.path_to_rpfm_cli
twgame_path= args.path_to_game
install_path=args.install_path




def run_rpfm(packfile, *args):
  subprocess.run([rpfmcli_path, "-v", "-g", twgame, "-p", packfile, *args], check=True)

def extract_packfiles():
  shutil.rmtree(extract_path, ignore_errors=True)
  shutil.rmtree(output_path, ignore_errors=True)
  os.makedirs(extract_path, exist_ok=True)
  run_rpfm(f"{twgame_path}/data/data.pack", "packfile", "-E", extract_path, "dummy", "db")
  run_rpfm(f"{twgame_path}/data/local_en.pack", "packfile", "-E", extract_path, "dummy", "text")

def make_package():
  shutil.copytree(template_path, output_path, dirs_exist_ok=True)
  os.makedirs(os.path.dirname(install_path), exist_ok=True)
  try:
    os.remove(install_path)
  except:
    pass
  run_rpfm(install_path, "packfile", "-n")
  for root, dirs, files in os.walk(output_path+"/db", topdown=False):
    relroot = os.path.relpath(root, output_path+"/db")
    for name in files:
      subprocess.run([rpfmcli_path, "-v", "-g", twgame, "-p", install_path, "packfile", "-a", "db" , relroot.replace("\\", "/") + "/"+ name], cwd=output_path+"/db", check=True)
  for root, dirs, files in os.walk(output_path+"/text", topdown=False):
    relroot = os.path.relpath(root, output_path+"/text")
    for name in files:
      subprocess.run([rpfmcli_path, "-v", "-g", twgame, "-p", install_path, "packfile", "-a", "text" , relroot.replace("\\", "/") + "/"+ name], cwd=output_path+"/text", check=True)

  run_rpfm(install_path, "packfile", "-l")
  print(f"Mod package written to: {install_path}")
  

def extract_db_to_tsv(packfile, tablefile):
  run_rpfm(f"{twgame_path}/data/{packfile}", "table", "-e", tablefile)

def pack_tsv_to_db(packfile, tablefile):
  run_rpfm(f"{twgame_path}/data/{packfile}", "table", "-i", tablefile)

class TWDBRow():
  def __init__(self, key_ids, row):
    self.key_ids = key_ids
    self.row = row

  def __getitem__(self, key):
    return self.row[self.key_ids[key]]

  def __setitem__(self, key, value):
    self.row[self.key_ids[key]] = value

  def copy(self):
    return TWDBRow(self.key_ids, self.row.copy())

class TWDBReaderImpl():
  def _read_header(self):
    try:
      self.tsv_file = open(f"{extract_path}/{self.tsvfile}", encoding="utf-8")
    except FileNotFoundError:
      extract_db_to_tsv(self.packfile, f"{extract_path}/{self.tablefile}")
      self.tsv_file = open(f"{extract_path}/{self.tsvfile}", encoding="utf-8")
      
    self.read_tsv = csv.reader(self.tsv_file, delimiter="\t")
    self.head_rows = []
    self.head_rows.append(next(self.read_tsv))
    self.head_rows.append(next(self.read_tsv))
    self.key_ids = {}
    i = 0
    for key in self.head_rows[1]:
        self.key_ids[key] = i
        i = i + 1

  def __enter__(self):
    self._read_header()
    self.rows_iter = map(lambda row: TWDBRow(self.key_ids, row), self.read_tsv)
    return self

  def __exit__(self, exc_type, exc_value, exc_tb):
    self.tsv_file.close()

  def make_writer(self):
    if self.head_rows is None:
      self._read_header()
      self.tsv_file.close()
    outtsvfile = self.tsvfile
    if self.outtsvfile is not None:
      outtsvfile = self.outtsvfile
    return TWDBWriter(self.tablename, self.tablefile, outtsvfile, self.packfile, self.head_rows, self.key_ids)

class TWDBReader(TWDBReaderImpl):
  def __init__(self, tablename):
    self.tablename = tablename
    self.tablefile = "db/" + self.tablename + "/" + self.tablename[0:-7]
    self.tsvfile = self.tablefile + ".tsv"
    self.outtsvfile = None
    self.head_rows = None
    self.packfile = "data.pack"

class TWLocDBReader(TWDBReaderImpl):
  def __init__(self, tablename):
    self.tablename = tablename
    self.tablefile = f"text/db/{self.tablename}.loc"
    self.tsvfile = f"text/db/{self.tablename}.tsv"
    self.outtsvfile = f"text/db/{self.tablename}.loc.tsv"
    self.head_rows = None
    self.packfile = "local_en.pack"

class TWDBWriter():
  def __init__(self, tablename, tablefile, tsvfile, packfile, head_rows, key_ids):
    self.tablename = tablename
    self.tablefile = tablefile
    self.tsvfile = tsvfile
    self.head_rows = head_rows
    self.key_ids = key_ids
    self.new_rows = []
    self.packfile = packfile

  def write(self):
    os.makedirs(os.path.dirname(f"{output_path}/{self.tsvfile}"), exist_ok=True)
    self.tsv_file = open(f"{output_path}/{self.tsvfile}", 'w', newline='', encoding="utf-8")
    self.tsv_writer = csv.writer(self.tsv_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in self.head_rows:
      self.tsv_writer.writerow(row)
    for row in self.new_rows:
      self.tsv_writer.writerow(row.row)
    self.tsv_file.close()
    pack_tsv_to_db(self.packfile,f"{output_path}/{self.tsvfile}")
    os.remove(f"{output_path}/{self.tsvfile}")

  def make_row(self):
    return TWDBRow(self.key_ids, ["" * len(self.head_rows[1])])

def read_to_dict(db_reader, key="key"):
  result = {}
  with db_reader:
    for row in db_reader.rows_iter:
      result[row[key]] = row
  return result

def read_to_dict_of_lists(db_reader, key="key"):
  result = {}
  with db_reader:
    for row in db_reader.rows_iter:
      if row[key] not in result:
        result[row[key]] = []
      result[row[key]].append(row)
  return result

def read_column_to_dict(db_reader, key, column):
  result = {}
  with db_reader:
    for row in db_reader.rows_iter:
      result[row[key]] = row[column]
  return result

def read_column_to_dict_of_lists(db_reader, key, column):
  result = {}
  with db_reader:
    for row in db_reader.rows_iter:
      if row[key] not in result:
        result[row[key]] = []
      result[row[key]].append(row[column])
  return result

extract_packfiles()

# shield
shields = read_column_to_dict(TWDBReader("unit_shield_types_tables"), "key", "missile_block_chance")

# melee
melee = read_to_dict(TWDBReader("melee_weapons_tables"))

# armour
armour = read_to_dict(TWDBReader("unit_armour_types_tables"))

# projectiles
projectiles = read_to_dict(TWDBReader("projectiles_tables"))

# ability phase stats
ability_phase_stats = read_to_dict_of_lists(TWDBReader("special_ability_phase_stat_effects_tables"), "phase")

# mount_to_entity
mount_entity = read_column_to_dict(TWDBReader("mounts_tables"), "key", "entity")

# projectiles_explosions_tables_projectiles_explosions
projectiles_explosions = read_to_dict(TWDBReader("projectiles_explosions_tables"))

# weapon_to_projectile
weapon_projectile = read_column_to_dict(TWDBReader("missile_weapons_tables"), "key", "default_projectile")

# weapon additional projectiles
weapon_alt_projectile = read_column_to_dict_of_lists(TWDBReader("missile_weapons_to_projectiles_tables"), "missile_weapon", "projectile")

# engine_to_weapon
engine_weapon = {}
engine_entity = {}
with TWDBReader("battlefield_engines_tables") as db_reader:
  for row in db_reader.rows_iter:
    engine_weapon[row["key"]] = row["missile_weapon"]
    engine_entity[row["key"]] = row["battle_entity"]

# battle entities
battle_entities = read_to_dict(TWDBReader("battle_entities_tables"))

endl = "\\\\n"

def posstr(stat, indent = 0):
  return indentstr(indent) + "[[col:green]]" + numstr(stat) +"[[/col]]"

def negstr(stat, indent = 0):
  return indentstr(indent) + "[[col:red]]" + numstr(stat) +"[[/col]]"

def indentstr(indent):
  return ("[[col:red]] [[/col]]" * indent)

def modstr(s):
  stat = float(s)
  if stat > 0:
    return posstr(s)
  if stat < 0:
    return negstr(s)
  return statstr(s)

def negmodstr(s):
  stat = float(s)
  if stat < 0:
    return posstr(s)
  if stat > 0:
    return negstr(s)
  return statstr(s)

def difftostr(stat):
  if stat > 0:
    return colstr("+" + numstr(stat), "green")
  if stat < 0:
    return negstr(stat)
  return ""

def negdifftostr(stat):
  if stat > 0:
    return colstr("+" + numstr(stat), "red")
  if stat < 0:
    return posstr(stat)
  return ""

def try_int(val):
  try:
    return int(val, 10)
  except ValueError:
    return val

def try_float(val):
  try:
    return float(val)
  except ValueError:
    return val

def numstr(stat):
  fstat = try_float(stat)
  if type(fstat) != float:
    return str(stat)
  ifstat = round(fstat, 0)
  if ifstat == fstat:
    return str(int(ifstat))
  return str(round(fstat, 2))

def colstr(s, col):
  return "[[col:"+ col + "]]" + s +"[[/col]]"

def statstr(stat):
  return "[[col:yellow]]" + numstr(stat) +"[[/col]]"

def statindent(name, value, indent, fn=statstr):
  return indentstr(indent) + name + " " + fn(value) + endl

# unit descriptions
descriptions_reader = TWLocDBReader("unit_description_short_texts")
descriptions_writer = descriptions_reader.make_writer()

descriptions = {}
with descriptions_reader:
  for row in descriptions_reader.rows_iter:
    descriptions_writer.new_rows.append(row)
    descid = row['key'].replace("unit_description_short_texts_text_", "", 1)
    descriptions[descid] = row

# description id keys
unit_description_id_reader = TWDBReader("unit_description_short_texts_tables")
unit_description_id_writer = unit_description_id_reader.make_writer()
with unit_description_id_reader:
  for row in unit_description_id_reader.rows_iter:
    unit_description_id_writer.new_rows.append(row)

# units
land_units_reader = TWDBReader("land_units_tables")
land_units_writer = land_units_reader.make_writer()

with land_units_reader:
  for row in land_units_reader.rows_iter:
    descid = row['short_description_text']
    unit = row.copy()
    desc = descriptions[descid].copy()
    newdescid = unit['key'] + "_statdesc"
    unit['short_description_text'] = newdescid
    desc['key'] = "unit_description_short_texts_text_" + newdescid
    new_descid_row = unit_description_id_writer.make_row()
    new_descid_row["key"] = newdescid
    unit_description_id_writer.new_rows.append(new_descid_row)
    land_units_writer.new_rows.append(unit)
    descriptions_writer.new_rows.append(desc)

    stats = {}
    desc_text = desc['text']
    desc['text'] = ""

    stats["campaign_range"] = unit['campaign_action_points']
    stats["capture_power"] = unit['capture_power']
    if unit['shield'] != 'none':
      stats["missile_block"] = shields[unit['shield']] + "%"
    
    if unit['primary_melee_weapon'] != '':
        meleeid = unit['primary_melee_weapon']
        meleerow = melee[meleeid]
        if meleerow['armour_piercing'] == 'true':
          stats["melee_wpn_half_enemy_armor_piercing"] = 'true'
        if meleerow['shield_piercing'] == 'true':
          stats["melee_wpn_full_enemy_shield_piercing"] = 'true'
        stats["melee_ap_dmg"] = meleerow['ap_damage']
    if unit['armour'] != '':
        armourid = unit['armour']
        armourrow = armour[armourid]
        if armourrow['weak_vs_missiles'] == '1':
          stats["armour_weak_v_missiles"] = 'true'
        if armourrow['bonus_vs_missiles'] == '1':
          stats["armour_bonus_v_missiles"] = 'true'

    entity = battle_entities[unit['man_entity']]
    charge_speed = float(entity["charge_speed"]) * 10
    speed = float(entity["run_speed"]) * 10
    accel = float(entity["acceleration"])
    mass = float(entity["mass"])
    health = int(entity["hit_points"]) + int(unit['bonus_hit_points'])
    if unit['engine'] != '':
        # speed characteristics are always overridden by engine and mount, even if engine is engine_mounted == false (example: catapult), verified by comparing stats
        engine = battle_entities[engine_entity[unit['engine']]]
        charge_speed = float(engine["charge_speed"]) * 10
        accel = float(engine["acceleration"])
        speed = float(engine["run_speed"]) * 10
        mass += float(engine["mass"])
        health += int(engine["hit_points"])
    if unit['mount'] != '':
        mount = battle_entities[mount_entity[unit['mount']]]
        # both engine and mount present - always chariots
        # verified, mount has higher priority than engine when it comes to determining speed (both increasing and decreasing), by comparing stats of units where speed of mount < or >  engine
        charge_speed = float(mount["charge_speed"]) * 10
        accel = float(mount["acceleration"])
        speed = float(mount["run_speed"]) * 10
        mass += float(mount["mass"])
        health += int(mount["hit_points"])

    stats["charge_speed"] = str(charge_speed)
    stats["acceleration"] = str(accel)
    stats["mass"] = str(mass)

    missileweapon = unit['primary_missile_weapon']
    if unit['engine'] != '':
      missileweapon = engine_weapon[unit['engine']]
    if missileweapon != '':
        stats["accuracy_bonus"] = unit['accuracy']
        stats["reload"] = unit['reload']

    for stat in stats:
        desc['text'] = " " + desc['text'] + " " + stat + " [[col:yellow]]" + stats[stat]+"[[/col]]\\\\n"
    if unit['mount'] != '' and unit['class'] != 'elph':
      dismounteddiff = ""
      md = int(unit['dismounted_melee_defense']) - int(unit['melee_defence'])
      if md != 0:
        dismounteddiff += statindent("melee_def", md, 2, difftostr)
      ma = int(unit['dismounted_melee_attack']) - int(unit['melee_attack'])
      if ma != 0:
        dismounteddiff += statindent("melee_att", ma, 2, difftostr)
      cb = int(unit['dismounted_charge_bonus']) - int(unit['charge_bonus'])
      if cb != 0:
        dismounteddiff += statindent("charge_bonus", cb, 2, difftostr)
      if dismounteddiff != "":
        desc['text'] += "dismounted stats: \\\\n" + dismounteddiff+ "\\\\n"

    if missileweapon != '':
        projectiletext = "default shot:\\\\n"
        projectileid = weapon_projectile[missileweapon]
        projectilerow = projectiles[projectileid]
        projectiletext  += statindent("dmg", projectilerow['damage'], 2)
        projectiletext  += statindent("ap_dmg", projectilerow['ap_damage'], 2)
        projectiletext  += statindent("fire_dmg", projectilerow['fire_damage'], 2)
        projectiletext  += statindent("marksman_bonus", projectilerow['marksmanship_bonus'], 2)
        projectiletext  += statindent("effective_range", projectilerow['effective_range'], 2)
        projectiletext  += statindent("base_reload_time", projectilerow['base_reload_time'], 2)
        if projectilerow['bonus_v_infantry'] != '0':
          projectiletext += statindent("bonus_v_inf", projectilerow['bonus_v_infantry'], 2)
        if projectilerow['bonus_v_cavalry'] != '0':
          projectiletext += statindent("bonus_v_large", projectilerow['bonus_v_cavalry'], 2)
        if projectilerow['explosion_type'] != '':
          explosionrow = projectiles_explosions[projectilerow['explosion_type']]
          projectiletext += statindent("explosion_dmg", explosionrow['detonation_damage'], 2)
          projectiletext += statindent("explosion_radius", explosionrow['detonation_radius'], 2)
        
        debuff = projectilerow['overhead_stat_effect']
        debufftype = "overhead"
        if debuff == '':
          debuff = projectilerow['contact_stat_effect']
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
          for altprojectileid in weapon_alt_projectile[missileweapon]:
            altprojectilerow = projectiles[altprojectileid]
            name = altprojectilerow['shot_type'].split("_")[-1]
            if name == 'default':
              name = altprojectileid
            projectiletext += name + " shot vs default:\\\\n"
            s = int(altprojectilerow['damage']) - int(projectilerow['damage'])
            if s != 0:
              projectiletext  += statindent("dmg", s, 2, difftostr)
            s = int(altprojectilerow['ap_damage']) - int(projectilerow['ap_damage'])
            if s != 0:
              projectiletext  += statindent("ap_dmg", s, 2, difftostr)
            s = float(altprojectilerow['fire_damage']) - float(projectilerow['fire_damage'])
            if s != 0:
              projectiletext  += statindent("fire_dmg", s, 2, difftostr)
            s = float(altprojectilerow['marksmanship_bonus']) - float(projectilerow['marksmanship_bonus'])
            if s != 0:
              projectiletext  += statindent("marksmanship", s, 2, difftostr)
            s = int(altprojectilerow['bonus_v_infantry']) - int(projectilerow['bonus_v_infantry'])
            if s != 0:
              projectiletext  += statindent("bonus_v_inf", s, 2, difftostr)
            s = int(altprojectilerow['bonus_v_cavalry']) - int(projectilerow['bonus_v_cavalry'])
            if s != 0:
              projectiletext  += statindent("bonus_v_cav", s, 2, difftostr)
            s = int(altprojectilerow['effective_range']) - int(projectilerow['effective_range'])
            if s != 0:
              projectiletext  += statindent("range", s, 2, difftostr)
            s = float(altprojectilerow['base_reload_time']) - float(projectilerow['base_reload_time'])
            if s != 0:
              projectiletext  += statindent("base_reload_time", s, 2, negdifftostr)
            s = float(altprojectilerow['calibration_area']) - float(projectilerow['calibration_area'])
            if s != 0:
              projectiletext  += statindent("calibration_area", s, 2, negdifftostr)
            if altprojectilerow['explosion_type'] != '':
              explosionrow = projectiles_explosions[altprojectilerow['explosion_type']]
              projectiletext += statindent("explosion_dmg", explosionrow['detonation_damage'], 2)
              projectiletext += statindent("explosion_radius", explosionrow['detonation_radius'], 2)

            debuff = altprojectilerow['overhead_stat_effect']
            debufftype = "overhead"
            if debuff == '':
              debuff = altprojectilerow['contact_stat_effect']
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
        desc['text'] += projectiletext
    desc['text'] += "\\\\n\\\\n" + desc_text

land_units_writer.write()
unit_description_id_writer.write()
descriptions_writer.write()

kv_rules = read_column_to_dict(TWDBReader("_kv_rules_tables"), "key", "value")

kv_fatigue = read_column_to_dict(TWDBReader("_kv_fatigue_tables"), "key", "value")

kv_morale = read_column_to_dict(TWDBReader("_kv_morale_tables"), "key", "value")

fatigue_order = ["active", "winded", "tired", "very_tired", "exhausted"]


fatigue_effects = {}
with TWDBReader("unit_fatigue_effects_tables") as db_reader:
  for row in db_reader.rows_iter:
    key = row["fatigue_level"].replace("threshold_", "", 1)
    stat = row["stat"].replace("scalar_", "", 1).replace("stat_", "", 1)
    if key not in fatigue_effects:
      fatigue_effects[key] = {}
    fatigue_effects[key][stat] = row["value"]

prev_level = {}
for fatigue_level in fatigue_order:
  for stat in prev_level:
    if stat not in fatigue_effects[fatigue_level]:
      fatigue_effects[fatigue_level][stat] = prev_level[stat]
  prev_level = fatigue_effects[fatigue_level]

xp_bonuses = {}
with TWDBReader("unit_experience_bonuses_tables") as db_reader:
  for row in db_reader.rows_iter:
    key = row["stat"].replace("stat_", "", 1)
    xp_bonuses[key] = row

rank_bonuses = {}
with TWDBReader("unit_stats_land_experience_bonuses_tables") as db_reader:
  for row in db_reader.rows_iter:
    key = row["xp_level"]
    #rank_fatigue_bonus[key] = row["fatigue"]
    result = {}
    rank = int(key)
    result["fatigue"] = row["fatigue"]
    result["melee_attack"] = row["melee_attack"]
    result["melee_defence"] = row["melee_defense"]
    result["reloading"] = row["core_reloading_skill"]
    result["morale"] = row["morale"]
    result["marksmanship"] = row["core_marksmanship"]
    for bonus_stat in xp_bonuses:
      stat_row = xp_bonuses[bonus_stat]
      growth_rate = float(stat_row["growth_rate"])
      growth_scalar = float(stat_row["growth_scalar"])
      value = round(growth_scalar * rank)
      if value > 0:
        result[bonus_stat] = str(float(result[bonus_stat]) + value)
    rank_bonuses[key] = result

# stat descriptions
with TWLocDBReader("ui_unit_stats") as db_reader:
  db_writer = db_reader.make_writer()
  for newrow in db_reader.rows_iter:
    db_writer.new_rows.append(newrow)
    newtext = ""
    key = newrow["key"]
    stats = {}
    if key == "ui_unit_stats_tooltip_text_stat_melee_attack":
      newtext += "|| Melee hit pct chance formula: " + statstr(kv_rules["melee_hit_chance_base"]) + " + melee_attack - enemy_melee_def, clamp (min: " + statstr(kv_rules["melee_hit_chance_min"]) + " max: " + statstr(kv_rules["melee_hit_chance_max"])  + ")" 
    if key == "ui_unit_stats_tooltip_text_stat_melee_defence":
      stats["melee_defence_direction_penalty_coefficient_flank"] = kv_rules["melee_defence_direction_penalty_coefficient_flank"]
      stats["melee_defence_direction_penalty_coefficient_rear"] = kv_rules["melee_defence_direction_penalty_coefficient_rear"]
    if key == "ui_unit_stats_tooltip_text_stat_armour":
      newtext += "||Armour non-ap-dmg-reduction formula: rand(0.5,1) * armour"
    if key == "ui_unit_stats_tooltip_text_stat_weapon_damage":
      newtext += "|| Terrain height difference dmg mod max: +/-" + statstr(float(kv_rules["melee_height_damage_modifier_max_coefficient"]) * 100) + "% at diff of +/- " + statstr(kv_rules["melee_height_damage_modifier_max_difference"]) + "m, linearly decreasing to 0"
    if key == "ui_unit_stats_tooltip_text_stat_charge_bonus":
      newtext += "|| Charge bonus lasts for " + statstr(kv_rules["charge_cool_down_time"] + "s") + " after first contact, linearly going down to 0. \\\\n"
      newtext += "Charge bonus is added to melee_attack and weapon_damage. Weapon_damage increase is split between ap and base dmg using the ap/base dmg ratio before the bonus.\\\\n"
      newtext += " || Bracing: \\\\n"
      newtext += indentstr(2) + "bracing is a multiplier (clamped to " +statstr(kv_rules["bracing_max_multiplier_clamp"]) + ") to the mass of the charged unit for comparison vs a charging one\\\\n"
      newtext += indentstr(2) + "to brace the unit must stand still in formation (exact time to get in formation varies) and not attack/fire\\\\n"           
      newtext += indentstr(2) + "bracing from ranks: 1: " + statstr(1.0) + " ranks 2-" + statstr(kv_rules["bracing_calibration_ranks"]) + " add " + statstr((float(kv_rules["bracing_calibration_ranks_multiplier"]) - 1) / (float(kv_rules["bracing_calibration_ranks"])  - 1)) + "\\\\n"
    if key == "ui_unit_stats_tooltip_text_stat_missile_strength":
      newtext += "|| Terrain height difference dmg mod max: +/-" + statstr(float(kv_rules["missile_height_damage_modifier_max_coefficient"]) * 100) + "% at diff of +/- " + kv_rules["missile_height_damage_modifier_max_difference"] + "m, linearly decreasing to 0||"
    if key == "ui_unit_stats_tooltip_text_scalar_missile_range":
      newtext += "|| \\\\nHit chance when shooting targets hiding in forests/scrub:" + statstr((1 - float(kv_rules["missile_target_in_cover_penalty"]))  * 100) + '\\\\n'
      newtext += "Friendly fire uses bigger hitboxes than enemy fire: height *= " + statstr(kv_rules["projectile_friendly_fire_man_height_coefficient"]) + " radius *= " + statstr(kv_rules["projectile_friendly_fire_man_radius_coefficient"]) + "\\\\n" 
      newtext += "Units with " + statstr("dual") + " trajectory will switch their aim to high if "+ statstr(float(kv_rules["unit_firing_line_of_sight_considered_obstructed_ratio"]) * 100) + "% of LOS is obstructed \\\\n"
      newtext += "Projectiles with high velocity and low aim are much better at hitting moving enemies."
      # todo: things like missile penetration, lethality seem to contradict other stat descriptions but don't seem obsolete as they weren't there in shogun2
      # need to do more testing before adding them in
    if key == "ui_unit_stats_tooltip_text_scalar_speed":
      newtext += "|| Fatigue effects: \\\\n"
      for fatigue_level in fatigue_order:
        newtext += fatigue_level + ": "
        for stat in fatigue_effects[fatigue_level]:
          newtext += " " + stat_icon[stat] + "" + statstr(float(fatigue_effects[fatigue_level][stat]) * 100) + "%"
        newtext += "\\\\n"
      newtext += " || Tiring/Resting: \\\\n"
      kvfatiguevals = ["charging", "climbing_ladders", "combat", "gradient_shallow_movement_multiplier", "gradient_steep_movement_multiplier", "gradient_very_steep_movement_multiplier",
      "idle", "limbering", "ready", "running", "running_cavalry", "running_artillery_horse", "shooting", "walking", "walking_artillery", "walking_horse_artillery"]
      for kvfatval in kvfatiguevals:
        newtext += kvfatval + " " + negmodstr(kv_fatigue[kvfatval]) + "\\\\n"
    
    if key == "ui_unit_stats_tooltip_text_stat_morale":
      # push the tooltip to be wider
      moraletext = "Morale mechanics: || ____________________________________________ \\\\n"
      moraletext += "total_hp_loss:" + "\\\\n"
      moraletext += indentstr(2) + "10%:" + modstr(kv_morale["total_casualties_penalty_10"]) + " 20%:" + modstr(kv_morale["total_casualties_penalty_20"]) + " 30%:" + modstr(kv_morale["total_casualties_penalty_30"]) + "\\\\n"
      moraletext += indentstr(2) + "40%:" + modstr(kv_morale["total_casualties_penalty_40"]) + " 50%:" + modstr(kv_morale["total_casualties_penalty_50"]) + " 60%:" + modstr(kv_morale["total_casualties_penalty_60"]) + "\\\\n"
      moraletext += indentstr(2) +  " 70%:" + modstr(kv_morale["total_casualties_penalty_70"]) + " 80%:" + modstr(kv_morale["total_casualties_penalty_80"]) + " 90%:" + modstr(kv_morale["total_casualties_penalty_90"]) + "\\\\n"
      moraletext += "60s_hp_loss:" + "\\\\n"
      moraletext += indentstr(2) + " 10%:" + modstr(kv_morale["extended_casualties_penalty_10"]) + " 15%:" + modstr(kv_morale["extended_casualties_penalty_15"]) + " 33%:" + modstr(kv_morale["extended_casualties_penalty_33"]) + "\\\\n"
      moraletext += indentstr(2) +  " 50%:" + modstr(kv_morale["extended_casualties_penalty_50"])  + " 80%:" + modstr(kv_morale["extended_casualties_penalty_80"]) + "\\\\n"
      # set to 0
      #moraletext += "4s_hp_loss:" + " 6%:" + modstr(kv_morale["recent_casualties_penalty_6"]) + " 10%:" + modstr(kv_morale["recent_casualties_penalty_10"]) + " 15%:" + modstr(kv_morale["recent_casualties_penalty_15"]) + "\\\\n"
      #moraletext += indentstr(2) +  " 33%:" + modstr(kv_morale["recent_casualties_penalty_33"]) + " 50%:" + modstr(kv_morale["recent_casualties_penalty_50"]) + "\\\\n"
      moraletext += "winning combat:" + " " + modstr(kv_morale["winning_combat"])  + " significantly " + modstr(kv_morale["winning_combat_significantly"]) + "\\\\n"  # set to 0 +  " slightly " + modstr(kv_morale["winning_combat_slightly"]) +"\\\\n"
      moraletext += "losing combat:" + " " + modstr(kv_morale["losing_combat"]) + " significantly " + modstr(kv_morale["losing_combat_significantly"]) + "\\\\n"
      moraletext += "charging: " + modstr(kv_morale["charge_bonus"]) + " timeout " + statstr(float(kv_morale["charge_timeout"]) / 10) +"s\\\\n"
      moraletext += "attacked in the flank " + modstr(kv_morale["was_attacked_in_flank"]) +"\\\\n"
      moraletext += "attacked in the rear " + modstr(kv_morale["was_attacked_in_rear"]) +"\\\\n"
      # set to 0
      #moraletext += "high ground vs all enemies " + modstr(kv_morale["ume_encouraged_on_the_hill"]) + "\\\\n"
      #moraletext += "defending walled nonbreached settlement " + modstr(kv_morale["ume_encouraged_fortification"]) + "\\\\n"
      moraletext += "defending on a plaza " + modstr(kv_morale["ume_encouraged_settlement_plaza"]) + "\\\\n"
      # set to 0
      #moraletext += "artillery:" + " hit " + modstr(kv_morale["ume_concerned_damaged_by_artillery"]) + " near miss (<="+ statstr(math.sqrt(float(kv_morale["artillery_near_miss_distance_squared"])))+") " + modstr(kv_morale["ume_concerned_attacked_by_artillery"]) + "\\\\n"
      #moraletext += "projectile hit" + modstr(kv_morale["ume_concerned_attacked_by_projectile"]) + "\\\\n"
      # set to 0
      #moraletext += "vigor: " + colstr("very_tired ", "fatigue_very_tired") + " " + modstr(kv_morale["ume_concerned_very_tired"])  + colstr(" exhausted ", "fatigue_exhausted") + modstr(kv_morale["ume_concerned_exhausted"]) + '\\\\n'
      moraletext += "army loses: " + modstr(kv_morale["ume_concerned_army_destruction"]) + ", conditions: \\\\n"
      moraletext += indentstr(2) +" power lost: " + statstr((1 - float(kv_morale["army_destruction_alliance_strength_ratio"])) * 100) + "% and balance is " + statstr((1.0 / float(kv_morale["army_destruction_enemy_strength_ratio"])) * 100) + '%\\\\n'
      moraletext += "general's death: " +  modstr(kv_morale["ume_concerned_general_dead"]) + " recently(60s?) " + modstr(kv_morale["ume_concerned_general_died_recently"]) + "\\\\n"
      # set to 0
      # moraletext += "surprise enemy discovery: " +  modstr(kv_morale["ume_concerned_surprised"]) + " timeout " + statstr(float(kv_morale["surprise_timeout"]) / 10) +"s\\\\n"
      # set to 0
      #moraletext += "flanks: " + "secure " + modstr(kv_morale["ume_encouraged_flanks_secure"]) + " 1_exposed " + modstr(kv_morale["ume_concerned_flanks_exposed_single"]) + " 2_exposed " + modstr(kv_morale["ume_concerned_flanks_exposed_multiple"]) + " range " + statstr(kv_morale["open_flanks_effect_range"]) + 'm\\\\n'
      moraletext += "routing balance: (" + statstr(kv_morale["routing_unit_effect_distance_flank"]) + "m in front/flanks)" + "\\\\n" 
      moraletext += indentstr(2) + "negative: (allies-enemies, clamp " + negstr(kv_morale["max_routing_friends_to_consider"]) + ")*" + negstr(kv_morale["routing_friends_effect_weighting"]) + "\\\\n"
      moraletext += indentstr(2) + "positive: (enemies-allies, clamp " + posstr(kv_morale["max_routing_enemies_to_consider"]) + ")*" + posstr(kv_morale["routing_enemies_effect_weighting"])+ '\\\\n'
      moraletext += "wavering:" + " " + statstr(kv_morale["ums_wavering_threshold_lower"])  + "-" + statstr(kv_morale["ums_wavering_threshold_upper"]) + "\\\\n"
      moraletext += indentstr(2) + "must spend " + statstr(float(kv_morale["waver_base_timeout"]) / 10)  + "s wavering before routing\\\\n"
      moraletext += "broken:" + " " + statstr(kv_morale["ums_broken_threshold_lower"]) + "-" + statstr(kv_morale["ums_broken_threshold_upper"]) + "\\\\n"
      moraletext += indentstr(2) + "can rally after " + statstr(float(kv_morale["broken_finish_base_timeout"]) / 10) + "s - level * " + statstr(float(kv_morale["broken_finish_timer_experience_bonus"]) / 10) + "s\\\\n"
      moraletext += indentstr(2) + "immune to rout for " + statstr(float(kv_morale["post_rally_no_rout_timer"])) + "s after rallying" + "\\\\n"
      #moraletext += indentstr(2) + "won't rally if enemies within? "  + statstr(kv_morale["enemy_effect_range"]) + "m" + "\\\\n"
      moraletext += indentstr(2) + "max rally countd "  + statstr(float(kv_morale["shatter_after_rout_count"]) - 1) + "\\\\n"
      moraletext += indentstr(2) + "1st rout shatter due to "  + statstr((1-float(kv_morale["shatter_after_first_rout_if_casulties_higher_than"])) * 100 )  + "% hp loss" + "\\\\n"
      moraletext += indentstr(2) + "2nd rout shatter due to "  + statstr((1-float(kv_morale["shatter_after_second_rout_if_casulties_higher_than"])) * 100 )  + "% hp loss" + "\\\\n"
      moraletext += "shock-rout: last 4s hp loss >=" + statstr(kv_morale["recent_casualties_shock_threshold"]) + "% and morale < 0"
      newrow["text"] = moraletext
    
    # todo: more kv_rules values: missile, collision, etc
    for s in stats:
      newtext += "\\\\n" + s + ": " + statstr(stats[s])
    newrow["text"] += newtext
  db_writer.write()

# misc strings
with TWLocDBReader("uied_component_texts") as db_reader:
  db_writer = db_reader.make_writer()
  for newrow in db_reader.rows_iter:
    db_writer.new_rows.append(newrow)
    newtext = ""
    key = newrow["key"]
    stat = {}

    if key == "uied_component_texts_localised_string_experience_tx_Tooltip_5c0016":
      newtext += "|| XP bonus to stats: "
      for stat in rank_bonuses["1"]:
        newtext += stat + " "
      newtext += "||"
      for rank in range(1, 10):
        #newtext += rank_icon(rank)
        newtext += "rank "+ str(rank) + ": "
        stats = rank_bonuses[str(rank)]
        for stat in stats:
          newtext += statstr(stats[stat]) + " " #stat_icon[stat] + " " + stats[stat] + " "
        newtext += "\\\\n"
    newrow["text"] += newtext
  db_writer.write()

make_package()