import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("master_session")?.value;

  if (!sessionCookie) return false;

  try {
    const session = JSON.parse(sessionCookie);
    return (
      session.role === "ADMIN" ||
      session.role === "MASTER_ADMIN"
    );
  } catch {
    return false;
  }
}

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ academyId: string }> }
) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const { academyId } = await params;

  try {
    const [academy, students, teachers, batches, papers, scheduledTests, questions] =
      await Promise.all([
        pool.query(
          `
          SELECT id, name, code, created_at
          FROM academies
          WHERE id = $1
          LIMIT 1
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            s.id,
            s.name,
            s.email,
            s.roll_number,
            s.class_name,
            s.created_at,
            EXISTS (
              SELECT 1
              FROM student_credentials sc
              WHERE sc.student_id = s.id
            ) AS has_password
          FROM students s
          WHERE s.academy_id = $1
          ORDER BY s.name
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            t.id,
            t.name,
            t.email,
            t.created_at,
            (t.password_hash IS NOT NULL) AS has_password
          FROM teachers t
          WHERE t.academy_id = $1
          ORDER BY t.name
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            b.id,
            b.name,
            b.class_name,
            b.created_by,
            b.created_at,
            COUNT(bs.student_id)::int AS student_count
          FROM batches b
          LEFT JOIN batch_students bs ON bs.batch_id = b.id
          WHERE b.academy_id = $1
          GROUP BY b.id
          ORDER BY b.name
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            p.id,
            p.code,
            p.exam,
            p.description,
            p.duration_minutes,
            p.status,
            p.created_by,
            t.name AS creator_name,
            t.email AS creator_email,
            p.created_at,
            COUNT(pq.question_id)::int AS question_count
          FROM papers p
          LEFT JOIN paper_questions pq ON pq.paper_id = p.id
          LEFT JOIN teachers t ON t.id::text = p.created_by::text
          WHERE p.academy_id = $1
          GROUP BY p.id, t.name, t.email
          ORDER BY p.created_at DESC
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            st.id,
            st.title,
            st.start_time,
            st.end_time,
            st.duration_minutes,
            st.status,
            st.paper_id,
            p.code AS paper_code,
            st.batch_id,
            b.name AS batch_name
          FROM scheduled_tests st
          LEFT JOIN papers p ON p.id = st.paper_id
          LEFT JOIN batches b ON b.id = st.batch_id
          WHERE st.academy_id = $1
          ORDER BY st.start_time DESC
          `,
          [academyId]
        ),
        pool.query(
          `
          SELECT
            pq.paper_id,
            pq.question_order,
            q.id,
            q.exam,
            q.subject,
            q.chapter_name,
            q.stem,
            q.options,
            q.correct_option,
            q.solution,
            q.difficulty,
            q.question_type
          FROM paper_questions pq
          INNER JOIN papers p ON p.id = pq.paper_id
          INNER JOIN questions q ON q.id = pq.question_id
          WHERE p.academy_id = $1
          ORDER BY pq.paper_id, pq.question_order
          `,
          [academyId]
        ),
      ]);

    if (academy.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Academy not found." },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      academy: academy.rows[0],
      students: students.rows,
      teachers: teachers.rows,
      batches: batches.rows,
      papers: papers.rows,
      scheduledTests: scheduledTests.rows,
      questions: questions.rows,
    });
  } catch (error) {
    console.error("ACADEMY DETAILS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Failed to load academy details.",
      },
      { status: 500 }
    );
  }
}