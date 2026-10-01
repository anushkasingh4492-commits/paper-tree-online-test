import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { getStudentGamification } from "@/lib/gamification";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type Session = {
  studentId?: string;
  academyId?: string;
  id?: string;
  role?: string;
};

export async function GET(
  _request: Request,
  context: { params: Promise<{ studentId: string }> }
) {
  try {
    const { studentId: requestedStudentId } = await context.params;
    const targetStudentId = String(requestedStudentId || "").trim();
    if (!targetStudentId) {
      return NextResponse.json({ success: false, error: "Student id is required." }, { status: 400 });
    }

    const cookieStore = await cookies();
    const studentRaw = cookieStore.get("student_session")?.value;
    const teacherRaw = cookieStore.get("master_session")?.value;
    const studentSession = studentRaw ? parseSessionCookie<Session>(studentRaw) : null;
    const teacherSession = teacherRaw ? parseSessionCookie<Session>(teacherRaw) : null;

    let academyId = "";
    let allowed = false;

    if (studentSession?.studentId && studentSession.academyId) {
      academyId = String(studentSession.academyId);
      if (String(studentSession.studentId) === targetStudentId) {
        allowed = true;
      } else {
        const access = await pool.query(
          `SELECT 1
             FROM batch_students viewer
             INNER JOIN batch_students target
               ON target.batch_id = viewer.batch_id
             INNER JOIN batches b
               ON b.id = viewer.batch_id
            WHERE viewer.student_id = $1
              AND target.student_id = $2
              AND b.academy_id = $3
            LIMIT 1`,
          [studentSession.studentId, targetStudentId, academyId]
        );
        allowed = (access.rowCount ?? 0) > 0;
      }
    } else if (teacherSession?.id && teacherSession.role === "TEACHER") {
      const teacher = await pool.query(
        `SELECT academy_id FROM teachers WHERE id = $1 LIMIT 1`,
        [teacherSession.id]
      );
      academyId = String(teacher.rows[0]?.academy_id || "");
      if (academyId) {
        const target = await pool.query(
          `SELECT 1 FROM students WHERE id = $1 AND academy_id = $2 LIMIT 1`,
          [targetStudentId, academyId]
        );
        allowed = (target.rowCount ?? 0) > 0;
      }
    }

    if (!academyId || !allowed) {
      return NextResponse.json({ success: false, error: "You are not allowed to view this student's badges." }, { status: 403 });
    }

    const student = await pool.query(
      `SELECT id, name FROM students WHERE id = $1 AND academy_id = $2 LIMIT 1`,
      [targetStudentId, academyId]
    );
    if (!student.rows[0]) {
      return NextResponse.json({ success: false, error: "Student not found." }, { status: 404 });
    }

    const game = await getStudentGamification(targetStudentId, academyId);

    return NextResponse.json({
      success: true,
      student: { id: targetStudentId, name: student.rows[0].name },
      level: game.level,
      levelName: game.levelName,
      streak: game.streak,
      testsCompleted: game.testsCompleted,
      badges: game.badges.filter((badge) => badge.earned),
    });
  } catch (error) {
    console.error("STUDENT BADGES ERROR", error);
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : "Could not load badges." },
      { status: 500 }
    );
  }
}
