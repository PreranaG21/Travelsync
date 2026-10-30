import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, Compass, Plane, Users, Car, Map, Briefcase, 
  ArrowRight, Star, MapPin, Tag, Heart, Globe, Palmtree,
  ShieldCheck, Clock, CheckCircle2, ChevronRight
} from 'lucide-react';

const TRIP_TYPES = [
  {
    id: 'family',
    title: 'Family Trip Planner',
    description: 'Create comfortable, balanced journeys designed around families, activities, convenience and shared experiences.',
    icon: Users,
    gradient: 'from-amber-500/20 to-orange-500/20',
    border: 'hover:border-amber-500/50',
    iconColor: 'text-amber-400',
    prompt: 'Plan a 5-day family trip to Singapore for 4 people under ₹1,20,000 with kid-friendly activities, zoo, and theme parks.'
  },
  {
    id: 'road_trip',
    title: 'Road Trip Planner',
    description: 'Plan routes, stops, activities and stays for your next road adventure.',
    icon: Car,
    gradient: 'from-sky-500/20 to-blue-500/20',
    border: 'hover:border-sky-500/50',
    iconColor: 'text-sky-400',
    prompt: 'Plan a 4-day scenic road trip from Mumbai to Goa for 3 friends under ₹40,000 with coastal stops and local eateries.'
  },
  {
    id: 'multi_city',
    title: 'Multi-City Trip Planner',
    description: 'Coordinate several destinations into one seamless journey.',
    icon: Map,
    gradient: 'from-indigo-500/20 to-purple-500/20',
    border: 'hover:border-indigo-500/50',
    iconColor: 'text-indigo-400',
    prompt: 'Plan a 7-day multi-city expedition across Paris and Rome for 2 people under ₹1,80,000 focusing on culture and history.'
  },
  {
    id: 'business',
    title: 'Business Trip Planner',
    description: 'Organize efficient business travel around meetings, hotels, travel times and schedules.',
    icon: Briefcase,
    gradient: 'from-emerald-500/20 to-teal-500/20',
    border: 'hover:border-emerald-500/50',
    iconColor: 'text-emerald-400',
    prompt: 'Plan a 3-day efficient business journey to Dubai for 1 traveler with airport transfers, business hotel, and evening dinner spots.'
  },
];

const TRAVEL_DEALS = [
  {
    destination: 'Bali',
    country: 'Indonesia',
    description: 'Tropical beaches, ancient sea temples, and volcanic wandering.',
    estimate: '₹45,000 - ₹65,000',
    image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=600&q=80',
    tag: 'Island Odyssey',
    prompt: 'Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.'
  },
  {
    destination: 'Paris',
    country: 'France',
    description: 'Iconic art museums, architectural landmarks & Seine riverside walks.',
    estimate: '₹95,000 - ₹1,40,000',
    image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=600&q=80',
    tag: 'Cultural Voyage',
    prompt: 'Plan a 5-day trip to Paris for 2 people under ₹1,20,000. Include Louvre Museum, Eiffel Tower and bakeries.'
  },
  {
    destination: 'Dubai',
    country: 'UAE',
    description: 'Futuristic skylines, desert dunes, luxury marinas and vibrant souks.',
    estimate: '₹70,000 - ₹1,00,000',
    image: 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80',
    tag: 'Modern Journey',
    prompt: 'Plan a 4-day trip to Dubai for 2 people with a budget of ₹85,000 including desert safari and Burj Khalifa.'
  },
  {
    destination: 'Goa',
    country: 'India',
    description: 'Golden sandy shores, Portuguese heritage forts and coastal culinary delights.',
    estimate: '₹22,000 - ₹35,000',
    image: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80',
    tag: 'Coastal Trek',
    prompt: 'Plan a 4-day beach vacation to Goa for 2 people under ₹30,000 with watersports, seafood, and sunset views.'
  },
  {
    destination: 'Tokyo',
    country: 'Japan',
    description: 'Harmonious blend of neon metropolis, ancient shrines, and culinary excellence.',
    estimate: '₹1,10,000 - ₹1,60,000',
    image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=600&q=80',
    tag: 'Urban Expedition',
    prompt: 'Plan a 6-day trip to Tokyo for 2 people under ₹1,40,000 exploring Shibuya, Asakusa temples, and authentic ramen.'
  },
  {
    destination: 'London',
    country: 'United Kingdom',
    description: 'Historic royal palaces, world-class theatre, and picturesque riverside parks.',
    estimate: '₹1,05,000 - ₹1,50,000',
    image: 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=600&q=80',
    tag: 'Historic Voyage',
    prompt: 'Plan a 5-day trip to London for 2 people under ₹1,30,000 with historic museums, Thames cruise, and cafes.'
  },
  {
    destination: 'Singapore',
    country: 'Singapore',
    description: 'Gardens by the Bay, futuristic skyways, and multicultural culinary feasts.',
    estimate: '₹65,000 - ₹90,000',
    image: 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=600&q=80',
    tag: 'Garden Odyssey',
    prompt: 'Plan a 4-day trip to Singapore for 2 people under ₹75,000 with Sentosa, Marina Bay, and street markets.'
  },
  {
    destination: 'Bangkok',
    country: 'Thailand',
    description: 'Grand ornate temples, lively night markets, and delicious street food.',
    estimate: '₹40,000 - ₹60,000',
    image: 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=600&q=80',
    tag: 'Culinary Wandering',
    prompt: 'Plan a 5-day trip to Bangkok for 2 people under ₹50,000 focusing on street food, temples, and river canals.'
  },
  {
    destination: 'Rome',
    country: 'Italy',
    description: 'Ancient Colosseum, Vatican treasures, charming cobblestones and espresso bars.',
    estimate: '₹90,000 - ₹1,35,000',
    image: 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=600&q=80',
    tag: 'Classical Journey',
    prompt: 'Plan a 5-day trip to Rome for 2 people under ₹1,15,000 with Colosseum, Vatican City, and authentic pasta spots.'
  },
  {
    destination: 'New York',
    country: 'United States',
    description: 'Central Park walks, Broadway theater, world-class dining, and skyline views.',
    estimate: '₹1,30,000 - ₹1,90,000',
    image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=600&q=80',
    tag: 'Metropolis Trek',
    prompt: 'Plan a 5-day trip to New York for 2 people under ₹1,60,000 with Broadway show, Central Park, and museum tours.'
  }
];

const TOP_DESTINATIONS = [
  {
    name: 'Bali, Indonesia',
    highlight: 'Temples, Coral Reefs & Volcanoes',
    image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=600&q=80',
    prompt: 'Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.'
  },
  {
    name: 'Goa, India',
    highlight: 'Forts, Coastlines & Night Bazaars',
    image: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80',
    prompt: 'Plan a 3-day trip to Goa for 2 people under ₹25,000. Focus on watersports and coastal food.'
  },
  {
    name: 'Dubai, UAE',
    highlight: 'Desert Safaris & Skylines',
    image: 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80',
    prompt: 'Plan a 4-day trip to Dubai for 2 people under ₹85,000.'
  },
  {
    name: 'Paris, France',
    highlight: 'Art, Architecture & Seine Cruises',
    image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=600&q=80',
    prompt: 'Plan a 5-day trip to Paris for 2 people under ₹1,20,000.'
  }
];

const REVIEWS = [
  {
    name: 'Aarav Mehta',
    role: 'Solo Explorer',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
    rating: 5,
    text: 'TravelSync turned my rough travel idea into a practical day-by-day plan. The flight options, stay suggestions, and day clustering saved me hours of manual research.'
  },
  {
    name: 'Sophia Chen',
    role: 'Family Vacation Planner',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
    rating: 5,
    text: 'Planning a multi-member family trip to Singapore was completely stress-free. The weather forecast integration and realistic daily pacing made our voyage smooth from start to finish.'
  },
  {
    name: 'Rohan Deshmukh',
    role: 'Budget Traveler',
    avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=150&q=80',
    rating: 5,
    text: 'The deterministic budget calculations are extremely accurate. It gave us a realistic breakdown of flights, accommodation, food, and transit so there were no surprise expenses.'
  },
  {
    name: 'Elena Rostova',
    role: 'Cultural Trekker',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=150&q=80',
    rating: 5,
    text: 'The attraction selections from OpenStreetMap gave us fascinating historic and viewpoint spots that standard commercial travel sites usually overlook. Highly recommended!'
  },
  {
    name: 'Vikram & Priya',
    role: 'Honeymoon Odyssey',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
    rating: 5,
    text: 'We planned our 5-day Bali adventure through TravelSync. The day-by-day itinerary was structured perfectly between relaxation, beach sunsets, and temple visits.'
  }
];

export default function LandingPage() {
  const navigate = useNavigate();

  const handlePlanClick = (prompt, tripType = 'leisure') => {
    navigate('/planner', { state: { prefilledPrompt: prompt, tripType } });
  };

  const scrollToDeals = () => {
    const el = document.getElementById('travel-deals');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen">
      {/* 1. Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 sm:pt-20 sm:pb-32">
        {/* Subtle Background Glows & Floating Motion */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1100px] h-[550px] bg-gradient-to-b from-brand-600/15 via-sky-500/10 to-transparent blur-3xl pointer-events-none -z-10"></div>
        <div className="absolute top-1/4 right-8 w-72 h-72 bg-sky-500/10 rounded-full blur-3xl pointer-events-none -z-10 animate-pulse"></div>
        <div className="absolute bottom-10 left-10 w-80 h-80 bg-brand-500/10 rounded-full blur-3xl pointer-events-none -z-10"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          {/* Tagline Pill */}
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-surface-900/90 border border-brand-500/30 text-brand-300 text-xs font-semibold shadow-glow mb-6 animate-fade-in">
            <Compass className="w-4 h-4 text-brand-400 animate-spin-slow" />
            <span>AI-Powered Autonomous Travel Planning</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
            TravelSync
            <span className="block text-2xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-brand-300 via-sky-200 to-indigo-300 bg-clip-text text-transparent mt-3">
              Built for Every Journey.
            </span>
          </h1>

          {/* Subheading with natural travel vocabulary */}
          <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Plan your next expedition, voyage, trek, or wandering odyssey. Enter your travel dreams in natural language and let our intelligent agents orchestrate flights, stays, weather, and curated daily schedules seamlessly.
          </p>

          {/* CTAs */}
          <div className="mt-9 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/planner"
              className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-brand-500 to-sky-500 text-white font-bold text-base shadow-glow hover:shadow-glow-lg hover:from-brand-600 hover:to-sky-600 active:scale-95 transition-all duration-200"
            >
              <Sparkles className="w-5 h-5" />
              <span>Plan My Trip</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <button
              onClick={scrollToDeals}
              className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-7 py-3.5 rounded-xl bg-surface-900 hover:bg-surface-800 text-slate-200 font-semibold text-base border border-surface-700 hover:border-brand-500/30 transition-all duration-200"
            >
              <Tag className="w-4 h-4 text-brand-400" />
              <span>Explore Travel Deals</span>
            </button>
          </div>
        </div>
      </section>

      {/* 2. Built for Every Trip Type Section */}
      <section className="py-16 bg-surface-950/60 border-y border-surface-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
              Personalized Orchestration
            </span>
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white mt-3">
              Built for Every Trip Type
            </h2>
            <p className="text-sm text-slate-400 mt-2">
              Whether you are planning a relaxed family getaway or a fast-paced business trek, select a trip style tailored to your needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {TRIP_TYPES.map((type) => {
              const Icon = type.icon;
              return (
                <div
                  key={type.id}
                  onClick={() => handlePlanClick(type.prompt, type.id)}
                  className={`glass-card rounded-2xl p-6 border border-surface-800 ${type.border} cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:shadow-glow flex flex-col justify-between group`}
                >
                  <div className="space-y-3">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${type.gradient} border border-surface-700 flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
                      <Icon className={`w-6 h-6 ${type.iconColor}`} />
                    </div>
                    <h3 className="text-lg font-bold text-white group-hover:text-brand-300 transition-colors">
                      {type.title}
                    </h3>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      {type.description}
                    </p>
                  </div>

                  <div className="mt-6 pt-3 border-t border-surface-800/80 flex items-center justify-between text-xs font-semibold text-brand-400 group-hover:text-brand-300">
                    <span>Select Trip Type</span>
                    <ChevronRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 3. Travel Deals Section */}
      <section id="travel-deals" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
                Curated Travel Estimates
              </span>
              <h2 className="text-2xl sm:text-4xl font-extrabold text-white mt-2">
                Travel Deals
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Explore popular world destinations with AI-optimized planning budgets and itinerary templates.
              </p>
            </div>
            <Link
              to="/planner"
              className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center gap-1 self-start sm:self-auto"
            >
              <span>Open Custom Planner</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {TRAVEL_DEALS.map((deal, idx) => (
              <div
                key={idx}
                onClick={() => handlePlanClick(deal.prompt)}
                className="glass-card rounded-2xl overflow-hidden border border-surface-800 hover:border-brand-500/50 cursor-pointer group transition-all duration-300 hover:-translate-y-1 shadow-lg flex flex-col justify-between"
              >
                <div>
                  <div className="h-44 relative overflow-hidden">
                    <img
                      src={deal.image}
                      alt={deal.destination}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-surface-950 via-surface-950/40 to-transparent"></div>
                    <span className="absolute top-3 right-3 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-brand-500/80 text-white backdrop-blur-md">
                      {deal.tag}
                    </span>
                  </div>

                  <div className="p-5 space-y-2">
                    <div>
                      <h3 className="text-lg font-bold text-white group-hover:text-brand-300 transition-colors">
                        {deal.destination}, {deal.country}
                      </h3>
                      <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">{deal.description}</p>
                    </div>
                  </div>
                </div>

                <div className="px-5 pb-5 pt-2 border-t border-surface-800 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Planning Estimate:</span>
                    <span className="font-bold text-brand-300">{deal.estimate}</span>
                  </div>
                  <button className="w-full py-2 px-3 rounded-xl bg-surface-900 group-hover:bg-brand-600 text-slate-200 group-hover:text-white text-xs font-semibold transition-colors flex items-center justify-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Plan This Trip</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. Top Destinations Section */}
      <section className="py-16 bg-surface-950/60 border-y border-surface-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-10">
            <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
              Popular Getaways
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">
              Top Destinations
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Handpicked travel hubs with active hotel records, attraction spots, and live weather telemetry.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {TOP_DESTINATIONS.map((dest, idx) => (
              <div
                key={idx}
                onClick={() => handlePlanClick(dest.prompt)}
                className="glass-card rounded-2xl overflow-hidden border border-surface-800 hover:border-brand-500/40 cursor-pointer group transition-all duration-300 hover:-translate-y-1"
              >
                <div className="h-40 relative overflow-hidden">
                  <img
                    src={dest.image}
                    alt={dest.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-surface-950 via-surface-950/30 to-transparent"></div>
                  <div className="absolute bottom-3 left-3">
                    <h3 className="text-base font-bold text-white">{dest.name}</h3>
                    <p className="text-[11px] text-slate-300">{dest.highlight}</p>
                  </div>
                </div>
                <div className="p-3 bg-surface-900/50 flex items-center justify-between text-xs font-medium text-brand-400 group-hover:text-brand-300">
                  <span>Explore Itinerary</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5. What Travelers Say (Reviews) */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <span className="text-xs font-bold uppercase tracking-widest text-brand-400 bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
              User Experiences
            </span>
            <h2 className="text-2xl sm:text-4xl font-extrabold text-white mt-2">
              What Travelers Say
            </h2>
            <p className="text-sm text-slate-400 mt-2">
              Feedback and reviews demonstrating TravelSync's multi-agent trip planning capabilities.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {REVIEWS.map((rev, idx) => (
              <div
                key={idx}
                className="glass-card rounded-2xl p-6 border border-surface-800 hover:border-brand-500/30 transition-all flex flex-col justify-between shadow-lg"
              >
                <div className="space-y-4">
                  {/* 5 Star Rating */}
                  <div className="flex items-center space-x-1 text-amber-400">
                    {[...Array(rev.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-amber-400" />
                    ))}
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed italic">
                    "{rev.text}"
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-surface-800/80 flex items-center space-x-3">
                  <img
                    src={rev.avatar}
                    alt={rev.name}
                    className="w-10 h-10 rounded-full object-cover border border-surface-700"
                    loading="lazy"
                  />
                  <div>
                    <h4 className="text-xs font-bold text-white">{rev.name}</h4>
                    <span className="text-[11px] text-slate-400">{rev.role}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
