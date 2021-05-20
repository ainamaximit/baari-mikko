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
-- Name: orders; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.orders (
    user_id integer NOT NULL,
    drink_id integer NOT NULL,
    "timestamp" timestamp without time zone,
    id integer NOT NULL
);


ALTER TABLE public.orders OWNER TO mikko;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO mikko;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


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
    quantity integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.recipes OWNER TO mikko;

--
-- Name: recipes_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_id_seq OWNER TO mikko;

--
-- Name: recipes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: mikko
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name text NOT NULL,
    face bytea NOT NULL,
    img text NOT NULL,
    admin boolean
);


ALTER TABLE public.users OWNER TO mikko;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: mikko
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO mikko;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mikko
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: drinks id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.drinks ALTER COLUMN id SET DEFAULT nextval('public.drinks_id_seq'::regclass);


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: pumps id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.pumps ALTER COLUMN id SET DEFAULT nextval('public.pumps_id_seq'::regclass);


--
-- Name: recipes id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: drinks; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.drinks (id, drink) FROM stdin;
1	Gin Tonic
2	Rommicola
3	Irish Coffee
4	Kelkka
5	Paha
6	Long Island
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
11	Lime mehu
12	Sitruunamehu
13	Tequila
14	Triple sec
15	Jaloviina
16	Absintti
17	Kahvilikööri
18	Omenamehu
19	Vermutti
20	Amaretto
21	Konjakki
22	Karpalomehu
23	Valkoviini
24	Energiajuoma
25	Sokeriliemi
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.orders (user_id, drink_id, "timestamp", id) FROM stdin;
\.


--
-- Data for Name: pumps; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.pumps (id, ingredient_id) FROM stdin;
1	5
2	4
3	3
4	2
5	12
6	25
7	13
8	14
9	9
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.recipes (drink_id, ingredient_id, quantity, id) FROM stdin;
1	5	150	2
2	2	50	3
2	4	150	4
4	10	30	5
4	9	30	6
4	8	140	7
6	13	20	8
6	9	20	9
6	2	20	10
6	14	20	11
6	3	20	12
6	13	40	13
6	25	50	14
6	4	10	15
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: mikko
--

COPY public.users (id, name, face, img, admin) FROM stdin;
16	Joe Biden	\\x8004958b040000000000008c156e756d70792e636f72652e6d756c74696172726179948c0c5f7265636f6e7374727563749493948c056e756d7079948c076e6461727261799493944b0085944301629487945294284b014b80859468038c0564747970659493948c02663894898887945294284b038c013c944e4e4e4affffffff4affffffff4b0074946289420004000000000000346b613f000000c0f23bc73f00000060dae4b63f00000040b2999dbf0000000034eec0bf0000000090c1a43f000000c07d28a1bf000000e089d4b3bf000000403eb6ab3f000000e0e522adbf0000004052f4ce3f0000004091a9abbf00000060d279d0bf00000020da67aabf000000c09a6daf3f00000000a822c03f000000e09721c3bf0000004073c6b0bf0000008035bbc9bf000000002aedafbf00000000da9886bf000000402bfea4bf000000003c8f9a3f00000000289eb2bf000000008c72cabf00000080961fcebf000000603c20a8bf00000080332fbabf000000c07a909cbf00000000cecac4bf00000040ac07b43f0000008088959fbf000000c0427cc2bf000000e0e070aabf00000000aa1da8bf0000008033939ebf000000804ba491bf000000c038f0adbf0000002073d6c03f000000a0cde49a3f00000000f3e6c6bf0000006055acc03f000000007a0b7e3f000000c0b2a1cb3f000000a027ddd23f00000000347275bf000000c0ab26a83f0000008045aab6bf000000400c71c13f00000000eaf3cebf000000c0cdd6ab3f000000c028eaa13f000000005783c53f000000809b8aad3f000000609c3bc23f000000806abbb2bf000000001a7f983f000000400a49c83f0000008014aec9bf000000a00823a33f000000401cd3a93f000000e08c11acbf000000408877a13f00000080a044a6bf00000000e57dbf3f00000040d538bc3f00000000f40584bf00000040f521b7bf00000000ddcac83f00000000e45eb8bf00000040a5debcbf000000c0c8869f3f0000006004f0b0bf000000003059c0bf00000060f174d5bf0000000070ac513f00000040a74dd13f000000202869c13f000000007cf3d2bf000000e0055cb3bf00000040ba4aa7bf000000804c38753f000000c06640a13f000000008815813f000000c0d68fa1bf00000020c786c1bf000000403d1aacbf00000000f4708dbf00000080c032cf3f00000000effebbbf00000000e4d97c3f000000c052a3cc3f000000604e96a83f000000202300c3bf000000804386ac3f000000009a65a2bf000000a08b2bbebf000000601ef08ebf000000a01421bebf00000000f994aabf00000080352b97bf00000020fd52c4bf0000000049cd9ebf00000020bd0ab13f000000e05acbd0bf00000040ccfec43f0000000009078dbf000000c05972b4bf0000004099d5acbf00000080abf3a4bf00000000e67d893f000000c0f2d5b03f000000003352cd3f000000c099ffcfbf00000020c5bcc93f000000400f35cd3f00000000fc7cadbf0000002009cbb33f00000000b2b5883f00000040b40db03f0000008065fda3bf000000402c4ba23f00000080c311b6bf000000405e01c1bf000000001e9d71bf0000008083be95bf00000000e0af833f000000805318b13f947494622e	faces/biden.jpg	t
\.


--
-- Name: drinks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.drinks_id_seq', 5, true);


--
-- Name: ingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.ingredients_id_seq', 24, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.orders_id_seq', 10, true);


--
-- Name: pumps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.pumps_id_seq', 3, true);


--
-- Name: recipes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.recipes_id_seq', 18, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mikko
--

SELECT pg_catalog.setval('public.users_id_seq', 55, true);


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
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: pumps pumps_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.pumps
    ADD CONSTRAINT pumps_pkey PRIMARY KEY (id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- Name: users users_face_key; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_face_key UNIQUE (face);


--
-- Name: users users_img_key; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_img_key UNIQUE (img);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: recipes_index_id; Type: INDEX; Schema: public; Owner: mikko
--

CREATE UNIQUE INDEX recipes_index_id ON public.recipes USING btree (id, drink_id) WHERE (id < 0);


--
-- Name: orders orders_drink_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_drink_id_fkey FOREIGN KEY (drink_id) REFERENCES public.drinks(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mikko
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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

