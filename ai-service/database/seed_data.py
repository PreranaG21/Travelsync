import logging
from database.db import SessionLocal, init_db
from database.models import Hotel, Attraction

logger = logging.getLogger("travelsync.seed")

# -----------------------------------------------------------------------
# Hotel seed data — 45+ hotels across 8 destinations
# -----------------------------------------------------------------------

HOTELS = [
    # BALI
    {"hotel_name": "Amnaya Resort Kuta", "city": "Bali", "location": "Kuta Beach Road, Bali", "rating": 4.8, "price_per_night": 4200.0, "room_type": "Deluxe Pool View", "amenities": "Free WiFi, Infinity Pool, Ocean View, Spa, Breakfast Included", "latitude": -8.7291, "longitude": 115.1692, "distance_from_center": 0.5},
    {"hotel_name": "Kuta Seaview Boutique Resort", "city": "Bali", "location": "Kuta, Bali", "rating": 4.5, "price_per_night": 3200.0, "room_type": "Superior Room", "amenities": "Free WiFi, Pool, Air Conditioning, Restaurant, Beach Access", "latitude": -8.7340, "longitude": 115.1725, "distance_from_center": 0.8},
    {"hotel_name": "Puri Garden Hotel & Hostel", "city": "Bali", "location": "Ubud Central, Bali", "rating": 4.3, "price_per_night": 2400.0, "room_type": "Garden View Room", "amenities": "Free WiFi, Garden, Terrace, Breakfast, Bicycle Rental", "latitude": -8.5069, "longitude": 115.2625, "distance_from_center": 1.2},
    {"hotel_name": "Grand Mirage Resort", "city": "Bali", "location": "Tanjung Benoa, Nusa Dua, Bali", "rating": 4.7, "price_per_night": 5800.0, "room_type": "Ocean Front Suite", "amenities": "All Inclusive, Private Beach, Water Sports, Spa, 5 Restaurants", "latitude": -8.7944, "longitude": 115.2302, "distance_from_center": 2.1},
    {"hotel_name": "Grandmas Plus Hotel Seminyak", "city": "Bali", "location": "Seminyak, Bali", "rating": 4.4, "price_per_night": 1950.0, "room_type": "Standard Double", "amenities": "Free WiFi, Pool, Bar, Air Conditioning, Laundry", "latitude": -8.6881, "longitude": 115.1590, "distance_from_center": 1.5},
    {"hotel_name": "The Layar Private Villas", "city": "Bali", "location": "Seminyak, Bali", "rating": 4.9, "price_per_night": 8500.0, "room_type": "Private Villa with Pool", "amenities": "Private Pool, Butler Service, Spa, Concierge, Gourmet Kitchen", "latitude": -8.6901, "longitude": 115.1570, "distance_from_center": 1.7},

    # GOA
    {"hotel_name": "Taj Holiday Village Resort & Spa", "city": "Goa", "location": "Candolim, North Goa", "rating": 4.8, "price_per_night": 6800.0, "room_type": "Sea Facing Cottage", "amenities": "Private Beach, Infinity Pool, Spa, 4 Restaurants, Water Sports", "latitude": 15.5167, "longitude": 73.7645, "distance_from_center": 1.2},
    {"hotel_name": "Alila Diwa Goa", "city": "Goa", "location": "Majorda, South Goa", "rating": 4.7, "price_per_night": 5500.0, "room_type": "Deluxe Room", "amenities": "Pool, Spa, Yoga, Restaurant, Beach Shuttle", "latitude": 15.3109, "longitude": 73.9142, "distance_from_center": 2.0},
    {"hotel_name": "Ibis Styles Goa Calangute", "city": "Goa", "location": "Calangute Beach, North Goa", "rating": 4.2, "price_per_night": 2800.0, "room_type": "Standard Room", "amenities": "Free WiFi, Pool, Bar, Breakfast Included", "latitude": 15.5441, "longitude": 73.7551, "distance_from_center": 0.4},
    {"hotel_name": "Zostel Goa", "city": "Goa", "location": "Arambol Beach, North Goa", "rating": 4.1, "price_per_night": 1200.0, "room_type": "Dormitory Bed", "amenities": "Free WiFi, Lounge, Communal Kitchen, Bonfire Area, Beach Access", "latitude": 15.6868, "longitude": 73.7031, "distance_from_center": 0.2},
    {"hotel_name": "Novotel Goa Candolim", "city": "Goa", "location": "Candolim, North Goa", "rating": 4.5, "price_per_night": 4200.0, "room_type": "Superior Room", "amenities": "Pool, Gym, Spa, Restaurant, Free WiFi, Beach Access", "latitude": 15.5183, "longitude": 73.7621, "distance_from_center": 0.9},

    # MUMBAI
    {"hotel_name": "The Taj Mahal Palace", "city": "Mumbai", "location": "Apollo Bunder, Colaba, Mumbai", "rating": 5.0, "price_per_night": 18000.0, "room_type": "Palace Room", "amenities": "Heritage Property, Sea View, Fine Dining, Spa, Concierge, Pool", "latitude": 18.9220, "longitude": 72.8347, "distance_from_center": 0.0},
    {"hotel_name": "Hotel Marine Plaza", "city": "Mumbai", "location": "Marine Drive, Mumbai", "rating": 4.3, "price_per_night": 5200.0, "room_type": "Sea View Room", "amenities": "Pool, Restaurant, Bar, Free WiFi, Gym", "latitude": 18.9398, "longitude": 72.8230, "distance_from_center": 2.1},
    {"hotel_name": "Trident Bandra Kurla", "city": "Mumbai", "location": "Bandra Kurla Complex, Mumbai", "rating": 4.6, "price_per_night": 7800.0, "room_type": "Deluxe Room", "amenities": "Pool, Gym, Spa, Business Center, Free WiFi", "latitude": 19.0640, "longitude": 72.8696, "distance_from_center": 5.2},
    {"hotel_name": "Zostel Mumbai", "city": "Mumbai", "location": "Fort, Mumbai", "rating": 4.0, "price_per_night": 900.0, "room_type": "Shared Dorm", "amenities": "Free WiFi, Lounge, Rooftop, City Views, Luggage Storage", "latitude": 18.9322, "longitude": 72.8355, "distance_from_center": 0.5},
    {"hotel_name": "Holiday Inn Mumbai International Airport", "city": "Mumbai", "location": "Andheri East, Mumbai", "rating": 4.4, "price_per_night": 4500.0, "room_type": "Standard Room", "amenities": "Airport Shuttle, Free WiFi, Pool, Gym, Restaurant", "latitude": 19.0968, "longitude": 72.8650, "distance_from_center": 7.8},

    # DELHI
    {"hotel_name": "The Imperial New Delhi", "city": "Delhi", "location": "Janpath, Connaught Place, New Delhi", "rating": 4.9, "price_per_night": 15000.0, "room_type": "Heritage Suite", "amenities": "Heritage Property, Fine Dining, Spa, Pool, Art Gallery, Concierge", "latitude": 28.6271, "longitude": 77.2196, "distance_from_center": 0.4},
    {"hotel_name": "Vivanta New Delhi Dwarka", "city": "Delhi", "location": "Dwarka, New Delhi", "rating": 4.5, "price_per_night": 5500.0, "room_type": "Superior Room", "amenities": "Pool, Spa, Gym, Restaurant, Metro Access, Free WiFi", "latitude": 28.5921, "longitude": 77.0460, "distance_from_center": 8.2},
    {"hotel_name": "Bloom Hotel Connaught Place", "city": "Delhi", "location": "Connaught Place, New Delhi", "rating": 4.2, "price_per_night": 2800.0, "room_type": "Deluxe Room", "amenities": "Free WiFi, Breakfast, Air Conditioning, 24hr Reception", "latitude": 28.6315, "longitude": 77.2167, "distance_from_center": 0.8},
    {"hotel_name": "Zostel Delhi", "city": "Delhi", "location": "Paharganj, New Delhi", "rating": 4.0, "price_per_night": 750.0, "room_type": "Dormitory Bed", "amenities": "Free WiFi, Common Area, Luggage Storage, Travel Desk", "latitude": 28.6448, "longitude": 77.2128, "distance_from_center": 1.5},

    # JAIPUR
    {"hotel_name": "Rambagh Palace", "city": "Jaipur", "location": "Bhawani Singh Road, Jaipur", "rating": 5.0, "price_per_night": 22000.0, "room_type": "Palace Suite", "amenities": "Royal Heritage, Gardens, Spa, Pool, Fine Dining, Polo Ground", "latitude": 26.8878, "longitude": 75.8141, "distance_from_center": 3.0},
    {"hotel_name": "Hotel Arya Niwas", "city": "Jaipur", "location": "Sansar Chandra Road, Jaipur", "rating": 4.2, "price_per_night": 2200.0, "room_type": "Standard Room", "amenities": "Garden, Restaurant, WiFi, Tour Desk, Room Service", "latitude": 26.9086, "longitude": 75.8166, "distance_from_center": 0.8},
    {"hotel_name": "Pearl Palace Heritage", "city": "Jaipur", "location": "Hathroi Fort Area, Jaipur", "rating": 4.5, "price_per_night": 1800.0, "room_type": "Heritage Room", "amenities": "Rooftop Restaurant, Free WiFi, Tours, Courtyard, Heritage Decor", "latitude": 26.9232, "longitude": 75.8052, "distance_from_center": 1.2},

    # BANGKOK
    {"hotel_name": "Mandarin Oriental Bangkok", "city": "Bangkok", "location": "Charoenkrung Road, Bangkok", "rating": 5.0, "price_per_night": 20000.0, "room_type": "River View Suite", "amenities": "River View, Heritage Property, Spa, Fine Dining, Fitness, Pool", "latitude": 13.7230, "longitude": 100.5167, "distance_from_center": 1.5},
    {"hotel_name": "Ibis Bangkok Sukhumvit", "city": "Bangkok", "location": "Sukhumvit 4, Bangkok", "rating": 4.2, "price_per_night": 2600.0, "room_type": "Standard Room", "amenities": "Free WiFi, Pool, Bar, BTS Access, 24hr Front Desk", "latitude": 13.7424, "longitude": 100.5566, "distance_from_center": 2.8},
    {"hotel_name": "NapPark Hostel Bangkok", "city": "Bangkok", "location": "Khaosan Road, Bangkok", "rating": 4.0, "price_per_night": 900.0, "room_type": "Capsule Bed", "amenities": "Free WiFi, Rooftop Lounge, Locker, Common Kitchen, Central Location", "latitude": 13.7585, "longitude": 100.4970, "distance_from_center": 0.5},
    {"hotel_name": "Chatrium Hotel Riverside Bangkok", "city": "Bangkok", "location": "Charoen Krung, Bangkok", "rating": 4.6, "price_per_night": 5800.0, "room_type": "River View Suite", "amenities": "Riverside Pool, Spa, 3 Restaurants, Gym, River Shuttle, Free WiFi", "latitude": 13.7125, "longitude": 100.5117, "distance_from_center": 2.2},

    # SINGAPORE
    {"hotel_name": "Marina Bay Sands", "city": "Singapore", "location": "Bay Front, Marina Bay, Singapore", "rating": 4.8, "price_per_night": 28000.0, "room_type": "Deluxe Room Marina View", "amenities": "Infinity Pool, Casino, Skypark, 3 Hotels, Fine Dining, Shopping", "latitude": 1.2839, "longitude": 103.8607, "distance_from_center": 0.3},
    {"hotel_name": "Hotel Indigo Singapore Katong", "city": "Singapore", "location": "Marine Parade Road, Katong, Singapore", "rating": 4.5, "price_per_night": 8500.0, "room_type": "Heritage Room", "amenities": "Peranakan Heritage, Pool, Restaurant, Free WiFi, Gym", "latitude": 1.3036, "longitude": 103.9025, "distance_from_center": 4.5},
    {"hotel_name": "Ibis Singapore on Bencoolen", "city": "Singapore", "location": "Bencoolen Street, Singapore", "rating": 4.1, "price_per_night": 4200.0, "room_type": "Standard Room", "amenities": "Free WiFi, Restaurant, Gym, Central Location, MRT Access", "latitude": 1.2988, "longitude": 103.8502, "distance_from_center": 0.8},

    # DUBAI
    {"hotel_name": "Burj Al Arab Jumeirah", "city": "Dubai", "location": "Jumeirah Beach Road, Dubai", "rating": 5.0, "price_per_night": 95000.0, "room_type": "Deluxe Suite", "amenities": "Luxury Butler, Private Beach, Helipad, 9 Restaurants, Spa, Rolls Royce Transfer", "latitude": 25.1412, "longitude": 55.1853, "distance_from_center": 4.2},
    {"hotel_name": "JW Marriott Marquis Dubai", "city": "Dubai", "location": "Sheikh Zayed Road, Business Bay, Dubai", "rating": 4.8, "price_per_night": 18000.0, "room_type": "Deluxe King Room", "amenities": "Pool, Spa, 8 Restaurants, Gym, Concierge, Metro Access", "latitude": 25.1866, "longitude": 55.2705, "distance_from_center": 2.1},
    {"hotel_name": "Rove City Centre Dubai", "city": "Dubai", "location": "Deira, Dubai", "rating": 4.4, "price_per_night": 5500.0, "room_type": "Standard Room", "amenities": "Pool, Gym, Free WiFi, Restaurant, Parking, Metro Access", "latitude": 25.2522, "longitude": 55.3300, "distance_from_center": 3.5},
    {"hotel_name": "Premier Inn Dubai Al Jaddaf", "city": "Dubai", "location": "Al Jaddaf, Dubai", "rating": 4.2, "price_per_night": 4200.0, "room_type": "Standard Double", "amenities": "Free WiFi, Pool, Restaurant, Gym, Metro Access, Free Parking", "latitude": 25.2285, "longitude": 55.3322, "distance_from_center": 5.1},
]

# -----------------------------------------------------------------------
# Attraction seed data — 45+ attractions across 8 destinations
# -----------------------------------------------------------------------

ATTRACTIONS = [
    # BALI
    {"attraction_name": "Tanah Lot Sea Temple", "destination": "Bali", "category": "culture", "estimated_visit_duration": 2.5, "estimated_cost": 60000.0 / 83, "latitude": -8.6215, "longitude": 115.0865},
    {"attraction_name": "Ubud Sacred Monkey Forest", "destination": "Bali", "category": "nature", "estimated_visit_duration": 2.0, "estimated_cost": 50000.0 / 83, "latitude": -8.5185, "longitude": 115.2591},
    {"attraction_name": "Tegallalang Rice Terraces & Jungle Swing", "destination": "Bali", "category": "adventure", "estimated_visit_duration": 3.0, "estimated_cost": 150000.0 / 83, "latitude": -8.4322, "longitude": 115.2814},
    {"attraction_name": "Mount Batur Sunrise Trekking", "destination": "Bali", "category": "adventure", "estimated_visit_duration": 5.0, "estimated_cost": 350000.0 / 83, "latitude": -8.2421, "longitude": 115.3752},
    {"attraction_name": "Seminyak Beach Sunset Walk", "destination": "Bali", "category": "beaches", "estimated_visit_duration": 2.5, "estimated_cost": 0.0, "latitude": -8.6862, "longitude": 115.1528},
    {"attraction_name": "Kecak Fire Dance at Uluwatu", "destination": "Bali", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 100000.0 / 83, "latitude": -8.8291, "longitude": 115.0849},
    {"attraction_name": "Jimbaran Bay Seafood Candlelight Dinner", "destination": "Bali", "category": "food", "estimated_visit_duration": 2.5, "estimated_cost": 200000.0 / 83, "latitude": -8.7817, "longitude": 115.1579},
    {"attraction_name": "Tirta Empul Holy Water Temple", "destination": "Bali", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 50000.0 / 83, "latitude": -8.4155, "longitude": 115.3150},
    {"attraction_name": "Nusa Penida Day Trip & Kelingking Beach", "destination": "Bali", "category": "beaches", "estimated_visit_duration": 8.0, "estimated_cost": 500000.0 / 83, "latitude": -8.7291, "longitude": 115.5026},

    # GOA
    {"attraction_name": "Baga Beach & Water Sports", "destination": "Goa", "category": "beaches", "estimated_visit_duration": 4.0, "estimated_cost": 800.0, "latitude": 15.5530, "longitude": 73.7545},
    {"attraction_name": "Basilica of Bom Jesus", "destination": "Goa", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 50.0, "latitude": 15.5009, "longitude": 73.9116},
    {"attraction_name": "Chapora Fort Sunset View", "destination": "Goa", "category": "adventure", "estimated_visit_duration": 2.0, "estimated_cost": 0.0, "latitude": 15.6039, "longitude": 73.7390},
    {"attraction_name": "Dudhsagar Waterfalls Jeep Safari", "destination": "Goa", "category": "nature", "estimated_visit_duration": 6.0, "estimated_cost": 1500.0, "latitude": 15.3143, "longitude": 74.3145},
    {"attraction_name": "Anjuna Flea Market", "destination": "Goa", "category": "culture", "estimated_visit_duration": 2.5, "estimated_cost": 0.0, "latitude": 15.5736, "longitude": 73.7391},
    {"attraction_name": "Spice Plantation Tour & Lunch", "destination": "Goa", "category": "food", "estimated_visit_duration": 3.0, "estimated_cost": 850.0, "latitude": 15.4340, "longitude": 73.9900},

    # MUMBAI
    {"attraction_name": "Gateway of India", "destination": "Mumbai", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 0.0, "latitude": 18.9220, "longitude": 72.8347},
    {"attraction_name": "Marine Drive Evening Walk", "destination": "Mumbai", "category": "beaches", "estimated_visit_duration": 2.0, "estimated_cost": 0.0, "latitude": 18.9399, "longitude": 72.8231},
    {"attraction_name": "Elephanta Caves Ferry Trip", "destination": "Mumbai", "category": "culture", "estimated_visit_duration": 4.0, "estimated_cost": 650.0, "latitude": 18.9633, "longitude": 72.9315},
    {"attraction_name": "Dharavi Slum Reality Tour", "destination": "Mumbai", "category": "culture", "estimated_visit_duration": 2.5, "estimated_cost": 800.0, "latitude": 19.0422, "longitude": 72.8538},
    {"attraction_name": "Crawford Market & Street Food Trail", "destination": "Mumbai", "category": "food", "estimated_visit_duration": 2.0, "estimated_cost": 400.0, "latitude": 18.9471, "longitude": 72.8334},

    # DELHI
    {"attraction_name": "Red Fort (Lal Qila)", "destination": "Delhi", "category": "culture", "estimated_visit_duration": 2.5, "estimated_cost": 35.0, "latitude": 28.6562, "longitude": 77.2410},
    {"attraction_name": "Qutub Minar Complex", "destination": "Delhi", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 40.0, "latitude": 28.5244, "longitude": 77.1855},
    {"attraction_name": "India Gate & Rajpath", "destination": "Delhi", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 0.0, "latitude": 28.6129, "longitude": 77.2295},
    {"attraction_name": "Humayun's Tomb", "destination": "Delhi", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 40.0, "latitude": 28.5933, "longitude": 77.2507},
    {"attraction_name": "Chandni Chowk Street Food Walk", "destination": "Delhi", "category": "food", "estimated_visit_duration": 3.0, "estimated_cost": 500.0, "latitude": 28.6506, "longitude": 77.2334},
    {"attraction_name": "Lotus Temple", "destination": "Delhi", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 0.0, "latitude": 28.5535, "longitude": 77.2588},

    # JAIPUR
    {"attraction_name": "Amber Fort & Elephant Ride", "destination": "Jaipur", "category": "culture", "estimated_visit_duration": 3.0, "estimated_cost": 1200.0, "latitude": 26.9855, "longitude": 75.8514},
    {"attraction_name": "Hawa Mahal (Palace of Winds)", "destination": "Jaipur", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 50.0, "latitude": 26.9239, "longitude": 75.8267},
    {"attraction_name": "City Palace Museum", "destination": "Jaipur", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 500.0, "latitude": 26.9258, "longitude": 75.8237},
    {"attraction_name": "Nahargarh Fort Sunset", "destination": "Jaipur", "category": "adventure", "estimated_visit_duration": 2.5, "estimated_cost": 100.0, "latitude": 26.9450, "longitude": 75.8043},
    {"attraction_name": "Johari Bazaar Gem Shopping", "destination": "Jaipur", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 0.0, "latitude": 26.9222, "longitude": 75.8239},

    # BANGKOK
    {"attraction_name": "Grand Palace & Temple of Emerald Buddha", "destination": "Bangkok", "category": "culture", "estimated_visit_duration": 3.0, "estimated_cost": 500.0, "latitude": 13.7500, "longitude": 100.4913},
    {"attraction_name": "Wat Pho Reclining Buddha", "destination": "Bangkok", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 200.0, "latitude": 13.7466, "longitude": 100.4930},
    {"attraction_name": "Chatuchak Weekend Market", "destination": "Bangkok", "category": "food", "estimated_visit_duration": 3.5, "estimated_cost": 500.0, "latitude": 13.7999, "longitude": 100.5503},
    {"attraction_name": "Chao Phraya River Night Cruise", "destination": "Bangkok", "category": "nightlife", "estimated_visit_duration": 2.5, "estimated_cost": 800.0, "latitude": 13.7563, "longitude": 100.4930},
    {"attraction_name": "Wat Arun Temple at Sunrise", "destination": "Bangkok", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 100.0, "latitude": 13.7437, "longitude": 100.4888},
    {"attraction_name": "Yaowarat Chinatown Street Food Tour", "destination": "Bangkok", "category": "food", "estimated_visit_duration": 2.5, "estimated_cost": 600.0, "latitude": 13.7390, "longitude": 100.5101},

    # SINGAPORE
    {"attraction_name": "Gardens by the Bay (Supertree Grove)", "destination": "Singapore", "category": "nature", "estimated_visit_duration": 3.0, "estimated_cost": 1800.0, "latitude": 1.2816, "longitude": 103.8636},
    {"attraction_name": "Sentosa Island & Universal Studios", "destination": "Singapore", "category": "adventure", "estimated_visit_duration": 7.0, "estimated_cost": 6500.0, "latitude": 1.2544, "longitude": 103.8199},
    {"attraction_name": "Merlion Park & Marina Bay", "destination": "Singapore", "category": "culture", "estimated_visit_duration": 1.5, "estimated_cost": 0.0, "latitude": 1.2868, "longitude": 103.8545},
    {"attraction_name": "Singapore Hawker Center Food Crawl", "destination": "Singapore", "category": "food", "estimated_visit_duration": 2.5, "estimated_cost": 1200.0, "latitude": 1.3048, "longitude": 103.8318},
    {"attraction_name": "Little India & Arab Street Heritage Walk", "destination": "Singapore", "category": "culture", "estimated_visit_duration": 3.0, "estimated_cost": 200.0, "latitude": 1.3066, "longitude": 103.8518},

    # DUBAI
    {"attraction_name": "Burj Khalifa Observation Deck", "destination": "Dubai", "category": "adventure", "estimated_visit_duration": 2.5, "estimated_cost": 4000.0, "latitude": 25.1972, "longitude": 55.2744},
    {"attraction_name": "Dubai Mall & Dubai Fountain", "destination": "Dubai", "category": "culture", "estimated_visit_duration": 3.0, "estimated_cost": 0.0, "latitude": 25.1985, "longitude": 55.2796},
    {"attraction_name": "Desert Safari with Dune Bashing", "destination": "Dubai", "category": "adventure", "estimated_visit_duration": 6.0, "estimated_cost": 5000.0, "latitude": 24.9832, "longitude": 55.3789},
    {"attraction_name": "Gold Souk & Spice Souk Walking Tour", "destination": "Dubai", "category": "culture", "estimated_visit_duration": 2.0, "estimated_cost": 0.0, "latitude": 25.2697, "longitude": 55.3033},
    {"attraction_name": "Palm Jumeirah Monorail & Beach", "destination": "Dubai", "category": "beaches", "estimated_visit_duration": 3.0, "estimated_cost": 1500.0, "latitude": 25.1121, "longitude": 55.1389},
]


def seed_database_if_empty():
    """
    Called at application startup.
    Creates all tables, then seeds hotels and attractions if tables are empty.
    """
    from database.db import init_db
    init_db()

    db = SessionLocal()
    try:
        hotel_count = db.query(Hotel).count()
        if hotel_count == 0:
            for h in HOTELS:
                db.add(Hotel(**h))
            db.commit()
            logger.info(f"Seeded {len(HOTELS)} hotels into database.")
        else:
            logger.info(f"Hotels already seeded ({hotel_count} records). Skipping.")

        attraction_count = db.query(Attraction).count()
        if attraction_count == 0:
            for a in ATTRACTIONS:
                db.add(Attraction(**a))
            db.commit()
            logger.info(f"Seeded {len(ATTRACTIONS)} attractions into database.")
        else:
            logger.info(f"Attractions already seeded ({attraction_count} records). Skipping.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during database seeding: {e}", exc_info=True)
    finally:
        db.close()
