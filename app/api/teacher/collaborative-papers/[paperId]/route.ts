import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { apiError, canViewPaper, getCollaborativeTeacher, logPaperActivity } from "@/lib/collaborative-papers";
export const runtime = "nodejs";
type Context = { params: Promise<{ paperId: string }> };
export async function GET(_request: Request, context: Context) {
  try {
    const teacher = await getCollaborativeTeacher(); if (!teacher) return apiError("Teacher login required.",401);
    const { paperId } = await context.params; const paper = await canViewPaper(paperId, teacher);
    if (!paper) return apiError("Paper not found or access denied.",404);
    const [sections, collaborators, activity] = await Promise.all([
      pool.query(`SELECT s.*, s.id::text AS id, s.paper_id::text AS paper_id, s.assigned_teacher_id::text AS assigned_teacher_id, t.name AS assigned_teacher_name,
        COALESCE((SELECT COUNT(*)::int FROM paper_section_questions q WHERE q.section_id=s.id),0) AS question_count,
        COALESCE((SELECT SUM(q.marks) FROM paper_section_questions q WHERE q.section_id=s.id),0) AS marks_total,
        COALESCE((SELECT jsonb_agg(jsonb_build_object('itemId',q.id::text,'questionId',q.question_id,'stem',COALESCE(q.question_snapshot->>'stem',q.question_snapshot->>'question',q.question_snapshot->>'question_text','Question content unavailable'),'marks',q.marks,'displayOrder',q.display_order,'sourceType',q.source_type) ORDER BY q.display_order) FROM paper_section_questions q WHERE q.section_id=s.id),'[]'::jsonb) AS questions
        FROM paper_sections s LEFT JOIN teachers t ON t.id=s.assigned_teacher_id WHERE s.paper_id::text=$1::text ORDER BY s.display_order,s.created_at`,[paperId]),
      pool.query(`SELECT c.id::text,c.teacher_id::text,c.invitation_status,c.created_at,c.accepted_at,t.name,t.email FROM paper_collaborators c JOIN teachers t ON t.id=c.teacher_id WHERE c.paper_id::text=$1::text ORDER BY c.created_at`,[paperId]),
      pool.query(`SELECT a.action,a.details,a.created_at,t.name AS actor_name FROM paper_activity_log a JOIN teachers t ON t.id=a.actor_teacher_id WHERE a.paper_id::text=$1::text ORDER BY a.created_at DESC LIMIT 30`,[paperId]),
    ]);
    return NextResponse.json({ success:true, currentTeacherId:teacher.id, paper:{...paper,id:String(paper.id),is_owner:Boolean(paper.is_owner)}, sections:sections.rows, collaborators:collaborators.rows, activity:activity.rows });
  } catch(error) { console.error("GET COLLABORATIVE PAPER",error); return apiError("Could not load paper details.",500); }
}
export async function PATCH(request: Request, context: Context) {
  try {
    const teacher=await getCollaborativeTeacher(); if(!teacher) return apiError("Teacher login required.",401);
    const {paperId}=await context.params; const paper=await canViewPaper(paperId,teacher);
    if(!paper || !paper.is_owner) return apiError("Only the paper owner can edit paper details.",403);
    if(["published","archived"].includes(String(paper.status))) return apiError("Published or archived papers cannot be edited.",409);
    const body=await request.json();
    const result=await pool.query(`UPDATE collaborative_papers SET title=COALESCE($3,title), exam=COALESCE($4,exam), class_name=COALESCE($5,class_name), board=COALESCE($6,board), duration_minutes=COALESCE($7,duration_minutes), total_marks=COALESCE($8,total_marks), version=version+1, updated_at=NOW() WHERE id::text=$1::text AND academy_id::text=$2::text RETURNING id::text,title,status,version`,[paperId,teacher.academy_id,body.title===undefined?null:String(body.title).trim(),body.exam===undefined?null:String(body.exam),body.className===undefined?null:String(body.className),body.board===undefined?null:String(body.board),body.durationMinutes===undefined?null:Number(body.durationMinutes),body.totalMarks===undefined?null:Number(body.totalMarks)]);
    await logPaperActivity(paperId,teacher.id,"paper_updated");
    return NextResponse.json({success:true,paper:result.rows[0]});
  } catch(error) { console.error("UPDATE COLLABORATIVE PAPER",error); return apiError("Could not update paper details.",500); }
}
