import React from 'react';
import { 
  Calculator, Plane, Building2, Ticket, Car, Utensils, 
  CheckCircle2, AlertTriangle, TrendingDown, ShieldCheck 
} from 'lucide-react';

export default function BudgetBreakdown({ budgetBreakdown, userBudget = 60000 }) {
  if (!budgetBreakdown) return null;

  const totalCost = Number(budgetBreakdown.total_cost || 0);
  const budget = Number(budgetBreakdown.budget || userBudget);
  const remaining = Number(budgetBreakdown.remaining_budget || (budget - totalCost));
  const status = budgetBreakdown.status || (totalCost <= budget ? 'UNDER_BUDGET' : 'OVER_BUDGET');
  const spentPct = Math.min(100, Math.round((totalCost / (budget || 1)) * 100));

  const items = [
    { name: 'Flights (Round Trip)', amount: budgetBreakdown.flight_cost || 0, icon: Plane, color: 'text-sky-400', bg: 'bg-sky-500/10' },
    { name: 'Accommodation / Hotel', amount: budgetBreakdown.hotel_cost || 0, icon: Building2, color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
    { name: 'Activities & Excursions', amount: budgetBreakdown.activity_cost || 0, icon: Ticket, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    { name: 'Local Transport & Transfers', amount: budgetBreakdown.transport_cost || 0, icon: Car, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { name: 'Food & Dining Allowance', amount: budgetBreakdown.food_cost || 0, icon: Utensils, color: 'text-orange-400', bg: 'bg-orange-500/10' },
  ];

  return (
    <div className="glass-card rounded-2xl p-6 sm:p-8 border border-surface-800 space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-surface-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center">
            <Calculator className="w-5 h-5 text-brand-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span>Financial Budget Analysis</span>
            </h3>
            <p className="text-xs text-slate-400">
              Deterministic calculation engine (Zero LLM arithmetic hallucination)
            </p>
          </div>
        </div>

        {/* Status Badge */}
        <div>
          {status === 'UNDER_BUDGET' && (
            <span className="px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5 shadow-sm">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              UNDER BUDGET ({budgetBreakdown.savings_percentage || Math.round((remaining/budget)*100)}% Saved)
            </span>
          )}
          {status === 'ON_BUDGET' && (
            <span className="px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-500/10 text-blue-300 border border-blue-500/30 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-blue-400" />
              ON BUDGET
            </span>
          )}
          {status === 'OVER_BUDGET' && (
            <span className="px-3 py-1.5 rounded-xl text-xs font-bold bg-rose-500/10 text-rose-300 border border-rose-500/30 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              OVER BUDGET (₹{Math.abs(remaining).toLocaleString('en-IN')})
            </span>
          )}
        </div>
      </div>

      {/* Overview Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-surface-900/70 p-4 rounded-xl border border-surface-800">
          <div className="text-xs text-slate-400 font-medium">Requested Target Budget</div>
          <div className="text-xl sm:text-2xl font-extrabold text-white mt-1">₹{budget.toLocaleString('en-IN')}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">User constraint</div>
        </div>

        <div className="bg-surface-900/70 p-4 rounded-xl border border-surface-800">
          <div className="text-xs text-slate-400 font-medium">Calculated Total Cost</div>
          <div className="text-xl sm:text-2xl font-extrabold text-brand-300 mt-1">₹{totalCost.toLocaleString('en-IN')}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">{spentPct}% of budget allocated</div>
        </div>

        <div className="bg-surface-900/70 p-4 rounded-xl border border-surface-800">
          <div className="text-xs text-slate-400 font-medium">Remaining Buffer</div>
          <div className={`text-xl sm:text-2xl font-extrabold mt-1 ${remaining >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            ₹{remaining.toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">{remaining >= 0 ? 'Available for shopping' : 'Exceeds budget'}</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div>
        <div className="flex justify-between text-xs font-semibold mb-2">
          <span className="text-slate-300">Budget Utilization</span>
          <span className="text-brand-400 font-mono">{spentPct}%</span>
        </div>
        <div className="w-full h-3 bg-surface-900 rounded-full overflow-hidden border border-surface-800">
          <div
            className={`h-full transition-all duration-700 ${
              spentPct > 100 ? 'bg-rose-500' : 'bg-gradient-to-r from-brand-500 to-sky-400'
            }`}
            style={{ width: `${Math.min(100, spentPct)}%` }}
          ></div>
        </div>
      </div>

      {/* Itemized Table */}
      <div className="space-y-2 pt-2">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          Itemized Expense Breakdown
        </h4>
        <div className="divide-y divide-surface-800/80 rounded-xl border border-surface-800 bg-surface-900/40 overflow-hidden">
          {items.map((item, idx) => {
            const Icon = item.icon;
            const itemPct = totalCost > 0 ? Math.round((item.amount / totalCost) * 100) : 0;
            return (
              <div key={idx} className="p-3.5 flex items-center justify-between hover:bg-surface-800/30 transition-colors">
                <div className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-lg ${item.bg} flex items-center justify-center`}>
                    <Icon className={`w-4 h-4 ${item.color}`} />
                  </div>
                  <div>
                    <span className="text-sm font-semibold text-white">{item.name}</span>
                    <span className="text-xs text-slate-400 block sm:inline sm:ml-2">({itemPct}% of total)</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-sm font-bold text-slate-200">
                    ₹{Number(item.amount).toLocaleString('en-IN')}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
