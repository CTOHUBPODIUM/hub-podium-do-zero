CREATE TABLE athletes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  birth_date DATE,
  category TEXT,
  position TEXT,
  responsible_name TEXT,
  responsible_email TEXT,
  responsible_phone TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE video_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  athlete_id UUID REFERENCES athletes(id),
  video_url TEXT NOT NULL,
  status TEXT DEFAULT 'received',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  athlete_id UUID REFERENCES athletes(id),
  video_submission_id UUID REFERENCES video_submissions(id),
  overall INT,
  speed INT,
  technique INT,
  game_iq INT,
  physical INT,
  potential INT,
  report_url TEXT,
  card_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  athlete_id UUID REFERENCES athletes(id),
  amount NUMERIC(10,2) DEFAULT 49.00,
  provider TEXT DEFAULT 'mercado_pago',
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);
