--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Homebrew)
-- Dumped by pg_dump version 15.12 (Homebrew)

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
-- Name: fmc_question_bank; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.fmc_question_bank (
    id integer NOT NULL,
    level integer NOT NULL,
    question_type character varying NOT NULL,
    question character varying NOT NULL,
    answer character varying NOT NULL,
    explanation character varying NOT NULL,
    image character varying,
    is_exam_ready boolean
);


ALTER TABLE public.fmc_question_bank OWNER TO autodidact;

--
-- Name: fmc_question_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.fmc_question_bank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fmc_question_bank_id_seq OWNER TO autodidact;

--
-- Name: fmc_question_bank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.fmc_question_bank_id_seq OWNED BY public.fmc_question_bank.id;


--
-- Name: generated_problems; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.generated_problems (
    id integer NOT NULL,
    user_name character varying NOT NULL,
    question text NOT NULL,
    answer character varying NOT NULL,
    operation character varying NOT NULL,
    level integer,
    attempted boolean,
    user_answer character varying,
    correct boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.generated_problems OWNER TO autodidact;

--
-- Name: generated_problems_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.generated_problems_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.generated_problems_id_seq OWNER TO autodidact;

--
-- Name: generated_problems_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.generated_problems_id_seq OWNED BY public.generated_problems.id;


--
-- Name: level_attempts; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.level_attempts (
    id integer NOT NULL,
    user_name character varying NOT NULL,
    operation character varying NOT NULL,
    level integer NOT NULL,
    attempt_number integer NOT NULL,
    score integer NOT NULL,
    total_questions integer NOT NULL,
    is_passed boolean,
    "timestamp" timestamp without time zone,
    user_id integer
);


ALTER TABLE public.level_attempts OWNER TO autodidact;

--
-- Name: level_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.level_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.level_attempts_id_seq OWNER TO autodidact;

--
-- Name: level_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.level_attempts_id_seq OWNED BY public.level_attempts.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    question_text character varying(500) NOT NULL,
    option_a character varying(255) NOT NULL,
    option_b character varying(255) NOT NULL,
    option_c character varying(255) NOT NULL,
    option_d character varying(255) NOT NULL,
    option_e character varying(255) NOT NULL,
    correct_answer character varying(5) NOT NULL,
    image_url character varying(500)
);


ALTER TABLE public.questions OWNER TO autodidact;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.questions_id_seq OWNER TO autodidact;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: quiz_responses; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.quiz_responses (
    id integer NOT NULL,
    session_id integer NOT NULL,
    question_index integer NOT NULL,
    selected_answer character varying(10) NOT NULL,
    correct_answer character varying(10) NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.quiz_responses OWNER TO autodidact;

--
-- Name: quiz_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.quiz_responses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quiz_responses_id_seq OWNER TO autodidact;

--
-- Name: quiz_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.quiz_responses_id_seq OWNED BY public.quiz_responses.id;


--
-- Name: quiz_sessions; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.quiz_sessions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    operation character varying(50) NOT NULL,
    level integer NOT NULL,
    session_id character varying(100) NOT NULL,
    question_data json NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.quiz_sessions OWNER TO autodidact;

--
-- Name: quiz_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.quiz_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quiz_sessions_id_seq OWNER TO autodidact;

--
-- Name: quiz_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.quiz_sessions_id_seq OWNED BY public.quiz_sessions.id;


--
-- Name: uploaded_files; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.uploaded_files (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL
);


ALTER TABLE public.uploaded_files OWNER TO autodidact;

--
-- Name: uploaded_files_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.uploaded_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.uploaded_files_id_seq OWNER TO autodidact;

--
-- Name: uploaded_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.uploaded_files_id_seq OWNED BY public.uploaded_files.id;


--
-- Name: user_answers; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.user_answers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    selected_answer character varying(10) NOT NULL,
    correct_answer character varying(10) NOT NULL
);


ALTER TABLE public.user_answers OWNER TO autodidact;

--
-- Name: user_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.user_answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_answers_id_seq OWNER TO autodidact;

--
-- Name: user_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.user_answers_id_seq OWNED BY public.user_answers.id;


--
-- Name: user_progress; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.user_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_name character varying NOT NULL,
    operation character varying NOT NULL,
    level_completed integer NOT NULL,
    dojo_points integer NOT NULL,
    current_level integer,
    total_attempts integer,
    ninja_stars integer DEFAULT 0
);


ALTER TABLE public.user_progress OWNER TO autodidact;

--
-- Name: user_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.user_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_progress_id_seq OWNER TO autodidact;

--
-- Name: user_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.user_progress_id_seq OWNED BY public.user_progress.id;


--
-- Name: user_scores; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.user_scores (
    id integer NOT NULL,
    user_name character varying NOT NULL,
    operation character varying NOT NULL,
    level integer NOT NULL,
    set_number integer,
    score integer NOT NULL,
    total_questions integer NOT NULL,
    is_completed boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.user_scores OWNER TO autodidact;

--
-- Name: user_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.user_scores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_scores_id_seq OWNER TO autodidact;

--
-- Name: user_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.user_scores_id_seq OWNED BY public.user_scores.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: autodidact
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    is_admin boolean,
    is_active boolean,
    ninja_stars integer DEFAULT 0,
    awarded_title character varying DEFAULT 'Beginner'::character varying
);


ALTER TABLE public.users OWNER TO autodidact;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: autodidact
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO autodidact;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autodidact
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: fmc_question_bank id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.fmc_question_bank ALTER COLUMN id SET DEFAULT nextval('public.fmc_question_bank_id_seq'::regclass);


--
-- Name: generated_problems id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.generated_problems ALTER COLUMN id SET DEFAULT nextval('public.generated_problems_id_seq'::regclass);


--
-- Name: level_attempts id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.level_attempts ALTER COLUMN id SET DEFAULT nextval('public.level_attempts_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Name: quiz_responses id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_responses ALTER COLUMN id SET DEFAULT nextval('public.quiz_responses_id_seq'::regclass);


--
-- Name: quiz_sessions id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_sessions ALTER COLUMN id SET DEFAULT nextval('public.quiz_sessions_id_seq'::regclass);


--
-- Name: uploaded_files id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.uploaded_files ALTER COLUMN id SET DEFAULT nextval('public.uploaded_files_id_seq'::regclass);


--
-- Name: user_answers id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_answers ALTER COLUMN id SET DEFAULT nextval('public.user_answers_id_seq'::regclass);


--
-- Name: user_progress id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_progress ALTER COLUMN id SET DEFAULT nextval('public.user_progress_id_seq'::regclass);


--
-- Name: user_scores id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_scores ALTER COLUMN id SET DEFAULT nextval('public.user_scores_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: fmc_question_bank; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.fmc_question_bank (id, level, question_type, question, answer, explanation, image, is_exam_ready) FROM stdin;
\.


--
-- Data for Name: generated_problems; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.generated_problems (id, user_name, question, answer, operation, level, attempted, user_answer, correct, created_at) FROM stdin;
\.


--
-- Data for Name: level_attempts; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.level_attempts (id, user_name, operation, level, attempt_number, score, total_questions, is_passed, "timestamp", user_id) FROM stdin;
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.questions (id, question_text, option_a, option_b, option_c, option_d, option_e, correct_answer, image_url) FROM stdin;
\.


--
-- Data for Name: quiz_responses; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.quiz_responses (id, session_id, question_index, selected_answer, correct_answer, "timestamp") FROM stdin;
\.


--
-- Data for Name: quiz_sessions; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.quiz_sessions (id, user_id, operation, level, session_id, question_data, "timestamp") FROM stdin;
\.


--
-- Data for Name: uploaded_files; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.uploaded_files (id, filename, file_path) FROM stdin;
\.


--
-- Data for Name: user_answers; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.user_answers (id, user_id, question_id, selected_answer, correct_answer) FROM stdin;
\.


--
-- Data for Name: user_progress; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.user_progress (id, user_id, user_name, operation, level_completed, dojo_points, current_level, total_attempts, ninja_stars) FROM stdin;
\.


--
-- Data for Name: user_scores; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.user_scores (id, user_name, operation, level, set_number, score, total_questions, is_completed, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: autodidact
--

COPY public.users (id, username, email, password, created_at, updated_at, is_admin, is_active, ninja_stars, awarded_title) FROM stdin;
1	Jo	mjyothionline@gmail.com	$2b$12$2KGp.37e0xxiSN8794FKDu/O0dvfkbQSZGaSm4UurXGXE.ZSfYYYe	2025-04-21 00:23:52.430204	2025-04-21 00:23:52.430209	f	t	0	Beginner
2	Arjun	arjunm0303@gmail.com	$2b$12$88bn5KvzB2.jwE7kPurH5eFdOOZ0XCqUc8aFzq0F10Hm1noPm0vmm	2025-04-21 19:16:14.654757	2025-04-21 19:16:14.654762	f	t	0	Beginner
\.


--
-- Name: fmc_question_bank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.fmc_question_bank_id_seq', 1, false);


--
-- Name: generated_problems_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.generated_problems_id_seq', 1, false);


--
-- Name: level_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.level_attempts_id_seq', 1, false);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.questions_id_seq', 1, false);


--
-- Name: quiz_responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.quiz_responses_id_seq', 1, false);


--
-- Name: quiz_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.quiz_sessions_id_seq', 1, false);


--
-- Name: uploaded_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.uploaded_files_id_seq', 1, false);


--
-- Name: user_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.user_answers_id_seq', 1, false);


--
-- Name: user_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.user_progress_id_seq', 1, false);


--
-- Name: user_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.user_scores_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autodidact
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: fmc_question_bank fmc_question_bank_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.fmc_question_bank
    ADD CONSTRAINT fmc_question_bank_pkey PRIMARY KEY (id);


--
-- Name: generated_problems generated_problems_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.generated_problems
    ADD CONSTRAINT generated_problems_pkey PRIMARY KEY (id);


--
-- Name: level_attempts level_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.level_attempts
    ADD CONSTRAINT level_attempts_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: quiz_responses quiz_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_pkey PRIMARY KEY (id);


--
-- Name: quiz_sessions quiz_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_sessions
    ADD CONSTRAINT quiz_sessions_pkey PRIMARY KEY (id);


--
-- Name: quiz_sessions quiz_sessions_session_id_key; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_sessions
    ADD CONSTRAINT quiz_sessions_session_id_key UNIQUE (session_id);


--
-- Name: uploaded_files uploaded_files_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.uploaded_files
    ADD CONSTRAINT uploaded_files_pkey PRIMARY KEY (id);


--
-- Name: user_answers user_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_pkey PRIMARY KEY (id);


--
-- Name: user_progress user_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_pkey PRIMARY KEY (id);


--
-- Name: user_scores user_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_scores
    ADD CONSTRAINT user_scores_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_fmc_question_bank_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_fmc_question_bank_id ON public.fmc_question_bank USING btree (id);


--
-- Name: ix_generated_problems_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_generated_problems_id ON public.generated_problems USING btree (id);


--
-- Name: ix_questions_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_questions_id ON public.questions USING btree (id);


--
-- Name: ix_uploaded_files_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_uploaded_files_id ON public.uploaded_files USING btree (id);


--
-- Name: ix_user_answers_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_user_answers_id ON public.user_answers USING btree (id);


--
-- Name: ix_user_progress_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_user_progress_id ON public.user_progress USING btree (id);


--
-- Name: ix_user_scores_id; Type: INDEX; Schema: public; Owner: autodidact
--

CREATE INDEX ix_user_scores_id ON public.user_scores USING btree (id);


--
-- Name: level_attempts level_attempts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.level_attempts
    ADD CONSTRAINT level_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: quiz_responses quiz_responses_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.quiz_sessions(id);


--
-- Name: quiz_sessions quiz_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.quiz_sessions
    ADD CONSTRAINT quiz_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_answers user_answers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_progress user_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autodidact
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

