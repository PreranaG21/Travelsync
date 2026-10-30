import React, { useState } from 'react';
import { 
  Bot, Clock, ChevronDown, ChevronUp, Cpu, CheckCircle2, 
  Terminal, Sparkles, Database, ShieldCheck, ArrowRight, Layers 
} from 'lucide-react';

export default function AgentTransparencyDrawer({ agentLogs = [] }) {
  const [expandedIndex, setExpandedIndex] = useState(0);

  if (!agentLogs || agentLogs.length === 0) return null;

  const totalTimeMs = agentLogs.reduce((acc, log) => acc + (Number(log.execution_time) || 0), 0);

  const getAgentColor = (name = '') => {
    const n = name.toLowerCase();
    if (n.includes('intent')) return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
    if (n.includes('flight')) return 'text-sky-400 bg-sky-500/10 border-sky-500/30';
    if (n.includes('hotel')) return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30';
    if (n.includes('weather')) return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
    if (n.includes('activity')) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    if (n.includes('budget')) return 'text-rose-400 bg-rose-500/10 border-rose-500/30';
    if (n.includes('critic')) return 'text-purple-400 bg-purple-500/10 border-purple-500/30';
    if (n.includes('revision')) return 'text-orange-400 bg-orange-500/10 border-orange-500/30';
    return 'text-brand-400 bg-brand-500/10 border-brand-500/30';
  };

  return (
    <div className="glass-card rounded-2xl p-6 sm:p-8 border border-brand-500/30 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-surface-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-600 flex items-center justify-center shadow-glow">
            <Cpu className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span>How TravelSync Planned Your Trip</span>
              <span className="text-xs font-mono font-normal px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30">
                Multi-Agent Telemetry
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              Granular execution trace of all specialized agents in the LangGraph pipeline
            </p>
          </div>
        </div>

        {/* Total Execution Metric */}
        <div className="flex items-center space-x-2 text-xs font-mono bg-surface-900 px-3 py-1.5 rounded-xl border border-surface-700 text-slate-300 self-start sm:self-auto">
          <Clock className="w-4 h-4 text-brand-400" />
          <span>Total Agent Time: <strong className="text-brand-300 font-bold">{totalTimeMs.toFixed(1)} ms</strong></span>
        </div>
      </div>

      {/* Agents Accordion List */}
      <div className="space-y-3">
        {agentLogs.map((log, idx) => {
          const isExpanded = expandedIndex === idx;
          const colorClass = getAgentColor(log.agent_name);

          return (
            <div
              key={idx}
              className="rounded-xl border border-surface-800 bg-surface-900/50 overflow-hidden transition-all duration-200"
            >
              {/* Accordion Header */}
              <button
                onClick={() => setExpandedIndex(isExpanded ? -1 : idx)}
                className="w-full p-4 flex items-center justify-between hover:bg-surface-800/40 transition-colors text-left"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-7 h-7 rounded-lg border flex items-center justify-center text-xs font-bold ${colorClass}`}>
                    {idx + 1}
                  </div>
                  <div>
                    <span className="text-sm font-bold text-white block sm:inline">{log.agent_name}</span>
                    <span className="text-xs text-slate-400 sm:ml-2 block sm:inline font-mono">
                      ({Number(log.execution_time || 0).toFixed(1)} ms)
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <span className="text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    {log.status || 'SUCCESS'}
                  </span>
                  <div className="p-1 rounded bg-surface-800 text-slate-400">
                    {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </div>
                </div>
              </button>

              {/* Accordion Body */}
              {isExpanded && (
                <div className="p-4 pt-0 space-y-3 text-xs border-t border-surface-800/60 bg-surface-950/40">
                  {/* Inputs */}
                  {log.input_data && (
                    <div className="space-y-1">
                      <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                        <Terminal className="w-3 h-3 text-slate-400" />
                        Agent Input Parameters
                      </div>
                      <div className="bg-surface-950 p-3 rounded-lg border border-surface-800 text-slate-300 font-mono overflow-x-auto leading-relaxed">
                        {log.input_data}
                      </div>
                    </div>
                  )}

                  {/* Outputs & Reasoning */}
                  {log.output_data && (
                    <div className="space-y-1">
                      <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-brand-400" />
                        Agent Reasoning & Output
                      </div>
                      <div className="bg-surface-950 p-3 rounded-lg border border-surface-800 text-brand-300 font-mono overflow-x-auto leading-relaxed">
                        {log.output_data}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
