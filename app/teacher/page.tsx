"use client";

import { useEffect, useMemo, useState, type ComponentType } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, BookOpenCheck, CheckSquare, Clock3, FileText, Filter, LayoutDashboard, LogOut, Moon, Search, Sparkles, TrendingUp, Trophy, UsersRound, type LucideProps } from "lucide-react";

type Paper = { id: string; code: string; exam: string; description: string; duration_minutes: number; status?: string; created_at: string; question_count: number };
type Branding = { name: string; logo_data?: string | null };
type StudentPerformance = { id: string; name: string; batches: string; testsTaken: number; averagePercentage: number; accuracy: number; currentStreak: number };
type CreationOption = { title: string; description: string; route: string; tone: "blue" | "violet" | "green"; Icon: ComponentType<LucideProps> };

const creationOptions: CreationOption[] = [
  { title: "Single Test", description: "Create a test by selecting questions manually.", route: "/teacher/cherry-pick", tone: "blue", Icon: CheckSquare },
  { title: "Collaborative Test", description: "Co-create and publish a test with other teachers.", route: "/teacher/collaborative-papers", tone: "violet", Icon: UsersRound },
  { title: "Generate Test", description: "Auto-generate a test from the question bank.", route: "/teacher/generate", tone: "green", Icon: Sparkles },
];

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Recently created" : new Intl.DateTimeFormat(undefined, { day: "numeric", month: "short", year: "numeric" }).format(date);
}

function paperTone(status?: string) {
  const normalized = status?.toLowerCase() || "";
  if (normalized.includes("collab")) return "violet";
  if (normalized.includes("generat")) return "green";
  return "blue";
}

export default function TeacherPage() {
  const router = useRouter();
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [branding, setBranding] = useState<Branding | null>(null);
  const [features, setFeatures] = useState<{ completeStudentReports: boolean } | null>(null);
  const [query, setQuery] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [students, setStudents] = useState<StudentPerformance[]>([]);
  const [performanceLoading, setPerformanceLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response = await fetch("/api/teacher/papers");
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.error || "Failed to load papers.");
        setPapers(result.papers || []);
      } catch (err) { setError(err instanceof Error ? err.message : "Failed to load papers."); }
      finally { setLoading(false); }
    }
    void loadDashboard();
    void fetch("/api/academy/tier", { cache: "no-store", credentials: "include" }).then((response) => response.json()).then((data) => { if (data?.success) setFeatures(data.features); }).catch(() => undefined);
    void fetch("/api/academy/branding", { cache: "no-store" }).then((response) => response.json()).then((data) => { if (data.success) setBranding(data.academy); }).catch(() => undefined);
    void fetch("/api/teacher/performance", { cache: "no-store" })
      .then((response) => response.json())
      .then((data) => { if (data?.success) setStudents(data.students || []); })
      .catch(() => undefined)
      .finally(() => setPerformanceLoading(false));
  }, []);

  const visiblePapers = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    if (!normalizedQuery) return papers;
    return papers.filter((paper) => [paper.description, paper.code, paper.exam, paper.status].some((value) => value?.toLowerCase().includes(normalizedQuery)));
  }, [papers, query]);
  const performanceSummary = useMemo(() => {
    if (!students.length) return null;
    const average = (key: "averagePercentage" | "accuracy") => Math.round(students.reduce((total, student) => total + student[key], 0) / students.length);
    return { averageScore: average("averagePercentage"), accuracy: average("accuracy"), activeStudents: students.filter((student) => student.testsTaken > 0).length, topStudents: [...students].sort((first, second) => second.averagePercentage - first.averagePercentage).slice(0, 3) };
  }, [students]);

  async function logout() { try { await fetch("/api/logout", { method: "POST", credentials: "include" }); } finally { router.push("/login"); } }

  return <div className="teacher-dashboard">
    <aside className="teacher-sidebar">
      <div className="teacher-brand">{branding?.logo_data ? <img src={branding.logo_data} alt="Institute logo" className="teacher-brand-logo" /> : <span className="teacher-brand-mark">{(branding?.name || "T").slice(0, 1)}</span>}<div><strong>{branding?.name || "Teacher Portal"}</strong><span>Educational studio</span></div></div>
      <p className="teacher-nav-label">Workspace</p>
      <nav className="teacher-nav" aria-label="Teacher navigation"><button className="teacher-nav-item is-active"><LayoutDashboard size={18} /><span>Dashboard</span></button><button className="teacher-nav-item" onClick={() => router.push("/teacher/cherry-pick")}><FileText size={18} /><span>Test management</span></button>{features?.completeStudentReports !== false && <button className="teacher-nav-item" onClick={() => router.push("/teacher/performance")}><BookOpenCheck size={18} /><span>Student performance</span></button>}</nav>
      <div className="teacher-sidebar-footer"><button className="teacher-nav-item" onClick={logout}><LogOut size={18} /><span>Logout</span></button></div>
    </aside>
    <div className="teacher-workspace">
      <header className="teacher-topbar"><div><p className="teacher-welcome">Welcome back</p><p className="teacher-topbar-copy">Create, manage and track your students&apos; performance.</p></div><button type="button" className="teacher-icon-button" aria-label="Theme settings"><Moon size={19} /></button></header>
      <main className="teacher-content">
        <section className="teacher-intro"><h1>Teacher <span>Dashboard</span></h1><p>Create, manage and publish assessments for your students.</p></section>
        <section className="teacher-panel teacher-create-panel" aria-labelledby="create-test-title"><h2 id="create-test-title">Create a Test</h2><p>Choose how you want to create a new assessment.</p><div className="teacher-creation-grid">{creationOptions.map(({ title, description, route, tone, Icon }) => <button key={title} type="button" onClick={() => router.push(route)} className={`teacher-creation-card teacher-tone-${tone}`}><Icon className="teacher-creation-icon" size={28} aria-hidden="true" /><span className="teacher-creation-title">{title}</span><span className="teacher-creation-description">{description}</span><span className="teacher-card-arrow"><ArrowRight size={17} /></span></button>)}</div></section>
        {features?.completeStudentReports !== false && <section className="teacher-panel teacher-performance-panel" aria-labelledby="performance-title"><div className="teacher-performance-header"><div className="teacher-tests-title"><span><TrendingUp size={23} /></span><div><h2 id="performance-title">Student Performance</h2><p>A live overview of your students&apos; test progress.</p></div></div><button type="button" className="teacher-view-link" onClick={() => router.push("/teacher/performance")}>View all <ArrowRight size={16} /></button></div>{performanceLoading && <div className="teacher-performance-empty">Loading student performance…</div>}{!performanceLoading && !performanceSummary && <div className="teacher-performance-empty">No student performance is available yet.</div>}{performanceSummary && <><div className="teacher-metrics"><div><span>Average score</span><strong>{performanceSummary.averageScore}%</strong></div><div><span>Average accuracy</span><strong>{performanceSummary.accuracy}%</strong></div><div><span>Active students</span><strong>{performanceSummary.activeStudents}<small> / {students.length}</small></strong></div></div><div className="teacher-top-students">{performanceSummary.topStudents.map((student, index) => <div key={student.id} className="teacher-student-row"><span className="teacher-rank">{index === 0 ? <Trophy size={16} /> : index + 1}</span><div><strong>{student.name}</strong><small>{student.batches || "No batch"} · {student.testsTaken} tests</small></div><b>{Math.round(student.averagePercentage)}%</b></div>)}</div></>}</section>}
        <section className="teacher-panel teacher-tests-panel" aria-labelledby="my-tests-title"><div className="teacher-tests-header"><div className="teacher-tests-title"><span><FileText size={23} /></span><div><h2 id="my-tests-title">My Tests</h2><p>View and manage the tests you&apos;ve created.</p></div></div><div className="teacher-table-controls"><label className="teacher-search"><Search size={17} /><span className="sr-only">Search tests</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search tests" /></label><button type="button" className={`teacher-filter-button ${showFilters ? "is-active" : ""}`} onClick={() => setShowFilters((value) => !value)}><Filter size={16} />Filter</button></div></div>
          {showFilters && <div className="teacher-filter-note">Use search to filter by test name, code, exam, or test type.</div>}
          {loading && <div className="teacher-empty-state">Loading your tests…</div>}{error && <div className="teacher-empty-state teacher-error-state">{error}</div>}{!loading && !error && visiblePapers.length === 0 && <div className="teacher-empty-state">{papers.length ? "No tests match your search." : "No tests created yet. Choose a method above to create your first test."}</div>}
          {!loading && !error && visiblePapers.length > 0 && <div className="teacher-table-wrap"><table className="teacher-tests-table"><thead><tr><th>Test name</th><th>Type</th><th>Exam</th><th>Questions</th><th>Duration</th></tr></thead><tbody>{visiblePapers.map((paper) => { const tone = paperTone(paper.status); return <tr key={paper.id}><td><div className="teacher-test-name"><span className={`teacher-test-file teacher-tone-${tone}`}><FileText size={17} /></span><div><strong>{paper.description || paper.code}</strong><small>{paper.exam || paper.code} · Created {formatDate(paper.created_at)}</small></div></div></td><td><span className={`teacher-type-badge teacher-tone-${tone}`}>{paper.status || "Test"}</span></td><td>{paper.exam || "—"}</td><td>{paper.question_count} questions</td><td><span className="teacher-duration"><Clock3 size={16} />{paper.duration_minutes} min</span></td></tr>; })}</tbody></table></div>}
        </section>
      </main>
    </div>
  </div>;
}
