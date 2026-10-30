import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Compass, Sparkles, MapPin, Bookmark, Menu, X, LogOut, LogIn, User, LayoutDashboard, Sliders } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Trip Planner', path: '/planner' },
    { name: 'Destinations', path: '/destinations' },
    { name: 'My Trips', path: '/my-trips' },
    { name: 'Dashboard', path: '/dashboard' },
  ];

  const isActive = (path) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && (location.pathname === path || (path === '/planner' && location.pathname === '/plan'))) return true;
    return false;
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-50 bg-[#F8F7F4]/90 backdrop-blur-md border-b border-[#E8E7E3]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center space-x-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-[#3D6E57] flex items-center justify-center text-white shadow-sm transition-transform duration-200 group-hover:scale-105">
              <Compass className="w-4.5 h-4.5" />
            </div>
            <div>
              <span className="text-lg font-semibold tracking-tight text-[#222222]">
                TravelSync
              </span>
              <span className="ml-1.5 text-[10px] font-medium tracking-widest text-[#3D6E57] uppercase bg-[#EBF2EE] px-1.5 py-0.5 rounded">
                AI
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1" aria-label="Main Navigation">
            {navLinks.map((link) => {
              const active = isActive(link.path);
              return (
                <Link
                  key={link.name}
                  to={link.path}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    active
                      ? 'bg-[#EBF2EE] text-[#2F5844] font-semibold'
                      : 'text-[#666660] hover:text-[#222222] hover:bg-[#F0EFEA]'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Desktop Auth Controls & CTA */}
          <div className="hidden md:flex items-center space-x-3">
            {isAuthenticated ? (
              <div className="flex items-center space-x-2">
                <Link
                  to="/profile"
                  className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white border border-[#E8E7E3] text-xs text-[#222222] hover:border-[#CADCD2] transition-colors"
                >
                  <div className="w-5 h-5 rounded-full bg-[#EBF2EE] text-[#2F5844] flex items-center justify-center font-bold text-[10px]">
                    {user?.name ? user.name[0].toUpperCase() : 'U'}
                  </div>
                  <span className="font-medium text-xs truncate max-w-[100px]">{user?.name || 'Traveler'}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-1.5 rounded-lg text-[#666660] hover:text-rose-600 hover:bg-rose-50 border border-transparent transition-colors"
                  title="Sign Out"
                  aria-label="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-[#FAF9F6] text-[#222222] font-medium text-xs border border-[#E8E7E3] transition-all"
              >
                <LogIn className="w-3.5 h-3.5 text-[#666660]" />
                <span>Sign In</span>
              </Link>
            )}

            <Link
              to="/planner"
              className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-[#3D6E57] hover:bg-[#2F5844] text-white text-xs font-medium shadow-sm transition-all"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Plan Trip</span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-[#666660] hover:text-[#222222] hover:bg-[#F0EFEA] focus:outline-none"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-[#E8E7E3] bg-[#F8F7F4] px-4 pt-2 pb-4 space-y-1">
          {navLinks.map((link) => {
            const active = isActive(link.path);
            return (
              <Link
                key={link.name}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  active
                    ? 'bg-[#EBF2EE] text-[#2F5844] font-semibold'
                    : 'text-[#666660] hover:text-[#222222] hover:bg-[#F0EFEA]'
                }`}
              >
                <span>{link.name}</span>
              </Link>
            );
          })}

          <div className="pt-2 border-t border-[#E8E7E3] flex flex-col gap-2">
            {isAuthenticated ? (
              <div className="flex items-center justify-between px-3 py-2 bg-white rounded-lg border border-[#E8E7E3]">
                <span className="text-xs text-[#222222] font-medium">Signed in as {user?.name}</span>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="text-xs text-rose-600 hover:underline font-medium"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full flex items-center justify-center space-x-2 px-3 py-2 rounded-lg bg-white text-[#222222] text-xs font-medium border border-[#E8E7E3]"
              >
                <LogIn className="w-4 h-4 text-[#666660]" />
                <span>Sign In</span>
              </Link>
            )}

            <Link
              to="/planner"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center space-x-2 px-3 py-2 rounded-lg bg-[#3D6E57] text-white text-xs font-medium shadow-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span>Plan Trip</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
