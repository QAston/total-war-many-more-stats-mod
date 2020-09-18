rmdir -Recurse extract
$schema = "three_kingdoms"
mkdir extract
$dbtables = "unit_shield_types_tables", "melee_weapons_tables", "unit_armour_types_tables", "projectiles_tables",
     "special_ability_phase_stat_effects_tables", "special_ability_phase_attribute_effects_tables", "special_ability_phases_tables",
     "projectiles_explosions_tables", "missile_weapons_tables",
     "battlefield_engines_tables", "mounts_tables", "ui_unit_bullet_point_enums_tables", "ui_unit_bullet_point_unit_overrides_tables",
     "land_units_tables", "battle_entities_tables", "main_units_tables", "special_ability_to_special_ability_phase_junctions_tables", 
     "unit_special_abilities_tables", "battle_vortexs_tables", "projectile_bombardments_tables", "land_units_officers_tables",
     "battle_personalities_tables", "land_units_additional_personalities_groups_junctions_tables", "battle_entity_stats_tables",
     "land_unit_articulated_vehicles_tables", "ground_type_to_stat_effects_tables",
     "_kv_morale_tables", "_kv_fatigue_tables", "_kv_rules_tables", "unit_experience_bonuses_tables", "unit_fatigue_effects_tables", "unit_stats_land_experience_bonuses_tables"


..\..\rpfm_cli -v -g $schema -p "G:\Epic\TotalWarSagaTROY\data\data.pack" packfile -E extract dummy db

Foreach ($table in $dbtables) {
   $p = "extract/db/" + $table + "/data__"
   ..\..\rpfm_cli -v -g $schema -p "G:\Epic\TotalWarSagaTROY\data\data.pack" table -e  $p
} 


..\..\rpfm_cli -v -g $schema -p "G:\Epic\TotalWarSagaTROY\data\local_en.pack" packfile -E extract dummy text

$loctables = "ui_unit_bullet_point_enums", "unit_abilities", "land_units", "unit_stat_localisations", "random_localisation_strings", "unit_attributes", "uied_component_texts"

Foreach ($table in $loctables) {
   $p = "extract/text/db/" + $table + ".loc"
   ..\..\rpfm_cli -v -g $schema -p "G:\Epic\TotalWarSagaTROY\data\local_en.pack" table -e  $p
} 
