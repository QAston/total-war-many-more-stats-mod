import csv
import os
import shutil
import subprocess
import argparse

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
      if key not in result:
        result[key] = []
      result[key].append(row)
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
      if key not in result:
        result[key] = []
      result[key].append(row[column])
  return result

extract_packfiles()

# shield
shields_reader = TWDBReader("unit_shield_types_tables")
shields = read_column_to_dict(shields_reader, "key", "missile_block_chance")

# melee
melee_reader = TWDBReader("melee_weapons_tables")
melee = read_to_dict(melee_reader)

# armour
armour_reader = TWDBReader("unit_armour_types_tables")
armour = read_to_dict(armour_reader)

# projectiles
projectiles_reader = TWDBReader("projectiles_tables")
projectiles = read_to_dict(projectiles_reader)

# ability phase stats
ability_phase_stats_reader = TWDBReader("special_ability_phase_stat_effects_tables")
ability_phase_stats = read_to_dict_of_lists(ability_phase_stats_reader, "phase")


# projectiles_explosions_tables_projectiles_explosions
projectiles_explosions_reader = TWDBReader("projectiles_explosions_tables")
projectiles_explosions = read_to_dict(projectiles_explosions_reader)

# weapon_to_projectile
weapon_projectile_reader = TWDBReader("missile_weapons_tables")
weapon_projectile = read_column_to_dict(weapon_projectile_reader, "key", "default_projectile")

# weapon additional projectiles
weapon_alt_projectile_reader = TWDBReader("missile_weapons_to_projectiles_tables")
weapon_alt_projectile = read_column_to_dict_of_lists(weapon_alt_projectile_reader, "missile_weapon", "projectile")

# engine_to_weapon
engine_weapon_reader = TWDBReader("battlefield_engines_tables")
engine_weapon = read_column_to_dict(engine_weapon_reader, "key", "missile_weapon")

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
    missileweapon = unit['primary_missile_weapon']
    if unit['engine'] != '':
      missileweapon = engine_weapon[unit['engine']]
    if missileweapon != '':
        stats["accuracy"] = unit['accuracy']
        stats["reload"] = unit['reload']

    for stat in stats:
        desc['text'] = " " + desc['text'] + " " + stat + " [[col:yellow]]" + stats[stat]+"[[/col]]\\\\n"
    if unit['mount'] != '' and unit['class'] != 'elph':
      dismounteddiff = ""
      md = int(unit['dismounted_melee_defense']) - int(unit['melee_defence'])
      if md != 0:
        dismounteddiff += " melee_def " + difftostr(md)
      ma = int(unit['dismounted_melee_attack']) - int(unit['melee_attack'])
      if ma != 0:
        dismounteddiff += " melee_att " + difftostr(ma)
      cb = int(unit['dismounted_charge_bonus']) - int(unit['charge_bonus'])
      if cb != 0:
        dismounteddiff += " charge_bonus " + difftostr(cb)
      if dismounteddiff != "":
        desc['text'] += " dismounted stats: " + dismounteddiff+ ";"

    if missileweapon != '':
        projectiletext = " default shot:\\\\n"
        projectileid = weapon_projectile[missileweapon]
        projectilerow = projectiles[projectileid]
        projectiletext += " ap_dmg " + statstr(projectilerow['ap_damage'])
        projectiletext += " marksmanship " + statstr(projectilerow['marksmanship_bonus'])
        if projectilerow['bonus_v_infantry'] != '0':
          projectiletext += " bonus_v_inf " + statstr(projectilerow['bonus_v_infantry'])
        if projectilerow['bonus_v_cavalry'] != '0':
          projectiletext += " bonus_v_large " + statstr(projectilerow['bonus_v_cavalry'])
        if projectilerow['explosion_type'] != '':
          explosionrow = projectiles_explosions[projectilerow['explosion_type']]
          projectiletext += " explosion_dmg " + statstr(explosionrow['detonation_damage'])
          projectiletext += " explosion_radius " + statstr(explosionrow['detonation_radius'])
        
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
          projectiletext += "\\\\n alt shot: "
          for altprojectileid in weapon_alt_projectile[missileweapon]:
            altprojectilerow = projectiles[altprojectileid]
            name = altprojectilerow['shot_type'].split("_")[-1]
            if name == 'default':
              name = altprojectileid
            projectiletext += name + ": \\\\n"
            s = int(altprojectilerow['damage']) - int(projectilerow['damage'])
            if s != 0:
              projectiletext += " dmg " + difftostr(s)
            s = int(altprojectilerow['ap_damage']) - int(projectilerow['ap_damage'])
            if s != 0:
              projectiletext += " ap_dmg " + difftostr(s)
            s = float(altprojectilerow['marksmanship_bonus']) - float(projectilerow['marksmanship_bonus'])
            if s != 0:
              projectiletext += " marksmanship " + difftostr(s)
            s = int(altprojectilerow['bonus_v_infantry']) - int(projectilerow['bonus_v_infantry'])
            if s != 0:
              projectiletext += " bonus_v_inf " + difftostr(s)
            s = int(altprojectilerow['bonus_v_cavalry']) - int(projectilerow['bonus_v_cavalry'])
            if s != 0:
              projectiletext += " bonus_v_cav " + difftostr(s)
            s = int(altprojectilerow['effective_range']) - int(projectilerow['effective_range'])
            if s != 0:
              projectiletext += " range " + difftostr(s)
            s = float(altprojectilerow['base_reload_time']) - float(projectilerow['base_reload_time'])
            if s != 0:
              projectiletext += " base_reload_time " + negdifftostr(s)
            s = float(altprojectilerow['calibration_area']) - float(projectilerow['calibration_area'])
            if s != 0:
              projectiletext += " calibration_area " + negdifftostr(s)
            if altprojectilerow['explosion_type'] != '':
              explosionrow = projectiles_explosions[altprojectilerow['explosion_type']]
              projectiletext += " explosion_dmg " + statstr(explosionrow['detonation_damage'])
              projectiletext += " explosion_radius " + statstr(explosionrow['detonation_radius'])

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

make_package()