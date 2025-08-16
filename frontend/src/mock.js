// Mock data for global radio stations
export const mockCountries = [
  { code: 'US', name: 'United States', flag: '🇺🇸' },
  { code: 'UK', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'FR', name: 'France', flag: '🇫🇷' },
  { code: 'DE', name: 'Germany', flag: '🇩🇪' },
  { code: 'JP', name: 'Japan', flag: '🇯🇵' },
  { code: 'AU', name: 'Australia', flag: '🇦🇺' },
  { code: 'CA', name: 'Canada', flag: '🇨🇦' },
  { code: 'BR', name: 'Brazil', flag: '🇧🇷' },
  { code: 'IN', name: 'India', flag: '🇮🇳' },
  { code: 'IT', name: 'Italy', flag: '🇮🇹' },
  { code: 'ES', name: 'Spain', flag: '🇪🇸' },
  { code: 'RU', name: 'Russia', flag: '🇷🇺' },
];

export const mockRadioStations = {
  US: [
    {
      id: '1',
      name: 'NPR News',
      frequency: '88.5 FM',
      genre: 'News/Talk',
      url: 'https://npr-ice.streamguys1.com/live.mp3',
      listeners: '2.1M',
      description: 'National Public Radio - News and Talk'
    },
    {
      id: '2',
      name: 'Classic Rock 101',
      frequency: '101.1 FM',
      genre: 'Classic Rock',
      url: 'https://stream.example.com/rock',
      listeners: '856K',
      description: 'The best classic rock hits'
    },
    {
      id: '3',
      name: 'Jazz Café',
      frequency: '95.7 FM',
      genre: 'Jazz',
      url: 'https://stream.example.com/jazz',
      listeners: '445K',
      description: 'Smooth jazz and classic standards'
    }
  ],
  UK: [
    {
      id: '4',
      name: 'BBC Radio 1',
      frequency: '97.7 FM',
      genre: 'Pop/Chart',
      url: 'https://stream.live.vc.bbcmedia.co.uk/bbc_radio_one',
      listeners: '5.2M',
      description: 'The UK\'s most popular music station'
    },
    {
      id: '5',
      name: 'Capital FM',
      frequency: '95.8 FM',
      genre: 'Contemporary',
      url: 'https://stream.example.com/capital',
      listeners: '3.1M',
      description: 'London\'s hit music station'
    }
  ],
  FR: [
    {
      id: '6',
      name: 'France Inter',
      frequency: '87.8 FM',
      genre: 'News/Culture',
      url: 'https://stream.example.com/franceinter',
      listeners: '2.8M',
      description: 'Service public de radio généraliste'
    },
    {
      id: '7',
      name: 'NRJ',
      frequency: '100.3 FM',
      genre: 'Pop/Dance',
      url: 'https://stream.example.com/nrj',
      listeners: '1.9M',
      description: 'Hit Music Only!'
    }
  ],
  DE: [
    {
      id: '8',
      name: 'WDR 2',
      frequency: '99.2 FM',
      genre: 'Pop/Rock',
      url: 'https://stream.example.com/wdr2',
      listeners: '1.5M',
      description: 'Nordrhein-Westfalens Popwelle'
    }
  ],
  JP: [
    {
      id: '9',
      name: 'J-Wave',
      frequency: '81.3 FM',
      genre: 'J-Pop/Alternative',
      url: 'https://stream.example.com/jwave',
      listeners: '2.3M',
      description: 'Tokyo\'s premium music station'
    }
  ],
  AU: [
    {
      id: '10',
      name: 'Triple J',
      frequency: '107.7 FM',
      genre: 'Alternative',
      url: 'https://stream.example.com/triplej',
      listeners: '1.2M',
      description: 'Australia\'s alternative music station'
    }
  ],
  CA: [
    {
      id: '11',
      name: 'CBC Radio One',
      frequency: '99.1 FM',
      genre: 'News/Talk',
      url: 'https://stream.example.com/cbc',
      listeners: '1.8M',
      description: 'Canada\'s national radio service'
    }
  ],
  BR: [
    {
      id: '12',
      name: 'Rádio Jovem Pan',
      frequency: '100.9 FM',
      genre: 'News/Music',
      url: 'https://stream.example.com/jovempan',
      listeners: '3.5M',
      description: 'A rádio que toca música'
    }
  ],
  IN: [
    {
      id: '13',
      name: 'Radio Mirchi',
      frequency: '98.3 FM',
      genre: 'Bollywood/Pop',
      url: 'https://stream.example.com/mirchi',
      listeners: '4.1M',
      description: 'It\'s Hot!'
    }
  ],
  IT: [
    {
      id: '14',
      name: 'Radio Deejay',
      frequency: '107.2 FM',
      genre: 'Pop/Rock',
      url: 'https://stream.example.com/deejay',
      listeners: '2.2M',
      description: 'La radio che parla alla tua voglia di musica'
    }
  ],
  ES: [
    {
      id: '15',
      name: 'Los 40',
      frequency: '95.9 FM',
      genre: 'Pop/Latin',
      url: 'https://stream.example.com/los40',
      listeners: '3.8M',
      description: 'La radio de la música en español'
    }
  ],
  RU: [
    {
      id: '16',
      name: 'Radio Europa Plus',
      frequency: '106.2 FM',
      genre: 'Pop/Dance',
      url: 'https://stream.example.com/europaplus',
      listeners: '2.7M',
      description: 'Только хиты!'
    }
  ]
};