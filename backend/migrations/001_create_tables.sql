-- =============================================================================
-- Startup Funding Intelligence Platform — Database Schema
-- Run this migration in the Supabase SQL Editor
-- =============================================================================

-- -------------------------------------------------------------------------
-- Table: startups
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS startups (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    startup_name    TEXT NOT NULL,
    industry        TEXT NOT NULL,
    location        TEXT NOT NULL,
    founded_year    INT NOT NULL,
    team_size       INT DEFAULT 1,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- -------------------------------------------------------------------------
-- Table: investors
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS investors (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    investor_name   TEXT NOT NULL,
    investor_type   TEXT NOT NULL,       -- e.g. 'VC', 'Angel', 'Corporate', 'Accelerator'
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- -------------------------------------------------------------------------
-- Table: funding_rounds
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS funding_rounds (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    startup_id      UUID NOT NULL REFERENCES startups(id) ON DELETE CASCADE,
    funding_amount  NUMERIC(15,2) NOT NULL DEFAULT 0,
    funding_round   TEXT NOT NULL,       -- e.g. 'Seed', 'Series A', 'Series B', 'Series C'
    investor_count  INT DEFAULT 0,
    date            DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- -------------------------------------------------------------------------
-- Table: startup_investors (many-to-many join)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS startup_investors (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    startup_id      UUID NOT NULL REFERENCES startups(id) ON DELETE CASCADE,
    investor_id     UUID NOT NULL REFERENCES investors(id) ON DELETE CASCADE,
    funding_round_id UUID REFERENCES funding_rounds(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE(startup_id, investor_id, funding_round_id)
);

-- -------------------------------------------------------------------------
-- Indexes for query performance
-- -------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_startups_industry ON startups(industry);
CREATE INDEX IF NOT EXISTS idx_startups_location ON startups(location);
CREATE INDEX IF NOT EXISTS idx_funding_rounds_startup ON funding_rounds(startup_id);
CREATE INDEX IF NOT EXISTS idx_funding_rounds_date ON funding_rounds(date);
CREATE INDEX IF NOT EXISTS idx_startup_investors_startup ON startup_investors(startup_id);
CREATE INDEX IF NOT EXISTS idx_startup_investors_investor ON startup_investors(investor_id);

-- -------------------------------------------------------------------------
-- Enable Row Level Security (recommended for Supabase)
-- -------------------------------------------------------------------------
ALTER TABLE startups ENABLE ROW LEVEL SECURITY;
ALTER TABLE investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding_rounds ENABLE ROW LEVEL SECURITY;
ALTER TABLE startup_investors ENABLE ROW LEVEL SECURITY;

-- Allow anonymous read access (for the frontend dashboard)
CREATE POLICY "Allow anonymous read on startups"
    ON startups FOR SELECT
    USING (true);

CREATE POLICY "Allow anonymous read on investors"
    ON investors FOR SELECT
    USING (true);

CREATE POLICY "Allow anonymous read on funding_rounds"
    ON funding_rounds FOR SELECT
    USING (true);

CREATE POLICY "Allow anonymous read on startup_investors"
    ON startup_investors FOR SELECT
    USING (true);

-- Allow service-role insert/update (for backend scraping/seeding)
CREATE POLICY "Allow service role insert on startups"
    ON startups FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role insert on investors"
    ON investors FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role insert on funding_rounds"
    ON funding_rounds FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role insert on startup_investors"
    ON startup_investors FOR INSERT
    WITH CHECK (true);
