-- Collaborative Question Paper Builder
-- Apply once to the existing Neon/PostgreSQL database before enabling the feature.
-- Uses the existing teachers, questions, papers, and paper_questions tables.

CREATE TABLE IF NOT EXISTS collaborative_papers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  academy_id UUID NOT NULL,
  owner_teacher_id TEXT NOT NULL,
  title TEXT NOT NULL,
  exam TEXT NOT NULL DEFAULT 'MHT-CET',
  class_name TEXT,
  board TEXT,
  exam_type TEXT,
  duration_minutes INTEGER NOT NULL DEFAULT 60 CHECK (duration_minutes > 0),
  total_marks NUMERIC(8,2),
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft','in_progress','in_review','approved','published','archived')),
  published_paper_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS collaborative_papers_academy_idx ON collaborative_papers (academy_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS collaborative_papers_owner_idx ON collaborative_papers (owner_teacher_id, updated_at DESC);

CREATE TABLE IF NOT EXISTS paper_collaborators (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID NOT NULL REFERENCES collaborative_papers(id) ON DELETE CASCADE,
  teacher_id TEXT NOT NULL,
  invited_by TEXT NOT NULL,
  invitation_status TEXT NOT NULL DEFAULT 'pending'
    CHECK (invitation_status IN ('pending','accepted','declined','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  accepted_at TIMESTAMPTZ,
  UNIQUE (paper_id, teacher_id)
);
CREATE INDEX IF NOT EXISTS paper_collaborators_teacher_idx ON paper_collaborators (teacher_id, invitation_status);

CREATE TABLE IF NOT EXISTS paper_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID NOT NULL REFERENCES collaborative_papers(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  title TEXT NOT NULL,
  assigned_teacher_id TEXT,
  display_order INTEGER NOT NULL DEFAULT 1,
  marks_target NUMERIC(8,2),
  question_count_target INTEGER,
  status TEXT NOT NULL DEFAULT 'not_started'
    CHECK (status IN ('not_started','in_progress','submitted','changes_requested','approved')),
  submitted_at TIMESTAMPTZ,
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS paper_sections_paper_idx ON paper_sections (paper_id, display_order);
CREATE INDEX IF NOT EXISTS paper_sections_assignee_idx ON paper_sections (assigned_teacher_id, status);

CREATE TABLE IF NOT EXISTS paper_section_questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  section_id UUID NOT NULL REFERENCES paper_sections(id) ON DELETE CASCADE,
  question_id TEXT NOT NULL,
  question_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_type TEXT NOT NULL DEFAULT 'manual'
    CHECK (source_type IN ('manual','generated','custom')),
  display_order INTEGER NOT NULL DEFAULT 1,
  marks NUMERIC(8,2) NOT NULL DEFAULT 1 CHECK (marks >= 0),
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (section_id, question_id),
  UNIQUE (section_id, display_order)
);
CREATE INDEX IF NOT EXISTS paper_section_questions_order_idx ON paper_section_questions (section_id, display_order);

CREATE TABLE IF NOT EXISTS paper_activity_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID NOT NULL REFERENCES collaborative_papers(id) ON DELETE CASCADE,
  section_id UUID REFERENCES paper_sections(id) ON DELETE SET NULL,
  actor_teacher_id TEXT NOT NULL,
  action TEXT NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS paper_activity_log_paper_idx ON paper_activity_log (paper_id, created_at DESC);

CREATE TABLE IF NOT EXISTS paper_revisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  paper_id UUID NOT NULL REFERENCES collaborative_papers(id) ON DELETE CASCADE,
  section_id UUID REFERENCES paper_sections(id) ON DELETE SET NULL,
  created_by TEXT NOT NULL,
  revision_type TEXT NOT NULL,
  snapshot JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS paper_revisions_paper_idx ON paper_revisions (paper_id, created_at DESC);
