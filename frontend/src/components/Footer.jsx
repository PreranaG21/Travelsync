import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, Heart, Shield, Globe } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-surface-800/80 bg-surface-950/95 text-slate-400 text-sm mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Col 1: Brand & Tagline */}
          <div className="space-y-3 md:col-span-2">
            <Link to="/" className="flex items-center space-x-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center shadow-glow">
                <Plane className="w-4 h-4 text-white transform -rotate-45" />
              </div>
              <span className="text-xl font-bold text-white tracking-tight">TravelSync</span>
            </Link>
            <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
              AI Multi-Agent Travel Planning System. Plan smarter, travel better with real-time flight, hotel, weather, and activity optimization.
            </p>
          </div>

          {/* Col 2: Quick Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Navigation</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/" className="hover:text-brand-400 transition-colors">Home</Link>
              </li>
              <li>
                <Link to="/planner" className="hover:text-brand-400 transition-colors">Trip Planner</Link>
              </li>
              <li>
                <Link to="/my-trips" className="hover:text-brand-400 transition-colors">My Trips</Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-brand-400 transition-colors">Sign In</Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Attribution & Legal */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Attribution & Data</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Attractions and mapping information sourced via <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer" className="text-brand-400 hover:underline">OpenStreetMap</a> contributors.
            </p>
            <p className="text-xs text-slate-500">
              Weather data provided via Open-Meteo.
            </p>
          </div>
        </div>

        <div className="border-t border-surface-800/60 mt-10 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© {new Date().getFullYear()} TravelSync. Plan Smarter. Travel Better.</p>
          <div className="flex items-center space-x-4 mt-3 sm:mt-0">
            <span>Academic Multi-Agent Demonstration</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
