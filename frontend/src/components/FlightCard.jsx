import React from 'react';
import { Plane, Clock, ArrowRight, ShieldCheck, Tag, Info } from 'lucide-react';

export default function FlightCard({ selectedFlight, flightOptions = [], isMockFlight = true, travelers = 2 }) {
  if (!selectedFlight || !selectedFlight.airline) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-surface-800 text-center text-slate-400">
        <Plane className="w-8 h-8 mx-auto text-slate-500 mb-2" />
        <p className="text-sm">No flight recommendations generated for this route.</p>
      </div>
    );
  }

  // Filter alternatives excluding the recommended flight
  const alternatives = flightOptions.filter(
    (f) => f.flight_number !== selectedFlight.flight_number
  );

  return (
    <div className="space-y-4">
      {/* Recommended Flight Card */}
      <div className="glass-card rounded-2xl p-6 border border-brand-500/30 relative overflow-hidden group hover:border-brand-400/50 transition-all">
        {/* Top Badges */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-surface-800">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-brand-500/20 text-brand-300 border border-brand-500/30 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5" />
              Recommended by Flight Agent
            </span>
            {isMockFlight ? (
              <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-surface-800 text-slate-400 border border-surface-700 flex items-center gap-1">
                <Info className="w-3 h-3 text-slate-400" />
                Demo Flight Engine
              </span>
            ) : (
              <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Amadeus Live API
              </span>
            )}
          </div>
          <div className="text-right">
            <span className="text-2xl font-extrabold text-white">₹{Number(selectedFlight.total_price || 0).toLocaleString('en-IN')}</span>
            <span className="text-xs text-slate-400 block">Total for {travelers} traveler{travelers > 1 ? 's' : ''}</span>
          </div>
        </div>

        {/* Flight Route Details */}
        <div className="py-5 grid grid-cols-1 sm:grid-cols-3 gap-4 items-center">
          {/* Departure */}
          <div>
            <div className="text-xs text-slate-400 font-medium">Departure</div>
            <div className="text-xl font-bold text-white mt-0.5">{selectedFlight.departure_time}</div>
            <div className="text-sm font-semibold text-slate-300 truncate">{selectedFlight.departure_city}</div>
          </div>

          {/* Duration & Stops Visual */}
          <div className="flex flex-col items-center justify-center text-center">
            <div className="text-xs text-slate-400 flex items-center gap-1 mb-1">
              <Clock className="w-3.5 h-3.5 text-brand-400" />
              <span>{selectedFlight.duration}</span>
            </div>
            <div className="w-full flex items-center justify-center space-x-2">
              <div className="h-0.5 flex-1 bg-surface-700"></div>
              <div className="w-6 h-6 rounded-full bg-brand-500/20 border border-brand-500/40 flex items-center justify-center">
                <Plane className="w-3 h-3 text-brand-300" />
              </div>
              <div className="h-0.5 flex-1 bg-surface-700"></div>
            </div>
            <div className="text-[11px] font-medium text-brand-400 mt-1">
              {selectedFlight.stops === 0 ? 'Non-Stop' : `${selectedFlight.stops} Stop${selectedFlight.stops > 1 ? 's' : ''}`}
            </div>
          </div>

          {/* Arrival */}
          <div className="text-right">
            <div className="text-xs text-slate-400 font-medium">Arrival</div>
            <div className="text-xl font-bold text-white mt-0.5">{selectedFlight.arrival_time}</div>
            <div className="text-sm font-semibold text-slate-300 truncate">{selectedFlight.arrival_city}</div>
          </div>
        </div>

        {/* Carrier Info Footer */}
        <div className="pt-4 border-t border-surface-800/80 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-200">{selectedFlight.airline}</span>
            <span className="text-surface-500">•</span>
            <span className="font-mono">{selectedFlight.flight_number}</span>
          </div>
          <div>
            <span>₹{Number(selectedFlight.price_per_person || (selectedFlight.total_price / travelers)).toLocaleString('en-IN')}/person</span>
          </div>
        </div>
      </div>

      {/* Alternative Flight Options */}
      {alternatives.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-1">
            Alternative Flight Options ({alternatives.length})
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {alternatives.map((alt, idx) => (
              <div
                key={idx}
                className="glass-card rounded-xl p-4 border border-surface-800 hover:border-surface-700 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-sm font-semibold text-white">{alt.airline}</span>
                    <span className="text-xs text-slate-400 block font-mono">{alt.flight_number}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-slate-200">₹{Number(alt.total_price).toLocaleString('en-IN')}</span>
                    <span className="text-[10px] text-slate-400 block">total</span>
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between text-xs text-slate-300 pt-2 border-t border-surface-800/60">
                  <span>{alt.departure_time} - {alt.arrival_time}</span>
                  <span className="text-slate-400">{alt.duration} • {alt.stops === 0 ? 'Non-Stop' : `${alt.stops} Stop`}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
