import React, { useState } from 'react';
import './App.css';
import { mockCountries, mockRadioStations } from './mock';
import CountrySelector from './components/CountrySelector';
import StationList from './components/StationList';
import RadioPlayer from './components/RadioPlayer';
import { Globe, Radio, Waves } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';

function App() {
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedStation, setSelectedStation] = useState(null);
  const [open, setOpen] = useState(false);

  const handleCountryChange = (country) => {
    setSelectedCountry(country);
    setSelectedStation(null); // Reset selected station when country changes
  };

  const handleStationSelect = (station) => {
    setSelectedStation(station);
  };

  const currentStations = selectedCountry ? mockRadioStations[selectedCountry.code] || [] : [];

  return (
    <div className="min-h-screen relative overflow-hidden bg-black">
      {/* Rotating Earth Background */}
      <div className="absolute inset-0 z-0">
        <div className="earth-container">
          <img 
            src="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHxlYXJ0aCUyMHNwYWNlfGVufDB8fHx8MTc1NTMzOTA3NXww&ixlib=rb-4.1.0&q=85"
            alt="Earth from space" 
            className="earth-image"
          />
        </div>
        <div className="absolute inset-0 bg-black/20"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen">
        {/* Header */}
        <header className="text-center py-8 px-4">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="relative">
              <Waves className="h-8 w-8 text-blue-400 animate-pulse" />
              <div className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Global Radio
            </h1>
            <Globe className="h-8 w-8 text-green-400 animate-spin" style={{ animationDuration: '20s' }} />
          </div>
          <p className="text-white/80 text-lg max-w-2xl mx-auto">
            Tune into radio stations from around the world. Select your country and discover local frequencies.
          </p>
        </header>

        {/* Main Content */}
        <div className="container mx-auto px-4 pb-8">
          <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            
            {/* Left Column - Country Selection */}
            <div className="lg:col-span-1 space-y-6">
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Globe className="h-5 w-5" />
                    Select Country
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CountrySelector
                    countries={mockCountries}
                    selectedCountry={selectedCountry}
                    onCountryChange={handleCountryChange}
                    open={open}
                    setOpen={setOpen}
                  />
                </CardContent>
              </Card>

              {/* Radio Player */}
              <RadioPlayer 
                station={selectedStation} 
                onClose={() => setSelectedStation(null)} 
              />
            </div>

            {/* Right Column - Station List */}
            <div className="lg:col-span-2">
              <Card className="bg-white/5 backdrop-blur-sm border-white/10 min-h-[500px]">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Radio className="h-5 w-5" />
                    {selectedCountry ? `${selectedCountry.name} Radio Stations` : 'Radio Stations'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {selectedCountry ? (
                    <StationList
                      stations={currentStations}
                      onStationSelect={handleStationSelect}
                      selectedStation={selectedStation}
                    />
                  ) : (
                    <div className="text-center py-12">
                      <Globe className="h-16 w-16 mx-auto mb-4 text-white/30" />
                      <h3 className="text-xl text-white/70 mb-2">Choose Your Country</h3>
                      <p className="text-white/50">
                        Select a country from the sidebar to explore available radio stations
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default App;