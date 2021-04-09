$rpfmcli_path="..\..\rpfm_cli"
$twgame="attila"
$twgame_path="G:\Steam\steamapps\common\Total War Attila\"

rmdir -Recurse extract
mkdir extract
$dbtables = "unit_shield_types_tables", "melee_weapons_tables", "unit_armour_types_tables", "projectiles_tables",
     "special_ability_phase_stat_effects_tables",
     "projectiles_explosions_tables", "missile_weapons_tables", "missile_weapons_to_projectiles_tables",
     "battlefield_engines_tables","land_units_tables", "unit_description_short_texts_tables"

& $rpfmcli_path -v -g $twgame -p "$twgame_path\data\data.pack" packfile -E extract dummy db

Start-Sleep -Seconds 10
Foreach ($table in $dbtables) {
   $p = "extract/db/" + $table + "/" + $table.Substring(0, $table.Length-7);
   
   & $rpfmcli_path -v -g $twgame -p  "$twgame_path\data\data.pack" table -e  $p
} 

& $rpfmcli_path -v -g $twgame -p "$twgame_path\data\local_en.pack" packfile -E extract dummy text

$loctables = "land_units", "unit_description_short_texts"

Foreach ($table in $loctables) {
   $p = "extract/text/db/" + $table + ".loc"
   & $rpfmcli_path -v -g $twgame -p "$twgame_path\data\local_en.pack" table -e  $p
} 
