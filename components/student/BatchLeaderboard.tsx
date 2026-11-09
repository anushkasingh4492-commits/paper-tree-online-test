"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ArrowUpRight,
  Crown,
  Medal,
  Search,
  Sparkles,
  Star,
  Trophy,
} from "lucide-react";
import StudentAvatar from "@/components/StudentAvatar";
import StudentBadgeModal from "@/components/StudentBadgeModal";
import StudentWorkspace from "./StudentWorkspace";
import { fetchStudentData } from "./student-api";
import type { DashboardPayload, LeaderboardMember, LeaderboardPayload } from "./student-types";

const placeStyle: Record<number, string> = {
  1: "gold",
  2: "silver",
  3: "bronze",
};
const EMPTY_STUDENTS: LeaderboardMember[] = [];

function Podium({ student, onBadges }: { student: LeaderboardMember; onBadges: () => void }) {
  const place = placeStyle[student.rank] ?? "bronze";
  return (
    <article className={`leaderboard-podium leaderboard-podium--${place}`}>
      {student.rank === 1 && <div className="leaderboard-podium__confetti" aria-hidden="true"><i /><i /><i /><i /><i /></div>}
      <div className="leaderboard-podium__crown"><Crown size={26} fill="currentColor" /></div>
      <div className="leaderboard-podium__rank">{student.rank === 1 ? <Trophy size={20} /> : <Medal size={19} />} <span>#{student.rank}</span></div>
      <div className="leaderboard-podium__avatar"><StudentAvatar avatarKey={student.avatarKey} name={student.name} size={66} /></div>
      <h3 title={student.name}>{student.name}</h3>
      <div className="leaderboard-podium__score">{student.average.toFixed(1)}<span>%</span></div>
      <p className="leaderboard-podium__completion">{student.completionPercent == null ? "—" : `${student.completionPercent}%`} tests complete</p>
      <div className="leaderboard-podium__tests">{student.testsTaken} completed tests</div>
      <button type="button" onClick={onBadges}><Trophy size={14} /> View badges</button>
      <div className="leaderboard-podium__base" aria-hidden="true">{student.rank}</div>
      {student.rank === 1 && <div className="leaderboard-podium__stars" aria-hidden="true"><Star size={12} fill="currentColor" /><Star size={10} fill="currentColor" /><Star size={12} fill="currentColor" /></div>}
    </article>
  );
}

export default function BatchLeaderboard() {
  const [data, setData] = useState<LeaderboardPayload | null>(null);
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [badgeStudent, setBadgeStudent] = useState<LeaderboardMember | null>(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchStudentData<LeaderboardPayload>("/api/student/batch-leaderboard"),
      fetchStudentData<DashboardPayload>("/api/dashboard"),
    ])
      .then(([leaderboard, profile]) => {
        if (!active) return;
        setData(leaderboard);
        setDashboard(profile);
      })
      .catch((reason: unknown) => {
        if (active) setError(reason instanceof Error ? reason.message : "Could not load the batch leaderboard.");
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  const students = data?.students ?? EMPTY_STUDENTS;
  const filtered = useMemo(() => {
    const needle = query.trim().toLocaleLowerCase();
    return needle ? students.filter((student) => student.name.toLocaleLowerCase().includes(needle)) : students;
  }, [query, students]);
  const topThree = [2, 1, 3].map((rank) => students.find((student) => student.rank === rank)).filter((student): student is LeaderboardMember => Boolean(student));
  const unreadCount = dashboard?.notifications?.filter((item) => !item.isRead).length ?? 0;
  const courseName = dashboard?.assignment?.courseName ?? data?.batch?.courseName ?? "";

  return (
    <StudentWorkspace active="leaderboard" forceDark studentName={dashboard?.student?.name ?? ""} courseName={courseName} unreadCount={unreadCount}>
      <div className="leaderboard-page">
        <header className="leaderboard-heading">
          <div className="leaderboard-heading__mark"><Trophy size={24} /></div>
          <div><p className="leaderboard-kicker">BATCH CHAMPIONS</p><h1>Batch leaderboard</h1><p>Celebrate progress, learn from your peers, and climb the ranks.</p></div>
          {data?.batch && <div className="leaderboard-batch-pill"><span>Your batch</span><strong>{data.batch.name}</strong><small>{data.batch.size} students</small></div>}
        </header>

        {loading ? <div className="leaderboard-loading" aria-live="polite">Loading your batch scores…</div>
          : error ? <div className="leaderboard-error" role="alert">{error}</div>
          : !data?.batch ? <div className="leaderboard-empty"><Trophy size={34} /><h2>No batch assigned yet</h2><p>Your leaderboard will appear once your academy adds you to a batch.</p></div>
          : <>
            <section className="leaderboard-podium-section" aria-label="Top three students">
              <div className="leaderboard-section-title"><div><p className="leaderboard-kicker">THE TOP THREE</p><h2>Batch podium</h2></div><div className="leaderboard-live"><span /> Live rankings</div></div>
              <div className="leaderboard-podium-grid">
                {topThree.map((student) => <Podium key={student.id} student={student} onBadges={() => setBadgeStudent(student)} />)}
              </div>
            </section>

            {data.currentStudent && <section className="leaderboard-you-card">
              <div className="leaderboard-you-card__medal"><Medal size={22} /></div>
              <div className="leaderboard-you-card__title"><p>YOUR POSITION</p><h2>Rank #{data.currentStudent.rank}<span> of {data.batch.size}</span></h2></div>
              <div className="leaderboard-you-card__stats"><div><span>Average score</span><strong>{data.currentStudent.average.toFixed(1)}%</strong></div><div><span>Best score</span><strong>{data.currentStudent.bestScore.toFixed(1)}%</strong></div><div><span>Tests completed</span><strong>{data.currentStudent.testsTaken}</strong></div></div>
              <ArrowUpRight size={20} />
            </section>}

            <section className="leaderboard-roster">
              <div className="leaderboard-roster__header">
                <div><p className="leaderboard-kicker">BATCH STANDINGS</p><h2>All players</h2><span>Ranked by average completed-test score.</span></div>
                <label className="leaderboard-search"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search student..." aria-label="Search student" />{query && <button type="button" onClick={() => setQuery("")} aria-label="Clear search">×</button>}</label>
              </div>
              <div className="leaderboard-table-scroll">
                <table className="leaderboard-table">
                  <thead><tr><th>Rank</th><th>Student</th><th>Tests / questions</th><th>Score progress</th><th>Average</th><th>Best score</th><th /></tr></thead>
                  <tbody>
                    {filtered.map((student) => (
                      <tr key={student.id} className={student.isCurrent ? "is-current" : ""}>
                        <td><span className={`leaderboard-rank leaderboard-rank--${placeStyle[student.rank] ?? "regular"}`}>{student.rank <= 3 ? <Medal size={17} /> : `#${student.rank}`}</span></td>
                        <td><div className="leaderboard-student"><StudentAvatar avatarKey={student.avatarKey} name={student.name} size={39} /><div><strong>{student.name}{student.isCurrent && <small className="leaderboard-you-tag">YOU</small>}</strong><span>{student.completionPercent == null ? "No assigned-test data" : `${student.completionPercent}% assigned tests complete`}</span></div></div></td>
                        <td><strong>{student.testsTaken}</strong><span className="leaderboard-questions">{student.questionsSeen} questions</span></td>
                        <td><div className="leaderboard-scorebar"><i style={{ width: `${Math.max(0, Math.min(100, student.average))}%` }} /></div></td>
                        <td><strong className="leaderboard-average">{student.average.toFixed(1)}%</strong></td>
                        <td><strong>{student.bestScore.toFixed(1)}%</strong></td>
                        <td><button className="leaderboard-badges-button" type="button" onClick={() => setBadgeStudent(student)}><Trophy size={14} /> View badges</button></td>
                      </tr>
                    ))}
                    {!filtered.length && <tr><td className="leaderboard-no-results" colSpan={7}>No students match “{query}”.</td></tr>}
                  </tbody>
                </table>
              </div>
              <div className="leaderboard-roster__foot"><Sparkles size={14} /> Scores update as completed test results are recorded.</div>
            </section>
          </>}
      </div>
      {badgeStudent && <StudentBadgeModal studentId={badgeStudent.id} studentName={badgeStudent.name} onClose={() => setBadgeStudent(null)} />}
    </StudentWorkspace>
  );
}
