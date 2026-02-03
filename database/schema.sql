-- ==========================================================
-- Database: personal_fitness_ml
-- Schema version: 1
-- Description: Personal fitness tracking for ML experiments
-- ==========================================================

-- ==========================================================
-- Table: activities
-- Description:
--   Catalog of activity types (run, walk, gym, trail, etc.)
-- ==========================================================

CREATE TABLE IF NOT EXISTS activities (
    activity_id           INTEGER PRIMARY KEY,
    activity_name         TEXT    NOT NULL UNIQUE,
    -- e.g. "run", "walk", "gym", "trail"
    activity_description  TEXT,
    -- optional longer description, e.g. "Outdoor running"
    is_active             INTEGER NOT NULL DEFAULT 1
    -- 1 = active activity type, 0 = inactive
);

-- Suggested initial rows (run this after creating the table if quiser):
-- INSERT INTO activities (activity_name, activity_description) VALUES
--   ('run',   'Running'),
--   ('walk',  'Walking'),
--   ('gym',   'Strength training / gym'),
--   ('trail', 'Motorcycle trail / enduro');


-- ==========================================================
-- Table: workout_sessions
-- Description:
--   One row per workout session, any activity type.
--   Some columns are general, others are specific to
--   certain activities (run/walk/trail/gym).
--   Score columns use a 1–5 scale.
-- ==========================================================

CREATE TABLE IF NOT EXISTS workout_sessions (
    -- Identification
    session_id              INTEGER PRIMARY KEY,
    activity_id             INTEGER NOT NULL,
    -- FK -> activities.activity_id (type of activity: run, walk, gym, trail)

    -- Date / basic info
    session_date            TEXT    NOT NULL,
    -- Date of the session in ISO format: "YYYY-MM-DD"
    duration_hhmm           TEXT    NOT NULL,
    -- Total duration of the session in "HH:MM" format, e.g. "00:45", "01:30"
    duration_minutes        REAL    NOT NULL,
    -- Total duration of the session in minutes (numeric), e.g. 45.0, 90.0
    day_of_week             INTEGER NOT NULL,
    -- Day of week as integer, e.g. 0=Monday, 6=Sunday (choose convention and keep consistent)

    notes                   TEXT,
    -- Optional free text notes about the session

    -- General context (valid for any activity)
    sleep_quality_score     INTEGER,
    -- 1–5 score: quality of the previous night's sleep (1 = very bad, 5 = very good)
    meal_before             TEXT,
    -- Description of pre-workout meal, e.g. "fasting", "light", "heavy"
    temperature_celsius     REAL,
    -- Approximate ambient temperature during the workout
    avg_heart_rate_bpm      REAL,
    -- Average heart rate in beats per minute (can be NULL, e.g. on trail without watch)
    effort_score            INTEGER,
    -- 1–5 score: how hard the workout felt (1 = very easy, 5 = extremely hard)
    post_workout_score      INTEGER,
    -- 1–5 score: how you feel after the workout (1 = very bad, 5 = excellent)

    -- Distance-based metrics (run/walk/trail)
    distance_km             REAL,
    -- Distance covered in kilometers (applies to run/walk/trail; can be NULL for gym)
    avg_pace_min_per_km     REAL,
    -- Average pace in minutes per kilometer, e.g. 5.30 = 5 min 18 s per km (main evolution metric for running)

    -- Trail-specific scores (all 1–5)
    trail_fatigue_score     INTEGER,
    -- 1–5 score: how tired you feel after the trail (1 = not tired, 5 = extremely tired)
    trail_safety_score      INTEGER,
    -- 1–5 score: how safe/confident you felt during the trail (1 = very unsafe, 5 = very safe)
    trail_overall_score     INTEGER,
    -- 1–5 score: overall experience of the trail (1 = terrible, 5 = amazing)

    -- Gym-specific metrics
    gym_plan_type           TEXT,
    -- Identifier for gym workout plan, e.g. "A", "B", "C" (leg day, upper body, etc.)
    gym_total_weight_kg     REAL,
    -- Total weight lifted in kg in this session (sum of sets * reps * weight)

    -- Foreign keys
    FOREIGN KEY (activity_id) REFERENCES activities (activity_id)
);
