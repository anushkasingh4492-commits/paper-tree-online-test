import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export type CollaborativeTeacher = { id: string; name: string; email: string; academy_id: string };
export async function getCollaborativeTeacher(): Promise<CollaborativeTeacher | null> {
  const raw = (await cookies()).get("master_session")?.value;
  const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
  if (session?.role !== "TEACHER" || !session.id) return null;
  const result = await pool.query(
    `SELECT id::text, name, email, academy_id::text FROM teachers WHERE id::text = $1::text LIMIT 1`,
    [String(session.id)],
  );
  const teacher = result.rows[0];
  return teacher?.academy_id ? teacher as CollaborativeTeacher : null;
}
export function apiError(message: string, status = 400) {
  return NextResponse.json({ success: false, error: message }, { status });
}
export async function getPaperAccess(paperId: string, teacher: CollaborativeTeacher) {
  const result = await pool.query(
    `SELECT p.*, (p.owner_teacher_id::text = $2::text) AS is_owner,
      EXISTS (SELECT 1 FROM paper_collaborators pc WHERE pc.paper_id = p.id AND pc.teacher_id::text = $2::text AND pc.invitation_status = 'accepted') AS is_collaborator
     FROM collaborative_papers p WHERE p.id::text = $1::text AND p.academy_id::text = $3::text LIMIT 1`,
    [paperId, teacher.id, teacher.academy_id],
  );
  return result.rows[0] ?? null;
}
export async function canViewPaper(paperId: string, teacher: CollaborativeTeacher) {
  const paper = await getPaperAccess(paperId, teacher);
  return paper && (paper.is_owner || paper.is_collaborator) ? paper : null;
}
export async function canEditSection(paperId: string, sectionId: string, teacher: CollaborativeTeacher) {
  const paper = await canViewPaper(paperId, teacher);
  if (!paper) return { paper: null, section: null, allowed: false };
  const result = await pool.query(
    `SELECT * FROM collaborative_paper_sections WHERE id::text = $1::text AND paper_id::text = $2::text LIMIT 1`,
    [sectionId, paperId],
  );
  const section = result.rows[0] ?? null;
  const allowed = Boolean(section && (paper.is_owner || (paper.is_collaborator && section.assigned_teacher_id && String(section.assigned_teacher_id) === teacher.id)));
  return { paper, section, allowed };
}
export async function logPaperActivity(paperId: string, teacherId: string, action: string, sectionId?: string | null, details: Record<string, unknown> = {}) {
  await pool.query(
    `INSERT INTO paper_activity_log (paper_id, section_id, actor_teacher_id, action, details) VALUES ($1::uuid, $2::uuid, $3, $4, $5::jsonb)`,
    [paperId, sectionId || null, teacherId, action, JSON.stringify(details)],
  );
}
export async function recordSectionRevision(paperId: string, sectionId: string, teacherId: string, revisionType: string) {
  const result = await pool.query(
    `SELECT s.*, COALESCE(jsonb_agg(jsonb_build_object('id', q.id, 'questionId', q.question_id, 'snapshot', q.question_snapshot, 'sourceType', q.source_type, 'displayOrder', q.display_order, 'marks', q.marks) ORDER BY q.display_order) FILTER (WHERE q.id IS NOT NULL), '[]'::jsonb) AS questions
     FROM collaborative_paper_sections s LEFT JOIN collaborative_paper_section_questions q ON q.section_id = s.id
     WHERE s.id::text = $1::text AND s.paper_id::text = $2::text GROUP BY s.id`,
    [sectionId, paperId],
  );
  if (result.rows[0]) await pool.query(
    `INSERT INTO paper_revisions (paper_id, section_id, created_by, revision_type, snapshot) VALUES ($1::uuid,$2::uuid,$3,$4,$5::jsonb)`,
    [paperId, sectionId, teacherId, revisionType, JSON.stringify(result.rows[0])],
  );
}
