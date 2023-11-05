--- CREATING DATABASE;

CREATE DATABASE statchekapi;

--- CREATING TABLES;

CREATE TABLE conferences (
    ID int NOT NULL,
    name varchar(100) NOT NULL,
    link varchar(100) NOT NULL,
    abbreviation varchar(1) NOT NULL,
    active bool NOT NULL,
    PRIMARY KEY(ID)
);

CREATE TABLE divisions (
    ID int NOT NULL,
    name varchar(100) NOT NULL,
    abbreviation varchar(5) NOT NULL,
    link varchar(100) NOT NULL,
    active bool NOT NULL,
    conference_id int NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT fk_conference
        FOREIGN KEY (conference_id)
            REFERENCES conferences(ID)
);

CREATE TABLE teams (
    ID int NOT NULL,
    team_id int NOT NULL,
    name varchar(100) NOT NULL,
    PRIMARY KEY(team_id)
);

CREATE TABLE teams_info (
    ID int NOT NULL,
    team_id int NOT NULL,
    name varchar(100) NOT NULL,
    abbreviation varchar(3) NOT NULL,
    location varchar(100) NOT NULL,
    inaugaration_year int NOT NULL,
    url varchar(100) NOT NuLL,
    venue varchar(100) NOT NULL,
    division_id int NOT NULL,
    conference_id int NOT NULL,
    PRIMARY KEY (ID),
    CONSTRAINT fk_team
        FOREIGN KEY (team_id) 
            REFERENCES teams(team_id),
    CONSTRAINT fk_division
        FOREIGN KEY (division_id) 
            REFERENCES divisions(ID),
    CONSTRAINT fk_conference
        FOREIGN KEY (conference_id) 
            REFERENCES conferences(ID)
);

CREATE TABLE teams_stats (
    ID int NOT NULL,
    team_id int NOT NULL,
    season int NOT NULL,
    games_played int NOT NULL,
    games_won int NOT NULL,
    games_lost int NOT NULL,
    games_lost_ot int NOT NULL,
    points int NOT NULL,
    points_pct float(5) NOT NULL,
    goals_per_game float(5) NOT NULL,
    goals_against_per_game float(5) NOT NULL,
    ev_gga_ratio float(5) NOT NULL,
    powerplay_pct float(5) NOT NULL,
    powerplay_goals float(5) NOT NULL,
    powerplay_goals_against float(5) NOT NULL,
    powerplay_opportunities float(5) NOT NULL,
    penaltykill_pct float(5) NOT NULL,
    shots_per_game float(5) NOT NULL,
    shots_allowed float(5) NOT NULL,
    win_when_score_first float(5) NOT NULL,
    win_when_opp_score_first float(5) NOT NULL,
    win_when_leading_first_per float(5) NOT NULL,
    win_when_leading_second_per float(5) NOT NULL,
    win_when_outshooting_opp float(5) NOT NULL,
    win_when_opp_outshooting float(5) NOT NULL,
    faceoffs_taken float(5) NOT NULL,
    faceoffs_won float(5) NOT NULL,
    faceoffs_lost float(5) NOT NULL,
    faceoff_win_pct float(5) NOT NULL,
    shooting_pct float(5) NOT NULL,
    save_pct float(5) NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT fk_team  
        FOREIGN KEY(team_id)
            REFERENCES teams(team_id)
);

CREATE TABLE teams_ranks(
    ID int NOT NULL,
    team_id int NOT NULL,
    season int NOT NULL,
    games_won varchar(10) NOT NULL,
    games_lost varchar(10) NOT NULL,
    games_lost_ot varchar(10) NOT NULL,
    points varchar(10) NOT NULL,
    points_pct varchar(10) NOT NULL,
    goals_per_game varchar(10) NOT NULL,
    goals_against_per_game varchar(10) NOT NULL,
    ev_gga_ratio varchar(10) NOT NULL,
    powerplay_pct varchar(10) NOT NULL,
    powerplay_goals varchar(10) NOT NULL,
    powerplay_goals_against varchar(10) NOT NULL,
    powerplay_opportunities varchar(10) NOT NULL,
    penaltykill_pct varchar(10) NOT NULL,
    shots_per_game varchar(10) NOT NULL,
    shots_allowed varchar(10) NOT NULL,
    win_when_score_first varchar(10) NOT NULL,
    win_when_opp_score_first varchar(10) NOT NULL,
    win_when_leading_first_per varchar(10) NOT NULL,
    win_when_leading_second_per varchar(10) NOT NULL,
    win_when_outshooting_opp varchar(10) NOT NULL,
    win_when_opp_outshooting varchar(10) NOT NULL,
    faceoffs_taken varchar(10) NOT NULL,
    faceoffs_won varchar(10) NOT NULL,
    faceoffs_lost varchar(10) NOT NULL,
    faceoff_win_pct varchar(10) NOT NULL,
    save_pct varchar(10) NOT NULL,
    shooting_pct varchar(10) NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT fk_team
        FOREIGN KEY(team_id)
            REFERENCES teams(team_id)
);

CREATE TABLE players(
    ID int NOT NULL,
    team_id int NOT NULL,
    player_id int NOT NULL,
    full_name varchar(100) NOT NULL,
    role varchar(100) NOT NULL,
    PRIMARY KEY (player_id),
    CONSTRAINT fk_team
    FOREIGN KEY (team_id) 
        REFERENCES teams(team_id)
);

CREATE TABLE rosters(
    roster_id int NOT NULL,
    team_id int NOT NULL,
    season int NOT NULL,
    player_id int NOT NULL,
    full_name varchar(100) NOT NULL,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    jersey_number int NOT NULL,
    position varchar(100) NOT NULL,
    position_code varchar(3) NOT NULL,
    PRIMARY KEY(roster_id),
    CONSTRAINT fk_team 
        FOREIGN KEY (team_id)
            REFERENCES teams(team_id),
    CONSTRAINT fk_player
    FOREIGN KEY (player_id) 
        REFERENCES players(player_id)
);

CREATE TABLE links(
    link_id int NOT NULL,
    team_id int NOT NULL,
    hashtag varchar(100) NOT NULL,
    instagram_link varchar(100) NOT NULL,
    twitter_link varchar(100) NOT NULL,
    PRIMARY KEY (link_id),
    CONSTRAINT fk_team
        FOREIGN KEY (team_id)
            REFERENCES teams(team_id)
);

CREATE TABLE users(
    user_id varchar(100) NOT NULL UNIQUE,
    email varchar(100) NOT NULL UNIQUE,
    password varchar(100) NOT NULL,
    created_at timestamptz NOT NULL 
        DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY(user_id)
);