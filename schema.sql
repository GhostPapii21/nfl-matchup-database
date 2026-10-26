CREATE TABLE espn_boxscores(game_id TEXT PRIMARY KEY,week INTEGER,source_url TEXT,retrieved_at TEXT,raw_path TEXT,data TEXT);

CREATE TABLE external_fetches(fetch_id TEXT PRIMARY KEY,source_id TEXT,source_url TEXT,retrieved_at TEXT,source_updated_at TEXT,status TEXT,raw_hash TEXT,raw_path TEXT,detail TEXT);

CREATE TABLE external_gaps(gap_id TEXT PRIMARY KEY,source_id TEXT,observed_at TEXT,reason TEXT,data TEXT);

CREATE TABLE external_observations(observation_id TEXT PRIMARY KEY,source_id TEXT,team_id TEXT,player_id TEXT,game_id TEXT,metric TEXT,value REAL,source_updated_at TEXT,data TEXT);

CREATE TABLE external_profile_links(game_id TEXT,team TEXT,side TEXT,observation_id TEXT REFERENCES external_observations(observation_id),relation TEXT,PRIMARY KEY(game_id,team,side,observation_id));

CREATE TABLE external_rosters(team_id TEXT,player_id TEXT,name TEXT,position TEXT,retrieved_at TEXT,PRIMARY KEY(team_id,player_id));

CREATE TABLE games(game_id TEXT PRIMARY KEY,date TEXT,status TEXT,data TEXT);

CREATE TABLE historical_game_audits(game_id TEXT PRIMARY KEY,week INTEGER,source_play_count INTEGER,stored_play_count INTEGER,player_stat_rows INTEGER,boxscore_teams INTEGER,raw_path TEXT,status TEXT);

CREATE TABLE ngs_carry_charts(season INTEGER,week INTEGER,ngs_esb_id TEXT,position TEXT,game_id TEXT,team_id TEXT,espn_player_id TEXT,source_url TEXT,image_path TEXT,data TEXT,PRIMARY KEY(season,week,ngs_esb_id));

CREATE TABLE ngs_carry_visual_notes(season INTEGER,week INTEGER,ngs_esb_id TEXT,data TEXT,PRIMARY KEY(season,week,ngs_esb_id));

CREATE TABLE ngs_route_charts(season INTEGER,week INTEGER,ngs_esb_id TEXT,game_id TEXT,team_id TEXT,espn_player_id TEXT,source_url TEXT,image_path TEXT,data TEXT,PRIMARY KEY(season,week,ngs_esb_id));

CREATE TABLE player_stats(game_id TEXT,team TEXT,player_id TEXT,player TEXT,category TEXT,data TEXT,PRIMARY KEY(game_id,team,player_id,category));

CREATE TABLE plays(game_id TEXT,play_id TEXT,offense_id TEXT,down INTEGER,distance INTEGER,play_type TEXT,yards REAL,data TEXT,PRIMARY KEY(game_id,play_id));

CREATE TABLE profiles(game_id TEXT,team TEXT,side TEXT,data TEXT,PRIMARY KEY(game_id,team,side));

CREATE TABLE supplemental_play_links(record_id TEXT PRIMARY KEY,game_id TEXT,play_id TEXT);

CREATE TABLE supplemental_records(record_id TEXT PRIMARY KEY,dataset TEXT,game_id TEXT,team_id TEXT,player_id TEXT,week INTEGER,source_url TEXT,retrieved_at TEXT,asset_updated_at TEXT,data TEXT);

CREATE VIEW profiles_with_external AS SELECT p.game_id,p.team,p.side,p.data AS profile_json,l.observation_id,l.relation,o.metric,o.value,o.data AS evidence_json FROM profiles p LEFT JOIN external_profile_links l ON p.game_id=l.game_id AND p.team=l.team AND p.side=l.side LEFT JOIN external_observations o USING(observation_id);
