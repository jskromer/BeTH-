-- Berkeley Event Value Twin - minimum viable schema (concept section 8)
-- PostgreSQL / PostGIS. Twelve tables; every dashboard result is reproducible
-- from these rows with no hidden spreadsheet cells.
--
-- PostGIS is optional for the first release (only the spatial columns need it).
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Editable scenarios (the five the model opens with, plus any user copies)
CREATE TABLE event_scenarios (
    id              TEXT PRIMARY KEY,
    label           TEXT NOT NULL,
    attendance      INTEGER NOT NULL,
    event_days      SMALLINT NOT NULL,
    one_day         BOOLEAN NOT NULL DEFAULT FALSE,
    parking_price   NUMERIC(8,2) NOT NULL DEFAULT 0,
    sponsorship     NUMERIC(12,2) NOT NULL DEFAULT 0,
    transit_service TEXT NOT NULL DEFAULT 'regular',   -- none | regular | event_plus
    note            TEXT
);

-- 2. Visitor segments (residents, day/overnight visitors, vendors)
CREATE TABLE attendance_segments (
    id                  TEXT PRIMARY KEY,
    label               TEXT NOT NULL,
    share               NUMERIC(5,4) NOT NULL,          -- fraction of attendance
    party_size          NUMERIC(4,2) NOT NULL,
    would_visit_anyway  NUMERIC(5,4) NOT NULL           -- counterfactual attribution input
);

-- 3. Per-segment spending profile (2025$ per person per event-day)
CREATE TABLE visitor_spending (
    segment_id          TEXT REFERENCES attendance_segments(id),
    spend_low           NUMERIC(10,2) NOT NULL,
    spend_mid           NUMERIC(10,2) NOT NULL,
    spend_high          NUMERIC(10,2) NOT NULL,
    attribution         NUMERIC(5,4) NOT NULL,          -- festival-attribution factor
    retention_berkeley  NUMERIC(5,4) NOT NULL,          -- Berkeley-retention factor
    PRIMARY KEY (segment_id)
);

-- 4. City service costs (Marina Fund chart of accounts, cost-type tagged)
CREATE TABLE city_service_costs (
    account          TEXT PRIMARY KEY,
    cost_low         NUMERIC(12,2) NOT NULL,
    cost_mid         NUMERIC(12,2) NOT NULL,
    cost_high        NUMERIC(12,2) NOT NULL,
    cost_type        TEXT NOT NULL,   -- incremental_cash | allocated | avoidable | fixed | capital_impact | opportunity
    scales_with_days BOOLEAN NOT NULL DEFAULT TRUE
);

-- 5. City revenue parameters (tax rates, fees, capture)
CREATE TABLE city_revenues (
    param   TEXT PRIMARY KEY,
    value   NUMERIC(12,6) NOT NULL,
    note    TEXT
);

-- 6. Modeled business impacts (IMPLAN + RIMS II cross-check multipliers)
CREATE TABLE business_impacts (
    source                   TEXT PRIMARY KEY,  -- implan | rims2
    output_multiplier        NUMERIC(6,4) NOT NULL,
    value_added_ratio        NUMERIC(6,4) NOT NULL,
    labor_income_ratio       NUMERIC(6,4) NOT NULL,
    jobs_per_million_output  NUMERIC(6,3) NOT NULL
);

-- 7. Transportation inputs (mode share, occupancy, VMT by origin)
CREATE TABLE transportation_inputs (
    param        TEXT PRIMARY KEY,
    scenario_key TEXT,               -- transit_service key where applicable
    value        NUMERIC(12,4) NOT NULL
);

-- 8. Parking inventory (spatially aware)
CREATE TABLE parking_inventory (
    id                  SERIAL PRIMARY KEY,
    name                TEXT NOT NULL,
    spaces              INTEGER NOT NULL,
    baseline_occupancy  NUMERIC(5,4) NOT NULL,
    reservable          BOOLEAN NOT NULL DEFAULT FALSE
    -- , geom GEOMETRY(Polygon, 4326)   -- enable with PostGIS
);

-- 9. Environmental impact factors
CREATE TABLE environmental_impacts (
    param   TEXT PRIMARY KEY,
    value   NUMERIC(12,4) NOT NULL,
    note    TEXT
);

-- 10. Community outcome indicators (kept as indicators, not dollarized)
CREATE TABLE community_outcomes (
    indicator   TEXT PRIMARY KEY,
    measured_by TEXT NOT NULL DEFAULT 'post-event survey'
);

-- 11. Model assumptions (Monte Carlo, weather, confidence targets)
CREATE TABLE model_assumptions (
    param   TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);

-- 12. Evidence register - every consequential input traced (concept screen 5)
CREATE TABLE evidence_sources (
    id          SERIAL PRIMARY KEY,
    field       TEXT NOT NULL,
    value       TEXT,
    source      TEXT NOT NULL,
    as_of       DATE,
    owner       TEXT,
    confidence  TEXT NOT NULL,       -- low | medium | high
    basis       TEXT NOT NULL,       -- measured | modeled | stipulated
    adjustment_procedure TEXT
);

-- Load seed values with: python3 model/load_seed.py  (or COPY from data/seed.json)
