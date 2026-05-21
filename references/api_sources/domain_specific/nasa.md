# NASA APIs

## Overview

- **Endpoint base:** `https://api.nasa.gov/`
- **Auth:** API key (use `DEMO_KEY` для testing)
- **Free tier:** 1000 req/hr с personal key
- **Docs:** https://api.nasa.gov/
- **Coverage:** Космос, Earth observation, planetary data, weather

## Auth setup

1. https://api.nasa.gov/ → register для personal key
2. `export NASA_API_KEY="..."`

## Available APIs

### APOD (Astronomy Picture of the Day)

```
GET /planetary/apod?api_key={key}&date=2024-03-15
```

### NeoWs (Near Earth Objects)

```
GET /neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={key}
```

### Earth imagery

```
GET /planetary/earth/imagery?lon=-95.33&lat=29.78&date=2024-01-01&api_key={key}
```

### NASA Image Library

```
GET https://images-api.nasa.gov/search?q={query}&media_type=image
```

### Mars Rover Photos

```
GET /mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={key}
```

## Use cases

- Space/astronomy research
- Earth observation
- Climate data (auxiliary к NOAA)
- Planetary science

## Combine with

- **NOAA** — для Earth weather/climate
- **ESA APIs** — для European space data
- **Copernicus** — для EU climate observations
