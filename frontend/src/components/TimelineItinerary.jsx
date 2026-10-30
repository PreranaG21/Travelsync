import React, { useState } from 'react';
import { 
  Calendar, Clock, MapPin, Tag, IndianRupee, 
  Palmtree, Compass, Utensils, Landmark, TreePine, Moon, Luggage, ChevronDown, ChevronUp 
} from 'lucide-react';

export default function TimelineItinerary({ activities = [], destination = 'Bali' }) {
  const [expandedDays, setExpandedDays] = useState(
    activities.reduce((acc, _, idx) => ({ ...acc, [idx]: true }), {})
  );

  const toggleDay = (idx) => {
    setExpandedDays((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const getCategoryBadge = (category = '') => {
    const cat = category.toLowerCase();
    if (cat === 'beaches') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 flex items-center gap-1">
          <Palmtree className="w-3 h-3" /> Beach
        </span>
      );
    }
    if (cat === 'adventure') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-500/10 text-amber-300 border border-amber-500/20 flex items-center gap-1">
          <Compass className="w-3 h-3" /> Adventure
        </span>
      );
    }
    if (cat === 'food') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-orange-500/10 text-orange-300 border border-orange-500/20 flex items-center gap-1">
          <Utensils className="w-3 h-3" /> Culinary
        </span>
      );
    }
    if (cat === 'culture') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center gap-1">
          <Landmark className="w-3 h-3" /> Culture
        </span>
      );
    }
    if (cat === 'nature') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 flex items-center gap-1">
          <TreePine className="w-3 h-3" /> Nature
        </span>
      );
    }
    if (cat === 'nightlife') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-pink-500/10 text-pink-300 border border-pink-500/20 flex items-center gap-1">
          <Moon className="w-3 h-3" /> Evening
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-300 border border-slate-700 flex items-center gap-1">
        <Luggage className="w-3 h-3" /> Logistics
      </span>
    );
  };

  if (!activities || activities.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-8 text-center text-slate-400">
        <Calendar className="w-10 h-10 mx-auto text-slate-500 mb-3" />
        <p>No activity schedule generated.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {activities.map((dayData, dayIdx) => {
        const isExpanded = expandedDays[dayIdx] !== false;
        const dayWeather = dayData.weather || {};

        return (
          <div
            key={dayIdx}
            className="glass-card rounded-2xl border border-surface-800 overflow-hidden transition-all duration-200"
          >
            {/* Day Header Accordion Toggle */}
            <button
              onClick={() => toggleDay(dayIdx)}
              className="w-full p-5 sm:p-6 bg-surface-900/60 hover:bg-surface-900/90 transition-colors flex items-center justify-between text-left"
            >
              <div className="flex flex-wrap items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center font-bold text-brand-300">
                  D{dayData.day}
                </div>
                <div>
                  <h4 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <span>Day {dayData.day}: {dayData.theme}</span>
                  </h4>
                  <div className="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
                    <span>{dayData.activities?.length || 0} scheduled activities</span>
                    {dayWeather.temp_max && (
                      <>
                        <span className="text-surface-600">•</span>
                        <span className="text-sky-300">{dayWeather.condition} ({dayWeather.temp_max}°C)</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="text-right hidden sm:block">
                  <span className="text-xs text-slate-400 block">Est. Day Spend</span>
                  <span className="text-sm font-bold text-slate-200">
                    ₹{Number(dayData.day_total_cost || 0).toLocaleString('en-IN')}
                  </span>
                </div>
                <div className="p-1 rounded-lg bg-surface-800 text-slate-400">
                  {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                </div>
              </div>
            </button>

            {/* Timeline Activities List */}
            {isExpanded && (
              <div className="p-5 sm:p-6 pt-2 space-y-4">
                <div className="relative pl-6 sm:pl-8 space-y-6 before:content-[''] before:absolute before:left-2 sm:before:left-3 before:top-3 before:bottom-3 before:w-0.5 before:bg-surface-800">
                  {dayData.activities?.map((act, actIdx) => (
                    <div key={actIdx} className="relative group">
                      {/* Timeline Dot */}
                      <div className="absolute -left-6 sm:-left-8 top-1.5 w-4 h-4 rounded-full bg-surface-950 border-2 border-brand-400 group-hover:border-brand-300 group-hover:scale-110 transition-all"></div>

                      {/* Activity Card */}
                      <div className="glass-card rounded-xl p-4 border border-surface-800/90 group-hover:border-brand-500/30 transition-all">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2">
                          <div className="flex items-center space-x-2">
                            <span className="px-2 py-0.5 rounded bg-surface-900 text-brand-300 font-mono text-xs font-semibold border border-surface-700 flex items-center gap-1">
                              <Clock className="w-3 h-3 text-brand-400" />
                              {act.time}
                            </span>
                            {getCategoryBadge(act.category)}
                          </div>
                          {act.cost > 0 && (
                            <div className="text-xs font-semibold text-slate-300">
                              ₹{Number(act.cost).toLocaleString('en-IN')}
                            </div>
                          )}
                        </div>

                        <h5 className="text-sm sm:text-base font-bold text-white group-hover:text-brand-300 transition-colors mt-1">
                          {act.title}
                        </h5>

                        <div className="flex items-center space-x-1 text-xs text-slate-400 mt-1">
                          <MapPin className="w-3.5 h-3.5 text-brand-400 shrink-0" />
                          <span className="truncate">{act.location}</span>
                        </div>

                        {act.notes && (
                          <p className="text-xs text-slate-400 mt-2 bg-surface-900/50 p-2 rounded-lg border border-surface-800/80">
                            {act.notes}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
