import React from 'react';
import { Radio, Users, Play } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

const StationList = ({ stations, onStationSelect, selectedStation }) => {
  if (!stations || stations.length === 0) {
    return (
      <Card className="bg-white/5 backdrop-blur-sm border-white/10">
        <CardContent className="p-8 text-center">
          <Radio className="h-12 w-12 mx-auto mb-4 text-white/40" />
          <p className="text-white/60">No radio stations available for this country</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
        <Radio className="h-5 w-5" />
        Available Stations ({stations.length})
      </h3>
      
      {stations.map((station) => (
        <Card 
          key={station.id}
          className={`transition-all duration-300 cursor-pointer hover:scale-[1.02] ${
            selectedStation?.id === station.id
              ? 'bg-white/20 border-white/40 ring-2 ring-white/30'
              : 'bg-white/5 border-white/10 hover:bg-white/10'
          }`}
          onClick={() => onStationSelect(station)}
        >
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <div className="flex-1">
                    <h4 className="font-semibold text-white text-lg">{station.name}</h4>
                    <p className="text-white/70 text-sm">{station.description}</p>
                  </div>
                  <Button
                    size="sm"
                    className="bg-white/20 hover:bg-white/30 text-white border-white/30"
                    onClick={(e) => {
                      e.stopPropagation();
                      onStationSelect(station);
                    }}
                  >
                    <Play className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="bg-blue-500/20 text-blue-200 border-blue-400/30">
                      {station.frequency}
                    </Badge>
                    <Badge variant="outline" className="border-white/30 text-white/80">
                      {station.genre}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-1 text-white/60 text-sm">
                    <Users className="h-3 w-3" />
                    <span>{station.listeners}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default StationList;