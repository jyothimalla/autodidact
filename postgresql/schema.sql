PGPASSWORD=OYBt6lZP8dnllu4EP3yhRHZ4JAdQD38I psql -h dpg-cvqfpj3ipnbc73crtsm0-a.oregon-postgres.render.com -U autodidact_user autodidact_db

-- Table: generated_problems
CREATE TABLE IF NOT EXISTS generated_problems (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    operation TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    attempted BOOLEAN DEFAULT FALSE,
    user_answer TEXT,
    correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: user_scores
CREATE TABLE IF NOT EXISTS user_scores (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    level INTEGER NOT NULL,
    set_number INTEGER NOT NULL DEFAULT 1, -- ✅ New
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,    -- ✅ New
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS generated_problems (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    operation TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    attempted BOOLEAN DEFAULT FALSE,
    user_answer TEXT,
    correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    level_completed INTEGER NOT NULL,
    dojo_points INTEGER NOT NULL
);

