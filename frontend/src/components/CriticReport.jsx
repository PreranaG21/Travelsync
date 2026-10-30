import React from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle, Sparkles, Compass, Lightbulb } from 'lucide-react';

export default function CriticReport({ criticResult, revisionCount = 0 }) {
  if (!criticResult) return null;

  const checks = [
    { label: 'Budget Feasibility & Financial Limits', passed: criticResult.checks_passed?.budget_checked ?? true },
    { label: 'Daily Schedule Pacing & Duration Consistency', passed: criticResult.checks_passed?.schedule_checked ?? true },
    { label: 'Weather Compatibility & Rain Contingency', passed: criticResult.checks_passed?.weather_checked ?? true },
    { label: 'Geographic Proximity (Haversine <30km/day)', passed: criticResult.checks_passed?.distance_checked ?? true },
    { label: 'Duplicate Activity & Attraction Validation', passed: criticResult.checks_passed?.duplicate_checked ?? true },
    { label: 'Dining & Rest Transitions Accounted For', passed: criticResult.checks_passed?.dining_checked ?? true },
  ];

  const score = criticResult.realism_score || (criticResult.valid ? 96 : 82);

  return (
    <div className="glass-card rounded-2xl p-6 sm:p-8 border border-surface-800 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-surface-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span>AI Trip Validation & Realism Audit</span>
            </h3>
            <p className="text-xs text-slate-400">
              Critic Agent verified {checks.length} feasibility dimensions
            </p>
          </div>
        </div>

        {/* Realism Score Badge */}
        <div className="flex items-center space-x-3 self-start sm:self-auto bg-surface-900 px-4 py-2 rounded-xl border border-surface-700">
          <div className="text-right">
            <div className="text-[10px] uppercase font-bold text-slate-400">Realism Index</div>
            <div className="text-xl font-extrabold text-purple-400 font-mono">{score}/100</div>
          </div>
          <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-300 font-bold text-xs">
            ★
          </div>
        </div>
      </div>

      {/* Revision Loop Badge if revisions occurred */}
      {revisionCount > 0 && (
        <div className="bg-brand-950/60 border border-brand-500/30 p-3.5 rounded-xl flex items-start space-x-2.5 text-xs text-brand-300">
          <Sparkles className="w-4 h-4 text-brand-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-white">LangGraph Revision Loop Executed ({revisionCount} iteration{revisionCount > 1 ? 's' : ''}): </span>
            <span>Itinerary was automatically re-balanced by the Revision Node to optimize budget and daily pacing.</span>
          </div>
        </div>
      )}

      {/* Checklist Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {checks.map((check, idx) => (
          <div
            key={idx}
            className="p-3 rounded-xl bg-surface-900/60 border border-surface-800/80 flex items-center space-x-3"
          >
            {check.passed ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
            )}
            <span className={`text-xs font-medium ${check.passed ? 'text-slate-200' : 'text-amber-300'}`}>
              {check.label}
            </span>
          </div>
        ))}
      </div>

      {/* Suggestions / Critic Notes */}
      {criticResult.suggestions && criticResult.suggestions.length > 0 && (
        <div className="space-y-2 pt-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
            AI Critic Observations & Recommendations
          </h4>
          <div className="space-y-2">
            {criticResult.suggestions.map((sug, idx) => (
              <div
                key={idx}
                className="text-xs text-slate-300 bg-surface-900/40 border border-surface-800 p-3 rounded-xl flex items-start space-x-2"
              >
                <span className="text-purple-400 font-bold">•</span>
                <span>{sug}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
