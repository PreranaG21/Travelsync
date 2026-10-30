import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Sparkles, SlidersHorizontal, MapPin, Calendar, 
  Users, IndianRupee, Compass, Palmtree, Utensils, 
  Landmark, Moon, TreePine, AlertCircle, RefreshCw, Car, Map, Briefcase, Heart 
} from 'lucide-react';
import { generateTrip } from '../services/api';
import AgentProgress from '../components/AgentProgress';

const SAMPLE_PROMPTS = [
  {
    title: 'Bali Flagship Journey',
    prompt: 'Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.',
    highlight: 'Flagship Academic Demo',
    tripType: 'leisure'
  },
  {
    title: 'Singapore Family Getaway',
    prompt: 'Plan a 5-day family trip to Singapore for 4 people under ₹1,20,000 with kid-friendly activities, zoo, and theme parks.',
    highlight: 'Family Style',
    tripType: 'family'
  },
  {
    title: 'Goa Coastal Weekend',
    prompt: 'Plan a 3-day trip to Goa for 2 people under ₹25,000. Focus on watersports, beach relaxation and Goan seafood.',
    highlight: 'Budget Coastal',
    tripType: 'road_trip'
  },
  {
    title: 'Dubai Luxury Getaway',
    prompt: 'Plan a 4-day luxury trip to Dubai for 2 people with a budget of ₹90,000. Include Burj Khalifa and desert safari.',
    highlight: 'Luxury Style',
    tripType: 'leisure'
  },
  {
    title: 'Bangkok Culinary & Temples',
    prompt: 'Plan a 5-day trip to Bangkok for 2 people under ₹50,000. I love night markets, street food, and historic temples.',
    highlight: 'Culture & Food',
    tripType: 'leisure'
  },
  {
    title: 'Paris & Rome Odyssey',
    prompt: 'Plan a 7-day multi-city expedition across Paris and Rome for 2 people under ₹1,80,000 focusing on culture and history.',
    highlight: 'Multi-City Trek',
    tripType: 'multi_city'
  }
];

const AVAILABLE_INTERESTS = [
  { id: 'beaches', label: 'Beaches & Ocean', icon: Palmtree },
  { id: 'adventure', label: 'Adventure & Treks', icon: Compass },
  { id: 'local food', label: 'Local Food & Dining', icon: Utensils },
  { id: 'culture', label: 'Culture & Temples', icon: Landmark },
  { id: 'nature', label: 'Nature & Wildlife', icon: TreePine },
  { id: 'nightlife', label: 'Nightlife & Lounges', icon: Moon },
];

const TRIP_TYPE_OPTIONS = [
  { id: 'leisure', label: 'Leisure / General' },
  { id: 'family', label: 'Family Vacation' },
  { id: 'road_trip', label: 'Road Trip' },
  { id: 'multi_city', label: 'Multi-City Journey' },
  { id: 'business', label: 'Business Travel' },
];

export default function PlannerPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const [prompt, setPrompt] = useState(
    location.state?.prefilledPrompt ||
    'Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.'
  );

  const [tripType, setTripType] = useState(location.state?.tripType || 'leisure');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [source, setSource] = useState('Mumbai');
  const [destination, setDestination] = useState('');
  const [durationDays, setDurationDays] = useState(5);
  const [travelers, setTravelers] = useState(2);
  const [budget, setBudget] = useState(60000);
  const [travelStyle, setTravelStyle] = useState('balanced');
  const [selectedInterests, setSelectedInterests] = useState(['beaches', 'adventure', 'local food']);

  const [isGenerating, setIsGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (location.state?.prefilledPrompt) {
      setPrompt(location.state.prefilledPrompt);
    }
    if (location.state?.tripType) {
      setTripType(location.state.tripType);
    }
  }, [location.state]);

  const toggleInterest = (id) => {
    if (selectedInterests.includes(id)) {
      setSelectedInterests(selectedInterests.filter((item) => item !== id));
    } else {
      setSelectedInterests([...selectedInterests, id]);
    }
  };

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    if (!prompt.trim()) {
      setErrorMsg('Please enter your travel request prompt.');
      return;
    }

    setErrorMsg('');
    setIsGenerating(true);

    try {
      const payload = {
        user_request: prompt.trim(),
        trip_type: tripType,
      };

      if (showAdvanced) {
        if (source) payload.source = source;
        if (destination) payload.destination = destination;
        if (durationDays) payload.duration_days = Number(durationDays);
        if (travelers) payload.travelers = Number(travelers);
        if (budget) payload.budget = Number(budget);
        if (travelStyle) payload.travel_style = travelStyle;
        if (selectedInterests.length > 0) payload.interests = selectedInterests;
      }

      const tripData = await generateTrip(payload);
      
      // Navigate to results page with trip payload
      navigate('/result', { state: { tripData } });
    } catch (err) {
      console.error('Trip generation error:', err);
      setErrorMsg(
        err.friendlyMessage ||
        err.message ||
        'TravelSync could not connect to the planning service. Please make sure the TravelSync services are running and try again.'
      );
      setIsGenerating(false);
    }
  };

  const handleSelectSample = (sample) => {
    setPrompt(sample.prompt);
    if (sample.tripType) setTripType(sample.tripType);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14">
      {/* Page Title */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3.5 py-1.5 rounded-full border border-brand-500/20">
          AI Multi-Agent Trip Planner
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white mt-3 tracking-tight">
          Where will your next journey take you?
        </h1>
        <p className="text-sm text-slate-300 mt-2.5 max-w-2xl mx-auto leading-relaxed">
          Describe your dream trip in natural language. Our 7 autonomous agents will search flights, verified stays, weather forecasts, attractions, and calculate a deterministic budget.
        </p>
      </div>

      {/* Main Input Box */}
      <div className="max-w-3xl mx-auto">
        <form onSubmit={handleGenerate} className="glass-card rounded-3xl p-5 sm:p-7 border border-brand-500/30 shadow-glow space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-2">
              Natural Language Travel Request
            </label>
            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={isGenerating}
              placeholder="e.g. Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food."
              className="w-full bg-surface-900/90 text-white rounded-2xl p-4 text-sm sm:text-base border border-surface-700 focus:border-brand-400 focus:ring-1 focus:ring-brand-400 focus:outline-none transition-colors resize-none placeholder:text-slate-500 disabled:opacity-50"
            />
          </div>

          {/* Quick Actions & Advanced Filters Toggle */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-300 hover:text-brand-300 transition-colors py-2 px-3.5 rounded-xl bg-surface-900 border border-surface-700"
            >
              <SlidersHorizontal className="w-3.5 h-3.5 text-brand-400" />
              <span>{showAdvanced ? 'Hide Custom Constraints' : 'Customize Optional Constraints'}</span>
            </button>

            <button
              type="submit"
              disabled={isGenerating || !prompt.trim()}
              className="inline-flex items-center space-x-2 px-7 py-3 rounded-xl bg-gradient-to-r from-brand-500 to-sky-500 hover:from-brand-600 hover:to-sky-600 text-white font-bold text-sm shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isGenerating ? 'Orchestrating Agents...' : 'Generate My Trip'}</span>
            </button>
          </div>

          {/* Advanced Filters Drawer */}
          {showAdvanced && (
            <div className="pt-4 border-t border-surface-800 space-y-4 animate-fade-in text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Departure City</label>
                  <input
                    type="text"
                    value={source}
                    onChange={(e) => setSource(e.target.value)}
                    placeholder="e.g. Mumbai"
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Destination</label>
                  <input
                    type="text"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    placeholder="e.g. Bali, Goa, Dubai"
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Trip Type</label>
                  <select
                    value={tripType}
                    onChange={(e) => setTripType(e.target.value)}
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  >
                    {TRIP_TYPE_OPTIONS.map((t) => (
                      <option key={t.id} value={t.id}>{t.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Duration</label>
                  <select
                    value={durationDays}
                    onChange={(e) => setDurationDays(Number(e.target.value))}
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  >
                    {[2, 3, 4, 5, 6, 7, 8, 10, 14].map((d) => (
                      <option key={d} value={d}>{d} Days</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Travelers</label>
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={travelers}
                    onChange={(e) => setTravelers(Number(e.target.value))}
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Total Budget (₹ INR)</label>
                  <input
                    type="number"
                    step={1000}
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 font-semibold block mb-1">Travel Style</label>
                  <select
                    value={travelStyle}
                    onChange={(e) => setTravelStyle(e.target.value)}
                    className="w-full bg-surface-900 rounded-xl p-2.5 text-white border border-surface-700 focus:border-brand-400 focus:outline-none"
                  >
                    <option value="balanced">Balanced Experience</option>
                    <option value="budget">Budget Friendly</option>
                    <option value="luxury">Luxury & Premium</option>
                  </select>
                </div>
              </div>

              {/* Interests Checkboxes */}
              <div>
                <label className="text-slate-400 font-semibold block mb-2">Interests & Preferences</label>
                <div className="flex flex-wrap gap-2">
                  {AVAILABLE_INTERESTS.map((interest) => {
                    const isSelected = selectedInterests.includes(interest.id);
                    const Icon = interest.icon;
                    return (
                      <button
                        type="button"
                        key={interest.id}
                        onClick={() => toggleInterest(interest.id)}
                        className={`px-3.5 py-2 rounded-xl font-medium transition-all flex items-center space-x-1.5 ${
                          isSelected
                            ? 'bg-brand-500/20 text-brand-300 border border-brand-500/40 shadow-sm'
                            : 'bg-surface-900 text-slate-400 border border-surface-800 hover:text-slate-200'
                        }`}
                      >
                        <Icon className="w-3.5 h-3.5" />
                        <span>{interest.label}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </form>

        {/* Error Notification with Friendly Retry Banner */}
        {errorMsg && (
          <div className="mt-5 p-5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-200 text-xs sm:text-sm space-y-2 animate-fade-in">
            <div className="flex items-center space-x-2 text-rose-300 font-bold">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>Planning Notice</span>
            </div>
            <p className="text-xs text-rose-200/90 leading-relaxed">
              {errorMsg}
            </p>
            <div className="pt-2">
              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="inline-flex items-center space-x-1.5 px-4 py-1.5 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-xs font-semibold text-rose-200 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Retry Generation</span>
              </button>
            </div>
          </div>
        )}

        {/* Live Multi-Agent Execution Progress Tracker */}
        {isGenerating && <AgentProgress isGenerating={isGenerating} />}

        {/* Sample Prompt Chips Grid */}
        <div className="mt-12 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Demonstration Planning Scenarios
            </h3>
            <span className="text-xs text-slate-500">Click any card to load</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {SAMPLE_PROMPTS.map((item, idx) => (
              <div
                key={idx}
                onClick={() => handleSelectSample(item)}
                className="glass-card rounded-2xl p-4 border border-surface-800 hover:border-brand-500/40 cursor-pointer transition-all hover:bg-surface-900/70 group shadow-md"
              >
                <div className="flex items-center justify-between pb-1.5">
                  <span className="text-xs font-bold text-white group-hover:text-brand-300 transition-colors">
                    {item.title}
                  </span>
                  <span className="text-[10px] uppercase font-bold text-brand-400 bg-brand-500/10 px-2 py-0.5 rounded-full border border-brand-500/20">
                    {item.highlight}
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mt-1">
                  "{item.prompt}"
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
