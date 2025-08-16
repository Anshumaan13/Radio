import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Radio, Users, MapPin } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Slider } from './ui/slider';
import { Badge } from './ui/badge';

const RadioPlayer = ({ station, onClose }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState([70]);
  const [isMuted, setIsMuted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume[0] / 100;
    }
  }, [volume]);

  const togglePlay = async () => {
    if (!station) return;
    
    setIsLoading(true);
    
    if (isPlaying) {
      if (audioRef.current) {
        audioRef.current.pause();
        setIsPlaying(false);
      }
    } else {
      // Mock playing - in real implementation, this would connect to actual stream
      setTimeout(() => {
        setIsPlaying(true);
        setIsLoading(false);
      }, 1000);
      return;
    }
    setIsLoading(false);
  };

  const toggleMute = () => {
    if (audioRef.current) {
      audioRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleVolumeChange = (newVolume) => {
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume[0] / 100;
    }
  };

  if (!station) {
    return (
      <Card className="w-full max-w-md mx-auto bg-white/10 backdrop-blur-md border-white/20">
        <CardContent className="p-6 text-center">
          <Radio className="h-12 w-12 mx-auto mb-4 text-white/60" />
          <p className="text-white/80">Select a radio station to start listening</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto bg-white/10 backdrop-blur-md border-white/20 transition-all duration-300 hover:bg-white/15">
      <CardContent className="p-6">
        <audio ref={audioRef} preload="none" />
        
        {/* Station Info */}
        <div className="text-center mb-6">
          <h3 className="text-xl font-bold text-white mb-1">{station.name}</h3>
          <div className="flex items-center justify-center gap-2 mb-2">
            <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
              {station.frequency}
            </Badge>
            <Badge variant="outline" className="border-white/30 text-white/90">
              {station.genre}
            </Badge>
          </div>
          <p className="text-white/70 text-sm mb-2">{station.description}</p>
          <div className="flex items-center justify-center gap-1 text-white/60 text-sm">
            <Users className="h-4 w-4" />
            <span>{station.listeners} listeners</span>
          </div>
        </div>

        {/* Play Controls */}
        <div className="flex items-center justify-center mb-6">
          <Button
            onClick={togglePlay}
            disabled={isLoading}
            size="lg"
            className="h-16 w-16 rounded-full bg-white/20 hover:bg-white/30 border-2 border-white/40 transition-all duration-300"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent" />
            ) : isPlaying ? (
              <Pause className="h-6 w-6 text-white" />
            ) : (
              <Play className="h-6 w-6 text-white ml-1" />
            )}
          </Button>
        </div>

        {/* Volume Control */}
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleMute}
            className="text-white hover:bg-white/10"
          >
            {isMuted ? (
              <VolumeX className="h-4 w-4" />
            ) : (
              <Volume2 className="h-4 w-4" />
            )}
          </Button>
          <div className="flex-1">
            <Slider
              value={volume}
              onValueChange={handleVolumeChange}
              max={100}
              step={1}
              className="w-full"
            />
          </div>
          <span className="text-white/70 text-sm w-8">{volume[0]}</span>
        </div>

        {/* Status Indicator */}
        {isPlaying && (
          <div className="flex items-center justify-center gap-2 mt-4 text-green-400">
            <div className="animate-pulse h-2 w-2 bg-green-400 rounded-full"></div>
            <span className="text-sm">Live</span>
            <div className="flex gap-1">
              <div className="animate-pulse h-1 w-1 bg-green-400 rounded-full" style={{animationDelay: '0ms'}}></div>
              <div className="animate-pulse h-1 w-1 bg-green-400 rounded-full" style={{animationDelay: '150ms'}}></div>
              <div className="animate-pulse h-1 w-1 bg-green-400 rounded-full" style={{animationDelay: '300ms'}}></div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default RadioPlayer;