SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: conferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conferences (
    id integer NOT NULL,
    conference_id integer NOT NULL,
    name character varying(100) NOT NULL,
    link character varying(100) NOT NULL,
    abbreviation character varying(1) NOT NULL,
    active boolean NOT NULL
);


--
-- Name: divisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.divisions (
    id integer NOT NULL,
    division_id integer NOT NULL,
    name character varying(100) NOT NULL,
    abbreviation character varying(5) NOT NULL,
    link character varying(100) NOT NULL,
    active boolean NOT NULL,
    conference_id integer NOT NULL
);


--
-- Name: links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.links (
    link_id integer NOT NULL,
    team_id integer NOT NULL,
    hashtag character varying(100) NOT NULL,
    instagram_link character varying(100) NOT NULL,
    twitter_link character varying(100) NOT NULL
);


--
-- Name: players; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.players (
    id integer NOT NULL,
    team_id integer NOT NULL,
    player_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    role character varying(100) NOT NULL
);


--
-- Name: rosters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rosters (
    roster_id integer NOT NULL,
    team_id integer NOT NULL,
    season integer NOT NULL,
    player_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    jersey_number integer NOT NULL,
    "position" character varying(100) NOT NULL,
    position_code character varying(3) NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(128) NOT NULL
);


--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    team_id integer NOT NULL,
    name character varying(100) NOT NULL
);


--
-- Name: teams_info; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams_info (
    id integer NOT NULL,
    team_id integer NOT NULL,
    name character varying(100) NOT NULL,
    abbreviation character varying(3) NOT NULL,
    location character varying(100) NOT NULL,
    inaugaration_year integer NOT NULL,
    url character varying(100) NOT NULL,
    venue character varying(100) NOT NULL,
    division_id integer NOT NULL,
    conference_id integer NOT NULL
);


--
-- Name: teams_ranks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams_ranks (
    id integer NOT NULL,
    team_id integer NOT NULL,
    season integer NOT NULL,
    games_won character varying(10) NOT NULL,
    games_lost character varying(10) NOT NULL,
    games_lost_ot character varying(10) NOT NULL,
    points character varying(10) NOT NULL,
    points_pct character varying(10) NOT NULL,
    goals_per_game character varying(10) NOT NULL,
    goals_against_per_game character varying(10) NOT NULL,
    ev_gga_ratio character varying(10) NOT NULL,
    powerplay_pct character varying(10) NOT NULL,
    powerplay_goals character varying(10) NOT NULL,
    powerplay_goals_against character varying(10) NOT NULL,
    powerplay_opportunities character varying(10) NOT NULL,
    penaltykill_pct character varying(10) NOT NULL,
    shots_per_game character varying(10) NOT NULL,
    shots_allowed character varying(10) NOT NULL,
    win_when_score_first character varying(10) NOT NULL,
    win_when_opp_score_first character varying(10) NOT NULL,
    win_when_leading_first_per character varying(10) NOT NULL,
    win_when_leading_second_per character varying(10) NOT NULL,
    win_when_outshooting_opp character varying(10) NOT NULL,
    win_when_opp_outshooting character varying(10) NOT NULL,
    faceoffs_taken character varying(10) NOT NULL,
    faceoffs_won character varying(10) NOT NULL,
    faceoffs_lost character varying(10) NOT NULL,
    faceoff_win_pct character varying(10) NOT NULL,
    save_pct character varying(10) NOT NULL,
    shooting_pct character varying(10) NOT NULL
);


--
-- Name: teams_stats; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams_stats (
    id integer NOT NULL,
    team_id integer NOT NULL,
    season integer NOT NULL,
    games_played integer NOT NULL,
    games_won integer NOT NULL,
    games_lost integer NOT NULL,
    games_lost_ot integer NOT NULL,
    points integer NOT NULL,
    points_pct real NOT NULL,
    goals_per_game real NOT NULL,
    goals_against_per_game real NOT NULL,
    ev_gga_ratio real NOT NULL,
    powerplay_pct real NOT NULL,
    powerplay_goals real NOT NULL,
    powerplay_goals_against real NOT NULL,
    powerplay_opportunities real NOT NULL,
    penaltykill_pct real NOT NULL,
    shots_per_game real NOT NULL,
    shots_allowed real NOT NULL,
    win_when_score_first real NOT NULL,
    win_when_opp_score_first real NOT NULL,
    win_when_leading_first_per real NOT NULL,
    win_when_leading_second_per real NOT NULL,
    win_when_outshooting_opp real NOT NULL,
    win_when_opp_outshooting real NOT NULL,
    faceoffs_taken real NOT NULL,
    faceoffs_won real NOT NULL,
    faceoffs_lost real NOT NULL,
    faceoff_win_pct real NOT NULL,
    shooting_pct real NOT NULL,
    save_pct real NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL
);


--
-- Name: conferences conferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conferences
    ADD CONSTRAINT conferences_pkey PRIMARY KEY (conference_id);


--
-- Name: divisions divisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.divisions
    ADD CONSTRAINT divisions_pkey PRIMARY KEY (division_id);


--
-- Name: links links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.links
    ADD CONSTRAINT links_pkey PRIMARY KEY (link_id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);


--
-- Name: rosters rosters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rosters
    ADD CONSTRAINT rosters_pkey PRIMARY KEY (roster_id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: teams_info teams_info_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_info
    ADD CONSTRAINT teams_info_pkey PRIMARY KEY (id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);


--
-- Name: teams_ranks teams_ranks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_ranks
    ADD CONSTRAINT teams_ranks_pkey PRIMARY KEY (id);


--
-- Name: teams_stats teams_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_stats
    ADD CONSTRAINT teams_stats_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: divisions fk_conference; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.divisions
    ADD CONSTRAINT fk_conference FOREIGN KEY (conference_id) REFERENCES public.conferences(conference_id);


--
-- Name: teams_info fk_conference; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_info
    ADD CONSTRAINT fk_conference FOREIGN KEY (conference_id) REFERENCES public.conferences(conference_id);


--
-- Name: teams_info fk_division; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_info
    ADD CONSTRAINT fk_division FOREIGN KEY (division_id) REFERENCES public.divisions(division_id);


--
-- Name: rosters fk_player; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rosters
    ADD CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players(player_id);


--
-- Name: teams_info fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_info
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: teams_stats fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_stats
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: teams_ranks fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams_ranks
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: players fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: rosters fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rosters
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: links fk_team; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.links
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

