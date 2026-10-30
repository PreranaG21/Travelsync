import React from 'react';
import { CloudSun, Sun, CloudRain, Cloud, Zap, Droplets, Info } from 'lucide-react';

export default function WeatherCard({ weather }) {
  if (!weather || !weather.forecast || weather.forecast.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-surface-800 text-center text-slate-400">
        <CloudSun className="w-8 h-8 mx-auto text-slate-500 mb-2" />
        <p className="text-sm">Weather information temporarily unavailable.</p>
      </div>
    );
  }

  const getWeatherIcon = (cond = '') => {
    const c = cond.toLowerCase();
    if (c.includes('thunder') || c.includes('storm')) {
      return <Zap className="w-6 h-6 text-amber-400" />;
    }
    if (c.includes('rain') || c.includes('drizzle') || c.includes('shower')) {
      return <CloudRain className="w-6 h-6 text-sky-400" />;
    }
    if (c.includes('cloud') || c.includes('overcast')) {
      return <Cloud className="w-6 h-6 text-slate-400" />;
    }
    return <Sun className="w-6 h-6 text-amber-400" />;
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-surface-800 space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-surface-800">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center">
            <CloudSun className="w-4 h-4 text-sky-400" />
          </div>
          <div>
            <h4 className="text-base font-bold text-white">Weather Forecast & Activity Compatibility</h4>
            <p className="text-xs text-slate-400">Provided by Open-Meteo REST API</p>
          </div>
        </div>
        <span className="text-xs font-medium text-sky-300 bg-sky-500/10 border border-sky-500/20 px-2.5 py-1 rounded-lg">
          Live Climate Feed
        </span>
      </div>

      {/* Summary Banner */}
      {weather.summary && (
        <div className="text-xs text-slate-300 bg-surface-900/80 border border-surface-800 p-3 rounded-xl flex items-start space-x-2">
          <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
          <span>{weather.summary}</span>
        </div>
      )}

      {/* 5-Day Forecast Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 pt-1">
        {weather.forecast.map((day, idx) => (
          <div
            key={idx}
            className="glass-card rounded-xl p-3.5 border border-surface-800/90 text-center flex flex-col justify-between hover:border-surface-700 transition-colors"
          >
            <div>
              <div className="text-xs font-bold text-slate-200">Day {day.day}</div>
              <div className="text-[10px] text-slate-400">{day.date}</div>
              
              <div className="my-3 flex justify-center">
                {getWeatherIcon(day.condition)}
              </div>

              <div className="text-xs font-semibold text-white">{day.condition}</div>
              <div className="text-sm font-extrabold text-white mt-1">
                {day.temp_max}° <span className="text-slate-400 text-xs font-normal">/ {day.temp_min}°C</span>
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-surface-800/80">
              <div className="flex items-center justify-center space-x-1 text-[11px] text-sky-300 mb-1.5">
                <Droplets className="w-3 h-3" />
                <span>{day.rain_probability}% Rain</span>
              </div>
              <span
                className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                  day.is_outdoor_suitable
                    ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                    : 'bg-amber-500/10 text-amber-300 border border-amber-500/20'
                }`}
              >
                {day.is_outdoor_suitable ? 'Outdoor Ready' : 'Indoor Preferred'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
