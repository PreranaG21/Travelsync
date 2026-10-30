import React, { useEffect, useState } from 'react';
import { 
  Bot, Plane, Building2, CloudSun, Compass, Calculator, 
  ShieldCheck, RefreshCw, CheckCircle2, Loader2, Sparkles 
} from 'lucide-react';

const AGENT_STEPS = [
  { id: 'intent', name: 'User Intent Agent', desc: 'Extracting destination, dates, budget & travel preferences...', icon: Bot },
  { id: 'flight', name: 'Flight Agent', desc: 'Searching airline routes, layovers & ranking flight fares...', icon: Plane },
  { id: 'hotel', name: 'Hotel Agent', desc: 'Querying PostgreSQL dataset for high-rated stays matching budget...', icon: Building2 },
  { id: 'weather', name: 'Weather Tool', desc: 'Retrieving 5-day forecast & rain probabilities from Open-Meteo...', icon: CloudSun },
  { id: 'activity', name: 'Activity Planner Agent', desc: 'Clustering attractions with Haversine distance & weather-safe slots...', icon: Compass },
  { id: 'budget', name: 'Budget Agent', desc: 'Executing deterministic financial math across flights, stays & food...', icon: Calculator },
  { id: 'critic', name: 'Critic / Validator Agent', desc: 'Auditing schedule realism, transit feasibility & budget compliance...', icon: ShieldCheck },
  { id: 'final', name: 'Final Assembly Agent', desc: 'Compiling structured day-by-day travel dashboard & agent telemetry...', icon: Sparkles }
];

export default function AgentProgress({ isGenerating }) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  useEffect(() => {
    if (!isGenerating) {
      setCurrentStepIndex(0);
      setElapsedSeconds(0);
      return;
    }

    // Step advancement timer (simulates realistic agent pipeline progress while LangGraph runs)
    const stepInterval = setInterval(() => {
      setCurrentStepIndex((prev) => (prev < AGENT_STEPS.length - 1 ? prev + 1 : prev));
    }, 700);

    const timerInterval = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(stepInterval);
      clearInterval(timerInterval);
    };
  }, [isGenerating]);

  return (
    <div className="w-full max-w-3xl mx-auto glass-card rounded-2xl p-6 sm:p-8 border border-brand-500/30 shadow-glow-lg animate-fade-in my-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-surface-800 gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center">
            <Loader2 className="w-5 h-5 text-brand-400 animate-spin" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span>TravelSync AI is Orchestrating Your Trip</span>
            </h3>
            <p className="text-xs text-slate-400">
              LangGraph StateGraph executing 7 specialized multi-agent nodes
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono bg-surface-900 px-3 py-1.5 rounded-lg border border-surface-700 text-brand-400 self-start sm:self-auto">
          <span>Elapsed:</span>
          <span className="font-bold text-white">{elapsedSeconds}s</span>
        </div>
      </div>

      {/* Steps List */}
      <div className="mt-6 space-y-3.5">
        {AGENT_STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isDone = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;
          const isPending = idx > currentStepIndex;

          return (
            <div
              key={step.id}
              className={`flex items-start space-x-4 p-3.5 rounded-xl transition-all duration-300 ${
                isCurrent
                  ? 'bg-brand-950/60 border border-brand-500/40 shadow-glow'
                  : isDone
                  ? 'bg-surface-900/40 border border-surface-800/80 text-slate-400'
                  : 'opacity-40 border border-transparent'
              }`}
            >
              {/* Status Icon */}
              <div className="shrink-0 mt-0.5">
                {isDone ? (
                  <div className="w-7 h-7 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" />
                  </div>
                ) : isCurrent ? (
                  <div className="w-7 h-7 rounded-lg bg-brand-500/20 border border-brand-400 flex items-center justify-center text-brand-300 animate-pulse">
                    <Loader2 className="w-4 h-4 animate-spin text-brand-400" />
                  </div>
                ) : (
                  <div className="w-7 h-7 rounded-lg bg-surface-800 flex items-center justify-center text-slate-500">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                )}
              </div>

              {/* Text info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className={`text-sm font-semibold ${isCurrent ? 'text-brand-300' : isDone ? 'text-slate-200' : 'text-slate-500'}`}>
                    {step.name}
                  </span>
                  {isCurrent && (
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
                      Processing
                    </span>
                  )}
                  {isDone && (
                    <span className="text-[10px] font-medium text-emerald-400">
                      Completed
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400 mt-0.5 truncate">
                  {step.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
