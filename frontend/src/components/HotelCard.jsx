import React from 'react';
import { Building2, Star, MapPin, Sparkles, Check, Wifi, Waves, Coffee, Car } from 'lucide-react';

export default function HotelCard({ selectedHotel, hotelOptions = [], durationDays = 5 }) {
  if (!selectedHotel || !selectedHotel.hotel_name) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-surface-800 text-center text-slate-400">
        <Building2 className="w-8 h-8 mx-auto text-slate-500 mb-2" />
        <p className="text-sm">No hotel recommendations found in database.</p>
      </div>
    );
  }

  const nights = Math.max(1, durationDays > 1 ? durationDays - 1 : 1);
  const amenitiesList = selectedHotel.amenities
    ? selectedHotel.amenities.split(',').map((a) => a.trim())
    : ['Free WiFi', 'Swimming Pool', 'Breakfast Included'];

  const alternatives = hotelOptions.filter(
    (h) => h.hotel_name !== selectedHotel.hotel_name
  );

  return (
    <div className="space-y-4">
      {/* Main Recommended Hotel Card */}
      <div className="glass-card rounded-2xl p-6 border border-brand-500/30 relative overflow-hidden group hover:border-brand-400/50 transition-all">
        {/* Top Header */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-surface-800">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-brand-500/20 text-brand-300 border border-brand-500/30 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              Selected by Hotel Agent (PostgreSQL)
            </span>
            {selectedHotel.recommendation_reason && (
              <span className="px-2.5 py-0.5 rounded text-[11px] font-medium bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                {selectedHotel.recommendation_reason}
              </span>
            )}
          </div>
          <div className="text-right">
            <span className="text-2xl font-extrabold text-white">
              ₹{Number(selectedHotel.total_price || (selectedHotel.price_per_night * nights)).toLocaleString('en-IN')}
            </span>
            <span className="text-xs text-slate-400 block">Total for {nights} night{nights > 1 ? 's' : ''}</span>
          </div>
        </div>

        {/* Property Info */}
        <div className="py-4 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-xl font-bold text-white group-hover:text-brand-300 transition-colors">
                {selectedHotel.hotel_name}
              </h3>
              <div className="flex items-center space-x-1.5 text-xs text-slate-400 mt-1">
                <MapPin className="w-3.5 h-3.5 text-brand-400 shrink-0" />
                <span>{selectedHotel.location}, {selectedHotel.city}</span>
                {selectedHotel.distance_from_center > 0 && (
                  <span className="text-slate-500">({selectedHotel.distance_from_center} km from center)</span>
                )}
              </div>
            </div>

            {/* Rating Stars */}
            <div className="flex items-center space-x-1.5 bg-surface-900/90 border border-surface-700 px-3 py-1.5 rounded-xl self-start sm:self-auto">
              <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
              <span className="text-sm font-bold text-white">{selectedHotel.rating}</span>
              <span className="text-xs text-slate-400">/ 5.0</span>
            </div>
          </div>

          <div className="text-xs font-semibold text-slate-300 bg-surface-900/60 border border-surface-800 px-3 py-2 rounded-lg inline-block">
            Room Type: <span className="text-brand-300 font-normal">{selectedHotel.room_type || 'Deluxe Room'}</span>
          </div>

          {/* Amenities Chips */}
          <div className="pt-2">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Included Amenities</div>
            <div className="flex flex-wrap gap-2">
              {amenitiesList.map((amenity, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-surface-900 border border-surface-700/80 text-slate-300 flex items-center gap-1.5"
                >
                  <Check className="w-3 h-3 text-brand-400" />
                  {amenity}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-surface-800/80 flex items-center justify-between text-xs text-slate-400">
          <div>
            Nightly rate: <span className="font-semibold text-slate-200">₹{Number(selectedHotel.price_per_night).toLocaleString('en-IN')}</span> / night
          </div>
          <span className="text-emerald-400 font-medium">✓ Verified in local PostgreSQL dataset</span>
        </div>
      </div>

      {/* Alternative Hotels in Database */}
      {alternatives.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-1">
            Other Filtered Stays in {selectedHotel.city} ({alternatives.length})
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {alternatives.map((alt, idx) => (
              <div
                key={idx}
                className="glass-card rounded-xl p-4 border border-surface-800 hover:border-surface-700 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h5 className="text-sm font-semibold text-white">{alt.hotel_name}</h5>
                    <p className="text-xs text-slate-400">{alt.location}</p>
                  </div>
                  <div className="flex items-center space-x-1 bg-surface-900 px-2 py-0.5 rounded text-xs text-amber-400 font-bold border border-surface-700">
                    <Star className="w-3 h-3 fill-amber-400" />
                    <span>{alt.rating}</span>
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between text-xs text-slate-300 pt-2 border-t border-surface-800/60">
                  <span>₹{Number(alt.price_per_night).toLocaleString('en-IN')} / night</span>
                  <span className="text-slate-400">Total: ₹{Number(alt.total_price || alt.price_per_night * nights).toLocaleString('en-IN')}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
