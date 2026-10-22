"use client";

import { useEffect, useRef, useState } from "react";

/* =========================================================
   MOTIVATIONAL LOADER
   ---------------------------------------------------------
   Shown while questions are being "loaded". Questions may
   already be available offline, but this screen keeps the
   student engaged with a countdown, animations and quotes
   so it feels like the backend is working hard for them.

   Props:
   - durationSeconds: how long the loader runs (default 3)
   - onComplete: called when the countdown finishes
   ========================================================= */

const QUOTES = [
  "Success is the sum of small efforts, repeated day in and day out.",
  "Believe you can and you're halfway there.",
  "The future belongs to those who believe in the beauty of their dreams.",
  "Don't watch the clock; do what it does. Keep going.",
  "Your limitation is only your imagination.",
  "Push yourself, because no one else is going to do it for you.",
  "Great things never come from comfort zones.",
  "Dream it. Wish it. Do it.",
];

const STATUS_MESSAGES = [
  "Connecting to secure exam server...",
  "Loading your questions...",
  "Preparing exam environment...",
  "Applying security settings...",
  "Almost ready...",
];

export default function MotivationalLoader({
  durationSeconds = 3,
  onComplete,
}: {
  durationSeconds?: number;
  onComplete: () => void;
}) {
  const [count, setCount] = useState(durationSeconds);
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [statusIndex, setStatusIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const startedRef = useRef(false);

  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;

    const interval = setInterval(() => {
      setCount((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    /* Rotate quotes and statuses while counting down */
    const quoteInterval = setInterval(() => {
      setQuoteIndex((prev) => (prev + 1) % QUOTES.length);
    }, 900);

    const statusInterval = setInterval(() => {
      setStatusIndex((prev) => (prev + 1) % STATUS_MESSAGES.length);
    }, 700);

    /* Smooth progress bar */
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) return 100;
        return prev + 10;
      });
    }, durationSeconds * 100);

    return () => {
      clearInterval(interval);
      clearInterval(quoteInterval);
      clearInterval(statusInterval);
      clearInterval(progressInterval);
    };
  }, [durationSeconds, onComplete]);

  return (
    <div className="fixed inset-0 z-50 bg-[#f5f7fb] flex flex-col items-center justify-center text-center p-6">
      {/* TOP: decorative glow */}
      <div className="absolute -top-20 -left-20 w-64 h-64 rounded-full bg-blue-50/40 blur-[100px] animate-pulse" />

      {/* Main card */}
      <div className="relative z-10 bg-white rounded-3xl border border-slate-200 shadow-2xl p-10 max-w-md w-full animate-[fadeIn_0.6s_ease-out]">
        {/* Header icon */}
        <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-blue-50 mb-6 text-2xl animate-bounce">
          📚
        </div>

        {/* Countdown */}
        <div className="mb-8">
          <span className="text-5xl font-black text-blue-600 tracking-tighter animate-pulse">
            {count}
          </span>
          <p className="mt-2 text-xs uppercase tracking-widest font-bold text-slate-400">
            seconds to go
          </p>
        </div>

        {/* Status message */}
        <div className="mb-6">
          <p className="text-sm font-medium text-slate-600">
            {STATUS_MESSAGES[statusIndex]}
          </p>
        </div>

        {/* Progress bar */}
        <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden mb-8 border border-slate-200">
          <div
            className="h-full bg-blue-600 rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Quote box */}
        <div className="relative rounded-2xl border border-slate-100 bg-slate-50 p-6 mb-8 animate-[float_3s_ease-in-out_infinite]">
          <div className="absolute left-4 top-4 text-slate-300 text-xl">&quot;</div>
          <p className="text-sm italic text-slate-700 leading-relaxed">
            {QUOTES[quoteIndex]}
          </p>
          <div className="absolute right-4 bottom-4 text-slate-300 text-xl">&quot;</div>
        </div>

        {/* Footer */}
        <div className="flex items-center gap-2 justify-center">
          <div className="h-2 w-2 rounded-full bg-blue-400 animate-ping" />
          <span className="text-xs text-slate-500 font-medium">
            Finalizing your paper…
          </span>
        </div>
      </div>

      {/* Bottom decorative glow */}
      <div className="absolute -bottom-20 -right-20 w-64 h-64 rounded-full bg-purple-50/40 blur-[100px] animate-pulse" />
    </div>
  );
}
