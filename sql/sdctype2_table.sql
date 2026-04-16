CREATE TABLE IF NOT EXISTS incoming_ducks (
    duck_id     INTEGER,
    duck_name   VARCHAR,
    breed       VARCHAR,
    location    VARCHAR,
    begin_date  DATE,
    end_date    DATE,
    is_current  BOOLEAN
);

INSERT INTO incoming_ducks VALUES
    (101, 'Quackers',   'Mallard',       'Pond B',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (102, 'Waddles',    'Pekin',         'Pond A',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (104, 'Splash',     'Muscovy',       'Pond C',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (105, 'Puddles',    'Indian Runner', 'Relocated',   CURRENT_DATE - INTERVAL '1 day', NULL, true);



CREATE TABLE IF NOT EXISTS master_ducks (
    record_id   INTEGER PRIMARY KEY,
    duck_id     INTEGER NOT NULL,
    duck_name   VARCHAR,
    breed       VARCHAR,
    location    VARCHAR,
    begin_date  DATE NOT NULL,
    end_date    DATE,
    is_current  BOOLEAN NOT NULL DEFAULT true
);

CREATE SEQUENCE IF NOT EXISTS duck_record_seq START 1;

INSERT INTO master_ducks VALUES
    (nextval('duck_record_seq'), 101, 'Quackers', 'Mallard',       'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 102, 'Waddles',  'Pekin',         'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 103, 'Feathers', 'Rouen',         'Pond B', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 105, 'Puddles',  'Indian Runner', 'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true);
