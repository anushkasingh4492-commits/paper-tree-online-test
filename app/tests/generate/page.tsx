"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { LeftSidebar } from "@/components/LeftSidebar";
import { TopNavbar } from "@/components/TopNavbar";
import {
  testSubjects,
  testDifficulties,
  testPresets,
} from "@/data/mock-dashboard";
import { StudentAvatar } from "@/components/StudentAvatar";
import { studentProfile } from "@/data/mock-dashboard";
import { Card } from "@/components/ui/Card";
import { Checkbox } from "@/components/ui/Checkbox";
import { Radio } from "@/components/ui/Radio";
import { Icon } from "@/components/Icon";
import { ArrowRight } from "lucide-react";

const SUBJECT_LABELS: Record<string, string> = {
  physics: "Physics",
  chemistry: "Chemistry",
  biology: "Biology",
};

export default function TestGeneratorPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [selectedChapters, setSelectedChapters] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState<string>("moderate");
  const [selectedPreset, setSelectedPreset] = useState<string>("half_paper");
  const [activeChapterTab, setActiveChapterTab] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const subjectsData = useMemo(
    () => testSubjects.map((s) => ({ ...s, chapters: s.chapters.map((c) => ({ ...c }))) }),
    []
  );

  const validationError = useMemo(() => {
    if (selectedSubjects.length === 0) {
      return "Please select at least one subject.";
    }
    return null;
  }, [selectedSubjects]);

  const activeError = error || validationError;

  const chapterCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    selectedSubjects.forEach((subjId) => {
      const subj = subjectsData.find((s) => s.id === subjId);
      counts[subjId] = subj?.chapters.filter((c) => c.selected).length ?? 0;
    });
    return counts;
  }, [selectedChapters, subjectsData, selectedSubjects]);

  const totalSelectedChapters = useMemo(
    () => Object.values(chapterCounts).reduce((a, b) => a + b, 0),
    [chapterCounts]
  );

  const activePreset = testPresets.find((p) => p.id === selectedPreset);

  const config = useMemo(() => {
    const totalMarks = activePreset?.totalMarks ?? 100;
    const durationMinutes = activePreset
      ? parseInt(activePreset.duration.replace(" minutes", ""))
      : 90;
    return { totalQuestions: totalMarks, totalMarks, durationMinutes };
  }, [activePreset]);

  const handleGenerateTest = async () => {
    if (activeError) {
      setError(activeError);
      return;
    }
    if (totalSelectedChapters === 0) {
      setError("Please select at least one chapter.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      router.push("/test-summary");
    }, 1500);
  };

  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-surface-app-bg text-text-primary">
      <div className="fixed xl:relative xl:inset-0 xl:top-0 xl:left-0 xl:h-screen xl:w-[220px] xl:border-r xl:border-border-default xl:flex xl:flex-col z-50 bg-surface-surface">
        <div className="h-[82px] px-5 flex items-center gap-3 border-b border-border-default">
          <div className="w-9 h-9 rounded-[11px] bg-brand-primary text-white flex items-center justify-center font-black text-lg shadow-sm">
            IC
          </div>
          <div className="flex flex-col">
            <div className="font-extrabold text-[15px] leading-4 text-text-primary">
              Infinity Classes
            </div>
            <div className="text-[9px] font-semibold tracking-[.17em] text-text-supporting-label mt-1">
              EDUCATIONAL STUDIO
            </div>
          </div>
        </div>
        <div className="px-4 pt-5 flex-1 overflow-y-auto">
          <p className="px-2 mb-2 text-[9px] uppercase tracking-[.16em] font-bold text-text-supporting-label">
            Workspace
          </p>
          <nav className="space-y-1">
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl bg-surface-subtle text-brand-purple text-xs font-bold">
              <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                <Icon name="home" size={16} className="text-brand-purple" />
              </span>
              Dashboard
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="test-tube" size={16} className="text-text-secondary" />
              </span>
              My Tests
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="analytics" size={16} className="text-text-secondary" />
              </span>
              Test Summary
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="trophy" size={16} className="text-text-secondary" />
              </span>
              Batch Leaderboard
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="book" size={16} className="text-text-secondary" />
              </span>
              Mistake Notebook
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="user" size={16} className="text-text-secondary" />
              </span>
              Edit Profile
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="star" size={16} className="text-text-secondary" />
              </span>
              My Achievements
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="alert" size={16} className="text-text-secondary" />
              </span>
              Boss Fight Queue
            </button>
            <button className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-text-secondary hover:bg-surface-app-bg text-xs font-medium">
              <span className="w-7 h-7 rounded-lg bg-surface-app-bg flex items-center justify-center">
                <Icon name="grid" size={16} className="text-text-secondary" />
              </span>
              Weak Areas Test
            </button>
          </nav>
        </div>
      </div>

      <main className="flex-1 w-full min-w-0 ml-0 xl:ml-[220px]">
        <TopNavbar />

        <div className="px-5 py-6 lg:px-8 lg:py-8">
          <div className="flex items-center justify-between gap-4 mb-8">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-2xl shadow-lg">
                <Icon name="test-tube" size={24} className="text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">
                    TEST GENERATOR
                  </span>
                </div>
                <h1 className="text-[24px] font-black text-text-primary tracking-tight">
                  Create a New Test
                </h1>
                <p className="text-[12px] text-text-body mt-1">
                  Configure your test and start practising with questions from the Paper Tree question bank.
                </p>
              </div>
            </div>
            <StudentAvatar
              avatarKey={studentProfile.avatarKey}
              name={studentProfile.firstName}
              size={32}
            />
          </div>

          <Card variant="default" padding="md" radius="large" className="border border-border-default mb-6">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-14 h-14 rounded-xl bg-surface-subtle flex items-center justify-center text-brand-purple">
                <Icon name="graduation-cap" size={28} />
              </div>
              <div className="flex-1">
                <div className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">
                  Your Assigned Course
                </div>
                <div className="text-[13px] font-bold text-text-primary">Your course is assigned by your academy.</div>
                <div className="mt-2 rounded-xl border border-brand-purple/20 bg-brand-purple/5 px-3 py-1">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-brand-purple flex items-center justify-center text-[10px] font-bold text-white">
                      P
                    </div>
                    <div className="text-xs font-bold text-text-primary">NEET</div>
                  </div>
                  <div className="text-[10px] text-text-body mt-1">
                    PCB – Physics + Chemistry + Biology
                  </div>
                  <div className="text-[10px] text-text-body mt-1">
                    This course and group were assigned by your academy and cannot be changed.
                  </div>
                </div>
              </div>
            </div>
          </div>
