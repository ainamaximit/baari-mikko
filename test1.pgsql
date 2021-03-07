--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

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
-- Name: drinks; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.drinks (
    id integer NOT NULL,
    drink character varying(50) NOT NULL
);


ALTER TABLE public.drinks OWNER TO mikko;

--
-- Name: drinks_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.drinks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.drinks_id_seq OWNER TO mikko;

--
-- Name: drinks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.drinks_id_seq OWNED BY public.drinks.id;


--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.ingredients (
    id integer NOT NULL,
    ingredient character varying(50) NOT NULL
);


ALTER TABLE public.ingredients OWNER TO mikko;

--
-- Name: ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredients_id_seq OWNER TO mikko;

--
-- Name: ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;


--
-- Name: pumps; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.pumps (
    id integer NOT NULL,
    ingredient_id integer
);


ALTER TABLE public.pumps OWNER TO mikko;

--
-- Name: pumps_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.pumps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pumps_id_seq OWNER TO mikko;

--
-- Name: pumps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.pumps_id_seq OWNED BY public.pumps.id;


--
-- Name: recipes; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.recipes (
    drink_id integer,
    ingredient_id integer,
    quantity real NOT NULL
);


ALTER TABLE public.recipes OWNER TO mikko;

--
-- Name: drinks id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.drinks ALTER COLUMN id SET DEFAULT nextval('public.drinks_id_seq'::regclass);


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: pumps id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.pumps ALTER COLUMN id SET DEFAULT nextval('public.pumps_id_seq'::regclass);


--
-- Data for Name: drinks; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.drinks (id, drink) FROM stdin;
1	Gin Tonic
2	Rommicola
3	Irish Coffee
4	Kelkka
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.ingredients (id, ingredient) FROM stdin;
1	Kahvi
2	Rommi
3	Gin
4	Cola
5	Tonic Water
6	Vesi
7	Viski
8	Appelsiinimehu
9	Vodka
10	Passoa
\.


--
-- Data for Name: pumps; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.pumps (id, ingredient_id) FROM stdin;
1	1
2	2
3	3
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.recipes (drink_id, ingredient_id, quantity) FROM stdin;
1	1	40
1	2	40
2	3	80
2	3	80
2	1	40
3	6	40
3	7	40
3	1	40
4	9	20
4	10	20
4	8	120
\.


--
-- Name: drinks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.drinks_id_seq', 4, true);


--
-- Name: ingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.ingredients_id_seq', 10, true);


--
-- Name: pumps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.pumps_id_seq', 3, true);


--
-- Name: drinks drinks_drink_key; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.drinks
    ADD CONSTRAINT drinks_drink_key UNIQUE (drink);


--
-- Name: drinks drinks_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.drinks
    ADD CONSTRAINT drinks_pkey PRIMARY KEY (id);


--
-- Name: ingredients ingredients_ingredient_key; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_ingredient_key UNIQUE (ingredient);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- Name: pumps pumps_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.pumps
    ADD CONSTRAINT pumps_pkey PRIMARY KEY (id);


--
-- Name: pumps pumps_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.pumps
    ADD CONSTRAINT pumps_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id) ON DELETE CASCADE;


--
-- Name: recipes recipe_drink_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipe_drink_id_fkey FOREIGN KEY (drink_id) REFERENCES public.drinks(id) ON DELETE CASCADE;


--
-- Name: recipes recipe_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipe_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

