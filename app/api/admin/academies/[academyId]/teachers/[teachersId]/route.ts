import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;
  try { const s = JSON.parse(decodeURIComponent(value)); return s.role === "ADMIN" || s.role === "MASTER_ADMIN"; } catch { return false; }
}

export async function PATCH(req: Request, { params }: { params: Promise<{ academyId: string; teachersId: string }> }) {
  if (!(await isMasterAdmin())) return NextResponse.json({ success:false,error:"Unauthorized" },{status:401});
  const { academyId, teachersId: teacherId } = await params;
  try {
    const body = await req.json(); const name=String(body.name||"").trim(); const email=String(body.email||"").trim().toLowerCase();
    if (!name || !email) return NextResponse.json({success:false,error:"Name and email are required."},{status:400});
    const dup=await pool.query(`SELECT id FROM teachers WHERE LOWER(email)=$1 AND id<>$2 LIMIT 1`,[email,teacherId]);
    if(dup.rows.length) return NextResponse.json({success:false,error:"That email is already in use."},{status:409});
    const r=await pool.query(`UPDATE teachers SET name=$1,email=$2 WHERE id=$3 AND academy_id=$4 RETURNING id,name,email,created_at`,[name,email,teacherId,academyId]);
    if(!r.rows.length)return NextResponse.json({success:false,error:"Teacher not found."},{status:404});
    return NextResponse.json({success:true,teacher:r.rows[0]});
  } catch(e){console.error("MASTER TEACHER PATCH ERROR:",e);return NextResponse.json({success:false,error:"Failed to update teacher."},{status:500});}
}

export async function DELETE(_req: Request,{params}:{params:Promise<{academyId:string;teachersId:string}>}){
  if(!(await isMasterAdmin()))return NextResponse.json({success:false,error:"Unauthorized"},{status:401});
  const {academyId,teachersId: teacherId}=await params;
  try{
    const r=await pool.query(`DELETE FROM teachers WHERE id=$1 AND academy_id=$2 RETURNING id`,[teacherId,academyId]);
    if(!r.rows.length)return NextResponse.json({success:false,error:"Teacher not found."},{status:404});
    return NextResponse.json({success:true});
  }catch(e){console.error("MASTER TEACHER DELETE ERROR:",e);return NextResponse.json({success:false,error:"Teacher could not be removed. They may own existing records."},{status:409});}
}
