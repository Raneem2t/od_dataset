--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

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
-- Name: datasets; Type: TABLE; Schema: public; Owner: raneem
--

CREATE TABLE public.datasets (
    id integer NOT NULL,
    title text,
    description text,
    keywords text[],
    source_url text,
    organization text,
    publication_date timestamp without time zone,
    last_modified_date timestamp without time zone,
    format text[],
    license text,
    source_platform text,
    raw_id text,
    author text,
    maintainer text,
    download_url text[],
    groups text[],
    code text,
    data_availability text,
    metadata_availability text,
    concepts text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.datasets OWNER TO raneem;

--
-- Name: datasets_id_seq; Type: SEQUENCE; Schema: public; Owner: raneem
--

CREATE SEQUENCE public.datasets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasets_id_seq OWNER TO raneem;

--
-- Name: datasets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raneem
--

ALTER SEQUENCE public.datasets_id_seq OWNED BY public.datasets.id;


--
-- Name: en_datasets; Type: TABLE; Schema: public; Owner: raneem
--

CREATE TABLE public.en_datasets (
    id integer DEFAULT nextval('public.datasets_id_seq'::regclass) NOT NULL,
    title text,
    description text,
    keywords text[],
    source_url text,
    organization text,
    publication_date timestamp without time zone,
    last_modified_date timestamp without time zone,
    format text[],
    license text,
    source_platform text,
    raw_id text,
    author text,
    maintainer text,
    download_url text[],
    groups text[],
    code text,
    data_availability text,
    metadata_availability text,
    concepts text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    title_en text,
    description_en text,
    detected_language text
);


ALTER TABLE public.en_datasets OWNER TO raneem;

--
-- Name: datasets id; Type: DEFAULT; Schema: public; Owner: raneem
--

ALTER TABLE ONLY public.datasets ALTER COLUMN id SET DEFAULT nextval('public.datasets_id_seq'::regclass);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: raneem
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- Name: datasets datasets_source_url_key; Type: CONSTRAINT; Schema: public; Owner: raneem
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_source_url_key UNIQUE (source_url);


--
-- Name: en_datasets en_datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: raneem
--

ALTER TABLE ONLY public.en_datasets
    ADD CONSTRAINT en_datasets_pkey PRIMARY KEY (id);


--
-- Name: en_datasets en_datasets_source_url_key; Type: CONSTRAINT; Schema: public; Owner: raneem
--

ALTER TABLE ONLY public.en_datasets
    ADD CONSTRAINT en_datasets_source_url_key UNIQUE (source_url);


--
-- Name: en_datasets_source_platform_idx; Type: INDEX; Schema: public; Owner: raneem
--

CREATE INDEX en_datasets_source_platform_idx ON public.en_datasets USING btree (source_platform);


--
-- Name: en_datasets_source_url_idx; Type: INDEX; Schema: public; Owner: raneem
--

CREATE INDEX en_datasets_source_url_idx ON public.en_datasets USING btree (source_url);


--
-- Name: idx_datasets_source_platform; Type: INDEX; Schema: public; Owner: raneem
--

CREATE INDEX idx_datasets_source_platform ON public.datasets USING btree (source_platform);


--
-- Name: idx_datasets_source_url; Type: INDEX; Schema: public; Owner: raneem
--

CREATE INDEX idx_datasets_source_url ON public.datasets USING btree (source_url);


--
-- PostgreSQL database dump complete
--

