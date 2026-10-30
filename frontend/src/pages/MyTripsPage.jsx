import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  History, Search, Sparkles, MapPin, Calendar, Users, 
  IndianRupee, ArrowRight, Clock, AlertCircle, RefreshCw, LogIn, User 
} from 'lucide-react';
import { getSavedTrips } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function MyTripsPage() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState('');

  const loadTrips = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getSavedTrips(30);
      setTrips(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Failed to load trips:', err);
      setError(
        err.friendlyMessage ||
        'Could not connect to backend server. Make sure Node.js and AI service are running.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTrips();
  }, [isAuthenticated]);

  const filteredTrips = trips.filter((t) => {
    const q = searchQuery.toLowerCase();
    return (
      (t.destination && t.destination.toLowerCase().includes(q)) ||
      (t.user_request && t.user_request.toLowerCase().includes(q)) ||
      (t.id && t.id.toLowerCase().includes(q))
    );
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-surface-800">
        <div>
          <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
            {isAuthenticated ? `Travel Archive • ${user?.name}` : 'Trip Archive'}
          </span>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white mt-2">
            Saved Travel Itineraries
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Browse and review previously generated multi-agent travel plans.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {!isAuthenticated && (
            <Link
              to="/login"
              className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-surface-900 text-slate-300 border border-surface-700 text-xs font-semibold hover:text-white"
            >
              <LogIn className="w-3.5 h-3.5 text-brand-400" />
              <span>Sign In to Sync</span>
            </Link>
          )}

          <button
            onClick={loadTrips}
            className="p-2.5 rounded-xl bg-surface-900 border border-surface-700 text-slate-300 hover:text-white hover:bg-surface-800 transition-colors"
            title="Refresh Trips"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <Link
            to="/planner"
            className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-500 to-sky-500 text-white font-semibold text-xs sm:text-sm shadow-glow hover:shadow-glow-lg"
          >
            <Sparkles className="w-4 h-4" />
            <span>Plan New Trip</span>
          </Link>
        </div>
      </div>

      {/* Search Input */}
      {trips.length > 0 && (
        <div className="relative max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by destination or keyword..."
            className="w-full bg-surface-900 rounded-xl pl-10 pr-4 py-2 text-sm text-white border border-surface-700 focus:border-brand-400 focus:outline-none transition-colors placeholder:text-slate-500"
          />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Loading state */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
          <p className="text-xs text-slate-400">Loading trips from database...</p>
        </div>
      ) : filteredTrips.length === 0 ? (
        /* Empty State */
        <div className="glass-card rounded-3xl p-12 text-center border border-surface-800 max-w-xl mx-auto space-y-4 shadow-glow">
          <div className="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mx-auto text-brand-400">
            <History className="w-7 h-7" />
          </div>
          <h3 className="text-xl font-bold text-white">No Trips Found</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto leading-relaxed">
            Your next adventure starts here. Enter a natural language request like "Plan a 5-day Bali trip under ₹60,000" to generate your first multi-agent itinerary.
          </p>
          <div className="pt-2">
            <Link
              to="/planner"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-brand-500 to-sky-500 text-white font-bold text-xs sm:text-sm shadow-glow"
            >
              <Sparkles className="w-4 h-4" />
              <span>Plan Your First Trip</span>
            </Link>
          </div>
        </div>
      ) : (
        /* Trips Grid */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTrips.map((trip) => {
            const formattedDate = trip.created_at
              ? new Date(trip.created_at).toLocaleDateString('en-IN', {
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric'
                })
              : 'Recent';

            return (
              <div
                key={trip.id}
                className="glass-card rounded-2xl p-6 border border-surface-800 hover:border-brand-500/40 transition-all duration-200 flex flex-col justify-between group shadow-lg"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-900 text-brand-400 border border-surface-700">
                      {trip.id}
                    </span>
                    <span className="text-[11px] text-slate-400 flex items-center gap-1">
                      <Clock className="w-3 h-3 text-slate-500" />
                      {formattedDate}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-white group-hover:text-brand-300 transition-colors">
                      {trip.destination}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2 mt-1 leading-relaxed">
                      "{trip.user_request}"
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-surface-800 text-xs">
                    <div className="flex items-center space-x-1 text-slate-300">
                      <Calendar className="w-3.5 h-3.5 text-brand-400" />
                      <span>{trip.duration_days} Days</span>
                    </div>

                    <div className="flex items-center space-x-1 text-slate-300">
                      <Users className="w-3.5 h-3.5 text-brand-400" />
                      <span>{trip.travelers} Travelers</span>
                    </div>
                  </div>

                  <div className="bg-surface-900/60 p-2.5 rounded-xl border border-surface-800/80 flex items-center justify-between text-xs">
                    <div>
                      <span className="text-[10px] text-slate-400 block">Total Spend</span>
                      <span className="font-bold text-white">₹{Number(trip.total_cost || trip.budget).toLocaleString('en-IN')}</span>
                    </div>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        trip.budget_status === 'UNDER_BUDGET'
                          ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                          : 'bg-blue-500/10 text-blue-300 border border-blue-500/20'
                      }`}
                    >
                      {trip.budget_status || 'UNDER_BUDGET'}
                    </span>
                  </div>
                </div>

                <div className="mt-5 pt-3 border-t border-surface-800">
                  <Link
                    to={`/trips/${trip.id}`}
                    className="w-full py-2 px-3 rounded-xl bg-surface-900 hover:bg-brand-600 text-slate-200 hover:text-white text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span>View Itinerary</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
