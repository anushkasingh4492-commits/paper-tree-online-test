import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

async function getAcademyAdmin(targetAcademyId?: string) {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return null;
  const data = parseSessionCookie<Record<string, unknown>>(value);

  if (data) {
    if (data.role === "ACADEMY_ADMIN" && data.academyId) return data;
    if ((data.role === "ADMIN" || data.role === "MASTER_ADMIN") && targetAcademyId) return { ...data, academyId: targetAcademyId };
    return null;
  }

  return null;
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const admin = await getAcademyAdmin(searchParams.get("academyId") || undefined);
  if (!admin) return NextResponse.json({success:false,error:"Unauthorized"},{status:401});
  try {
    const result=await pool.query(`SELECT s.id,s.name,s.email,s.class_name,s.created_at,EXISTS(SELECT 1 FROM student_credentials sc WHERE sc.student_id=s.id) AS has_password FROM students s WHERE s.academy_id=$1 ORDER BY s.name`,[admin.academyId]);
    return NextResponse.json({success:true,students:result.rows});
  } catch(e){console.error("ACADEMY STUDENTS GET ERROR:",e);return NextResponse.json({success:false,error:"Failed to load students"},{status:500});}
}

export async function POST(req: Request) {
  try {
    const body=await req.json(); const academyId=String(body.academyId||"").trim(); const admin=await getAcademyAdmin(academyId);
    if(!admin)return NextResponse.json({success:false,error:"Unauthorized"},{status:401});
    const name=String(body.name||"").trim();
const email=String(body.email||"").trim().toLowerCase();
const password=String(body.password||"");
const className=String(body.className||"").trim();
const batchId=String(body.batchId||"").trim();
    if(!name||!email||!password)return NextResponse.json({success:false,error:"Name, email and password are required."},{status:400});
    if(password.length<6)return NextResponse.json({success:false,error:"Student password must be at least 6 characters"},{status:400});
    const academy=await pool.query(`SELECT student_limit,subscription_end,status,(SELECT COUNT(*)::int FROM students WHERE academy_id=$1) AS student_count FROM academies WHERE id=$1`,[admin.academyId]);
    const settings=academy.rows[0];
    if(!settings)return NextResponse.json({success:false,error:"Academy not found."},{status:404});
    if(settings.status!=="ACTIVE")return NextResponse.json({success:false,error:"This academy is not active."},{status:403});
    if(settings.subscription_end&&new Date(settings.subscription_end)<new Date())return NextResponse.json({success:false,error:"The academy subscription has expired."},{status:403});
    if(Number(settings.student_count)>=Number(settings.student_limit))return NextResponse.json({success:false,error:"The academy has reached its student limit."},{status:409});
    const existing=await pool.query(`SELECT id FROM students WHERE LOWER(email)=LOWER($1) LIMIT 1`,[email]);
    if(existing.rows.length)return NextResponse.json({success:false,error:"This email is already registered. Use a different email."},{status:409});
    const studentId=randomUUID();
const passwordHash=await bcrypt.hash(password,10);

if (batchId) {
  const batchResult = await pool.query(
    `SELECT id FROM batches WHERE id=$1 AND academy_id=$2 LIMIT 1`,
    [batchId, admin.academyId]
  );

  if (!batchResult.rows.length) {
    return NextResponse.json(
      {
        success:false,
        error:"Selected batch was not found in this academy."
      },
      {status:404}
    );
  }
}

await pool.query(
  `INSERT INTO students(id,name,email,class_name,academy_id)
   VALUES($1,$2,$3,$4,$5)`,
  [studentId,name,email,className,admin.academyId]
);

await pool.query(
  `INSERT INTO student_credentials(student_id,password_hash)
   VALUES($1,$2)`,
  [studentId,passwordHash]
);

if (batchId) {
  await pool.query(
    `INSERT INTO batch_students(batch_id,student_id)
     VALUES($1,$2)
     ON CONFLICT DO NOTHING`,
    [batchId,studentId]
  );
}

return NextResponse.json({
  success:true,
  student:{
    id:studentId,
    name,
    email,
    className
  },
  credentials:{
    username:email,
    password
  }
});
  } catch(error){console.error("ACADEMY STUDENTS POST ERROR:",error);return NextResponse.json({success:false,error:error instanceof Error?error.message:"Failed to create student"},{status:500});}
}

export async function DELETE(req: Request) {
  const { searchParams } = new URL(req.url);
  const admin = await getAcademyAdmin(searchParams.get("academyId") || undefined);
  const studentId = searchParams.get("id") || "";
  if (!admin) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const owned = await client.query(`SELECT id FROM students WHERE id=$1 AND academy_id=$2`, [studentId, admin.academyId]);
    if (!owned.rowCount) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: "Student not found in this academy." }, { status: 404 }); }
    await client.query(`DELETE FROM batch_students WHERE student_id=$1`, [studentId]);
    await client.query(`DELETE FROM notifications WHERE student_id=$1::text`, [studentId]);
    await client.query(`DELETE FROM test_attempts WHERE student_id=$1`, [studentId]);
    await client.query(`DELETE FROM student_credentials WHERE student_id=$1`, [studentId]);
    await client.query(`DELETE FROM students WHERE id=$1 AND academy_id=$2`, [studentId, admin.academyId]);
    await client.query("COMMIT");
    return NextResponse.json({ success: true });
  } catch (error) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not remove student." }, { status: 500 }); }
  finally { client.release(); }
}
