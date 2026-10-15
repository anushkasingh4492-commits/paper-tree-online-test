import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { apiError, canViewPaper, getCollaborativeTeacher, logPaperActivity } from "@/lib/collaborative-papers";
export const runtime="nodejs";
type Context={params:Promise<{paperId:string}>};
export async function POST(request:Request,context:Context){
 try{const teacher=await getCollaborativeTeacher();if(!teacher)return apiError("Teacher login required.",401);const {paperId}=await context.params;const paper=await canViewPaper(paperId,teacher);if(!paper||!paper.is_owner)return apiError("Only the paper owner can add sections.",403);
 const body=await request.json();const subject=String(body.subject||"").trim();if(!subject)return apiError("Subject is required.");let assignee:string|null=null;
 if(body.assignedTeacherId){const t=await pool.query(`SELECT id FROM teachers WHERE id::text=$1::text AND academy_id::text=$2::text`,[String(body.assignedTeacherId),teacher.academy_id]);if(!t.rows[0])return apiError("Assigned professor is not in this academy.",400);assignee=String(t.rows[0].id);}
 const r=await pool.query(`INSERT INTO collaborative_paper_sections(paper_id,subject,title,assigned_teacher_id,display_order,marks_target,question_count_target,status) VALUES($1::uuid,$2,$3,$4::uuid,$5,$6,$7,'not_started') RETURNING *`,[paperId,subject,String(body.title||subject),assignee,Number(body.displayOrder)||1,body.marksTarget==null?null:Number(body.marksTarget),body.questionCountTarget==null?null:Number(body.questionCountTarget)]);
 if (assignee) await pool.query(`INSERT INTO paper_collaborators(paper_id,teacher_id,invited_by,invitation_status) VALUES($1::uuid,$2::uuid,$3::uuid,'pending') ON CONFLICT(paper_id,teacher_id) DO NOTHING`,[paperId,assignee,teacher.id]);
 await pool.query(`UPDATE collaborative_papers SET status='in_progress',version=version+1,updated_at=NOW() WHERE id::text=$1::text`,[paperId]);await logPaperActivity(paperId,teacher.id,"section_created",String(r.rows[0].id),{subject});return NextResponse.json({success:true,section:r.rows[0]},{status:201});
 }catch(e){console.error("ADD PAPER SECTION",e);return apiError("Could not add section.",500)}
}
