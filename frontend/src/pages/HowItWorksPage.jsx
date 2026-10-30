import React, { useState } from 'react';
import { 
  Cpu, Layers, GitFork, RefreshCw, HelpCircle, ChevronDown, ChevronUp 
} from 'lucide-react';

const PRODUCT_FAQS = [
  {
    q: 'What is an AI Agent and why use a Multi-Agent Architecture instead of a single LLM prompt?',
    a: 'An AI Agent is an autonomous entity capable of perceiving context, making decisions, using external tools (databases, APIs), and executing actions towards a specific goal. Single-prompt LLM systems suffer from context overloading, hallucinated financial calculations, and lack of deterministic verification. Decomposing the system into specialized agents (Intent, Flight, Hotel, Activity, Budget, Critic) ensures modularity, tool specialization, and deterministic accuracy.'
  },
  {
    q: 'Why use LangGraph instead of standard sequential pipelines?',
    a: 'LangGraph allows modeling non-linear, cyclic workflows with stateful conditional routing. TravelSync requires a Critic Agent to inspect itineraries and route back into a Revision Loop when budget or pacing constraints fail. Linear chains cannot perform feedback loops or stateful cyclic re-planning.'
  },
  {
    q: 'What is Shared State in LangGraph and what does TravelState contain?',
    a: 'Shared State (TravelState) is a typed state dictionary passed and accumulated across graph nodes. In TravelSync, TravelState stores extracted user requirements, retrieved flight/hotel options, weather forecasts, scheduled activities, deterministic budget metrics, critic findings, revision counters, and execution logs.'
  },
  {
    q: 'Why are budget calculations handled deterministically rather than by the LLM?',
    a: 'LLMs are probabilistic language models prone to mathematical hallucinations and rounding errors. Financial budgeting requires exact deterministic arithmetic (Flight + Hotel + Activities + Transit + Food = Total Cost) to guarantee accurate expenditure metrics and compliance with target budgets.'
  },
  {
    q: 'How does the Haversine formula prevent unrealistic itineraries?',
    a: 'The Haversine formula calculates great-circle geographic distances between latitude and longitude coordinates. The Activity Planner Agent uses it to cluster nearby attractions on the same day, preventing impossible itineraries where travelers are scheduled to leap across distant regions within the same day.'
  },
  {
    q: 'How does TravelSync handle API failures gracefully?',
    a: 'TravelSync implements multi-tier fallback resilience. If Amadeus Flight API is unconfigured or rate-limited, high-fidelity mock flights are ranked. If Open-Meteo is offline, default climate projections are applied. If Gemini API is unreachable, a robust regex/rule-based intent parser operates without breaking the application.'
  }
];

export default function HowItWorksPage() {
  const [openFaqIndex, setOpenFaqIndex] = useState(0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 space-y-12">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto">
        <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
          System Architecture & Core Mechanics
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white mt-3">
          How TravelSync Works
        </h1>
        <p className="text-sm text-slate-400 mt-2 leading-relaxed">
          Deep dive into the state machine, specialized AI agents, and deterministic budgeting.
        </p>
      </div>

      {/* High-Level Architecture Flow Diagram */}
      <div className="glass-card rounded-3xl p-6 sm:p-10 border border-brand-500/30 shadow-glow space-y-8">
        <div className="flex items-center space-x-3 pb-4 border-b border-surface-800">
          <div className="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center">
            <GitFork className="w-5 h-5 text-brand-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Multi-Agent Orchestration Flow</h3>
            <p className="text-xs text-slate-400">Cyclic state machine with conditional Critic-Revision loop</p>
          </div>
        </div>

        {/* Visual Graph Pipeline */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-surface-900/80 border border-amber-500/30 space-y-2">
            <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">Node 1</span>
            <h4 className="text-sm font-bold text-white">Intent Agent</h4>
            <p className="text-xs text-slate-400">Gemini LLM parses natural language query into structured schema.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-sky-500/30 space-y-2">
            <span className="text-[10px] font-bold text-sky-400 uppercase tracking-wider block">Node 2</span>
            <h4 className="text-sm font-bold text-white">Flight Agent</h4>
            <p className="text-xs text-slate-400">Amadeus API / mock engine ranks routes by price & duration.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-indigo-500/30 space-y-2">
            <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider block">Node 3</span>
            <h4 className="text-sm font-bold text-white">Hotel Agent</h4>
            <p className="text-xs text-slate-400">Queries database for hotels by location, rating & budget.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-cyan-500/30 space-y-2">
            <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block">Node 4</span>
            <h4 className="text-sm font-bold text-white">Weather Tool</h4>
            <p className="text-xs text-slate-400">Queries Open-Meteo REST API for 5-day rain & temp forecast.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-emerald-500/30 space-y-2">
            <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Node 5</span>
            <h4 className="text-sm font-bold text-white">Activity Planner</h4>
            <p className="text-xs text-slate-400">Haversine clustering groups attractions to minimize daily travel.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-rose-500/30 space-y-2">
            <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">Node 6</span>
            <h4 className="text-sm font-bold text-white">Budget Agent</h4>
            <p className="text-xs text-slate-400">Deterministic calculation: Flights + Stays + Activities + Food.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-purple-500/30 space-y-2">
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider block">Node 7 (Conditional)</span>
            <h4 className="text-sm font-bold text-white">Critic Agent</h4>
            <p className="text-xs text-slate-400">Audits realism & conflicts. If invalid, routes to Revision Node.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface-900/80 border border-brand-500/30 space-y-2">
            <span className="text-[10px] font-bold text-brand-400 uppercase tracking-wider block">Node 8</span>
            <h4 className="text-sm font-bold text-white">Final Assembly</h4>
            <p className="text-xs text-slate-400">Assembles final dashboard and stores telemetry in DB.</p>
          </div>
        </div>

        {/* Highlight Banner */}
        <div className="p-4 rounded-2xl bg-surface-900 border border-surface-700 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-300">
          <div className="flex items-center space-x-2">
            <RefreshCw className="w-4 h-4 text-brand-400 animate-spin" style={{ animationDuration: '6s' }} />
            <span><strong>Conditional Feedback Loop:</strong> If the Critic detects budget excess or overloaded days, the Revision Node adjusts attractions and re-triggers Budget & Critic evaluation (Max 2 iterations).</span>
          </div>
        </div>
      </div>

      {/* Product FAQs Section */}
      <div className="glass-card rounded-3xl p-6 sm:p-10 border border-surface-800 space-y-6">
        <div className="flex items-center space-x-3 pb-4 border-b border-surface-800">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center">
            <HelpCircle className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Frequently Asked Questions & Product Architecture</h3>
            <p className="text-xs text-slate-400">Key theoretical and optimization details of the planning engine</p>
          </div>
        </div>

        <div className="space-y-3">
          {PRODUCT_FAQS.map((item, idx) => {
            const isOpen = openFaqIndex === idx;
            return (
              <div
                key={idx}
                className="rounded-xl border border-surface-800 bg-surface-900/40 overflow-hidden transition-all"
              >
                <button
                  onClick={() => setOpenFaqIndex(isOpen ? -1 : idx)}
                  className="w-full p-4 flex items-center justify-between text-left hover:bg-surface-800/40 transition-colors"
                >
                  <span className="text-sm font-bold text-white flex items-center gap-2">
                    <span className="text-brand-400 font-mono text-xs">Q{idx + 1}:</span>
                    {item.q}
                  </span>
                  <div className="p-1 rounded bg-surface-800 text-slate-400 shrink-0 ml-2">
                    {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </div>
                </button>

                {isOpen && (
                  <div className="p-4 pt-0 text-xs text-slate-300 leading-relaxed border-t border-surface-800/60 bg-surface-950/40">
                    <p className="p-3 rounded-lg bg-surface-900/80 border border-surface-800 text-slate-300 font-normal">
                      {item.a}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
