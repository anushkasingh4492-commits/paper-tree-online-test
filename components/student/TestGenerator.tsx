"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  Check,
  CircleHelp,
  Clock3,
  FileCheck2,
  Minus,
  Plus,
} from "lucide-react";
import {
  MARKS_PER_QUESTION,
  MINUTES_PER_MARK,
  PRESETS,
  ROUND_MINUTES,
  type Preset,
  type PresetSubject,
} from "@/lib/test-presets";
import StudentWorkspace from "./StudentWorkspace";
import { fetchStudentData } from "./student-api";
import type { DashboardPayload, GeneratorChapter } from "./student-types";

type GeneratorData = {
  success?: boolean;
  error?: string;
  course: string;
  exam: string;
  chapters: GeneratorChapter[];
};

function displaySubject(value: string) {
  const normalized = value.trim().toLowerCase();
  if (["math", "maths", "mathematics"].includes(normalized)) return "Mathematics";
  if (["bio", "biology"].includes(normalized)) return "Biology";
  if (normalized === "physics") return "Physics";
  if (normalized === "chemistry") return "Chemistry";
  return value.trim().replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function presetSubjectName(subject: PresetSubject) {
  if (subject === "maths" || subject === "jee-maths") return "Mathematics";
  if (subject === "biology") return "Biology";
  if (subject.endsWith("physics")) return "Physics";
  if (subject.endsWith("chemistry")) return "Chemistry";
  return subject;
}

function presetDetails(preset: Preset) {
  const questions = Object.values(preset.subjects).reduce((sum, count) => sum + (count ?? 0), 0);
  const marks = Object.entries(preset.subjects).reduce((sum, [subject, count]) => {
    const key = subject as PresetSubject;
    return sum + (count ?? 0) * (MARKS_PER_QUESTION[key] ?? 1);
  }, 0);
  const minutes = marks * MINUTES_PER_MARK;
  const duration = Math.ceil(minutes / ROUND_MINUTES) * ROUND_MINUTES;
  return { questions, marks, duration };
}

function canonicalExam(value: string) {
  if (value === "mhtcet") return "MHT-CET";
  return value.toUpperCase();
}

export default function TestGenerator() {
  const router = useRouter();
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [generator, setGenerator] = useState<GeneratorData | null>(null);
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [activeSubject, setActiveSubject] = useState("");
  const [selectedChapters, setSelectedChapters] = useState<Record<string, string[]>>({});
  const [difficulty, setDifficulty] = useState("Balanced");
  const [selectedPresetId, setSelectedPresetId] = useState("");
  const [loadingData, setLoadingData] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchStudentData<DashboardPayload>("/api/dashboard"),
      fetchStudentData<GeneratorData>("/api/student/test-generator"),
    ])
      .then(([dashboardData, generatorData]) => {
        if (!active) return;
        const availableSubjects = [...new Set(generatorData.chapters.map((chapter) => displaySubject(chapter.subject)))];
        setDashboard(dashboardData);
        setGenerator(generatorData);
        setSelectedSubjects(availableSubjects);
        setActiveSubject(availableSubjects[0] ?? "");
      })
      .catch((reason: unknown) => {
        if (active) setLoadError(reason instanceof Error ? reason.message : "Could not load test generator data.");
      })
      .finally(() => { if (active) setLoadingData(false); });
    return () => { active = false; };
  }, []);

  const availableSubjects = useMemo(
    () => [...new Set((generator?.chapters ?? []).map((chapter) => displaySubject(chapter.subject)))],
    [generator?.chapters]
  );
  const chaptersBySubject = useMemo(() => {
    const groups = new Map<string, GeneratorChapter[]>();
    (generator?.chapters ?? []).forEach((item) => {
      const subject = displaySubject(item.subject);
      groups.set(subject, [...(groups.get(subject) ?? []), item]);
    });
    return groups;
  }, [generator?.chapters]);
  const currentChapters = chaptersBySubject.get(activeSubject) ?? [];
  const matchingPresets = useMemo(() => {
    const wanted = [...selectedSubjects].sort();
    if (!wanted.length) return [];
    return PRESETS.filter((preset) => {
      const includes = Object.keys(preset.subjects).map((subject) => presetSubjectName(subject as PresetSubject)).sort();
      return includes.length === wanted.length && includes.every((subject, index) => subject === wanted[index]);
    });
  }, [selectedSubjects]);
  const selectedPreset = matchingPresets.find((preset) => preset.id === selectedPresetId) ?? matchingPresets[0];

  const presetSummary = selectedPreset ? presetDetails(selectedPreset) : null;
  const chapterCount = selectedSubjects.reduce((count, subject) => count + (selectedChapters[subject]?.length ?? 0), 0);
  const selectedQuestionAvailability = useMemo(() => {
    if (!selectedPreset) return 0;
    return Object.entries(selectedPreset.subjects).reduce((available, [rawSubject, needed]) => {
      const subject = presetSubjectName(rawSubject as PresetSubject);
      const chapters = selectedChapters[subject] ?? [];
      const candidates = chaptersBySubject.get(subject) ?? [];
      const count = chapters.length
        ? candidates.filter((item) => chapters.includes(item.chapter)).reduce((sum, item) => sum + item.questionCount, 0)
        : candidates.reduce((sum, item) => sum + item.questionCount, 0);
      return available + Math.min(count, needed ?? 0);
    }, 0);
  }, [chaptersBySubject, selectedChapters, selectedPreset]);
  const isShortOnQuestions = Boolean(presetSummary && selectedQuestionAvailability < presetSummary.questions);
  const studentName = dashboard?.student?.name ?? "";
  const courseName = generator?.course ?? dashboard?.assignment?.courseName ?? "";

  function toggleSubject(subject: string) {
    setSelectedSubjects((current) => {
      const next = current.includes(subject) ? current.filter((value) => value !== subject) : [...current, subject];
      setActiveSubject((active) => next.includes(active) ? active : next[0] ?? "");
      return next;
    });
  }

  function toggleChapter(chapter: string) {
    setSelectedChapters((current) => {
      const selected = current[activeSubject] ?? [];
      const next = selected.includes(chapter) ? selected.filter((item) => item !== chapter) : [...selected, chapter];
      return { ...current, [activeSubject]: next };
    });
  }

  function selectAllChapters() {
    setSelectedChapters((current) => ({ ...current, [activeSubject]: currentChapters.map((item) => item.chapter) }));
  }

  function clearChapters() {
    setSelectedChapters((current) => ({ ...current, [activeSubject]: [] }));
  }

  async function generateTest() {
    setError("");
    if (!selectedSubjects.length) {
      setError("Choose at least one subject.");
      return;
    }
    if (!selectedPreset) {
      setError("There is no matching test preset for the selected subjects.");
      return;
    }
    if (isShortOnQuestions) {
      setError("The selected chapters do not have enough questions for this preset. Choose more chapters or a shorter preset.");
      return;
    }

    setGenerating(true);
    try {
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          exam: canonicalExam(generator?.exam ?? ""),
          course: courseName,
          subjects: selectedSubjects,
          chaptersBySubject: Object.fromEntries(
            selectedSubjects.map((subject) => [subject, selectedChapters[subject] ?? []])
          ),
          difficulty,
          presetId: selectedPreset.id,
          questionCount: presetSummary?.questions,
          duration: presetSummary?.duration,
        }),
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.error || "Could not generate your test.");
      if (!result.testId) throw new Error("The generated test did not return a test ID.");
      router.push(`/test/${result.testId}/result`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not generate your test.");
    } finally {
      setGenerating(false);
    }
  }

  if (loadingData || loadError) {
    return (
      <StudentWorkspace active="tests" studentName={studentName} courseName={courseName}>
        {loadingData ? <div className="test-generator-loading">Loading your assigned course…</div> : <div className="test-generator-error" role="alert">{loadError}</div>}
      </StudentWorkspace>
    );
  }

  return (
    <StudentWorkspace active="tests" studentName={studentName} courseName={courseName}>
      <div className="test-generator">
        <div className="test-generator__intro">
          <div className="test-generator__eyebrow"><FileCheck2 size={15} /> ASSIGNED COURSE: {courseName || "—"}</div>
          <h1>Build your practice test</h1>
          <p>Choose your subjects, chapters, and test format. Your question bank and course assignment determine what is available.</p>
        </div>
        <div className="test-generator__layout">
          <div className="test-generator__steps">
            <section className="test-generator-card">
              <div className="test-generator-card__heading"><span className="test-generator-step">01</span><div><h2>Choose subjects</h2><p>Select the subjects you want to practise.</p></div></div>
              <div className="test-generator-subjects">
                {availableSubjects.map((subject) => {
                  const selected = selectedSubjects.includes(subject);
                  return (
                    <button className={`test-generator-subject ${selected ? "is-selected" : ""}`} type="button" key={subject} onClick={() => toggleSubject(subject)} aria-pressed={selected}>
                      <span className="test-generator-subject__check">{selected && <Check size={14} />}</span>
                      <span><strong>{subject}</strong><small>{chaptersBySubject.get(subject)?.length ?? 0} available chapters</small></span>
                    </button>
                  );
                })}
              </div>
              {availableSubjects.some((subject) => subject === "Biology") && availableSubjects.some((subject) => subject === "Mathematics") && <p className="test-generator-note"><CircleHelp size={14} /> Biology and Mathematics are in separate course groups. Select the subject assigned to your batch.</p>}
              {!selectedSubjects.length && <p className="test-generator-warning" role="alert">Select at least one subject to continue.</p>}
            </section>

            <section className="test-generator-card">
              <div className="test-generator-card__heading"><span className="test-generator-step">02</span><div><h2>Choose chapters</h2><p>Select one or more chapters, or leave all clear to include every available chapter.</p></div></div>
              {selectedSubjects.length ? (
                <>
                  <div className="test-generator-chapter-tabs" role="tablist" aria-label="Subject chapters">
                    {selectedSubjects.map((subject) => <button key={subject} type="button" role="tab" aria-selected={activeSubject === subject} className={activeSubject === subject ? "is-active" : ""} onClick={() => setActiveSubject(subject)}>{subject}</button>)}
                  </div>
                  <div className="test-generator-chapter-actions">
                    <span>{selectedChapters[activeSubject]?.length ?? 0} selected</span>
                    <button type="button" onClick={selectAllChapters}><Plus size={13} /> Select all</button>
                    <button type="button" onClick={clearChapters}><Minus size={13} /> Clear</button>
                  </div>
                  <div className="test-generator-chapter-list">
                    {currentChapters.map((item) => {
                      const checked = (selectedChapters[activeSubject] ?? []).includes(item.chapter);
                      return <label key={item.chapter} className={checked ? "is-selected" : ""}><input type="checkbox" checked={checked} onChange={() => toggleChapter(item.chapter)} /><span>{item.chapter}</span><small>{item.questionCount} questions</small></label>;
                    })}
                    {!currentChapters.length && <p className="test-generator-note">No chapters are available for this subject in your assigned course.</p>}
                  </div>
                </>
              ) : <p className="test-generator-note">Choose a subject to view its chapters.</p>}
            </section>

            <section className="test-generator-card">
              <div className="test-generator-card__heading"><span className="test-generator-step">03</span><div><h2>Select difficulty</h2><p>Choose the question difficulty mix for this test.</p></div></div>
              <div className="test-generator-difficulties">
                {[
                  { name: "Easy", description: "Build confidence" },
                  { name: "Moderate", description: "Steady practice" },
                  { name: "Balanced", description: "A varied mix" },
                  { name: "Hard", description: "Challenge yourself" },
                ].map((item) => <button type="button" key={item.name} aria-pressed={difficulty === item.name} className={difficulty === item.name ? "is-selected" : ""} onClick={() => setDifficulty(item.name)}><strong>{item.name}</strong><small>{item.description}</small></button>)}
              </div>
            </section>

            <section className="test-generator-card">
              <div className="test-generator-card__heading"><span className="test-generator-step">04</span><div><h2>Choose a test preset</h2><p>Question split, marks, and duration are calculated from the selected preset.</p></div></div>
              {matchingPresets.length ? <div className="test-generator-presets">
                {matchingPresets.map((preset) => {
                  const summary = presetDetails(preset);
                  const selected = preset.id === (selectedPreset?.id ?? selectedPresetId);
                  return <button type="button" key={preset.id} aria-pressed={selected} className={selected ? "is-selected" : ""} onClick={() => setSelectedPresetId(preset.id)}>
                    <span className="test-generator-preset-radio">{selected && <i />}</span><span className="test-generator-preset-name">{preset.name}</span><span className="test-generator-preset-detail">{summary.questions} questions</span><span className="test-generator-preset-detail">{summary.marks} marks · {summary.duration} min</span>
                  </button>;
                })}
              </div> : <p className="test-generator-warning" role="alert">No preset is available for this subject combination.</p>}
            </section>
          </div>

          <aside className="test-generator-summary">
            <div className="test-generator-summary__top"><p>TEST SUMMARY</p><h2>{courseName || "Practice test"}</h2><span>Review your configuration before generating.</span></div>
            <div className="test-generator-summary__rows">
              <div><span>Subjects</span><strong>{selectedSubjects.length ? selectedSubjects.join(", ") : "—"}</strong></div>
              <div><span>Chapters selected</span><strong>{chapterCount}</strong></div>
              <div><span>Preset</span><strong>{selectedPreset?.name ?? "—"}</strong></div>
              <div><span>Total questions</span><strong>{displayCount(presetSummary?.questions)}</strong></div>
              <div><span>Total marks</span><strong>{displayCount(presetSummary?.marks)}</strong></div>
              <div><span>Duration</span><strong>{presetSummary ? `${presetSummary.duration} min` : "—"}</strong></div>
              <div><span>Difficulty</span><strong>{difficulty}</strong></div>
            </div>
            {isShortOnQuestions && <p className="test-generator-warning" role="alert">Selected chapters provide {selectedQuestionAvailability} matching questions; this preset requires {presetSummary?.questions}.</p>}
            {error && <p className="test-generator-error" role="alert">{error}</p>}
            <button type="button" disabled={generating || !selectedPreset || isShortOnQuestions} onClick={generateTest} className="test-generator-summary__button">{generating ? "Generating…" : "Generate test"} <ArrowRight size={17} /></button>
            <p className="test-generator-summary__foot"><Clock3 size={14} /> Your test is created from your academy’s live question bank.</p>
          </aside>
        </div>
      </div>
    </StudentWorkspace>
  );
}

function displayCount(value?: number) {
  return value === undefined ? "—" : value.toLocaleString();
}
