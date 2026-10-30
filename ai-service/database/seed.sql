-- TravelSync Seed Data
-- Curated Hotels (45+) and Attractions (45+) across Bali, Goa, Mumbai, Delhi, Jaipur, Bangkok, Singapore, Dubai

-- Clear existing data if necessary
DELETE FROM activities;
DELETE FROM itineraries;
DELETE FROM agent_logs;
DELETE FROM flights;
DELETE FROM trips;
DELETE FROM hotels;
DELETE FROM attractions;

-- ==============================================================================
-- HOTELS DATASET
-- ==============================================================================

-- --- 1. BALI, INDONESIA ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Amnaya Resort Kuta', 'Bali', 'Kuta / Tuban', 4.8, 4200.00, 'Deluxe Room with Balcony', 'Free WiFi, Swimming Pool, Spa, Breakfast Included, Fitness Center, Airport Shuttle', -8.729100, 115.169200, 1.2),
('Padma Resort Legian', 'Bali', 'Legian Beachfront', 4.9, 9500.00, 'Ocean View Suite', 'Infinity Pool, Private Beach Access, Lagoon Bar, Full Spa, Kids Club, Tennis Court', -8.705800, 115.163900, 3.5),
('Grandmas Plus Hotel Seminyak', 'Bali', 'Seminyak Central', 4.4, 1950.00, 'Superior Double Room', 'High Speed WiFi, Spa, Walking Distance to Beach, 24h Front Desk, Air Conditioning', -8.691200, 115.158400, 4.8),
('Komaneka at Bisma Ubud', 'Bali', 'Ubud Valley', 4.9, 8200.00, 'Jungle View Villa', 'Valley Infinity Pool, Organic Breakfast, Daily Yoga, Spa Sanctuary, Shuttle to Ubud Center', -8.513500, 115.258200, 22.0),
('Puri Garden Hotel & Hostel', 'Bali', 'Pengosekan, Ubud', 4.6, 2400.00, 'Private Poolside Room', 'Puppy Therapy Sessions, Daily Free Yoga, Pool, Free Breakfast, Evening BBQ', -8.520400, 115.263500, 23.5),
('RIMBA by AYANA Bali', 'Bali', 'Jimbaran Cliffs', 4.8, 11500.00, 'Resort View King', 'Access to Rock Bar, 12 Swimming Pools, Private Beach, 19 Restaurants, Thalasso Spa', -8.788500, 115.141500, 12.4),
('Ubud Tropical Garden Resort', 'Bali', 'Monkey Forest Road, Ubud', 4.5, 3100.00, 'Garden Deluxe Bungalow', 'Tropical Garden, 2 Swimming Pools, Restaurant, Free Breakfast, Balinese Architecture', -8.517800, 115.261200, 22.8);

-- --- 2. GOA, INDIA ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Santana Beach Resort', 'Goa', 'Candolim Beach Road', 4.5, 3200.00, 'Standard AC Room', '2 Swimming Pools, Beach Access (100m), Multi-Cuisine Restaurant, Free Breakfast, Bar', 15.518200, 73.763400, 2.0),
('Taj Fort Aguada Resort & Spa', 'Goa', 'Sinquerim, Candolim', 4.8, 12500.00, 'Sea View Cottage', 'Historic Sea Views, World-Class Spa, Private Dining, Swimming Pool, Watersports', 15.492500, 73.769900, 4.5),
('W Goa', 'Goa', 'Vagator Beachfront', 4.7, 14000.00, 'Fabulous Room', 'Rock Pool, Sunsets at Woobar, AWAY Spa, 24/7 Gym, Direct Beach Path', 15.602800, 73.734800, 12.0),
('Thehosteller Goa Calangute', 'Goa', 'Calangute Market Road', 4.3, 1450.00, 'Private Deluxe AC Room', 'Rooftop Cafe, High-Speed WiFi, Social Lounge, Bike Rental, Pool Table', 15.541200, 73.755400, 1.0),
('Heritage Village Resort & Spa', 'Goa', 'Arossim Beach, South Goa', 4.6, 5800.00, 'Heritage Superior Room', 'Ayurvedic Spa, Swimming Pool, Portuguese Architecture, Live Entertainment', 15.328400, 73.899400, 24.0),
('Bloomrooms @ Calangute', 'Goa', 'Calangute, North Goa', 4.4, 2800.00, 'Signature Queen Room', 'Modern Minimalist Decor, Cloud Beds, Cafe, Swimming Pool, 24h Concierge', 15.539800, 73.761200, 1.5);

-- --- 3. MUMBAI, INDIA ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('The Taj Mahal Palace', 'Mumbai', 'Colaba Waterfront', 4.9, 18500.00, 'Heritage Palace Wing Room', 'Historic Landmark, Sea Facing, Fine Dining, Jiva Spa, Butler Service, Pool', 18.921700, 72.833200, 1.0),
('Residency Hotel Fort', 'Mumbai', 'Fort Heritage District', 4.5, 4200.00, 'Executive Double Room', 'High Speed WiFi, Free Breakfast, Central Historic Location, Concierge, Room Service', 18.935400, 72.834800, 1.8),
('Trident Nariman Point', 'Mumbai', 'Marine Drive', 4.7, 9800.00, 'Premier Sea View Room', 'Queens Necklace Panoramic Views, Outdoor Pool, Spa, 3 Award-Winning Restaurants', 18.927200, 72.821100, 2.2),
('Hotel Suba Palace', 'Mumbai', 'Apollo Bunder, Colaba', 4.3, 3600.00, 'Superior Room', 'Buffet Breakfast, Walking Distance to Gateway of India, Clean Modern Interiors', 18.922900, 72.832100, 1.1),
('JW Marriott Mumbai Juhu', 'Mumbai', 'Juhu Beachfront', 4.8, 13000.00, 'Deluxe Ocean View Room', 'Direct Juhu Beach Access, Saltwater Pool, Luxury Spa, Lotus Cafe, Nightclub', 19.100900, 72.826200, 18.5);

-- --- 4. DELHI, INDIA ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('The Imperial New Delhi', 'Delhi', 'Janpath, Connaught Place', 4.8, 14500.00, 'Heritage Colonial Room', 'Art Deco Architecture, Historic Gardens, 7 Restaurants, Imperial Spa, Outdoor Pool', 28.622900, 77.217700, 0.8),
('Bloomrooms @ Janpath', 'Delhi', 'Janpath, New Delhi', 4.4, 3400.00, 'Value Queen Room', 'Modern Minimalist, Spotless Clean, High Speed WiFi, Cafe, Metro Connectivity (200m)', 28.623100, 77.219500, 1.0),
('The Lalit New Delhi', 'Delhi', 'Barakhamba Road, Connaught Place', 4.6, 7500.00, 'Deluxe City View Room', 'Rooftop Pool, Rejuve Spa, Kitty Su Nightclub, 24h 24/7 Restaurant, Business Center', 28.630500, 77.228900, 1.2),
('Hotel City Star', 'Delhi', 'Pahar Ganj / Central Station', 4.2, 2100.00, 'Deluxe Room', 'Free Airport Pickup, Rooftop Restaurant, 24h Room Service, High Speed WiFi', 28.643200, 77.215400, 2.5),
('The Leela Palace New Delhi', 'Delhi', 'Chanakyapuri Diplomatic Enclave', 4.9, 19000.00, 'Grande Deluxe Room', 'Rooftop Temperature-Controlled Infinity Pool, ESPA Spa, Michelin Star Dining (Le Cirque)', 28.579800, 77.186200, 6.0);

-- --- 5. JAIPUR, INDIA ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Umaid Bhawan - A Heritage Style Boutique Hotel', 'Jaipur', 'Bani Park', 4.6, 3800.00, 'Royal Deluxe Room', 'Traditional Rajasthani Frescoes, Swimming Pool, Rooftop Puppet Show & Restaurant', 26.927200, 75.790500, 2.5),
('Rambagh Palace', 'Jaipur', 'Bhawani Singh Road', 4.9, 28000.00, 'Palace Room', 'Former Royal Residence, Peacocks on Lawn, Polo Bar, Jiva Grande Spa, Royal Butler', 26.897800, 75.808900, 4.0),
('Pearl Palace Heritage Boutique Hotel', 'Jaipur', 'Ajmer Road', 4.7, 2600.00, 'Heritage Themed Room', 'Unique Handcrafted Rooms, Peacock Rooftop Restaurant nearby, High-Speed WiFi', 26.912400, 75.789100, 2.0),
('ITC Rajputana, a Luxury Collection Hotel', 'Jaipur', 'Palace Road', 4.7, 8900.00, 'Rajputana Chamber', 'Kaya Kalp Spa, Outdoor Pool, Royal Dining (Peshawri), Lush Courtyards', 26.920400, 75.795800, 1.8),
('Hotel Kalyan Heritage', 'Jaipur', 'Hathroi Fort, Ajmer Road', 4.3, 1750.00, 'Deluxe AC Room', 'Rooftop Restaurant with Fort View, Friendly Staff, Travel Desk, Free WiFi', 26.915200, 75.792500, 2.1);

-- --- 6. BANGKOK, THAILAND ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Amara Bangkok Hotel', 'Bangkok', 'Surawong / Silom', 4.6, 4600.00, 'Executive Room', 'Rooftop Sky Pool, 24h Sky Gym, High-Speed WiFi, Silom Night Market Walking Distance', 13.729100, 100.528400, 2.0),
('Siam Kempinski Hotel Bangkok', 'Bangkok', 'Pathum Wan / Siam Paragon', 4.9, 16500.00, 'Cabana Room with Pool Access', 'Multiple Freeform Pools, Michelin Star Sra Bua by Kiin Kiin, Direct Siam Paragon Mall Path', 13.748900, 100.535800, 0.5),
('Ibis Styles Bangkok Silom', 'Bangkok', 'Silom Road', 4.4, 2700.00, 'Standard Room', 'Rooftop Pool, Colorful Pop Art Decor, Near Sala Daeng BTS & Silom MRT, Buffet Breakfast', 13.727800, 100.532100, 2.2),
('Chatrium Hotel Riverside Bangkok', 'Bangkok', 'Chao Phraya Riverside', 4.7, 7800.00, 'Grand Room River View', 'Infinity Pool overlooking River, Free River Shuttle Boat to BTS, Riverside Terrace', 13.710500, 100.508200, 4.5),
('Lub d Bangkok Siam', 'Bangkok', 'Rama 1 Road, Siam', 4.5, 2100.00, 'Deluxe Private Double', 'Next to National Stadium BTS, Cinema Lounge, Trendy Bar, Fast WiFi, Laundry', 13.746800, 100.529800, 1.0);

-- --- 7. SINGAPORE ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Marina Bay Sands', 'Singapore', 'Marina Bay', 4.8, 32000.00, 'Deluxe City View Room', 'World-Famous 57th Floor Infinity Pool, SkyPark Observation Deck, Casino, Luxury Mall', 1.283800, 103.859100, 1.0),
('Hotel G Singapore', 'Singapore', 'Bugis / Middle Road', 4.4, 6200.00, 'Good Queen Room', 'Boutique Lifestyle Hotel, 2 Renowned Restaurants (25 Degrees Burger), High-Speed WiFi', 1.299500, 103.852400, 1.5),
('PARKROYAL COLLECTION Pickering', 'Singapore', 'Chinatown / Upper Pickering', 4.7, 14800.00, 'Urban Room', 'Hotel-in-a-Garden Architecture, Dedicated Wellness Floor, Infinity Pool, St. Gregory Spa', 1.286200, 103.847100, 1.2),
('YOTEL Singapore Orchard Road', 'Singapore', 'Orchard Road', 4.5, 7400.00, 'Premium Queen Cabin', 'Smart Space-Saving Cabins, Robot Room Service, Outdoor Pool, Heart of Orchard Shopping', 1.306100, 103.832500, 3.0),
('Champion Hotel', 'Singapore', 'Joo Chiat / Katong', 4.2, 3900.00, 'Superior Double Room', 'Heritage Peranakan Neighborhood, Quiet Clean Rooms, Free WiFi, Delicious Food Nearby', 1.314800, 103.901500, 6.8);

-- --- 8. DUBAI, UAE ---
INSERT INTO hotels (hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center) VALUES
('Rove Downtown Dubai', 'Dubai', 'Downtown Dubai', 4.6, 5200.00, 'Rover Room Burj View', 'Burj Khalifa Views, Outdoor Saltwater Pool, 24h Laundromat, The Daily Restaurant, Reel Cinema', 25.201400, 55.279800, 1.0),
('Atlantis, The Palm', 'Dubai', 'Palm Jumeirah', 4.8, 26000.00, 'Ocean King Room', 'Unlimited Aquaventure Waterpark Access, The Lost Chambers Aquarium, Nobu Restaurant, Private Beach', 25.130400, 55.117200, 18.0),
('Citymax Hotel Bur Dubai', 'Dubai', 'Bur Dubai Heritage Quarter', 4.2, 2900.00, 'Standard Queen Room', 'Rooftop Pool, 24h Gym, Huddle Sports Bar, Free Shuttle to Dubai Mall & Beach', 25.248200, 55.297400, 6.5),
('Address Sky View', 'Dubai', 'Downtown Dubai', 4.9, 19500.00, 'Sky View Room', 'Twin-Tower Infinity Pool overlooking Burj Khalifa, Glass SkyWalk, Luxury Spa, Ce La Vi Club', 25.201800, 55.267800, 1.2),
('Millennium Place Dubai Marina', 'Dubai', 'Dubai Marina', 4.5, 6800.00, 'Superior Marina View Room', 'Walking Distance to Marina Walk & JBR Beach, MasterChef TV Experience Restaurant, Pool', 25.074500, 55.139400, 19.5);


-- ==============================================================================
-- ATTRACTIONS DATASET
-- ==============================================================================

-- --- 1. BALI, INDONESIA ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Uluwatu Temple & Sunset Kecak Dance', 'Bali', -8.829100, 115.084900, 'culture', 3.0, 850.00),
('Ubud Sacred Monkey Forest Sanctuary', 'Bali', -8.518800, 115.260600, 'nature', 2.5, 450.00),
('Tegallalang Rice Terraces & Jungle Swing', 'Bali', -8.434900, 115.278500, 'nature', 3.0, 650.00),
('Seminyak Beach & Sunset Beach Clubs', 'Bali', -8.691200, 115.158400, 'beaches', 3.5, 300.00),
('Tanah Lot Sea Temple', 'Bali', -8.621200, 115.086800, 'culture', 2.5, 400.00),
('Mount Batur Sunrise Trekking', 'Bali', -8.242300, 115.375200, 'adventure', 5.0, 1800.00),
('Nusa Dua Beach & Water Blow', 'Bali', -8.802100, 115.234100, 'beaches', 3.0, 150.00),
('Jimbaran Bay Seafood Candlelight Dinner', 'Bali', -8.769200, 115.166800, 'food', 2.5, 1200.00),
('Tegenungan Waterfall & River Dip', 'Bali', -8.575200, 115.289400, 'adventure', 2.0, 250.00),
('Ubud Traditional Art Market & Palace', 'Bali', -8.506900, 115.262500, 'culture', 2.0, 100.00);

-- --- 2. GOA, INDIA ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Fort Aguada & Lighthouse', 'Goa', 15.492500, 73.773800, 'culture', 2.0, 100.00),
('Baga & Calangute Beach Watersports', 'Goa', 15.555300, 73.751700, 'adventure', 4.0, 1500.00),
('Basilica of Bom Jesus & Old Goa Churches', 'Goa', 15.500900, 73.911600, 'culture', 2.5, 50.00),
('Anjuna Flea Market & Sunset Point', 'Goa', 15.580400, 73.742800, 'nightlife', 3.0, 200.00),
('Dudhsagar Waterfalls Trek & Safari', 'Goa', 15.314400, 74.314300, 'adventure', 6.0, 2200.00),
('Palolem Beach & Silent Noise Headphone Party', 'Goa', 15.010000, 74.023200, 'beaches', 4.0, 500.00),
('Fontainhas Latin Quarter Heritage Walk', 'Goa', 15.498900, 73.834400, 'culture', 2.0, 300.00),
('Fishermans Wharf Riverside Goan Feast', 'Goa', 15.228100, 73.948200, 'food', 2.0, 950.00);

-- --- 3. MUMBAI, INDIA ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Gateway of India & Colaba Causeway Walk', 'Mumbai', 18.922000, 72.834700, 'culture', 2.5, 0.00),
('Marine Drive Promenade & Chowpatty Street Food', 'Mumbai', 18.943200, 72.823000, 'beaches', 2.5, 250.00),
('Elephanta Caves Island Boat Trip', 'Mumbai', 18.963300, 72.931500, 'culture', 4.5, 450.00),
('Chhatrapati Shivaji Maharaj Terminus (CSMT)', 'Mumbai', 18.940000, 72.835400, 'culture', 1.5, 0.00),
('Bandra Bandstand, Fort & Street Cafes', 'Mumbai', 19.043800, 72.819800, 'nightlife', 3.0, 400.00),
('Sanjay Gandhi National Park & Kanheri Caves', 'Mumbai', 19.221500, 72.912600, 'adventure', 4.0, 300.00),
('Mohammed Ali Road Iconic Food Trail', 'Mumbai', 18.956800, 72.834100, 'food', 2.5, 600.00);

-- --- 4. DELHI, INDIA ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Qutub Minar Complex', 'Delhi', 28.524500, 77.185500, 'culture', 2.0, 250.00),
('Red Fort (Lal Qila) & Sound and Light Show', 'Delhi', 28.656200, 77.241000, 'culture', 3.0, 300.00),
('Humayuns Tomb & Sunder Nursery Walk', 'Delhi', 28.593300, 77.250700, 'nature', 2.5, 200.00),
('India Gate & Kartavya Path Stroll', 'Delhi', 28.612900, 77.229500, 'culture', 1.5, 0.00),
('Chandni Chowk Old Delhi Culinary & Spice Trail', 'Delhi', 28.650600, 77.230300, 'food', 3.0, 500.00),
('Swaminarayan Akshardham Temple & Water Show', 'Delhi', 28.612700, 77.277300, 'culture', 3.5, 350.00),
('Hauz Khas Village Fort, Lake & Nightlife', 'Delhi', 28.549400, 77.194700, 'nightlife', 3.0, 600.00);

-- --- 5. JAIPUR, INDIA ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Amber Fort & Sheesh Mahal Palace', 'Jaipur', 26.985500, 75.851300, 'culture', 3.5, 350.00),
('Hawa Mahal (Palace of Winds)', 'Jaipur', 26.923900, 75.826700, 'culture', 1.5, 100.00),
('City Palace & Royal Observatory (Jantar Mantar)', 'Jaipur', 26.925800, 75.823700, 'culture', 2.5, 400.00),
('Nahargarh Fort Sunset Viewpoint & Cycling', 'Jaipur', 26.937800, 75.815600, 'adventure', 3.0, 200.00),
('Johari Bazaar Gems & Traditional Textiles', 'Jaipur', 26.920400, 75.828100, 'culture', 2.0, 150.00),
('Chokhi Dhani Rajasthani Cultural Village & Thali', 'Jaipur', 26.766300, 75.836200, 'food', 4.0, 1200.00),
('Galta Ji (Monkey Temple & Sacred Springs)', 'Jaipur', 26.916100, 75.858200, 'nature', 2.0, 100.00);

-- --- 6. BANGKOK, THAILAND ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('The Grand Palace & Wat Phra Kaew (Emerald Buddha)', 'Bangkok', 13.750000, 100.491400, 'culture', 3.0, 1200.00),
('Wat Arun (Temple of Dawn) River Ferry', 'Bangkok', 13.743700, 100.488800, 'culture', 2.0, 250.00),
('Chatuchak Weekend Market Shopping Spree', 'Bangkok', 13.799900, 100.550100, 'culture', 4.0, 300.00),
('Chinatown (Yaowarat Road) Night Street Food', 'Bangkok', 13.741200, 100.508300, 'food', 2.5, 600.00),
('Damnoen Saduak Floating Market Tour', 'Bangkok', 13.518600, 99.957500, 'adventure', 4.5, 1100.00),
('ICONSIAM Riverside Mall & Indoor Floating Market', 'Bangkok', 13.726700, 100.510900, 'nightlife', 3.0, 200.00),
('Lumphini Park Swan Boats & Monitor Lizards', 'Bangkok', 13.731400, 100.541600, 'nature', 2.0, 50.00);

-- --- 7. SINGAPORE ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Gardens by the Bay & Supertree Grove Light Show', 'Singapore', 1.281600, 103.863600, 'nature', 3.5, 1400.00),
('Marina Bay Sands SkyPark Observation Deck', 'Singapore', 1.283800, 103.859100, 'culture', 2.0, 1800.00),
('Sentosa Island & Universal Studios Singapore', 'Singapore', 1.254000, 103.823800, 'adventure', 6.0, 4800.00),
('Singapore Zoo & Night Safari Tram Tour', 'Singapore', 1.404300, 103.793000, 'nature', 4.5, 3200.00),
('Chinatown & Maxwell Hawker Centre Food Trail', 'Singapore', 1.280400, 103.844800, 'food', 2.5, 600.00),
('Little India & Haji Lane Street Murals', 'Singapore', 1.306000, 103.852400, 'culture', 2.5, 200.00),
('Jewel Changi Rain Vortex & Canopy Park', 'Singapore', 1.360200, 103.989800, 'nature', 2.5, 450.00);

-- --- 8. DUBAI, UAE ---
INSERT INTO attractions (attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost) VALUES
('Burj Khalifa 124th Floor & Dubai Fountain Show', 'Dubai', 25.197200, 55.274400, 'culture', 3.0, 3600.00),
('Dubai Desert Safari, Dune Bashing & BBQ Camp', 'Dubai', 24.831500, 55.612300, 'adventure', 6.0, 2800.00),
('Dubai Marina Yacht Cruise & JBR Walk', 'Dubai', 25.078400, 55.137800, 'beaches', 3.5, 1800.00),
('Dubai Mall Aquarium & Underwater Zoo', 'Dubai', 25.198500, 55.279600, 'nature', 2.5, 1900.00),
('Al Fahidi Historical District & Gold Souk Abra Ride', 'Dubai', 25.263100, 55.297200, 'culture', 3.0, 250.00),
('Museum of the Future', 'Dubai', 25.219200, 55.281900, 'culture', 2.5, 3200.00),
('Miracle Garden & Butterfly Park', 'Dubai', 25.059900, 55.244400, 'nature', 3.0, 1600.00);
