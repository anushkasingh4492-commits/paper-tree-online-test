import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { apiError, getCollaborativeTeacher, logPaperActivity } from "@/lib/collaborative-papers";
export const runtime = "nodejs";

export async function GET() {
  try {
    const teacher = await getCollaborativeTeacher();
    if (!teacher) return apiError("Teacher login required.", 401);
    const result = await pool.query(
      `SELECT p.id::text, p.title, p.exam, p.class_name, p.board, p.duration_minutes, p.total_marks, p.status, p.updated_at,
        p.owner_teacher_id::text, owner.name AS owner_name,
        (p.owner_teacher_id::text = $1::text) AS is_owner,
        COALESCE((SELECT COUNT(*)::int FROM collaborative_paper_sections s WHERE s.paper_id = p.id),0) AS section_count,
        COALESCE((SELECT COUNT(*)::int FROM collaborative_paper_sections s WHERE s.paper_id = p.id AND s.status = 'approved'),0) AS approved_sections,
        COALESCE((SELECT COUNT(*)::int FROM collaborative_paper_section_questions q JOIN collaborative_paper_sections s ON s.id=q.section_id WHERE s.paper_id=p.id),0) AS question_count
       FROM collaborative_papers p JOIN teachers owner ON owner.id = p.owner_teacher_id
       WHERE p.academy_id::text = $2::text AND (p.owner_teacher_id::text = $1::text OR EXISTS (
         SELECT 1 FROM paper_collaborators c WHERE c.paper_id=p.id AND c.teacher_id::text=$1::text AND c.invitation_status='accepted'))
       ORDER BY p.updated_at DESC`, [teacher.id, teacher.academy_id]);
    const invitations = await pool.query(
      `SELECT c.id::text AS invitation_id, c.paper_id::text, c.created_at, p.title, owner.name AS owner_name
       FROM paper_collaborators c JOIN collaborative_papers p ON p.id=c.paper_id JOIN teachers owner ON owner.id=p.owner_teacher_id
       WHERE c.teacher_id::text=$1::text AND c.invitation_status='pending' AND p.academy_id::text=$2::text ORDER BY c.created_at DESC`,
      [teacher.id, teacher.academy_id]);
    return NextResponse.json({ success: true, papers: result.rows, invitations: invitations.rows });
  } catch (error) {
    console.error("COLLABORATIVE PAPERS LIST", error);
    return apiError("Could not load collaborative papers. Apply the collaborative-papers database migration if it has not been run.", 500);
  }
}

export async function POST(request: Request) {
  const client = await pool.connect();
  try {
    const teacher = await getCollaborativeTeacher();
    if (!teacher) return apiError("Teacher login required.", 401);
    const body = await request.json();
    const title = String(body.title || "").trim();
    const exam = String(body.exam || "MHT-CET").trim();
    const duration = Number(body.durationMinutes ?? 60);
    if (!title) return apiError("Paper title is required.");
    if (!Number.isInteger(duration) || duration < 1 || duration > 600) return apiError("Duration must be between 1 and 600 minutes.");
    const sections = Array.isArray(body.sections) ? body.sections : [];
    await client.query("BEGIN");
    const created = await client.query(
      `INSERT INTO collaborative_papers (academy_id, owner_teacher_id, title, exam, class_name, board, exam_type, duration_minutes, total_marks, status)
       VALUES ($1::uuid,$2::uuid,$3,$4,$5,$6,$7,$8,$9,'draft') RETURNING *`,
      [teacher.academy_id, teacher.id, title, exam, body.className ? String(body.className) : null, body.board ? String(body.board) : null, body.examType ? String(body.examType) : null, duration, body.totalMarks == null || body.totalMarks === "" ? null : Number(body.totalMarks)]);
    const paper = created.rows[0];
    for (let i = 0; i < sections.length; i++) {
      const section = sections[i];
      const subject = String(section.subject || "").trim();
      if (!subject) continue;
      let assignedTeacherId: string | null = null;
      if (section.assignedTeacherId) {
        const check = await client.query(`SELECT id FROM teachers WHERE id::text=$1::text AND academy_id::text=$2::text`, [String(section.assignedTeacherId), teacher.academy_id]);
        if (!check.rows[0]) throw new Error("A section assignee does not belong to your academy.");
        assignedTeacherId = String(check.rows[0].id);
      }
      await client.query(
        `INSERT INTO collaborative_paper_sections (paper_id, subject, title, assigned_teacher_id, display_order, marks_target, question_count_target)
         VALUES ($1::uuid,$2,$3,$4::uuid,$5,$6,$7)`,
        [paper.id, subject, String(section.title || subject).trim(), assignedTeacherId, Number(section.displayOrder) || i + 1, section.marksTarget == null || section.marksTarget === "" ? null : Number(section.marksTarget), section.questionCountTarget == null || section.questionCountTarget === "" ? null : Number(section.questionCountTarget)]);
      if (assignedTeacherId) {
        await client.query(
          `INSERT INTO paper_collaborators (paper_id, teacher_id, invited_by, invitation_status)
           VALUES ($1::uuid,$2::uuid,$3::uuid,'pending') ON CONFLICT (paper_id, teacher_id) DO NOTHING`,
          [paper.id, assignedTeacherId, teacher.id],
        );
      }
    }
    await client.query("COMMIT");
    await logPaperActivity(String(paper.id), teacher.id, "paper_created", null, { title });
    return NextResponse.json({ success: true, paper: { id: paper.id, title: paper.title, status: paper.status } }, { status: 201 });
  } catch (error) {
    await client.query("ROLLBACK").catch(() => undefined);
    console.error("CREATE COLLABORATIVE PAPER", error);
    return apiError(error instanceof Error ? error.message : "Could not create collaborative paper.", 500);
  } finally { client.release(); }
}
