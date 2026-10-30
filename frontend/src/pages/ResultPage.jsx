import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, useParams, Link } from 'react-router-dom';
import { 
  Sparkles, ArrowLeft, Bookmark, BookmarkCheck, 
  MapPin, Calendar, Users, IndianRupee, Download, AlertCircle, RefreshCw, Printer 
} from 'lucide-react';
import { getTripById } from '../services/api';
import { exportItineraryPDF } from '../services/pdfExport';
import FlightCard from '../components/FlightCard';
import HotelCard from '../components/HotelCard';
import WeatherCard from '../components/WeatherCard';
import TimelineItinerary from '../components/TimelineItinerary';
import BudgetBreakdown from '../components/BudgetBreakdown';
import CriticReport from '../components/CriticReport';
import AgentTransparencyDrawer from '../components/AgentTransparencyDrawer';

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { id } = useParams();

  const [tripData, setTripData] = useState(location.state?.tripData || null);
  const [loading, setLoading] = useState(!location.state?.tripData && !!id);
  const [error, setError] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (!tripData && id) {
      setLoading(true);
      getTripById(id)
        .then((res) => {
          if (res.itinerary) {
            setTripData({
              ...res.itinerary,
              trip_id: res.trip.id,
              agent_logs: res.agent_logs || []
            });
          }
          setLoading(false);
        })
        .catch((err) => {
          setError(`Could not retrieve trip: ${err.message}`);
          setLoading(false);
        });
    }
  }, [id, tripData]);

  const handleDownloadPDF = () => {
    if (!tripData) return;
    setDownloading(true);
    try {
      exportItineraryPDF(tripData);
    } catch (err) {
      console.error('PDF export error:', err);
    } finally {
      setDownloading(false);
    }
  };

  const handleSaveToggle = () => {
    setIsSaved(!isSaved);
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center">
        <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <h3 className="text-lg font-bold text-white">Retrieving Saved Itinerary...</h3>
      </div>
    );
  }

  if (error || !tripData) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <div className="glass-card rounded-2xl p-8 border border-surface-800 space-y-4">
          <AlertCircle className="w-12 h-12 text-amber-400 mx-auto" />
          <h2 className="text-xl font-bold text-white">No Itinerary Data Found</h2>
          <p className="text-sm text-slate-400">
            {error || 'Please generate a new travel plan using our natural language trip planner.'}
          </p>
          <div className="pt-2">
            <Link
              to="/planner"
              className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-brand-500 text-white font-semibold text-sm shadow-glow"
            >
              <Sparkles className="w-4 h-4" />
              <span>Go to Trip Planner</span>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const destination = tripData.destination || 'Destination';
  const duration = tripData.duration_days || 5;
  const travelers = tripData.travelers || 2;
  const budget = Number(tripData.budget || 60000);
  const totalCost = Number(tripData.budget_breakdown?.total_cost || budget);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8 animate-fade-in">
      {/* Top Navigation & Action Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-surface-800">
        <Link
          to="/planner"
          className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Plan Another Trip</span>
        </Link>

        <div className="flex items-center space-x-3 self-start sm:self-auto">
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-brand-500 to-sky-500 text-white shadow-glow hover:from-brand-600 hover:to-sky-600 transition-all active:scale-95"
          >
            <Download className="w-4 h-4" />
            <span>{downloading ? 'Preparing PDF...' : 'Download Itinerary (PDF)'}</span>
          </button>

          <button
            onClick={handleSaveToggle}
            className={`inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all ${
              isSaved
                ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                : 'bg-surface-900 text-slate-300 border-surface-700 hover:text-white hover:bg-surface-800'
            }`}
          >
            {isSaved ? <BookmarkCheck className="w-4 h-4 text-emerald-400" /> : <Bookmark className="w-4 h-4" />}
            <span>{isSaved ? 'Trip Saved' : 'Save Trip'}</span>
          </button>
        </div>
      </div>

      {/* Hero Header Banner */}
      <div className="glass-card rounded-3xl p-6 sm:p-10 border border-brand-500/30 relative overflow-hidden shadow-glow">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-brand-500/20 text-brand-300 border border-brand-500/30 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              AI Multi-Agent Itinerary
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-surface-900 text-slate-300 border border-surface-700 font-mono">
              Trip ID: {tripData.trip_id || 'ID-100'}
            </span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            Your {duration}-Day {destination} Journey
          </h1>

          {/* Quick Metrics Bar */}
          <div className="flex flex-wrap items-center gap-4 sm:gap-6 pt-3 text-xs sm:text-sm text-slate-300">
            <div className="flex items-center space-x-1.5">
              <MapPin className="w-4 h-4 text-brand-400" />
              <span>{tripData.source || 'Mumbai'} → {destination}</span>
            </div>

            <div className="flex items-center space-x-1.5">
              <Calendar className="w-4 h-4 text-brand-400" />
              <span>{duration} Days & {Math.max(1, duration - 1)} Nights</span>
            </div>

            <div className="flex items-center space-x-1.5">
              <Users className="w-4 h-4 text-brand-400" />
              <span>{travelers} Traveler{travelers > 1 ? 's' : ''}</span>
            </div>

            <div className="flex items-center space-x-1.5">
              <IndianRupee className="w-4 h-4 text-emerald-400" />
              <span>Total Cost: <strong className="text-white font-bold">₹{totalCost.toLocaleString('en-IN')}</strong> (Budget: ₹{budget.toLocaleString('en-IN')})</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Flight & Hotel Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
            <span>Flight Recommendation</span>
          </h2>
          <FlightCard
            selectedFlight={tripData.selected_flight}
            flightOptions={tripData.flight_options}
            isMockFlight={tripData.is_mock_flight}
            travelers={travelers}
          />
        </div>

        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
            <span>Accommodation Match</span>
          </h2>
          <HotelCard
            selectedHotel={tripData.selected_hotel}
            hotelOptions={tripData.hotel_options}
            durationDays={duration}
          />
        </div>
      </div>

      {/* Weather Forecast Section */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Destination Weather Analysis (Open-Meteo)
        </h2>
        <WeatherCard weather={tripData.weather} />
      </div>

      {/* Timeline Section */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Curated Day-by-Day Schedule (OpenStreetMap & Haversine Clustered)
        </h2>
        <TimelineItinerary activities={tripData.activities} destination={destination} />
      </div>

      {/* Financial Budget Analysis */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Deterministic Financial Audit
        </h2>
        <BudgetBreakdown
          budgetBreakdown={tripData.budget_breakdown}
          userBudget={budget}
        />
      </div>

      {/* Critic / Validation Report */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Multi-Agent Realism & Critic Inspection
        </h2>
        <CriticReport
          criticResult={tripData.critic_result}
          revisionCount={tripData.revision_count}
        />
      </div>

      {/* Multi-Agent Transparency Drawer */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Planning Details & Telemetry
        </h2>
        <AgentTransparencyDrawer agentLogs={tripData.agent_logs} />
      </div>
    </div>
  );
}
